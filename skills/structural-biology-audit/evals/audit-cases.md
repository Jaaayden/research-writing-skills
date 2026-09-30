# Independent behavioral evaluation cases

The following 13 sets are synthetic materials that test audit behavior only; they do not represent the correctness of real structures. During evaluation, read SKILL.md first, then load reference files as needed for each claim. Do not present data that was not provided as if it had been recalculated.

## Cryo-EM and chemical contacts

Use structural-biology-audit to audit the following six independent structural conclusions. The materials below are the complete available materials for synthetic cases used to validate skill behavior; they do not correspond to real deposited structures. Judge each case only from the supplied materials. You may consult the skill references to explain methods, but do not claim to have inspected maps that were not provided or repeated calculations. For each case, provide a verdict, evidence location, limitations, and missing or discriminating evidence.

### E1

Original statement: The structure was determined at 2.8 Å resolution.

Material E1-M1: During late-stage refinement, the two particle half-sets shared a high-resolution reference that had not been low-pass filtered. The authors called this gold-standard. The reported FSC used the 0.143 criterion; the resolution was 2.8 Å after a tight binary mask and 3.8 Å unmasked. No phase-randomization or noise-substitution correction was reported. No half-map files were provided; only the curve and the method text above were available.

### E2

Original statement: The ligand is clearly resolved.

Material E2-F1: The global FSC at 0.143 was 2.8 Å; the local resolution at the site was approximately 5.0 Å. The paper says that only a blob was visible when the whole-map display level was set to 0.7, and that a connected shape appeared only after lowering the ligand display level to 0.3. One aromatic ring and two key substituents lacked separate density support. An ideal ligand dictionary was used for the coordinates, and occupancy was fixed at 1.0. No local fit or comparison with other poses was reported; no raw map was available for calculation.

### E3

Original statement: Asp54 forms a hydrogen bond with the carbonyl oxygen of ligand L.

Material E3-C1: The two atoms are carboxylate Oδ2 and a neutral amide carbonyl O. The pH was 7.4, and the authors explicitly modeled Asp54 as a deprotonated carboxylate. The O···O distance is 3.0 Å, there is no intervening water, and PyMOL displayed a yellow line. No proton positions, donor–acceptor direction, or other chemical evidence were provided.

### E4

Original statement: Mg2+ is definitively identified at site M.

Material E4-M1: The coordinates label the ion MG; the mean distance to its six coordinating oxygen neighbors is 2.38 Å. The buffer contained 200 mM NaCl and 2 mM MgCl2. Refinement used specified MG restraints and fixed occupancy at 1.0. There was only one spherical electron-density peak and a global Rfree value, with no anomalous scattering, refinement of alternative ions, or comparison of site B factors. Na, water, and other interpretations have not been ruled out.

### E5

Original statement: The reported gold-standard half-map FSC resolution is 3.1 Å at the 0.143 criterion.

Material E5-M1: The processing log states that particles were divided into independent half-sets from the initial 3D refinement, with low-pass-filtered initialization. The noise-substitution-corrected masked curve crossed 0.143 at 3.1 Å; the unmasked curve crossed at 3.2 Å. The methods, soft-mask parameters, and curve types were all reported. The statement reports only this convention; it does not claim that all sites are at 3.1 Å, that the model is entirely correct, or that a mechanism is established. The case does not provide the actual half-map files, so the curve cannot be independently recalculated.

### E6

Original statement: The Lys87–ligand contact is consistent with a hydrogen bond.

Material E6-G1: For X-ray data with a reported diffraction limit of 1.2 Å, the heavy-atom coordinates for Lys Nζ and the neutral amide carbonyl O have continuous local density support, the rotamer has no clash, and no better alternative conformation was found. The pH of 7.0 and the chemical environment support Lys as a donor and the carbonyl as an acceptor. D···A is 3.0 Å; after adding an ideal H, H···A is 2.0 Å and D–H···A is 170 degrees. The H coordinate was added by software and was not directly resolved. The original statement says only “consistent with” and does not claim that the proton was experimentally observed.

## Cross-method, conflicting, and positive cases

Use structural-biology-audit to verify the following seven independent conclusions. The case data are synthetic textual materials and do not correspond to real structures; method sources are real papers included in the skill. Do not edit any files, add records, or generate an article. For each item, provide a verdict, evidence location, limitations, and missing or discriminating evidence; resolve literature disagreements conditionally.

### C1

Original statement: The complete structures are identical (RMSD=0.4 Å).

Material C1-A1: Each protein has 320 residues. RMSD was calculated only for the 84 Cα atoms in the conserved core; a 20-residue key active-site loop was not aligned, and the two domains are rotated by 18 degrees relative to each other. No density support or local analysis was provided for the excluded region.

### C2

Original statement: The AlphaFold region is experimentally more mobile because its B factor is 95.

Material C2-P1: The structure is from AlphaFold2; the PDB B-factor column contains pLDDT. There is no X-ray/EM experiment, dynamics measurement, or thermodynamic measurement. The region has pLDDT 95 and high inter-chain PAE. The authors compare 95 with 65 for another segment as evidence of motion.

### C3

Original statement: The apo and holo structures prove induced fit rather than conformational selection.

Material C3-S1: Two crystal models of the same construct show an open apo state and a closed holo state; the models are supported by density, but the crystal forms differ. There are no measurements of binding kinetics, the population of minor apo states, or pathway flux. The discussion cites Hammes, Chang & Oas 2009.

### C4

Original statement: This protein is a physiological dimer because PISA places the dimer first.

Material C4-B1: PISA was run on crystal coordinates containing the complete native sequence, and the dimer ranked first. Independent SEC-MALS under the same buffer, ligand, and temperature, and over a concentration range sufficient to cover concentrations relevant to the structural experiment, supports a monomer. The paper does not explain the conflict. This is the only solution measurement; there are no intracellular stoichiometry data.

### C5

Original statement: A register error is proven because an AlphaFold-based checker flagged residues120–140.

Material C5-V1: The current coordinates have no obvious geometry anomalies in this region. The tool proposes a +2 alternative register; the AF2 prediction and current model use the same sequence. The map is inaccessible, the alternative register was not compared for map fit, and no high-resolution reference was obtained. The authors cite register-errors2024 and state that every putative error in the paper has been experimentally confirmed.

### C6

Original statement A: Resolution must be reported only at the fixed 0.143 criterion from Rosenthal–Henderson 2003; van Heel–Schatz 2005 has been proven wrong.

Original statement B: The 2024 Addendum to AF3 changes the original paper's accuracy, so all accuracy claims in the original paper are invalid; the original Cruickshank 1999 formula can be reused without an erratum.

Material C6-R1: The two discussions of FSC methods, the AF3 paper and addendum, and Cruickshank/erratum are all real DOIs selected in the skill and can be checked in their original publications or indexes. Evaluate each of these conclusions about conflicting or updated sources separately; do not decide by voting on citation counts.

### C7

Original statement: The aligned catalytic core has a closely matching backbone conformation in these two coordinate models.

Material C7-A1: The same protein and sequence and the same core boundaries are used; consistent chain/residue mapping and 84 modeled Cα atoms are provided, with no missing residues or insertions. After superposing those 84 atoms, the RMSD is 0.4 Å, and the largest per-residue deviation in the core is 0.8 Å. The statement is limited to a comparison of the core backbone in the coordinate models and does not concern unaligned regions, function, or experimental correctness of the models.
