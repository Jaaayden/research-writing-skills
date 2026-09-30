#!/usr/bin/env python3
"""Install a small, upstream-backed skill collection into a project."""
from __future__ import annotations

import argparse
import ast
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BEGIN = '<!-- BEGIN research-writing-skills -->'
END = '<!-- END research-writing-skills -->'


class ManageError(Exception):
    pass


def relative(value):
    p = PurePosixPath(value)
    if not value or p.is_absolute() or any(x in value for x in ['\\', ':', '\n']) or any(x in ('..', '.') for x in value.split('/')):
        raise ManageError(f'不安全的相对路径：{value!r}')
    return p


def no_links(path):
    for p in [path, *path.parents]:
        if p.is_symlink():
            raise ManageError(f'不接受软链接目录或文件：{p}')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def record(data, mode='100644'):
    return {'sha256': digest(data), 'git_blob_sha1': hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest(), 'size': len(data), 'mode': mode}


def tree_hashes(path):
    no_links(path)
    if not path.is_dir():
        raise ManageError(f'缺少技能目录：{path}')
    result = {}
    for p in sorted(path.rglob('*')):
        if p.is_symlink():
            raise ManageError(f'技能不能包含软链接：{p}')
        if p.is_file():
            result[p.relative_to(path).as_posix()] = digest(p.read_bytes())
        elif not p.is_dir():
            raise ManageError(f'不支持的文件类型：{p}')
    return result


