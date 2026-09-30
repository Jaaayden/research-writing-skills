# Complete Original Papers

Use the English guides to identify the audit issue and source ID. Use the original paper, applicable erratum/addendum, and available supplements to establish what the source actually says. Reopen original evidence for definitions, numerical criteria, scope exceptions, methodological disputes, or a verdict that depends on precise wording. Do not turn a source summary into proof of the target study's claim.

## Resolve a paper

From the skill directory, run the read-only resolver:

```bash
python3 scripts/resolve_fulltext.py --source chen2013
python3 scripts/resolve_fulltext.py --source cruickshank1999 --source cruickshank1999-erratum
python3 scripts/resolve_fulltext.py --all
```

First check `references/papers/<source-id>.pdf`: a bundled file can be opened directly without Zotero. The resolver matches source IDs to catalog DOIs, then lists bundled papers, optional local copies and Zotero Desktop PDF attachments. Zotero must be running with its local API enabled for its attachment lookup; if it is unavailable, existing skill-local PDFs remain in the output alongside the API error. The resolver uses loopback GET requests, requires no write key, and does not import, download, modify, extract, or upload documents. Returned paths are runtime information, not portable metadata to commit.

DOI matching is exact after normalization. A general Zotero title/creator search may not find a DOI, so do not treat an empty text-search result as proof that the item is absent. Duplicate DOI records, multiple PDFs, missing local files, and unavailable Zotero are reported rather than silently resolved by title similarity.

## Check the actual version

The catalog records the SHA-256 and page count of the PDF reviewed on 2026-09-30. Compare the resolved file with that snapshot:

- A matching hash identifies the reviewed file; it does not prove every page or result was reviewed. Consult `fulltext_review.coverage` and `unresolved`.
- A different hash may reflect a different version, replacement, annotation or byte-level change. Inspect identity, version and pagination before reusing old locations. A mismatch does not by itself establish scientific disagreement.
- Retain alternative attachments when relevant; do not silently pick an accepted manuscript or an older version over the version of record.

Inspect the needed pages with available PDF-reading tools. Distinguish PDF page indices from printed journal pages. Render formulas, tables and figures when text extraction loses layout, Greek letters or symbols. Search text to navigate, but return to the page image when the interpretation depends on those details.

A complete main-article PDF may still omit separate Supplementary Information, datasets or code. Check them when the claim depends on them; existing catalog limitations remain in force until those materials are actually reviewed.

## Storage and redistribution

The public skill includes **20 complete source PDFs** in [papers/](papers/README.md). Every included file retains the exact original attachment bytes and has a recorded article-specific redistribution grant. [redistribution.json](redistribution.json) records all 39 decisions, evidence locations, versions, hashes and conditions. Papers retain their individual terms; the repository MIT license does not relicense these PDFs. Two included papers have noncommercial restrictions (Leonarski 2017 and TM-align 2005); the IUPAC article uses its own acknowledgment-based republication grant. The remaining 17 use the exact CC BY version recorded for each file.

The **19 PDFs without confirmed permission for this distribution remain in Zotero**. A restricted or unestablished redistribution status does not weaken a paper's scientific evidence; resolve the relevant original by DOI rather than selecting sources by whether a PDF is bundled. New or replacement attachments are not automatically cleared for public distribution by an earlier decision.

The resolver also recognizes `full-text/<source-id>.pdf` for an explicitly prepared private local bundle. That directory is excluded from Git, and this repository's project installer explicitly excludes it from copies. Copies should preserve complete original bytes and be checked against the catalog; editing or translating the source PDF is not part of this workflow. Do not assume another installer honors that exclusion.

A public repository copy requires permission for the particular PDF version, retention of attribution/copyright/license notices, and compliance with any noncommercial or third-party conditions. Free reading, PMC availability, an author's self-archiving right, generic journal policy, or text-and-data-mining access alone does not establish a full-PDF redistribution grant. The license record is a dated check for this bundle; it is not a universal clearance for other versions, supplements, figures, software or uses.
