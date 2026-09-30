#!/usr/bin/env python3
"""Resolve local PDF files for sources in the structural biology audit catalog.

The resolver only reads the catalog, existing local files, and Zotero's
loopback read API. It never downloads, extracts, copies, or uploads PDF content.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = SKILL_ROOT / "references" / "sources.json"
BUNDLED_PAPERS_DIR = SKILL_ROOT / "references" / "papers"
FULLTEXT_DIR = SKILL_ROOT / "full-text"
ZOTERO_API_ROOT = "http://127.0.0.1:23119/api/users/0/items"
DEFAULT_PAGE_SIZE = 100
REQUEST_TIMEOUT_SECONDS = 5
DOI_RESOLVER_HOSTS = {"doi.org", "dx.doi.org"}


class ResolverError(Exception):
    """An expected resolver failure that can be reported as JSON."""


def normalize_doi(value: Any) -> str:
    """Normalize DOI prefixes and URL encoding while keeping exact identity."""
    if not isinstance(value, str):
        return ""
    text = value.strip()
    if not text:
        return ""

    parsed = urllib.parse.urlsplit(text)
    if parsed.scheme.lower() in {"http", "https"} and parsed.hostname:
        if parsed.hostname.lower() in DOI_RESOLVER_HOSTS:
            text = urllib.parse.unquote(parsed.path).lstrip("/")
    elif text[:4].lower() == "doi:":
        text = text[4:].strip()

    return urllib.parse.unquote(text).strip().casefold()


_EXTRA_DOI_RE = re.compile(r"^\s*doi\s*:\s*(\S.*?)\s*$", re.IGNORECASE | re.MULTILINE)


def zotero_item_dois(item: dict[str, Any]) -> set[str]:
    """Return DOI values explicitly present in Zotero item metadata."""
    data = item.get("data")
    if not isinstance(data, dict):
        return set()

    values: list[Any] = [data.get("DOI")]
    extra = data.get("extra")
    if isinstance(extra, str):
        values.extend(_EXTRA_DOI_RE.findall(extra))

    url = data.get("url")
    if isinstance(url, str):
        parsed = urllib.parse.urlsplit(url.strip())
        if parsed.scheme.lower() in {"http", "https"} and parsed.hostname:
            if parsed.hostname.lower() in DOI_RESOLVER_HOSTS:
                values.append(urllib.parse.unquote(parsed.path).lstrip("/"))

    return {doi for value in values if (doi := normalize_doi(value))}


def _read_json(url: str, *, label: str) -> Any:
    request = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        raise ResolverError(f"Zotero {label} request failed with HTTP {exc.code}.") from None
    except urllib.error.URLError as exc:
        reason = getattr(exc, "reason", None)
        if isinstance(reason, OSError):
            detail = reason.strerror or reason.__class__.__name__
        else:
            detail = str(reason or exc.reason or "connection failed")
        raise ResolverError(f"Zotero local API is unavailable during {label}: {detail}.") from None
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise ResolverError(f"Zotero returned invalid JSON during {label}.") from None
    except TimeoutError:
        raise ResolverError(f"Zotero {label} request timed out.") from None
    except OSError as exc:
        raise ResolverError(f"Zotero {label} request failed: {exc.strerror or exc.__class__.__name__}.") from None


class ZoteroReader:
    """Read top-level items and their child attachments from local Zotero."""

    def __init__(self, page_size: int = DEFAULT_PAGE_SIZE) -> None:
        if page_size < 1 or page_size > 100:
            raise ValueError("page_size must be between 1 and 100")
        self.page_size = page_size

    def matching_parents(
        self, requested_dois: set[str]
    ) -> tuple[dict[str, list[dict[str, Any]]], int]:
        matches = {doi: [] for doi in requested_dois}
        offset = 0
        scanned = 0
        seen_pages: set[tuple[str, ...]] = set()

        while True:
            query = urllib.parse.urlencode(
                {"format": "json", "limit": self.page_size, "start": offset}
            )
            page = _read_json(
                f"{ZOTERO_API_ROOT}/top?{query}", label=f"top-level item page at start={offset}"
            )
            if not isinstance(page, list):
                raise ResolverError("Zotero returned an unexpected top-level item response.")
            if not page:
                break

            page_keys = tuple(
                str(item.get("key", "")) for item in page if isinstance(item, dict)
            )
            if page_keys and page_keys in seen_pages:
                raise ResolverError(
                    f"Zotero pagination repeated the page at start={offset}; stopping to avoid an incomplete lookup."
                )
            seen_pages.add(page_keys)

            for item in page:
                if not isinstance(item, dict):
                    continue
                scanned += 1
                for doi in zotero_item_dois(item) & requested_dois:
                    matches[doi].append(item)

            offset += len(page)
            if len(page) < self.page_size:
                break

        return matches, scanned

    def child_attachments(self, parent: dict[str, Any]) -> list[dict[str, Any]]:
        key = parent.get("key")
        if not isinstance(key, str) or not key:
            raise ResolverError("A DOI-matched Zotero item has no item key for attachment lookup.")
        encoded_key = urllib.parse.quote(key, safe="")
        query = urllib.parse.urlencode({"format": "json"})
        children = _read_json(
            f"{ZOTERO_API_ROOT}/{encoded_key}/children?{query}",
            label="attachment child-item lookup",
        )
        if not isinstance(children, list):
            raise ResolverError("Zotero returned an unexpected attachment child-item response.")
        return [
            child
            for child in children
            if isinstance(child, dict)
            and isinstance(child.get("data"), dict)
            and child["data"].get("itemType") == "attachment"
        ]


def _file_uri_path(value: Any) -> Path | None:
    """Decode a local file URI, including percent-escaped filenames."""
    if not isinstance(value, str):
        return None
    parsed = urllib.parse.urlsplit(value.strip())
    if parsed.scheme.lower() != "file":
        return None
    if parsed.netloc and parsed.netloc.lower() != "localhost":
        return None
    if not parsed.path:
        return None
    return Path(urllib.parse.unquote(parsed.path))


def _local_path(value: Any) -> Path | None:
    if not isinstance(value, str) or not value.strip():
        return None
    value = value.strip()
    as_uri = _file_uri_path(value)
    if as_uri is not None:
        return as_uri
    if value.lower().startswith("file:"):
        return None
    path = Path(value)
    return path if path.is_absolute() else None


def _is_pdf_attachment(attachment: dict[str, Any]) -> bool:
    data = attachment.get("data")
    if not isinstance(data, dict):
        return False
    content_type = str(data.get("contentType", "")).split(";", 1)[0].strip().lower()
    filename = str(data.get("filename", "")).strip().lower()
    if content_type == "application/pdf" or filename.endswith(".pdf"):
        return True
    for value in (data.get("url"), attachment.get("links", {}).get("enclosure", {}).get("href")):
        if isinstance(value, str):
            parsed = urllib.parse.urlsplit(value)
            if parsed.path.lower().endswith(".pdf"):
                return True
    return False


def _attachment_locations(attachment: dict[str, Any]) -> tuple[list[Path], list[str]]:
    """Return local path candidates and direct PDF URLs without fetching them."""
    data = attachment.get("data", {})
    links = attachment.get("links", {})
    paths: list[Path] = []
    urls: list[str] = []

    if isinstance(links, dict):
        enclosure = links.get("enclosure", {})
        if isinstance(enclosure, dict):
            href = enclosure.get("href")
            path = _file_uri_path(href)
            if path is not None:
                paths.append(path)
            elif isinstance(href, str) and href.lower().startswith(("http://", "https://")):
                if urllib.parse.urlsplit(href).path.lower().endswith(".pdf"):
                    urls.append(href)

    if isinstance(data, dict):
        path = _local_path(data.get("path"))
        if path is not None:
            paths.append(path)
        url = data.get("url")
        if isinstance(url, str) and url.strip():
            parsed = urllib.parse.urlsplit(url.strip())
            content_type = str(data.get("contentType", "")).split(";", 1)[0].strip().lower()
            if (
                content_type == "application/pdf"
                or parsed.path.lower().endswith(".pdf")
                or str(data.get("filename", "")).lower().endswith(".pdf")
            ):
                urls.append(url.strip())

    # Preserve separate attachment records, but avoid reporting the same URI twice
    # when Zotero exposes it in both the path and enclosure fields.
    unique_paths: list[Path] = []
    seen_paths: set[str] = set()
    for path in paths:
        identity = str(path)
        if identity not in seen_paths:
            seen_paths.add(identity)
            unique_paths.append(path)
    unique_urls = list(dict.fromkeys(urls))
    return unique_paths, unique_urls


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_catalog(path: Path = CATALOG_PATH) -> list[dict[str, Any]]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except OSError as exc:
        raise ResolverError(f"Could not read source catalog: {exc.strerror or exc.__class__.__name__}.") from None
    except json.JSONDecodeError:
        raise ResolverError("Source catalog contains invalid JSON.") from None

    sources = payload.get("sources") if isinstance(payload, dict) else None
    if not isinstance(sources, list):
        raise ResolverError("Source catalog does not contain a sources array.")
    valid_sources = [source for source in sources if isinstance(source, dict)]
    if not valid_sources:
        raise ResolverError("Source catalog contains no valid source records.")
    return valid_sources


def _file_record(
    path: Path,
    *,
    source: str,
    reviewed_sha256: str,
    parent_index: int | None = None,
    attachment_index: int | None = None,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    display_path = str(path)
    details: dict[str, Any] = {"source": source, "path": display_path}
    if parent_index is not None:
        details["zotero_parent_index"] = parent_index
    if attachment_index is not None:
        details["zotero_attachment_index"] = attachment_index

    try:
        if not path.is_file():
            return None, {**details, "reason": "File is missing or is not a regular file."}
        actual_sha256 = _sha256(path)
    except OSError as exc:
        reason = exc.strerror or exc.__class__.__name__
        return None, {**details, "reason": f"File could not be read: {reason}."}

    matches = actual_sha256.casefold() == reviewed_sha256.casefold() if reviewed_sha256 else None
    record: dict[str, Any] = {
        **details,
        "sha256": actual_sha256,
        "matches_reviewed_snapshot": matches,
    }
    return record, None


def _empty_source_result(source: dict[str, Any]) -> dict[str, Any]:
    review = source.get("fulltext_review")
    if not isinstance(review, dict):
        review = {}
    return {
        "id": source.get("id"),
        "doi": source.get("doi"),
        "title": source.get("title"),
        "reviewed_pdf_sha256": review.get("pdf_sha256"),
        "available_pdf_paths": [],
        "available_pdf_urls": [],
        "available_pdfs": [],
        "missing_pdf_candidates": [],
        "matches_reviewed_snapshot": False,
        "preferred_snapshot_paths": [],
        "zotero_lookup": {"status": "not_attempted"},
        "errors": [],
    }


def resolve(
    sources: list[dict[str, Any]],
    source_ids: list[str],
    *,
    page_size: int = DEFAULT_PAGE_SIZE,
) -> tuple[dict[str, Any], int]:
    by_id: dict[str, dict[str, Any]] = {}
    for source in sources:
        source_id = source.get("id")
        if isinstance(source_id, str):
            by_id[source_id] = source

    selected_ids = list(dict.fromkeys(source_ids))
    errors: list[str] = []
    results: list[dict[str, Any]] = []
    valid_sources: list[dict[str, Any]] = []

    for source_id in selected_ids:
        source = by_id.get(source_id)
        if source is None:
            errors.append(f"Unknown source ID: {source_id}.")
            continue
        result = _empty_source_result(source)
        results.append(result)
        valid_sources.append(source)

    requested_dois = {
        doi
        for source in valid_sources
        if (doi := normalize_doi(source.get("doi")))
    }
    for source, result in zip(valid_sources, results):
        if not normalize_doi(source.get("doi")):
            result["errors"].append("Source record has no valid DOI.")

    # Check skill-local copies before querying Zotero so they remain available
    # in the output even when Zotero is closed.
    for source, result in zip(valid_sources, results):
        source_id = source.get("id")
        if not isinstance(source_id, str):
            continue
        for local_path, local_source in (
            (BUNDLED_PAPERS_DIR / f"{source_id}.pdf", "bundled paper"),
            (FULLTEXT_DIR / f"{source_id}.pdf", "full-text directory"),
        ):
            if not (local_path.exists() or local_path.is_symlink()):
                continue
            record, missing = _file_record(
                local_path,
                source=local_source,
                reviewed_sha256=str(result.get("reviewed_pdf_sha256") or ""),
            )
            if record is not None:
                result["available_pdfs"].append(record)
            if missing is not None:
                result["missing_pdf_candidates"].append(missing)

    try:
        if requested_dois:
            reader = ZoteroReader(page_size=page_size)
            parents_by_doi, scanned = reader.matching_parents(requested_dois)
        else:
            reader = None
            parents_by_doi, scanned = {}, 0
        api_error = None
    except (ResolverError, ValueError) as exc:
        parents_by_doi = {}
        scanned = 0
        api_error = str(exc)

    for source, result in zip(valid_sources, results):
        doi = normalize_doi(source.get("doi"))
        if api_error:
            result["zotero_lookup"] = {"status": "error", "error": api_error}
            result["errors"].append(api_error)
            continue

        parents = parents_by_doi.get(doi, [])
        if not parents:
            message = f"No Zotero top-level item matched DOI {source.get('doi')} after normalization."
            result["zotero_lookup"] = {"status": "not_found", "error": message}
            result["errors"].append(message)
            continue

        attachments_by_parent: list[list[dict[str, Any]]] = []
        child_error: str | None = None
        for parent in parents:
            try:
                attachments_by_parent.append(reader.child_attachments(parent))
            except ResolverError as exc:
                child_error = str(exc)
                attachments_by_parent.append([])

        pdf_attachment_count = sum(
            1
            for attachments in attachments_by_parent
            for attachment in attachments
            if _is_pdf_attachment(attachment)
        )
        result["zotero_lookup"] = {
            "status": "found",
            "top_level_item_matches": len(parents),
            "pdf_attachment_count": pdf_attachment_count,
            "ambiguous": len(parents) > 1 or pdf_attachment_count > 1,
        }
        if child_error:
            result["zotero_lookup"]["error"] = child_error
            result["errors"].append(child_error)

        for parent_index, attachments in enumerate(attachments_by_parent, start=1):
            for attachment_index, attachment in enumerate(attachments, start=1):
                if not _is_pdf_attachment(attachment):
                    continue
                paths, urls = _attachment_locations(attachment)
                for path in paths:
                    record, missing = _file_record(
                        path,
                        source="Zotero attachment",
                        reviewed_sha256=str(result.get("reviewed_pdf_sha256") or ""),
                        parent_index=parent_index,
                        attachment_index=attachment_index,
                    )
                    if record is not None:
                        result["available_pdfs"].append(record)
                    if missing is not None:
                        result["missing_pdf_candidates"].append(missing)
                for url in urls:
                    result["available_pdf_urls"].append(
                        {
                            "source": "Zotero attachment",
                            "url": url,
                            "matches_reviewed_snapshot": None,
                            "zotero_parent_index": parent_index,
                            "zotero_attachment_index": attachment_index,
                        }
                    )

        if pdf_attachment_count == 0:
            message = "DOI-matched Zotero item has no PDF child attachment."
            result["zotero_lookup"]["error"] = message
            result["errors"].append(message)

    for result in results:
        # Keep all candidates and duplicates, with the reviewed bytes first when
        # present. A changed file remains visible with its own current hash.
        result["available_pdfs"].sort(
            key=lambda record: (
                record.get("matches_reviewed_snapshot") is not True,
                {"bundled paper": 0, "full-text directory": 1, "Zotero attachment": 2}.get(
                    record.get("source"), 3
                ),
                record.get("zotero_parent_index", 0),
                record.get("zotero_attachment_index", 0),
            )
        )
        result["available_pdf_paths"] = [record["path"] for record in result["available_pdfs"]]
        result["matches_reviewed_snapshot"] = any(
            record.get("matches_reviewed_snapshot") is True
            for record in result["available_pdfs"]
        )
        result["preferred_snapshot_paths"] = [
            record["path"]
            for record in result["available_pdfs"]
            if record.get("matches_reviewed_snapshot") is True
        ]
        if result["missing_pdf_candidates"]:
            count = len(result["missing_pdf_candidates"])
            result["errors"].append(
                f"{count} PDF candidate path(s) are missing or unreadable; see missing_pdf_candidates."
            )
    payload = {
        "catalog": str(CATALOG_PATH),
        "zotero_api": ZOTERO_API_ROOT,
        "zotero_top_level_items_scanned": scanned,
        "source_count": len(results),
        "errors": errors,
        "sources": results,
    }
    exit_code = 1 if errors or any(source["errors"] for source in results) else 0
    return payload, exit_code


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Resolve existing PDF paths from references/papers/<ID>.pdf, optional "
            "full-text/<ID>.pdf, and Zotero's read-only loopback API. PDF content "
            "is never downloaded or extracted."
        )
    )
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument(
        "--source",
        dest="source_ids",
        action="append",
        metavar="ID",
        help="Resolve one source; repeat this option to resolve multiple IDs.",
    )
    selection.add_argument("--all", action="store_true", help="Resolve every catalog source.")
    parser.add_argument(
        "--page-size",
        type=int,
        default=DEFAULT_PAGE_SIZE,
        metavar="N",
        help="Zotero items per page (1–100; default: 100).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        sources = _load_catalog()
    except ResolverError as exc:
        print(json.dumps({"errors": [str(exc)], "sources": []}, indent=2))
        return 2

    if not 1 <= args.page_size <= 100:
        print(
            json.dumps(
                {"errors": ["--page-size must be between 1 and 100."], "sources": []},
                indent=2,
            )
        )
        return 2

    known_ids = [source.get("id") for source in sources if isinstance(source.get("id"), str)]
    source_ids = known_ids if args.all else args.source_ids
    payload, exit_code = resolve(sources, source_ids or [], page_size=args.page_size)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