def read_json(path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as e:
        raise ManageError(f'无法读取 {path}：{e}') from e


def atomic_write(path, data):
    no_links(path)
    tmp = path.with_name(path.name + '.tmp')
    no_links(tmp)
    try:
        tmp.write_bytes(data)
        tmp.replace(path)
    finally:
        tmp.unlink(missing_ok=True)


def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()


def load_config(root=ROOT):
    root = Path(root).resolve()
    no_links(root)
    sources, lock = read_json(root / 'sources.json'), read_json(root / 'upstreams.lock.json')
    if sources.get('schema_version') != 1 or lock.get('schema_version') != 1:
        raise ManageError('不支持的清单版本')
    if set(sources['upstreams']) != set(lock['sources']):
        raise ManageError('锁文件来源集合与清单不一致')
    for name, spec in sources['skills'].items():
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
            raise ManageError(f'无效技能名称：{name}')
        relative(spec.get('path', spec.get('local', '')))
        if 'upstream' not in spec:
            no_links(root / spec['local'])
    relative(sources['runtime']['requirements'])
    for name, spec in sources['upstreams'].items():
        entry = lock['sources'][name]
        if entry['github'] != spec['github'] or not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', spec['github']):
            raise ManageError('上游来源与锁文件不一致')
        if not re.fullmatch(r'[a-f0-9]{40}', entry['commit']):
            raise ManageError('上游必须锁定到完整提交 SHA')
        prefixes = [s['path'] + '/' for s in sources['skills'].values() if s.get('upstream') == name]
        for path, info in entry['files'].items():
            relative(path)
            if not any(path.startswith(prefix) for prefix in prefixes) or info.get('mode') not in ('100644', '100755'):
                raise ManageError(f'锁文件包含未授权资源：{path}')
            if not re.fullmatch(r'[a-f0-9]{64}', info['sha256']) or not re.fullmatch(r'[a-f0-9]{40}', info['git_blob_sha1']):
                raise ManageError(f'无效文件摘要：{path}')
        for prefix in prefixes:
            if prefix + 'SKILL.md' not in entry['files']:
                raise ManageError(f'上游技能缺少 SKILL.md：{prefix}')
    return {'root': root, 'sources': sources, 'lock': lock}


def fetch_bytes(url):
    for attempt in range(2):
        try:
            with urlopen(Request(url, headers={'User-Agent': 'research-writing-skills'}), timeout=30) as response:
                return response.read()
        except (HTTPError, URLError, TimeoutError) as e:
            if attempt == 0 and (not isinstance(e, HTTPError) or e.code in (429, 500, 502, 503, 504)):
                time.sleep(1)
                continue
            raise ManageError(f'下载失败：{url} ({type(e).__name__})') from e


def download_files(entry, fetch=fetch_bytes):
    def one(item):
        path, expected = item
        data = fetch(f'https://raw.githubusercontent.com/{entry["github"]}/{entry["commit"]}/{quote(path, safe="/")}')
        actual = record(data, expected['mode'])
        if actual != expected:
            raise ManageError(f'上游文件校验失败：{path}')
        return path, data
    with ThreadPoolExecutor(max_workers=6) as pool:
        return dict(pool.map(one, entry['files'].items()))


def update_upstream(config, dry_run=False, fetch=fetch_bytes):
    changed = {}
    new_lock = json.loads(json.dumps(config['lock']))
    for name, spec in config['sources']['upstreams'].items():
        repo, ref = spec['github'], spec['ref']
        commit = json.loads(fetch(f'https://api.github.com/repos/{repo}/commits/{quote(ref, safe="")}'))['sha']
        if not re.fullmatch(r'[a-f0-9]{40}', commit):
            raise ManageError('GitHub 返回无效提交 SHA')
        old = config['lock']['sources'][name]
        if commit == old['commit']:
            print(f'{name}：已是上游最新版本 {commit[:12]}')
            continue
        tree = json.loads(fetch(f'https://api.github.com/repos/{repo}/git/trees/{commit}?recursive=1'))
        if tree.get('truncated'):
            raise ManageError('GitHub 文件树不完整，停止更新')
        prefixes = [s['path'] + '/' for s in config['sources']['skills'].values() if s.get('upstream') == name]
        selected = {}
        for item in tree['tree']:
            if item['type'] != 'blob' or not any(item['path'].startswith(p) for p in prefixes):
                continue
            relative(item['path'])
            if item['mode'] not in ('100644', '100755'):
                raise ManageError(f'上游新增不支持的资源：{item["path"]}')
            selected[item['path']] = item
        for prefix in prefixes:
            if prefix + 'SKILL.md' not in selected:
                raise ManageError(f'上游删除或移动了技能：{prefix}')
        changed[name] = {'previous': old['commit'], 'commit': commit}
        print(f'{name}：{old["commit"][:12]} → {commit[:12]}，{len(selected)} 个技能文件')
        print(f'审阅上游变化：https://github.com/{repo}/compare/{old["commit"]}...{commit}')
        if dry_run:
            continue
        license_path = config['root'] / 'licenses' / 'K-Dense-AI-MIT.md'
        if license_path.exists() and fetch(f'https://raw.githubusercontent.com/{repo}/{commit}/LICENSE.md') != license_path.read_bytes():
            raise ManageError('上游许可证已改变，请先人工核对许可文件；锁文件未更新')
        entry = {'github': repo, 'ref': ref, 'commit': commit, 'files': {}}
        def one(item):
            path, meta = item
            data = fetch(f'https://raw.githubusercontent.com/{repo}/{commit}/{quote(path, safe="/")}')
            info = record(data, meta['mode'])
            if info['git_blob_sha1'] != meta['sha']:
                raise ManageError(f'上游 Git blob 校验失败：{path}')
            return path, info
        with ThreadPoolExecutor(max_workers=6) as pool:
            entry['files'] = dict(sorted(pool.map(one, selected.items())))
        new_lock['sources'][name] = entry
    if changed and not dry_run:
        atomic_write(config['root'] / 'upstreams.lock.json', json_bytes(new_lock))
    return changed


def project_paths(project):
    project = Path(project).expanduser().resolve()
    no_links(project)
    if not project.is_dir():
        raise ManageError(f'项目目录不存在：{project}')
    agents = project / '.agents'
    runtime = agents / 'research-writing-skills'
    for p in [agents, agents / 'skills', runtime, runtime / 'state.json', project / 'AGENTS.md']:
        no_links(p)
    return project, agents / 'skills', runtime


def expected_skills(config):
    result = {}
    for name, spec in config['sources']['skills'].items():
        if 'local' in spec:
            result[name] = tree_hashes(config['root'] / spec['local'])
        else:
            entry = config['lock']['sources'][spec['upstream']]
            prefix = spec['path'] + '/'
            result[name] = {p[len(prefix):]: i['sha256'] for p, i in entry['files'].items() if p.startswith(prefix)}
    return result


def check_owned(skills, state):
    for name, hashes in state['skills'].items():
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
            raise ManageError('安装状态含无效技能名')
        if tree_hashes(skills / name) != hashes:
            raise ManageError(f'{name} 存在手动修改或缺失文件，请先备份并处理；未覆盖内容')


def check_runtime(runtime, state):
    allowed = {'envs', 'licenses', 'ENVIRONMENT.md', 'state.json'}
    for path in runtime.iterdir():
        if path.name not in allowed or path.is_symlink():
            raise ManageError(f'运行目录存在未受管内容：{path}；保留内容并停止操作')
    envs = runtime / 'envs'
    if envs.exists():
        for path in envs.iterdir():
            no_links(path)
            fingerprint = state.get('envs', {}).get(path.name)
            if not fingerprint or not path.is_dir():
                raise ManageError(f'存在未受管 Python 环境：{path}')
            marker = path / '.research-writing-skills.json'
            no_links(marker)
            if read_json(marker) != {'owner': 'research-writing-skills', 'requirements_sha256': fingerprint}:
                raise ManageError(f'Python 环境归属记录已改变：{path}')
    support = state.get('support_files', {})
    actual = {}
    for path in [runtime / 'ENVIRONMENT.md', *list((runtime / 'licenses').rglob('*'))]:
        if path.is_symlink():
            raise ManageError(f'运行资源不能是软链接：{path}')
        if path.is_dir():
            raise ManageError(f'许可证目录包含未受管子目录：{path}')
        if path.is_file():
            actual[path.relative_to(runtime).as_posix()] = digest(path.read_bytes())
    if actual != support:
        raise ManageError('运行环境说明或许可证存在手动修改，保留内容并停止操作')


def managed_text(text):
    if text.count(BEGIN) != text.count(END) or text.count(BEGIN) > 1:
        raise ManageError('AGENTS.md 的受管标记不完整或重复')
    if BEGIN not in text:
        return None
    start, end = text.index(BEGIN), text.index(END) + len(END)
    if end <= start:
        raise ManageError('AGENTS.md 的受管标记顺序错误')
    return text[start:end]


def instruction_block(python, skills):
    return f'{BEGIN}\n这五项科研技能的 Python 脚本使用本项目隔离解释器：`{python}`。\n技能目录：`{skills}`。脚本使用绝对路径；上游示例的 scripts/ 路径相对于对应技能目录。\n调用解释器时为路径加引号，并设置 PYTHONDONTWRITEBYTECODE=1。不要把依赖安装到系统 Python。\n{END}'


def replace_instructions(text, block, previous=None):
    existing = managed_text(text)
    if existing is not None:
        if previous is None or existing != previous:
            raise ManageError('AGENTS.md 中的受管环境指引被手动修改或不属于本安装')
        return text.replace(existing, block, 1)
    if previous is not None:
        raise ManageError('AGENTS.md 中的受管环境指引已缺失')
    return text + ('\n' if text and not text.endswith('\n') else '') + block + '\n'


def run_checked(command, runner=subprocess.run, **kwargs):
    try:
        completed = runner([str(x) for x in command], capture_output=True, text=True, **kwargs)
    except (OSError, subprocess.SubprocessError) as e:
        raise ManageError(f'无法执行 {command[0]}：{e}') from e
    if completed.returncode:
        raise ManageError(f'命令失败：{command[0]}\n{completed.stderr or completed.stdout or ""}')
    return completed


def environment(config, runtime, runner=subprocess.run):
    requirements = config['root'] / config['sources']['runtime']['requirements']
    fingerprint = digest(requirements.read_bytes())
    envdir = runtime / 'envs' / fingerprint[:16]
    no_links(envdir)
    python = envdir / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    newly_created = not envdir.exists()
    marker = envdir / '.research-writing-skills.json'
    if not newly_created:
        no_links(marker)
        if not marker.is_file() or read_json(marker) != {'owner': 'research-writing-skills', 'requirements_sha256': fingerprint}:
            raise ManageError(f'拒绝复用未受管虚拟环境：{envdir}')
    try:
        if newly_created:
            envdir.parent.mkdir(parents=True, exist_ok=True)
            if shutil.which('uv'):
                run_checked(['uv', 'venv', '--python', sys.executable, envdir], runner)
            else:
                run_checked([sys.executable, '-m', 'venv', envdir], runner)
        if not python.is_file():
            raise ManageError('虚拟环境的 Python 不存在')
        if shutil.which('uv'):
            run_checked(['uv', 'pip', 'install', '--python', python, '--require-hashes', '-r', requirements], runner)
            run_checked(['uv', 'pip', 'check', '--python', python], runner)
        else:
            run_checked([python, '-m', 'pip', 'install', '--require-hashes', '-r', requirements], runner)
            run_checked([python, '-m', 'pip', 'check'], runner)
        imports = config['sources']['runtime']['required_imports']
        code = 'import sys,importlib; assert sys.version_info >= (3,11); ' + '; '.join(f'importlib.import_module({name!r})' for name in imports)
        run_checked([python, '-c', code], runner)
        atomic_write(marker, json_bytes({'owner': 'research-writing-skills', 'requirements_sha256': fingerprint}))
    except BaseException:
        if newly_created and envdir.exists():
            shutil.rmtree(envdir)
        raise
    return python, fingerprint, newly_created


def validate_tree(path, name, python, config, runner=subprocess.run):
    # YAML is validated by the project interpreter, never by a global package.
    code = '''import sys,re,pathlib,yaml
p=pathlib.Path(sys.argv[1]); text=(p/'SKILL.md').read_text(encoding='utf-8')
m=re.match(r'^---\\n(.*?)\\n---(?:\\n|$)',text,re.S); assert m, 'YAML front matter missing'
d=yaml.safe_load(m.group(1)); assert isinstance(d,dict), 'front matter must be a mapping'
assert d.get('name')==sys.argv[2], 'name differs from directory'
desc=d.get('description'); assert isinstance(desc,str) and 0<len(desc.strip())<=1024, 'invalid description'
'''
    run_checked([python, '-c', code, path, name], runner)
    allowed = set(sys.stdlib_module_names) | set(config['sources']['runtime']['required_imports']) | set(config['sources']['runtime']['optional_imports'])
    scripts = path / 'scripts'
    allowed |= {p.stem for p in scripts.glob('*.py')}
    for file in scripts.glob('*.py'):
        try:
            tree = ast.parse(file.read_text(encoding='utf-8'))
        except SyntaxError as e:
            raise ManageError(f'脚本语法与本机 Python 不兼容：{file}') from e
        for node in ast.walk(tree):
            imported = []
            if isinstance(node, ast.Import):
                imported = [a.name.split('.')[0] for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
                imported = [node.module.split('.')[0]]
            for module in imported:
                if module not in allowed:
                    raise ManageError(f'上游新增 Python 依赖 {module}；请更新 sources.json 和 runtime 锁文件后重试')
        if not file.name.startswith('_'):
            env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
            run_checked([python, file, '--help'], runner, env=env, timeout=20)
    for file in path.rglob('*.md'):
        text = file.read_text(encoding='utf-8')
        for target in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)', text):
            if target.startswith(('http:', 'https:', 'mailto:', '#')):
                continue
            target = target.split('#', 1)[0]
            if target and not (file.parent / target).is_file():
                raise ManageError(f'缺少本地引用资源：{file} → {target}')
        # Backtick paths in the skill itself are local runtime dependencies.
        if file.name == 'SKILL.md':
            for target in re.findall(r'`((?:scripts|references|assets)/[^`\s]+)`', text):
                if not any(c in target for c in '<>*') and not (path / target).exists():
                    raise ManageError(f'缺少本地资源：{name}/{target}')


def install_project(config, project, runner=subprocess.run, fetch=fetch_bytes):
    project, skills, runtime = project_paths(project)
    expected = expected_skills(config)
    state_path = runtime / 'state.json'
    state = read_json(state_path) if state_path.exists() else None
    if state:
        check_owned(skills, state)
        check_runtime(runtime, state)
        if set(state['skills']) != set(expected):
            raise ManageError('技能组已改变，请先卸载旧技能组')
    else:
        if runtime.exists():
            raise ManageError(f'存在未受管运行目录：{runtime}')
        for name in expected:
            if (skills / name).exists() or (skills / name).is_symlink():
                raise ManageError(f'存在同名未受管技能：{name}')
    agent_path = project / 'AGENTS.md'
    old_agents = agent_path.read_bytes() if agent_path.exists() else None
    old_text = (old_agents or b'').decode('utf-8')
    managed_text(old_text)
    requirements_sha = digest((config['root'] / config['sources']['runtime']['requirements']).read_bytes())
    if state and state['skills'] == expected and state['requirements_sha256'] == requirements_sha and Path(state['python']).is_file():
        return check_project(config, project, runner)
    runtime.mkdir(parents=True, exist_ok=True)
    created_env = False
    python = None
    try:
        with tempfile.TemporaryDirectory(prefix='staging-', dir=runtime) as tmp:
            staging = Path(tmp)
            for source_name, entry in config['lock']['sources'].items():
                payloads = download_files(entry, fetch)
                for name, spec in config['sources']['skills'].items():
                    if spec.get('upstream') != source_name:
                        continue
                    prefix = spec['path'] + '/'
                    for path, data in payloads.items():
                        if not path.startswith(prefix):
                            continue
                        dest = staging / name / relative(path[len(prefix):])
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        dest.write_bytes(data)
                        dest.chmod(0o755 if entry['files'][path]['mode'] == '100755' else 0o644)
            for name, spec in config['sources']['skills'].items():
                if 'local' in spec:
                    shutil.copytree(config['root'] / spec['local'], staging / name)
            for name, hashes in expected.items():
                if tree_hashes(staging / name) != hashes:
                    raise ManageError(f'暂存技能校验失败：{name}')
            python, fingerprint, created_env = environment(config, runtime, runner)
            for name in expected:
                validate_tree(staging / name, name, python, config, runner)
            block = instruction_block(python, skills)
            new_agents = replace_instructions(old_text, block, state.get('agents_block') if state else None).encode()
            new_state = {'schema_version': 1, 'skills': expected, 'python': str(python), 'requirements_sha256': fingerprint,
                         'source_commits': {n: e['commit'] for n, e in config['lock']['sources'].items()},
                         'agents_block': block, 'created_agents': state['created_agents'] if state else old_agents is None}
            new_state['envs'] = dict(state.get('envs', {}) if state else {})
            new_state['envs'][fingerprint[:16]] = fingerprint
            license_files = [p for p in (config['root'] / 'licenses').glob('*') if p.is_file()]
            support_paths = [runtime / 'ENVIRONMENT.md', *(runtime / 'licenses' / p.name for p in license_files)]
            old_files = {p: p.read_bytes() if p.exists() else None for p in [state_path, *support_paths]}
            backup, moved, placed = staging / 'previous', [], []
            backup.mkdir()
            skills.mkdir(parents=True, exist_ok=True)
            try:
                for name in expected:
                    dest = skills / name
                    if dest.exists():
                        dest.replace(backup / name)
                        moved.append(name)
                    (staging / name).replace(dest)
                    placed.append(name)
                atomic_write(agent_path, new_agents)
                docs = f'# 项目科研技能环境\n\nPython：`{python}`\n\n技能：{", ".join(expected)}\n\n脚本使用该解释器和技能中的绝对路径，也可通过仓库的 manage.py run --project 调用。\n可选 scholarly 未默认安装；API key 不属于安装前提。\n'
                atomic_write(runtime / 'ENVIRONMENT.md', docs.encode())
                for license_file in license_files:
                    no_links(license_file)
                    (runtime / 'licenses').mkdir(exist_ok=True)
                    atomic_write(runtime / 'licenses' / license_file.name, license_file.read_bytes())
                new_state['support_files'] = {p.relative_to(runtime).as_posix(): digest(p.read_bytes()) for p in support_paths}
                atomic_write(state_path, json_bytes(new_state))
            except BaseException:
                for name in reversed(placed):
                    shutil.rmtree(skills / name)
                for name in moved:
                    (backup / name).replace(skills / name)
                if old_agents is None:
                    agent_path.unlink(missing_ok=True)
                else:
                    agent_path.write_bytes(old_agents)
                for p, data in old_files.items():
                    if data is None:
                        p.unlink(missing_ok=True)
                    else:
                        p.write_bytes(data)
                raise
    except BaseException:
        if state is None:
            shutil.rmtree(runtime)
        elif created_env and python is not None:
            shutil.rmtree(python.parent.parent)
        raise
    print(f'已安装 {len(expected)} 个项目技能；Python：{python}')
    return new_state


def check_project(config, project, runner=subprocess.run):
    project, skills, runtime = project_paths(project)
    state = read_json(runtime / 'state.json')
    if state.get('schema_version') != 1:
        raise ManageError('无效安装状态')
    check_owned(skills, state)
    check_runtime(runtime, state)
    if managed_text((project / 'AGENTS.md').read_text(encoding='utf-8')) != state['agents_block']:
        raise ManageError('项目环境指引缺失或已修改')
    python = Path(state['python'])
    if python != runtime / 'envs' / state['requirements_sha256'][:16] / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python'):
        raise ManageError('项目路径已移动或 Python 状态不安全，请重新安装环境')
    no_links(python.parent)
    if not python.is_file():
        raise ManageError('项目隔离 Python 已缺失')
    code = 'import sys,importlib; assert sys.version_info >= (3,11); ' + '; '.join(f'importlib.import_module({m!r})' for m in config['sources']['runtime']['required_imports'])
    run_checked([python, '-c', code], runner)
    print(f'检查通过：{len(state["skills"])} 个技能；Python：{python}')
    for m, purpose in config['sources']['runtime']['optional_imports'].items():
        print(f'可选依赖 {m} 未由本工具安装：{purpose}')
    return state


def run_script(config, project, skill, script, args, runner=subprocess.run):
    state = check_project(config, project, runner)
    if skill not in state['skills']:
        raise ManageError(f'技能未安装：{skill}')
    rel = relative(script)
    if len(rel.parts) != 2 or rel.parts[0] != 'scripts' or rel.suffix != '.py':
        raise ManageError('请指定 scripts/目录中的 Python 脚本')
    project = Path(project).expanduser().resolve()
    path = project / '.agents/skills' / skill / rel
    no_links(path)
    if not path.is_file():
        raise ManageError(f'脚本不存在：{script}')
    completed = runner([state['python'], str(path), *args], cwd=str(project), env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
    return completed.returncode


def uninstall_project(config, project):
    project, skills, runtime = project_paths(project)
    state = read_json(runtime / 'state.json')
    check_owned(skills, state)
    check_runtime(runtime, state)
    agents = project / 'AGENTS.md'
    text = agents.read_text(encoding='utf-8')
    if managed_text(text) != state['agents_block']:
        raise ManageError('环境指引已修改，卸载停止以保留用户内容')
    text = text.replace(state['agents_block'] + '\n', '', 1) if state['agents_block'] + '\n' in text else text.replace(state['agents_block'], '', 1)
    for name in state['skills']:
        shutil.rmtree(skills / name)
    if state['created_agents'] and not text.strip():
        agents.unlink()
    else:
        atomic_write(agents, text.encode())
    shutil.rmtree(runtime)
    print(f'已卸载 {len(state["skills"])} 个受管技能和运行环境；保留其他项目内容')


def main():
    parser = argparse.ArgumentParser(description='科研技能：上游更新、项目安装和隔离环境')
    commands = parser.add_subparsers(dest='command', required=True)
    update = commands.add_parser('update', help='检查上游并更新锁文件')
    update.add_argument('--dry-run', action='store_true')
    for name in ['install', 'check', 'run', 'uninstall']:
        command = commands.add_parser(name)
        command.add_argument('--project', required=True)
        if name == 'run':
            command.add_argument('skill')
            command.add_argument('script')
            command.add_argument('args', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if sys.version_info < (3, 11):
        parser.error('需要 Python 3.11+')
    try:
        config = load_config()
        if args.command == 'update':
            update_upstream(config, args.dry_run)
        elif args.command == 'install':
            install_project(config, args.project)
        elif args.command == 'check':
            check_project(config, args.project)
        elif args.command == 'uninstall':
            uninstall_project(config, args.project)
        else:
            return run_script(config, args.project, args.skill, args.script, args.args)
    except (ManageError, OSError, ValueError, KeyError) as e:
        print(f'错误：{e}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
