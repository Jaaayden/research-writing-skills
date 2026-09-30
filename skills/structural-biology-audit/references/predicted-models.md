# Predicted Model Audit

Invoke as needed when a paper uses predicted coordinates, such as AlphaFold models, to make claims about experimental structures, ligand binding, interfaces, or mechanisms. Predicted models can suggest structural hypotheses or aid interpretation; without experimental data, do not call them “determined structures.”

## Model provenance and scope of the question

- Record the model family/generation, output used, target sequence, and residue range; for complexes, also check partners, construct, mutations/modifications, and ligand inputs. Record the database, weights, code, run date, and sampling details only when they affect model identity, reproducibility, or the current claim.
- AlphaFold 2, AlphaFold-Multimer, and AlphaFold 3 have different tasks, inputs, and scores and must not be conflated. If a paper says only “AlphaFold” and the version cannot be identified from context, mark the version as unspecified.
- When citing benchmark evaluations, state the task, test set, homology filtering, training cutoff, and sampling/ranking procedure. Benchmark success rates describe that test set, not the probability that an individual target is correct.

## Confidence and coordinate fields

- pLDDT is the model’s estimate of local accuracy; PAE describes predicted aligned error in the relative positioning of residues/chains; pTM/ipTM are overall or interface scores. None is an experimental observation, binding affinity, occupancy, or probability that an individual target is correct.
- High intrachain pLDDT does not guarantee domain arrangement, side-chain, or interface accuracy; inspect the regions relevant to the claim, do not hide weak regions with an average score, and do not apply a universal threshold to declare a structure correct.
- Do not treat prediction confidence as an experimental B factor. If confidence is stored in the B-factor field of a predicted PDB/mmCIF file, first check the generating program and file provenance, then state what the field means; experimental B factors are also affected by data and refinement conditions.

## Prediction priors and experimental support

- If predicted coordinates were used for molecular replacement, initial model building, rebuilding missing regions, restraints, or refinement, record their use. Agreement between a predicted model and the same data it helped fit is not independent evidence; check whether the experimental data can distinguish the original model from reasonable alternatives.
- When a predicted model is placed into cryo-EM or X-ray density, inspect support in the actual experimental map and record the relevant resolution, map processing, and fitting conditions. For discrepancies, also consider construct, ligand, modification, crystal contacts, and conformational state; report high-confidence conflicts rather than resolving them by score alone.
- Predicted ligand or ion positions are not experimental evidence of binding, occupancy, stoichiometry, or function. Binding or mechanistic claims need corresponding experimental support.

## Register-checking tools

- checkMySequence requires a cryo-EM map, coordinate model, and chain sequence; it uses residue assignments supported by the map to flag possible register problems. The paper’s p-value cutoff is an empirical choice based on fragment benchmarks, not the probability that a model is wrong. Test fragments can be extended from 20 to 60 residues; the authors note that detectable errors typically need to exceed about 10 residues, and shorter errors may be missed. Treat the result as a candidate and re-examine the map, sequence, and alternative registers.
- Contact-map screening tools such as conkit-validate compare contacts in a model with predicted AF2 contacts; this is a map-independent computational signal, not experimental validation. The paper first requires a register error spanning at least 5 consecutive residues, then applies filters, and ultimately calls the output a putative error. It depends on contact-prediction quality; conformational differences or fold switches may also trigger a flag, so check against local experimental data and sequence.

## Generation, evaluation, and code boundaries

- The 2021 AF2 paper reports performance for that version on CASP14 and specific PDB benchmarks; benchmark relationships between pLDDT/pTM and measured structural error cannot be transferred unconditionally to later AF2 pipelines or AF3.
- The 2024 AF3 paper covers specific evaluation tasks involving proteins, nucleic acids, ligands, ions, and modifications, and still reports limitations in conformational coverage, hallucination in disordered regions, chirality/clashes, and accuracy for some targets. When restating its numbers, check the training cutoff and output-ranking procedure for that task. For example, the PoseBusters models used a 2019-09-30 cutoff, while other main evaluations used a 2021-09-30 cutoff; standard results selected the top-confidence prediction from 5 model seeds and 5 diffusion samples per seed, while a specific antibody analysis used 1,000 seeds.
- The AF3 Addendum says that the underlying inference code was released after the original paper was published; it does not correct the original paper’s accuracy or scientific conclusions. Check code availability and license terms separately for the version used.

## References and original locations

- Jumper et al. (2021), [DOI: 10.1038/s41586-021-03819-2](https://doi.org/10.1038/s41586-021-03819-2): Fig. 2c,d comparing pLDDT/pTM with lDDT/TM-score on PDB benchmarks (PDF p. 3); “MSA depth and cross-chain contacts” and Discussion (p. 6); Methods “Inference regimen”, “Metrics”, and “Test set of recent PDB sequences” (pp. 9–10).
- Abramson et al. (2024), [DOI: 10.1038/s41586-024-07487-w](https://doi.org/10.1038/s41586-024-07487-w): Fig. 1 and architecture (PDF pp. 2–4); “Accuracy across complex types”, “Predicted confidences track accuracy”, “Model limitations”, and Figs. 4–5 (pp. 5–7); Methods “Inference regime”, “Metrics”, “Recent PDB evaluation set”, and “PoseBusters” (pp. 9–10); Extended Data Figs. 7–8 and Table 1 (pp. 18–19, 21).
- Abramson et al. (2024), [Addendum DOI: 10.1038/s41586-024-08416-7](https://doi.org/10.1038/s41586-024-08416-7): full short paper (PDF p. 1), which states that inference code was released later.
- Akdel et al. (2022), [DOI: 10.1038/s41594-022-00849-w](https://doi.org/10.1038/s41594-022-00849-w): Figs. 1, 3–6 and corresponding results (PDF pp. 2–10); Methods on oligomerization and experimental model building (pp. 13–15). The pocket analysis notes that the high-confidence subset may be affected by template bias; the oligomer test allowed potential overlap with training data.
- Terwilliger et al. (2024), [DOI: 10.1038/s41592-023-02087-4](https://doi.org/10.1038/s41592-023-02087-4): “Comparing AlphaFold predictions with density maps” and Fig. 1 (PDF p. 2); Fig. 4, Table 1, and “Using confidence (pLDDT) to estimate errors” (p. 5); Methods and “Control experiments and limitations” (pp. 8–9). Among 102 selected high-quality crystallographic models/maps, about 10% of Cα coordinates with pLDDT >90 differed from the reference structure by more than 2 Å; this proportion is limited by sample composition and crystallization conditions.
- Chojnowski (2022), [DOI: 10.1107/S2059798322005009](https://doi.org/10.1107/S2059798322005009): §2 on input and fragment assignment, §§3.1–3.4 on data and methods, §§4.1–4.7 and Conclusions (PDF pp. 2–10), Figs. 1, 2, 7–9. The author describes high-confidence mismatches as possible register problems; threshold selection, compensation for low resolution, and limitations for short errors are in §§4.1, 4.2, and Conclusions.
- Sánchez Rodríguez et al. (2024), [DOI: 10.1107/S2052252524009114](https://doi.org/10.1107/S2052252524009114): §§2.1–2.6 on data sets/screening, §§3.1–3.6 on results, cross-checks, and limitations, and Figs. 1–11 (PDF pp. 2–12). Scope: cryo-EM and X-ray PDB entries at 3–5 Å resolution through 2022-04-05; the authors call the output putative register errors and show a calcineurin fold-switch false positive in Fig. 11.

These sources support treating predictions as auditable hypotheses; they do not provide a free pass to skip checking the current target.
