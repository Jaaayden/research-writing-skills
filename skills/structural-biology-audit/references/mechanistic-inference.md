# Structure-to-Mechanism Inference Audit

Invoke as needed when a paper infers temporal order, causality, catalysis, allostery, or a ligand-recognition pathway from structural differences.
A static structure is first evidence from coordinates under specific preparation, ligand, and data-collection conditions; mechanistic conclusions require evidence that can distinguish competing explanations.

## Separate observations from inferences

- First state the directly observed differences: atom/residue positions, interfaces, ligands, ions, density, and model uncertainty.
- Then state the authors’ interpretation and identify whether it is a mechanistic hypothesis or a conclusion tested by independent experiments.
- Check whether both structures represent the same sequence/construct, consistent chain mapping, and comparable experimental states.
- Check apo/bound state, mutations, crystal form, temperature, pH, ions, substrate/cofactor, and other conditions; do not mislabel a difference in conditions as a single causal variable.
- If the structures come from different molecules, constructs, or determination methods, rule out differences due to resolution, model bias, lattice, or missing density.
- If only geometric proximity or a hydrogen-bond diagram is shown, write “consistent with an interaction hypothesis”; for a mechanistic conclusion, examine chemistry, density, and other evidence.

## Do not infer conformational selection / induced fit from two endpoints

- Two static endpoints cannot determine whether the ligand binds first or the protein changes conformation first, nor can they establish pathway flux or state populations.
- “The apo structure differs from the holo structure” shows only that the observed structural states differ; it does not by itself prove ligand-induced conformational change.
- A claim that “a minor conformation exists before ligand binding” requires evidence for populations in the unbound state; its proportion cannot be inferred from the bound-state coordinates.
- Hammes et al. analyze the two as kinetic pathways and argue that their mechanistic weights should be determined by reaction flux, not by considering one rate constant in isolation.
- The two pathways may operate in parallel, or their relative dominance may change with ligand or protein concentration; do not force the mechanism into a binary label.
- If the paper lacks the relevant kinetic/population evidence, downgrade the conclusion to “the observed states are consistent with a mechanism” and state that the pathway has not been determined.
- Do not infer real temporal order from the ordering of static structures, figure sequence, or labels such as “open/closed.”

## Allostery and causality

- Simultaneous changes at a distal site and active site do not establish information transfer or functional causality; check for ligand-state and functional readouts as well.
- Domain motion may suggest candidate coupling, but assess alternative explanations such as overall flexibility, different ligand states, assembly state, construct, or crystal environment.
- Separate causality between “conformational change” and “activity change”; check whether the paper provides perturbation/rescue experiments or other evidence that can support causality.
- MWC is a classical model proposed for allosteric transitions, not a universal explanation for any two structures.
- The original MWC model starts from assumptions of a symmetric oligomer, equivalent protomers, and a T/R conformational equilibrium, and proposes a concerted transition. First check whether the system meets these premises and whether the model has been tested against functional/thermodynamic data. The footnote to Table 1 in Monod et al. also says the case summary is incomplete, some systems were inadequately described at the time, and the signs for positive/negative effects include the authors’ interpretation.
- Do not claim that a protein undergoes a concerted transition between two discrete states merely because two conformations were observed; check the model assumptions and their applicability to the system.
- For dynamic or multi-conformation systems, a single model cannot represent the full ensemble; observing multiple conformations experimentally also does not by itself establish population equilibria or exchange rates.

## Catalysis and chemical steps

- A structure can show candidate substrate poses, catalytic residues, and potential interactions; these observations alone do not prove transition-state stabilization or a chemical step.
- Check whether local density supports active-site residues, whether chemical state/protonation is ambiguous, and whether the ligand is a substrate, product, analog, or inhibitor.
- If a claim concerns reaction direction, rate-limiting steps, or catalytic causality, confirm that the paper provides functional/kinetic evidence that tests the proposed mechanism.
- Distinguish “may participate” or “consistent with a catalytic geometry” from “demonstrates the catalytic mechanism”; use the former when evidence is insufficient.

## State, temperature, and populations

- Models from X-ray/EM may represent a specific state or a constrained representation of multiple states; a single coordinate set is not automatically the unique physiological conformation.
- Room-temperature and cryogenic crystals may show different conformational populations; temperature differences alone do not prove physiological functional change or mechanistic direction.
- Density-supported alternate conformations can support heterogeneity; without population or time-resolved measurements, do not use model occupancies to claim a solution equilibrium or kinetics.
- If a predicted model is included in a mechanistic figure, apply the predicted-model audit; a predicted state cannot serve as an observed intermediate.

## Handling inconsistent evidence

- First distinguish structural facts directly supported by data, interpretations derived from models, and causal conclusions tested experimentally.
- When sources conflict, first compare sample, construct, conditions, data quality, and analysis method; then judge which is more applicable to the current claim.
- If reported information cannot resolve the conflict, retain both interpretations and state what discriminating evidence is missing; do not substitute citation count for applicability.

## Specified references and locations

- Hammes, Chang & Oas (2009), [DOI: 10.1073/pnas.0907195106](https://doi.org/10.1073/pnas.0907195106): PDF pp. 1–4 for the introduction, reaction networks, and Results (Figs. 1–3), plus p. 5 for flux-calculation methods. The DHFR and flavodoxin–FMN cases calculate pathway flux from the given kinetic constants; the pathways can operate in parallel, and flux ratios change with ligand/protein concentration. This paper supports flux analysis methods and specific kinetic cases, not proof of pathways from static structures.
- Monod, Wyman & Changeux (1965), [DOI: 10.1016/S0022-2836(65)80285-6](https://doi.org/10.1016/S0022-2836(65)80285-6): PDF pp. 2–8 (printed pp. 89–95) for model derivation; pp. 9–11 (printed pp. 96–98) for Table 1 and its footnotes; pp. 18–25 (printed pp. 105–112) and pp. 26–30 (printed pp. 113–117) for assumptions, alternative transition pathways, and discussion. The original paper proposes a model with symmetry and equivalent-subunit assumptions; the authors acknowledge that the listed data are incomplete and that kinetic/thermodynamic experiments were still needed to distinguish which symmetric transition mechanisms apply to real systems. Use it as a theoretical framework, not an empirical conclusion for arbitrary proteins.
- Fraser et al. (2011), [DOI: 10.1073/pnas.1111325108](https://doi.org/10.1073/pnas.1111325108): PDF pp. 1–5, especially Figs. 1, 3–5 and Discussion; supports differences in conformational distributions visible in room-temperature/cryogenic crystals, but does not determine solution populations, functional direction, or state order.
- Henzler-Wildman & Kern (2007), [DOI: 10.1038/nature06522](https://doi.org/10.1038/nature06522): PDF pp. 1–8, especially p. 7 on how X-ray snapshots cannot provide state probabilities or interconversion rates; this is a dynamics review, so trace claims about specific systems to the cited primary experiments.
- Motlagh et al. (2014), [DOI: 10.1038/nature13001](https://doi.org/10.1038/nature13001): PDF pp. 1–7, especially p. 1 on limitations of the phenomenological MWC/KNF models and pp. 3–7 on the ensemble framework; this is an allostery review, not direct experimental validation for any particular system.

Without evidence that distinguishes competing mechanisms, a structure can suggest a testable hypothesis but cannot establish a causal pathway on its own.
