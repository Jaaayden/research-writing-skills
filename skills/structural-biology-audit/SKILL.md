---
name: structural-biology-audit
description: Audit whether structural-biology claims are supported by traceable evidence. Use for single-particle cryo-EM, macromolecular X-ray crystallography, local density and contacts, model validation, structure comparisons, and assembly or mechanism claims derived from experimental or predicted structures. Does not write articles.
---

# Structural Biology Evidence Audit

Assess **whether this specific claim is justified by these data under these conditions**. Audit the cited method papers as well as the target study. Publication, citation count, established software, or PDB/EMDB deposition does not establish correctness.

The current scope is single-particle cryo-EM, macromolecular X-ray crystallography, and issues shared across methods. Specialized criteria for cryo-ET, helical reconstruction, NMR, and SAXS have not been established here; identify that scope gap rather than applying SPA or crystallographic criteria mechanically.

## Select guidance by claim

Read only the guides relevant to the current claim:

| Claim or concern | Guide |
|---|---|
| FSC, global/local resolution, anisotropy, sharpening | [cryo-em.md](references/cryo-em.md) |
| Diffraction data, cutoff, Rwork/Rfree, coordinate precision | [xray.md](references/xray.md) |
| Ligand identity/pose, density, hydrogen bonds, Mg²⁺ and other mononuclear metal sites | [ligand-density.md](references/ligand-density.md) |
| Alignment scope, RMSD, domains, conformational differences | [structure-comparison.md](references/structure-comparison.md) |
| Local fit, geometry, sequence/register, validation reports | [model-validation.md](references/model-validation.md) |
| Evidence required by resolved, binds, hydrogen bond, stabilizes, causes | [terminology.md](references/terminology.md) |
| Processing, reference/model bias, classification, symmetry, overfitting, held-out data | [data-processing-and-bias.md](references/data-processing-and-bias.md) |
| Actual construct, assembly, crystal contacts, buffer conditions, temperature | [biological-context.md](references/biological-context.md) |
| Predictions versus experiment, pLDDT/PAE/ipTM | [predicted-models.md](references/predicted-models.md) |
| Static structures, dynamics, causality, induced fit/conformational selection, allostery | [mechanistic-inference.md](references/mechanistic-inference.md) |

Use [sources.md](references/sources.md) for source roles and scope. Look up source IDs or DOIs in [sources.json](references/sources.json) for metadata, citation snapshots, versions, and verified original passages. The catalog is **not a table of automatic pass/fail thresholds**. For access to complete original papers, see [full-text.md](references/full-text.md).

The English guides are navigation and audit prompts, not replacements for the papers. For a method-dependent verdict, disputed interpretation, exact definition, numerical criterion, or exception, open the relevant original PDF and its applicable update, and inspect the needed text, methods, figures, and supplements. If a guide disagrees with the verified source, qualify or correct the guide-derived interpretation; do not silently privilege the summary. A PDF being available does not mean it has been read or that its results have been independently reproduced.

## Audit workflow

1. **Decompose the claim.** Preserve its exact wording. Separate observations, identity/interaction assignments, comparisons, and mechanistic inferences. Establish method, accession/version, chain/residue/ligand, experimental state, and controls. Resolve what the materials provide; ask only about unknowns that affect the verdict.
2. **Establish accessible evidence.** Read the article, methods, available supplements, and public PDB/EMDB validation reports. Retrieve coordinates, maps/half-maps, masks, or structure factors when the claim warrants them. Record coverage and publication/deposition versions. Distinguish checking a report, recomputing from deposited data, and reprocessing raw data. Reading a paper may support “the authors report X”; it does not support “independent recomputation confirms X.” Coordinates or pictures alone do not establish that density, FSC, or processing was checked. Missing materials do not prove an error.
3. **Check assumptions and independence.** Verify construct/sequence, sample conditions, processing, classification/symmetry, references, prediction priors, half-set/test-set independence, and refinement restraints. Agreement with a restraint is not independent evidence. A prior used in modeling cannot be counted again as independent corroboration.
4. **Move from global to local evidence.** Global statistics provide context; the claimed atoms, residues, ligand, or interface need local support. Distinguish EM and X-ray maps, FSC, correlation coefficients, B factors/occupancies, and OMIT-map interpretations. Interpret distances, angles, and scores with chemistry, data quality, and uncertainty.
5. **Compare relevant alternatives.** Consider competing conformations, ligand poses/identities, ions/water, sequence assignments, assemblies, or processing assumptions that plausibly explain these observations. Do not turn all theoretical possibilities into a mandatory experiment list. Calculate when an available tool can resolve a material ambiguity; record inputs, versions, and key parameters. Do not default to installing large packages or reprocessing an entire particle dataset.
6. **Match the verdict to the wording.** Resolve source conflicts first, then assign a verdict below. Limit it to the claim and conditions actually checked; do not expand the task into article writing. If the source set does not cover the issue, verify directly relevant primary literature before adopting a new rule.

