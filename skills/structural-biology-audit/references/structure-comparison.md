# Structural Comparison Audit

Invoke as needed only when claims refer to the same fold, the same conformation, structural similarity, or a conformational change.
Comparison scores describe similarity for a specified atom set, residue mapping, and superposition target; by themselves, they do not establish function, evolution, or mechanism.

## Define the objects being compared

- Confirm whether the objects are the same protein, homologous proteins, complexes, or a predicted model; record the structure source and whether it is experimental or predicted.
- Align sequences or entity identifiers and check species, isoform, mutations, missing segments, tags, fusion proteins, and construct boundaries.
- Specify whether the comparison is of the full chain, a domain, a local site, or a complex; report global and local results separately when needed.
- State the chains, atom sets, residue correspondences, treatment of missing residues, and superposition program/version used.
- Specify whether the comparison uses Cα, backbone, or all heavy atoms; including side chains or ligands changes what the result means.
- For repeated domains, oligomers, or symmetry-related chains, explain how chain correspondence and symmetry-equivalent solutions were handled.
- If structures have chain breaks, unresolved loops, or different numbering, first establish an explicit one-to-one residue mapping.
- Check whether the mapping spans insertions, deletions, or chain permutations; residue pairs assigned by automatic alignment software are not experimental identity annotations.
- Inspect alignment coverage and unaligned regions; a high score for a short local segment does not imply whole-protein similarity.
- If the structures differ in ligand, ion, crystal form, temperature, or assembly state, list these first as condition variables rather than directly calling the difference an intrinsic protein change.
- For flexible proteins, check whether different reasonable alignments change the main conclusion; do not report only the result with the lowest RMSD.
- For multidomain proteins, assess intradomain folds and interdomain arrangements separately so that a global fit does not hide local differences.
- When comparing a predicted model with an experimental model, record model confidence and the experimentally resolved regions that can be compared.

## RMSD / normalized distance

- When reporting RMSD, also state the number of corresponding atoms, residue coverage, and segments used; an Å value alone cannot be reproduced.
- Do not directly rank RMSD values calculated with different lengths, coverage, or residue mappings.
- Specify whether RMSD is for Cα, backbone, or all atoms; values for different atom sets are not the same metric.
- In interpreting RMSD, distinguish “similar after alignment” from “same whole-chain conformation”; a local alignment can hide global movement.
- Provide the residues used for fitting; if the core is fitted first and peripheral changes are then examined, report both ranges separately.
- Carugo–Pongor normalized RMSD corrects for size effects; it cannot remedy an incorrect alignment, incorrect residue correspondence, or differences in structure quality.
- When using normalized RMSD, report the reference length and the number of residues actually used in the formula so the result can be recalculated and distinguished from raw RMSD.
- This normalized formula is based on a specific statistical derivation; do not apply it mechanically to short alignments, and do not treat it as a criterion for functional equivalence.
- If one structure is a predicted model and the other is experimental, first confirm that the comparison is restricted to credible regions and state where local data support a difference.

## TM-align / TM-score

- TM-align optimizes residue alignment for structural similarity; report the program, chain lengths, alignment length/coverage, and which chain was used for each normalization.
- The TM-align study used 0.5 as a benchmark for its specific PDB fold-classification task; do not present 0.5 as a universal hard threshold.
- TM-score normalization depends on target length; if the tool returns values normalized by both chain lengths, do not report only the higher value without saying so.
- When reporting results for local domains or different boundaries, identify the segment scored; the global score may be affected by interdomain arrangement.
- The method can also find structural analogs for folds or misfolded models; a high structural score does not mean a model is correct.
- A high TM-score or low RMSD alone does not prove homology, the same ligand preference, the same activity, or the same physiological state.
- For complex comparisons, examine the monomer, interface, and relative chain positions separately; similar single-chain folds do not guarantee the same assembly.
- If chain identity or oligomeric symmetry operations are ambiguous, list the correspondence options and check whether the result depends on one particular chain pairing.

## Constraints on wording conclusions

- With only one metric, write “similar within the specified alignment range” rather than broadly claiming “the same structure.”
- If a conclusion depends on a local site, provide its local alignment, ligand/cofactor state, and supporting data.
- If a conclusion depends on a structural change, confirm that residue mapping is consistent and distinguish rigid-body domain motion, local rearrangement, and model-building differences.
- If the conclusion is unstable to alignment method, coverage, or construct changes, mark it as uncertain; do not select whichever result best supports the narrative.
- If resolution, local density, or model quality differs substantially, limit the comparison to regions supported by data in both structures.
- Check that residue mapping is consistent around the active site; verify ligand orientation or side-chain differences against local data.
- Use structural comparison to locate differences to test; take functional or mechanistic interpretation to the corresponding audit rather than extrapolating from scores.

## Specified references and locations

- Carugo & Pongor (2001), [DOI: 10.1110/ps.690101](https://doi.org/10.1110/ps.690101): PDF pp. 1–4 (printed pp. 1470–1473), especially pp. 2 and 4 for the constructed data, equations 2–5, and scope. The normalization addresses size effects in the number of equivalent residues in an alignment; its parameters were derived from 180 nonhomologous PDB proteins and an artificial set made by randomizing their Cα coordinates. The authors recommend it for alignments longer than 40 residues; the equation becomes negative below 14 residues, so do not use it to rank alignments shorter than the recommended range. It does not correct an incorrect mapping and is not a calibration criterion for functional equivalence.
- Zhang & Skolnick (2005), [DOI: 10.1093/nar/gki524](https://doi.org/10.1093/nar/gki524): PDF pp. 2–3 (printed pp. 2303–2304) for methods and coverage comparisons; PDF p. 4 (printed p. 2305) for interpretation of TM-score 0.5; PDF pp. 7–8 (printed pp. 2308–2309) for predicted-model/decoy comparisons. The authors explicitly describe 0.5 as an empirical threshold oriented toward structural modeling, not a universal hard boundary across tasks; their decoy results also show that similarity to a known structure cannot by itself validate a model.

These two references support distance and structural-alignment methods; they are not standalone evidence for function, assembly, or mechanism.
