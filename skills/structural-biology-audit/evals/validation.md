# Validation Record

Validation date: 2026-09-30. Cases are in [audit-cases.md](audit-cases.md).

## Methods and scope

Two independent evaluators in new contexts read the final skill and on-demand guides, then separately audited the six EM/chemistry cases and seven cross-method cases; they were not given the expected answers. The main task was to review each verdict, evidence location, and applicable boundary. The following is a summary of the final results; C6 contains two independent adjudications.

This is an acceptance check of text-audit behavior, not validation of real PDB/EMDB entries; particles and reflection data were not reprocessed, and map metrics were not calculated. The scope of source review and unchecked supplementary materials are recorded item by item in `references/sources.json`.

## Behavioral results

| Case | Result | Acceptance criteria |
|---|---|---|
| E1 | Requires qualification | 2.8 Å is only the reported masked value; the shared high-resolution reference between half-sets and the binary mask leave validation insufficient. This does not justify asserting that the true value is 3.8 Å. |
| E2 | Requires qualification | A global resolution of 2.8 Å does not establish that the ligand is clearly resolved locally; an ideal dictionary and fixed occupancy cannot validate the density by themselves. |
| E3 | Contradicted by evidence | Given the stated chemical states, both atoms are acceptors; a PyMOL distance line cannot create a donor. |
| E4 | Insufficient evidence | Distances obtained with Mg restraints, a spherical peak, and Mg in the buffer do not rule out Na or water; distance alone also cannot reclassify the site as Na. |
| E5 | Supported | The materials support the qualified reported-FSC convention; without a half-map, independent recalculation cannot be claimed. |
| E6 | Supported | The chemistry, local density, and geometry support “consistent with a hydrogen bond”; software-added H does not need to be misrepresented as experimentally resolved. |
| C1 | Contradicted by evidence (coordinate models only) | An RMSD for the 84/320-residue core cannot establish that the complete structures are identical; the reported domain rotation conflicts with identity of the overall structures. |
| C2 | Contradicted by evidence (evidence source only) | The pLDDT in an AF file is not an experimental B factor; actual mobility remains undetermined. |
| C3 | Requires qualification | Two static endpoints do not adjudicate induced fit versus conformational selection; condition-matched kinetic and pathway-flux evidence is needed. |
| C4 | Insufficient evidence | Under matched conditions, SEC-MALS is the more direct evidence for solution state, while PISA gives a crystal-based candidate; intracellular assembly remains unresolved. |
| C5 | Insufficient evidence | An AF-based register warning is a candidate; the claim that “every putative error has been experimentally confirmed” conflicts with false positives in the source. |
| C6-A | Requires qualification | FSC criteria are adjudicated according to their statistical definitions and conditions; citation counts do not invalidate the other criterion, and there is no requirement to report only one threshold. |
| C6-B | Contradicted by evidence | The AF3 Addendum is a code-release note; the specific correction in the erratum must be applied to the Cruickshank formula. |
| C7 | Supported | The coordinates support the trajectory of the 84 Cα atoms in the core under the stated mapping and boundaries; this does not extend to the full chain, all backbone atoms, function, or experimental correctness. |

Verdicts are not scored mechanically by a single label: E1's “Requires qualification” limits the claim to the reported value while explicitly noting that validation of the actual resolution is insufficient; the contradictions for C1/C2 likewise cover only conflicts with positive evidence already available, and unknown biological questions are not judged incorrect. All 13 cases meet the acceptance boundaries above.

## Evaluation feedback and checks