## Source quality and conflicts

- **Roles:** Anchor each topic in widely used foundational methods and supplement them with community recommendations and targeted validation/correction studies. Record one citation database and date. High citation counts indicate reach, not correctness; describe newer or narrowly focused studies by their actual role.
- **Original evidence and updates:** Check source passages, figures, assumptions, sample/resolution range, and available corrections, retractions, or subsequent validation through the journal, PubMed, or Crossmark. Metadata/abstract-only checks support background or pending entries, not operational rules. Finding no update is not an exhaustive proof that none exists.
- **Versions and coverage:** Record reviewed sections, PDF page indices, journal page numbers, figures, and unreviewed material; distinguish the two page-number systems. Identify accepted manuscripts, preprints, and versions of record. Check the version of record where numbering, wording, or methods may differ. A source snapshot supports only its documented coverage.
- **Comparability:** Determine whether two sources address the same proposition, statistic, definition, construct, conditions, resolution, and software/structure version. Different scope or reporting conventions do not automatically constitute a contradiction.
- **Evidence under matched conditions:** Compare directly relevant data, independence, reproducibility, limitations, formal recommendations, and targeted criticism. Assess experimental data quality too. Recency, citations, or reputation do not decide the outcome. Analyses sharing the same data/prior are not independent replicates.
- **Conditional adjudication:** State “Under X, prefer A because…; B applies under Y or cannot resolve this question because…,” with original evidence locations. If evidence is incomparable or inadequate, retain “source dispute unresolved” or “unresolved for these data,” and identify discriminating evidence.
- **Traceability:** Separate source findings, the resulting audit inference, and hypotheses still requiring validation. Apply errata to the passages they correct. Interpret an addendum by its actual content, not by its publication category.

## Output

For each claim, report:

**Original claim | Verdict | Evidence location | Applicability limits | Missing or discriminating evidence**. Add **Adjudication rationale** for source conflicts. Prefer article section/figure/supplement, DOI, PDB/EMDB accession and version, chain/residue, map type, and relevant parameters. A methodological citation does not replace the target study's local experimental evidence.

| Verdict | Meaning |
|---|---|
| Supported | Accessible, checked evidence supports the claim's strength and scope; state the conditions. |
| Requires qualification | Evidence supports part of the observation, but the wording exceeds its scope, identity certainty, or mechanistic strength. |
| Insufficient evidence | Key evidence is missing, unverifiable, or unable to distinguish interpretations; this does not establish that the claim is false. |
| Contradicted by evidence | Checked affirmative evidence conflicts with this specific claim; identify the conflict and evidence quality. |

“Modeled as Mg²⁺,” a PyMOL distance line, high pLDDT, or good global resolution does not by itself establish ion identity, a hydrogen bond, experimental correctness, or local resolvability. A static structure can support a snapshot observation; causality and mechanism require suitable independent evidence from the relevant system.

This skill defaults to read-only auditing. Altering coordinates, redepositing structures, writing to Zotero, or uploading unpublished material to an external validation service requires authorization for that action; an audit request alone does not imply it.
