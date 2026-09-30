"""Isolated behavioral tests for the research-writing-skills installer.

The fixtures intentionally use a tiny synthetic upstream tree. No GitHub or
package-index requests are made by this suite.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from urllib.parse import urlparse


REPO_ROOT = Path(__file__).resolve().parents[1]
MANAGE_PATH = REPO_ROOT / "scripts" / "manage.py"
REMOTE_SKILLS = (
    "scientific-writing",
    "paper-lookup",
    "citation-management",
    "peer-review",
)
LOCAL_SKILL = "structural-biology-audit"


def load_manage_module():
    if not MANAGE_PATH.is_file():
        raise RuntimeError(f"installer script is missing: {MANAGE_PATH}")
    spec = importlib.util.spec_from_file_location("research_skills_manage", MANAGE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import installer script: {MANAGE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def file_record(data: bytes) -> dict[str, object]:
    return {
        "sha256": hashlib.sha256(data).hexdigest(),
        "git_blob_sha1": hashlib.sha1(
            f"blob {len(data)}\0".encode("ascii") + data
        ).hexdigest(),
        "size": len(data),
        "mode": "100644",
    }


class InstallerFixture:
    """Build a miniature, lock-file-backed repo and fake project install."""

    def __init__(self, temp_root: Path):
        temp_root = temp_root.resolve()
        self.repo = temp_root / "installer repo"
        self.project = temp_root / "Project with spaces"
        self.repo.mkdir()
        self.project.mkdir()
        self.payloads: dict[str, bytes] = {}
        self.write_repo_version("v1")
        self.manage = load_manage_module()
        self.config = self.manage.load_config(root=self.repo)
        self.fetch_calls: list[tuple[object, ...]] = []

    def write_repo_version(self, label: str) -> None:
        upstream = "synthetic-upstream"
        skill_config = {
            name: {"upstream": upstream, "path": f"skills/{name}"}
            for name in REMOTE_SKILLS
        }
        skill_config[LOCAL_SKILL] = {"local": f"skills/{LOCAL_SKILL}"}
        sources = {
            "schema_version": 1,
            "minimum_python": "3.11",
            "upstreams": {upstream: {"github": "example/skills", "ref": "main"}},
            "skills": skill_config,
            "runtime": {
                "requirements": "runtime/requirements.txt",
                "required_imports": [],
                "optional_imports": {},
            },
        }
        locked_files: dict[str, dict[str, object]] = {}
        payloads: dict[str, bytes] = {}
        for name in REMOTE_SKILLS:
            base = f"skills/{name}"
            skill_md = f"---\nname: {name}\ndescription: fixture {label}\n---\n\n{label}\n".encode()
            script = (
                "import json, sys\n"
                "print(json.dumps(sys.argv[1:]))\n"
            ).encode()
            for relative, data in (
                (f"{base}/SKILL.md", skill_md),
                (f"{base}/scripts/probe.py", script),
            ):
                payloads[relative] = data
                locked_files[relative] = file_record(data)

        local_dir = self.repo / "skills" / LOCAL_SKILL
        (local_dir / "references").mkdir(parents=True, exist_ok=True)
        (local_dir / "SKILL.md").write_text(
            f"---\nname: {LOCAL_SKILL}\ndescription: local fixture\n---\n\nLocal {label}\n",
            encoding="utf-8",
        )
        (local_dir / "references" / "guide.md").write_text(
            f"Local helper {label}\n", encoding="utf-8"
        )
        (self.repo / "runtime").mkdir(exist_ok=True)
        # Empty requirements keep the fixture independent from pip and network.
        (self.repo / "runtime" / "requirements.txt").write_text("", encoding="utf-8")
        (self.repo / "sources.json").write_text(
            json.dumps(sources, indent=2) + "\n", encoding="utf-8"
        )
        lock = {
            "schema_version": 1,
            "sources": {
                upstream: {
                    "github": "example/skills",
                    "ref": "main",
                    "commit": hashlib.sha1(label.encode("utf-8")).hexdigest(),
                    "files": locked_files,
                }
            },
        }
        (self.repo / "upstreams.lock.json").write_text(
            json.dumps(lock, indent=2) + "\n", encoding="utf-8"
        )
        self.payloads = payloads

    def reload_config(self):
        return self.manage.load_config(root=self.repo)

    def fetch(self, *args, **kwargs):
        """Resolve a requested raw path from the synthetic locked payload set."""
        self.fetch_calls.append(tuple(args))
        for value in (*args, *kwargs.values()):
            if isinstance(value, bytes):
                return value
            if not isinstance(value, str):
                continue
            path = urlparse(value).path.lstrip("/")
            for candidate, payload in self.payloads.items():
                if path == candidate or path.endswith("/" + candidate):
                    return payload
                # Some implementations pass the repository-relative path itself.
                if value == candidate:
                    return payload
        raise AssertionError(f"synthetic fetch received an unexpected request: {args!r} {kwargs!r}")

    def successful_runner(self, command, **kwargs):
        """Mock subprocess calls and materialize the requested isolated Python."""
        command = [str(part) for part in command]
        env_root = self.project / ".agents" / "research-writing-skills" / "envs"
        if any("venv" in part.lower() for part in command):
            env_root.mkdir(parents=True, exist_ok=True)
            env_dir = next(
                (Path(part) for part in command if str(part).startswith(str(env_root))),
                None,
            )
            if env_dir is None:
                # Requirements-hash directory may be derived from the config and
                # passed as the last argument to `python -m venv` / `uv venv`.
                env_dir = Path(command[-1])
            bin_dir = env_dir / ("Scripts" if os.name == "nt" else "bin")
            bin_dir.mkdir(parents=True, exist_ok=True)
            python_path = bin_dir / ("python.exe" if os.name == "nt" else "python")
            python_path.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            python_path.chmod(0o755)
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

    def install(self, config=None, *, runner=None, fetch=None):
        return self.manage.install_project(
            config or self.config,
            self.project,
            runner=runner or self.successful_runner,
            fetch=fetch or self.fetch,
        )


class InstallerBehaviorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.fixture = InstallerFixture(Path(self.temp.name))
        self.manage = self.fixture.manage

    def tearDown(self):
        self.temp.cleanup()

    def test_install_is_repeatable_and_preserves_existing_agent_instructions(self):
        project = self.fixture.project
        agents = project / "AGENTS.md"
        agents.write_text("Project-specific instruction.\n", encoding="utf-8")

        self.fixture.install()
        agents_after_first = agents.read_text(encoding="utf-8")
        self.fixture.install()
        agents_after_second = agents.read_text(encoding="utf-8")

        self.assertIn("Project-specific instruction.", agents_after_second)
        self.assertEqual(agents_after_first, agents_after_second)
        self.assertEqual(agents_after_second.count(self.manage.BEGIN), 1)
        self.assertEqual(agents_after_second.count(self.manage.END), 1)
        self.assertTrue((project / ".agents" / "skills" / REMOTE_SKILLS[0] / "SKILL.md").is_file())

    def test_install_refuses_unknown_or_modified_managed_skill_content(self):
        skill_dir = self.fixture.project / ".agents" / "skills" / REMOTE_SKILLS[0]
        skill_dir.mkdir(parents=True)
        user_file = skill_dir / "SKILL.md"
        user_file.write_text("my unrelated skill\n", encoding="utf-8")
        with self.assertRaises(self.manage.ManageError):
            self.fixture.install()
        self.assertEqual(user_file.read_text(encoding="utf-8"), "my unrelated skill\n")

    def test_unbalanced_agent_markers_are_rejected_without_project_changes(self):
        agents = self.fixture.project / "AGENTS.md"
        agents.write_text(self.manage.BEGIN + "\nmanual text\n", encoding="utf-8")

        with self.assertRaises(self.manage.ManageError):
            self.fixture.install()
        self.assertEqual(agents.read_text(encoding="utf-8"), self.manage.BEGIN + "\nmanual text\n")
        self.assertFalse((self.fixture.project / ".agents" / "research-writing-skills").exists())

    def test_lock_path_traversal_and_symlinked_skill_destination_are_rejected(self):
        fixture = self.fixture
        lock_path = fixture.repo / "upstreams.lock.json"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        entry = lock["sources"]["synthetic-upstream"]["files"]
        item = entry.pop(f"skills/{REMOTE_SKILLS[0]}/SKILL.md")
        entry["skills/../escape/SKILL.md"] = item
        lock_path.write_text(json.dumps(lock), encoding="utf-8")
        with self.assertRaises(self.manage.ManageError):
            fixture.reload_config()

        # Restore a clean fixture config, then verify a target symlink cannot
        # redirect an install outside .agents/skills.
        fixture.write_repo_version("v1")
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        skills = fixture.project / ".agents" / "skills"
        skills.mkdir(parents=True)
        (skills / REMOTE_SKILLS[0]).symlink_to(outside, target_is_directory=True)
        with self.assertRaises(self.manage.ManageError):
            fixture.install()
        self.assertEqual(list(outside.iterdir()), [])

    def test_reinstall_refuses_to_overwrite_a_user_modified_managed_file(self):
        fixture = self.fixture
        fixture.install()
        user_file = fixture.project / ".agents" / "skills" / REMOTE_SKILLS[0] / "SKILL.md"
        user_file.write_text("user-edited skill\n", encoding="utf-8")

        with self.assertRaises(self.manage.ManageError):
            fixture.install()
        self.assertEqual(user_file.read_text(encoding="utf-8"), "user-edited skill\n")

    def test_install_rejects_source_checksum_mismatch_before_writing(self):
        key = f"skills/{REMOTE_SKILLS[0]}/SKILL.md"
        self.fixture.payloads[key] = b"tampered upstream content\n"
        with self.assertRaises(self.manage.ManageError):
            self.fixture.install()
        self.assertFalse((self.fixture.project / ".agents" / "skills").exists())

    def test_managed_upgrade_and_failed_upgrade_leave_a_coherent_old_install(self):
        fixture = self.fixture
        fixture.install()
        skill_file = fixture.project / ".agents" / "skills" / REMOTE_SKILLS[0] / "SKILL.md"
        old_content = skill_file.read_bytes()
        old_state = (fixture.project / ".agents" / "research-writing-skills" / "state.json").read_bytes()

        fixture.write_repo_version("v2")
        config_v2 = fixture.reload_config()

        def fail_env(command, **kwargs):
            raise OSError("simulated dependency install failure")

        with self.assertRaises((self.manage.ManageError, OSError)):
            fixture.install(config_v2, runner=fail_env)
        self.assertEqual(skill_file.read_bytes(), old_content)
        self.assertEqual(
            (fixture.project / ".agents" / "research-writing-skills" / "state.json").read_bytes(),
            old_state,
        )

        fixture.install(config_v2)
        self.assertIn(b"v2", skill_file.read_bytes())
        self.assertNotEqual(skill_file.read_bytes(), old_content)

    def test_mid_transaction_failure_restores_old_skills_state_and_agent_block(self):
        fixture = self.fixture
        fixture.install()
        skill_file = fixture.project / ".agents" / "skills" / REMOTE_SKILLS[0] / "SKILL.md"
        old_content = skill_file.read_bytes()
        state_path = fixture.project / ".agents" / "research-writing-skills" / "state.json"
        old_state = state_path.read_bytes()
        agents = fixture.project / "AGENTS.md"
        old_agents = agents.read_bytes()

        fixture.write_repo_version("v2")
        config_v2 = fixture.reload_config()
        atomic_write = self.manage.atomic_write

        def fail_state_write(path, data):
            if Path(path).name == "state.json":
                raise OSError("simulated final transaction write failure")
            return atomic_write(path, data)

        with mock.patch.object(self.manage, "atomic_write", side_effect=fail_state_write):
            with self.assertRaises(OSError):
                fixture.install(config_v2)

        self.assertEqual(skill_file.read_bytes(), old_content)
        self.assertEqual(state_path.read_bytes(), old_state)
        self.assertEqual(agents.read_bytes(), old_agents)

    def test_run_uses_project_environment_and_forwards_script_arguments(self):
        fixture = self.fixture
        fixture.install()
        seen = {}

        def run_capture(command, **kwargs):
            seen["command"] = [str(part) for part in command]
            return subprocess.CompletedProcess(command, 0, stdout="[]", stderr="")

        self.manage.run_script(
            fixture.config,
            fixture.project,
            REMOTE_SKILLS[0],
            "scripts/probe.py",
            ["--query", "protein structures"],
            runner=run_capture,
        )
        command = seen["command"]
        self.assertIn(str(fixture.project / ".agents" / "research-writing-skills" / "envs"), command[0])
        self.assertEqual(command[-2:], ["--query", "protein structures"])

    def test_uninstall_preserves_unrelated_skills_modified_files_and_user_agent_text(self):
        fixture = self.fixture
        fixture.install()
        skills_root = fixture.project / ".agents" / "skills"
        other_skill = skills_root / "my-own-skill" / "SKILL.md"
        other_skill.parent.mkdir(parents=True)
        other_skill.write_text("do not delete\n", encoding="utf-8")
        modified = skills_root / REMOTE_SKILLS[0] / "SKILL.md"
        managed_content = modified.read_bytes()
        modified.write_text("user customization\n", encoding="utf-8")
        agents = fixture.project / "AGENTS.md"
        agents.write_text(agents.read_text(encoding="utf-8") + "User-added after install.\n", encoding="utf-8")

        with self.assertRaises(self.manage.ManageError):
            self.manage.uninstall_project(fixture.config, fixture.project)
        self.assertTrue((fixture.project / ".agents" / "research-writing-skills" / "state.json").is_file())
        self.assertEqual(modified.read_text(encoding="utf-8"), "user customization\n")
        self.assertTrue(other_skill.is_file())

        # Once the managed file is restored, uninstall removes only the owned
        # resources and leaves text added outside the marker block untouched.
        modified.write_bytes(managed_content)
        self.manage.uninstall_project(fixture.config, fixture.project)

        self.assertTrue(other_skill.is_file())
        self.assertIn("User-added after install.", agents.read_text(encoding="utf-8"))
        self.assertNotIn("research-writing-skills", agents.read_text(encoding="utf-8"))

    def test_uninstall_refuses_to_remove_untracked_runtime_files(self):
        fixture = self.fixture
        fixture.install()
        runtime = fixture.project / ".agents" / "research-writing-skills"
        note = runtime / "user-notes.txt"
        note.write_text("keep this file\n", encoding="utf-8")
        state_before = (runtime / "state.json").read_bytes()
        skill_before = (
            fixture.project / ".agents" / "skills" / REMOTE_SKILLS[0] / "SKILL.md"
        ).read_bytes()

        with self.assertRaises(self.manage.ManageError):
            self.manage.uninstall_project(fixture.config, fixture.project)

        self.assertEqual(note.read_text(encoding="utf-8"), "keep this file\n")
        self.assertEqual((runtime / "state.json").read_bytes(), state_before)
        self.assertEqual(
            (fixture.project / ".agents" / "skills" / REMOTE_SKILLS[0] / "SKILL.md").read_bytes(),
            skill_before,
        )

    def test_update_dry_run_reports_upstream_change_without_writing_lock(self):
        fixture = self.fixture
        lock_path = fixture.repo / "upstreams.lock.json"
        original_lock = lock_path.read_bytes()
        old_payloads = fixture.payloads
        new_commit = "f" * 40
        new_payloads = {
            path: data.replace(b"v1", b"v2")
            for path, data in old_payloads.items()
        }
        tree = []
        for path, data in new_payloads.items():
            record = file_record(data)
            tree.append({
                "type": "blob",
                "path": path,
                "mode": record["mode"],
                "sha": record["git_blob_sha1"],
            })
        requested = []

        def update_fetch(url):
            requested.append(url)
            if "/commits/" in url:
                return json.dumps({"sha": new_commit}).encode()
            if "/git/trees/" in url:
                return json.dumps({"truncated": False, "tree": tree}).encode()
            raise AssertionError(f"dry-run unexpectedly fetched source content: {url}")

        changes = self.manage.update_upstream(fixture.config, dry_run=True, fetch=update_fetch)

        self.assertEqual(changes["synthetic-upstream"]["commit"], new_commit)
        self.assertEqual(lock_path.read_bytes(), original_lock)
        self.assertEqual(len(requested), 2)

    def test_install_rolls_back_agent_file_when_a_later_transaction_step_fails(self):
        fixture = self.fixture
        agents = fixture.project / "AGENTS.md"
        initial = "Keep this project instruction.\n"
        agents.write_text(initial, encoding="utf-8")

        def fail_runner(command, **kwargs):
            raise OSError("simulated environment setup failure")

        with self.assertRaises((self.manage.ManageError, OSError)):
            fixture.install(runner=fail_runner)
        self.assertEqual(agents.read_text(encoding="utf-8"), initial)
        self.assertFalse((fixture.project / ".agents" / "research-writing-skills" / "state.json").exists())

    def test_update_commits_verified_content_and_rejects_a_bad_blob_atomically(self):
        fixture = self.fixture
        lock_path = fixture.repo / "upstreams.lock.json"
        previous = lock_path.read_bytes()
        payloads = {path: data.replace(b"v1", b"v2") for path, data in fixture.payloads.items()}
        tree = [{"type": "blob", "path": path, "mode": "100644", "sha": file_record(data)["git_blob_sha1"]}
                for path, data in payloads.items()]
        corrupt = True

        def update_fetch(url):
            if "/commits/" in url:
                return json.dumps({"sha": "f" * 40}).encode()
            if "/git/trees/" in url:
                return json.dumps({"truncated": False, "tree": tree}).encode()
            for path, data in payloads.items():
                if url.endswith('/' + path):
                    return b"broken" if corrupt else data
            raise AssertionError(url)

        with self.assertRaises(self.manage.ManageError):
            self.manage.update_upstream(fixture.config, fetch=update_fetch)
        self.assertEqual(lock_path.read_bytes(), previous)
        corrupt = False
        self.manage.update_upstream(fixture.config, fetch=update_fetch)
        new_config = fixture.reload_config()
        updated = new_config['lock']['sources']['synthetic-upstream']
        self.assertEqual(updated['commit'], "f" * 40)
        for path, data in payloads.items():
            self.assertEqual(updated['files'][path], file_record(data))
        fixture.payloads = payloads
        fixture.install(new_config)
        installed = fixture.project / '.agents' / 'skills' / REMOTE_SKILLS[0] / 'SKILL.md'
        self.assertIn(b"v2", installed.read_bytes())

    def test_run_rejects_script_path_traversal_and_symlink_escape(self):
        fixture = self.fixture
        fixture.install()
        outside = Path(self.temp.name) / "outside.py"
        outside.write_text("print('outside')\n", encoding="utf-8")
        with self.assertRaises(self.manage.ManageError):
            self.manage.run_script(
                fixture.config,
                fixture.project,
                REMOTE_SKILLS[0],
                "../../outside.py",
                [],
                runner=fixture.successful_runner,
            )

        skill_dir = fixture.project / ".agents" / "skills" / REMOTE_SKILLS[1]
        moved = fixture.project / ".agents" / "skills" / (REMOTE_SKILLS[1] + "-saved")
        skill_dir.rename(moved)
        skill_dir.symlink_to(outside.parent, target_is_directory=True)
        with self.assertRaises(self.manage.ManageError):
            self.manage.run_script(
                fixture.config,
                fixture.project,
                REMOTE_SKILLS[1],
                "scripts/probe.py",
                [],
                runner=fixture.successful_runner,
            )


if __name__ == "__main__":
    unittest.main()
