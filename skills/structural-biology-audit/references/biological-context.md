# Biological Context and Experimental Conditions Audit

Invoke as needed when claims generalize crystal contacts, sedimentation/assembly, a specific conformation, or a binding state to the native protein.
The purpose of this check is to determine whether the molecule, environment, and assembly state represented by the structure match the biological claim.

## Construct and sample

- Compare the native sequence, experimental construct, and coordinate sequence; state species, isoform, chain identity, and residue-number mapping.
- Check construct boundaries, deleted domains/loops, mutations, tags, fusion proteins, stabilizing modifications, and crosslinks.
- If the study used a truncation, mutant, or fusion construct, check whether the deleted portion contributes to the interface, conformational constraints, or functional regulation.
- Verify that every component in the complex was actually present in the sample; distinguish co-expression, co-purification, added ligand, and components introduced during model building.
- Check that the entity definitions for chains in the structure match the names used in the paper; do not mistake a tag or fusion chain for a native partner.
- If the sample was prepared from multiple components together, confirm that purification records or the experimental description support the reported components and stoichiometry.
- List residues, chain segments, ligands, or partners absent from the coordinates as unknown; do not automatically interpret their absence as physical absence or disorder.
- Missing electron density, low local resolution, and absence from the sample are different explanations and should be stated separately.
- If construct or sample information is not reported, mark it “not verifiable”; do not fill in metadata from a structure figure.

## Environment and state

- Record reported pH, salt/ions, ligands/cofactors, concentration, temperature, precipitant, cryoprotectant, detergent, and crosslinking conditions.
- Distinguish biochemical assay conditions, purification/buffer conditions, crystallization conditions, and data-collection temperature; do not conflate them as “physiological conditions.”
- If a key condition is unreported, do not treat the omission as evidence of a conventional condition; state that it is unknown.
- For components such as metals, sulfate, phosphate, or glycerol, check whether they are physiological components, buffer/precipitant constituents, or of unknown origin.
- For glycosylation, lipids, cofactors, and covalent modifications, check whether the sample expression system and experiments support the chemical state shown in the coordinates.
- A ligand or ion in the structure may alter an interface or conformation; verify its chemical identity and sample provenance before using it for functional interpretation.
- If the experiment used high concentrations or added stabilizers, state how these may limit the range of assemblies or conformations to which the result can be generalized.
- Cryogenic cooling, lattice packing, and different crystal forms can affect the observed conformation; do not treat a single coordinate model as the only solution-state conformation.
- Changes in temperature or conditions may change conformational populations; without independent measurement, do not treat coordinate occupancies as population fractions in solution.

## Biological assembly and crystal contacts

- Record separately the asymmetric unit, author-assigned biological assembly, crystallographic symmetry-related chains, and assemblies inferred by analysis software.
- Check whether symmetry operations for the biological assembly generate chains outside the asymmetric unit, and confirm that figures and coordinates use the same assembly definition.
- A displayed multimer does not establish that the multimer exists in the sample or in solution; first check chain count, symmetry operations, and the origin of the interface.
- Check whether the claimed interface is formed mainly by crystallographic symmetry mates or is present in the author-assigned biological assembly.
- Treat PISA results as assembly predictions based on the physicochemistry of crystal interfaces, not as solution experiments.
- Do not decide stoichiometry from a PISA ranking or a single interface-energy value; scores are affected by modeling assumptions and the crystal environment.
- Krissinel (2011) computational estimates suggest that weak interactions with a dissociation constant Kd ≥ 100 μM have a substantial chance of disappearing during crystallization; the author estimated that about 20% of PDB protein dimers have a greater than 50% risk of being misannotated. This is an overall model estimate, not a posterior probability for any particular structure.
- Check whether PISA includes crystallization precipitants or non-native ligands in the interface; use the paper to judge whether they represent components present in the sample.
- Check the ligand set, chain set, and coordinate version used for PISA analysis; note when different settings yield different candidate assemblies.
- Look for independent solution or biochemical assembly evidence actually reported in the paper, and confirm that its concentration, salt, pH, temperature, and ligand conditions are compatible with the claim.
- Compare the concentration, ligand, and buffer conditions for independent assembly measurements in one place; mismatched conditions limit how conflicts can be resolved.
- If independent evidence conflicts with the crystal or predicted assembly, report the conflict and condition differences; do not silently choose the side that better fits the authors’ model.
- The 80–90% reported by PISA (2007) is the authors’ success rate on their evaluation set and cannot be converted into a confidence probability for an individual structure.
- Do not conclude a weak, transient, or condition-dependent complex from crystallographic evidence alone; label it a candidate interface/assembly.

## Temperature and conformational populations

- If the paper compares room-temperature and cryogenic structures, check whether they come from the same system and whether the corresponding density and model building support the comparison.
- Check for alternate conformations or state-dependent local density at functional sites, near crystal contacts, and in mobile loops.
- Low-temperature crystals may rearrange side chains/packing and reduce visible alternate conformations; this is a possible bias to examine, not evidence that every cryogenic structure is distorted.
- Multiple conformations in room-temperature crystal density provide evidence of conformational heterogeneity; a single representative model does not by itself give conformational populations or kinetic rates.
- Separate “different states were observed” from “the state order/function causality was established”; the latter requires independent evidence. See the mechanism audit.

## Specified references and locations

- Krissinel & Henrick (2007), [DOI: 10.1016/j.jmb.2007.05.022](https://doi.org/10.1016/j.jmb.2007.05.022): abstract and PDF pp. 2–11, 19–20 (printed pp. 775–784, 792–793). The paper enumerates candidate assemblies from crystal contacts and filters them using interface physicochemistry, thermodynamics, and graph search; 80–90% is the overall recovery rate on the authors’ benchmark, not a per-structure confidence. The conclusion explicitly says the study deliberately did not include temperature, salinity, pH, or subunit concentration.
- Krissinel (2011), [DOI: 10.1107/S0907444911007232](https://doi.org/10.1107/S0907444911007232): abstract, PDF pp. 2–8 (especially Figs. 1, 3–4 and the case studies), and p. 9 conclusion. 3bxc is a counterexample of a tight tetramer in the crystal that is monomeric in solution; the YopM 1G9U/1JL5 case shows that calcium conditions can change the crystal prediction, while SEC and crosslinking experiments support calcium-dependent solution assembly. The paper also states that PISA dissociation free energy is not a single score for which “higher is always better”; weak binding and condition-dependent systems require independent experimental confirmation.
- Fraser et al. (2011), [DOI: 10.1073/pnas.1111325108](https://doi.org/10.1073/pnas.1111325108): results on PDF pp. 1–5, Figs. 1–5, and Discussion. The study compares 30 room-temperature/cryogenic high-resolution crystallographic data sets and uses Ringer/qFit to examine density-supported alternate conformations, showing that cooling can change the observed distribution of side-chain conformations. It supports temperature effects on populations visible within crystals; model occupancy cannot be directly converted to solution-state fractions or kinetics.

If construct, sample environment, or independent assembly evidence is missing, retain that limitation in the final conclusion.