- Comparisons with alternative poses or partial occupancies under “clearly resolved” were limited to cases with a realistic ambiguity, avoiding a uniform experimental threshold for every local-shape claim; the independent evaluators confirmed the revision.
- PDF page sequence numbers and journal print page numbers are now labeled separately; mixed location references in the cross-method evaluation report were corrected against the source catalog.
- The official `skill-creator` `quick_validate.py` returned `Skill is valid!`.
- The source catalog passed checks for 39 unique DOI/IDs, 37 primary publications plus 2 updates, original-text locations, PDF page ranges, a consistent citation-count date, bidirectional update links, and local Markdown links.
- Zotero API readback confirmed the titles, journals, years, collections, subject and role tags of 39 entries, 39 PDF attachments, and two bidirectional update links. The initial bibliography check also verified authors and DOIs; original collections were retained for reused entries.
- At the initial delivery, the skill directory contained no API credentials, private Zotero paths, complete PDFs, or extracted full text. Later authorized PDF packaging is documented separately below. Full-text reading is not described as recalculation of original data.

## English revision and direct-PDF access

Revision date: 2026-09-30.

- An independent fidelity review compared all ten English guides and the English source-catalog descriptions with the previous committed version. It found no material scientific drift: conditions, units, numerical values, equation corrections, source locations and reviewed/unreviewed coverage were preserved. English punctuation was then normalized, and the DPI wording was clarified to identify coordinate uncertainty rather than diffraction measurement precision.
- A fresh-context evaluator, without expected answers, audited E1, E3, E5, E6, C4, C6 and C7. It returned Insufficient evidence, Contradicted by evidence, Supported, Supported, Requires qualification, Contradicted by evidence for both C6 subclaims, and Supported, respectively. These labels preserve the acceptance boundaries above: the masked FSC value remains a report rather than an unbiased independent validation; PISA does not override matched-condition solution evidence; and exclusive FSC or update interpretations conflict with the original sources. Differences from an earlier label are not evidence of a failed boundary when the same uncertainty and scope are preserved.
- Feedback clarified that missing half-maps limit a particular check rather than introducing a fifth verdict; a narrowly worded report can remain Supported. The independence audit now traces high-resolution information leakage through initialization and refinement rather than treating any shared initializer as an automatic failure. The synthetic X-ray hydrogen-bond case now calls 1.2 Å a reported diffraction limit, keeping its atom-level density evidence separate.
- The read-only PDF resolver passed offline fixtures for percent-encoded file paths, reviewed-snapshot preference, duplicate DOI/attachment records, differing hashes, missing files and an unavailable Zotero API. A live paginated scan of 660 top-level Zotero items matched all 39 catalog DOIs and found 39 available PDFs with reviewed-snapshot hashes. Availability is not a claim that every page was read or a result was recomputed.
- The skill passed the official `quick_validate.py`. The repository's existing 16 unit tests passed; this task did not change the installer.

## Authorized public PDF bundle

Review date: 2026-09-30.

- Per-file review of all 39 attached versions established 20 applicable express grants for this unchanged public, noncommercial educational/research distribution: 17 CC BY files (five 2.0 UK, three 3.0, nine 4.0), one CC BY-NC 4.0 file, one historical NAR/OUP noncommercial grant, and one IUPAC article-specific republication grant. Five records are not cleared under the reviewed restrictive terms and 14 have permission not established. All 19 remain in Zotero.
- An independent review checked the grants against actual PDF notices and authoritative publisher/CC records, including the generic rights-reserved footer alongside Read 2011's specific CC BY grant. It identified four bibliographic/page-count slips in a temporary review report; the maintained catalog and final redistribution record use the correct, previously verified versions and citations. Those slips did not refer to different DOI-matched PDFs.
- The bundle retains original bytes, copyright/license notices and full author/citation attribution; no PDF is relicensed under the repository MIT license. Noncommercial restrictions are explicit for Leonarski 2017 and TM-align 2005. Separate supplements, software and data are outside the grant unless actually included and covered.
- PDF annotation checks found no non-link annotations in the 20 included files. Restricted files with downloader network information and unclear third-party permissions were excluded. Private Zotero paths and credentials are not included in the public records.
- The final file/hash check matches every bundled PDF to its catalog review snapshot and redistribution record; files without a permitted decision are absent from the public bundle. The repository installer excludes private `full-text/` copies while retaining the licensed `references/papers/` files.
