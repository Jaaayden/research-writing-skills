# 配体、局部密度与金属位点

用于审计“配体已解析 / clearly resolved”“某姿势得到密度支持”“形成特定相互作用”及 Mg²⁺指认。把论文直接报告的结果与本指南的审计判断分开；不要把一个指标或一条可视化线当作结论。

## 先确认地图类型，再看局部证据

| 方法 | 可检查的证据 | 解释边界 |
|---|---|---|
| X-ray | 由反射数据计算的电子密度、差值图和 ligand RSCC/RSR；可计算常规 OMIT 或 polder map。 | RSCC/RSR 是具体计算流程产生的局部 fit 指标，不是脱离数据、地图和软件定义的化学证据。polder 是针对 X-ray bulk-solvent mask 的 OMIT 方法。【[read2011] DOI 10.1016/j.str.2011.08.006，“Ligands”；[polder2017] DOI 10.1107/S2059798316018210，§§1–2】 |
| Cryo-EM | 实验 cryo-EM map、配体及其口袋的局部 fit、局部分辨率、原子可解析性分数；检查实际显示 contour 与处理信息。 | 全图 FSC 分辨率不能代替配体处的局部分辨率或原子可解析性。Q-score 以已拟合模型的原子周围 map profile 计算，不验证配体化学或立体化学。【[pintilie2020] DOI 10.1038/s41592-020-0731-1，Introduction、§“Q-score”、Discussion；[ligand-challenge2024] DOI 10.1038/s41592-024-02321-7，Discussion、Recommendations】 |

**原文结论：** Ligand Challenge 展示的三张 cryo-EM map 使用不同的 contour level；局部配体 map 还会受到局部分辨率、占有率、多构象、柔性/无序、化学修饰及辐射损伤影响。【[ligand-challenge2024] DOI 10.1038/s41592-024-02321-7，Fig. 2 caption、Discussion】

**审计判断：** 记录 map 来源、处理/锐化版本、配体局部分辨率和展示 contour（σ 或 map value）。在相同设置下看配体和邻近口袋；检查密度是否连续、能否区分关键原子/环/取代基。不要把单独调低 contour 后才出现的外形当作 clearly resolved 的证明；如并列展示不同 contour，应标注各自数值并说明展示目的。也不要设跨数据集通用的通过阈值。可并看未经锐化与处理后的 map。Pintilie 等在正文报告 sharpening 可提高可见细节与 Q-score，但过度 sharpening 后 Q-score 会下降；正文将此结果指向 Supplementary Fig. 5，本次未独立核查该补图。【[pintilie2020] DOI 10.1038/s41592-020-0731-1，“Q-scores of atoms in proteins”，PDF p. 3（正文描述；Supplementary Fig. 5 未独立核查）；[ligand-challenge2024] DOI 10.1038/s41592-024-02321-7，Fig. 2 caption】

## 密度、模型化学与替代解释都要过关

- **逐片段看局部 fit。** 对照配体、周围蛋白/核酸、离子和水的局部支持；不要只报全模型或整分子平均值。Ligand Challenge 发现局部 ligand/ligand-environment fit-to-map 与 coordinates-only 指标可彼此独立。当前 Phenix `validate_ligands` 文档（2026-09-30 查阅）描述的是 X-ray 验证：分别报告整体与刚性片段 RSCC，并提供配体周围 3 Å 的 `sites` RSCC 作为环境参照。因此整体分数尚可仍可能掩盖局部弱密度。【[ligand-challenge2024] DOI 10.1038/s41592-024-02321-7，Discussion、Fig. 3、Extended Data Fig. 3B、Supplementary Data S3；[Phenix 官方文档](https://www.phenix-online.org/documentation/reference/validate_ligands.html)，“How it works”“Metrics”“Possible Problems”，访问于 2026-09-30】
- **核对化学与立体化学。** 核验配体身份/CCD、原子完整性、键连及共价连接；检查键长、键角、平面性、手性、环构象、应变、 clashes 和周围接触。几何合理不等于密度支持，fit 好也不等于几何正确。【[ligand-challenge2024] DOI 10.1038/s41592-024-02321-7，Discussion、Recommendations】
- **比较替代解释。** 检查密度是否可能来自水、缓冲液/结晶添加物、另一姿势或部分占有的多构象。弱密度还可能来自无序/柔性，而非错误配体身份。【[polder2017] DOI 10.1107/S2059798316018210，§3.1.2、§5、Fig. 5；[ligand-challenge2024] DOI 10.1038/s41592-024-02321-7，Results、Fig. 5、Extended Data Fig. 4A–B、Discussion】

## X-ray 与 cryo-EM 的 fit 指标不能直接互换

- **RSCC/RSR 要交代实现。** Read 等的 wwPDB X-ray VTF 建议报告配体几何异常和局部密度 fit；其中指出大型配体整体分数可能掩盖局部问题，并建议将 ligand RSR 与蛋白部分比较。该文未定义 cryo-EM RSCC 或为所有配体规定普适 RSCC 阈值。【[read2011] DOI 10.1016/j.str.2011.08.006，“Ligands”】
- **按软件说明解释具体 RSCC。** 当前 Phenix 文档说明，X-ray RSCC 在距配体非氢原子 1.5 Å 范围内的网格点上，比较删除配体后计算的 `2mFo−DFc` map 与含配体计算的 `DFmodel` map；另报告整配体、刚性片段，以及周围 3 Å 蛋白/DNA/RNA 原子的 `sites` 分数。该页的主要用法、方法、指标和问题说明均为 X-ray，页面注明工具面向以 X-ray 数据精修的模型；关键词表里出现 cryo-EM map 的 `resolution` 参数不足以定义 cryo-EM RSCC 算法。记录实际 map、软件及计算定义；不把此 X-ray 流程外推到 cryo-EM，也不跨数据类型或软件直接比较数值。【[Phenix 官方文档](https://www.phenix-online.org/documentation/reference/validate_ligands.html)，“Usage”“How it works”“Metrics”“Possible Problems”“List of all available keywords”，访问于 2026-09-30】
- **OMIT/polder 是晶体学证据。** 移除待检原子后计算 X-ray OMIT map，可降低模型对自身密度的影响；bulk-solvent mask 可能进入空出的 OMIT 区并遮蔽弱信号。Polder 在 OMIT 区排除 bulk solvent，可能增强弱配体信号。【[polder2017] DOI 10.1107/S2059798316018210，Abstract、§§1–3.1、Figs. 1–6】
- **OMIT/polder 不是独立证明。** Polder 在紧凑口袋中可能将溶剂或口袋形状显示成类似待检原子的密度；论文展示虚构配体也可产生正峰。并看常规 OMIT、polder、差值图、替代解释和局部化学，不以 polder 连续峰单独断定配体存在。【[polder2017] DOI 10.1107/S2059798316018210，§5、Table 2、Fig. 2】
- **Cryo-EM 看 map-local evidence。** Q-score 衡量原子周围 map profile 与参考 Gaussian 的相似度；它依赖模型拟合位置，并不检验立体化学。原文展示在所选 contour 下缺少包围某原子的表面时，Q-score 仍可能较高，因此要同时看实际 contour、局部 map、分辨率及模型化学。【[pintilie2020] DOI 10.1038/s41592-020-0731-1，§“Q-score”、Fig. 3、Discussion】
- **B-factor/ADP 和 occupancy 不是独立密度证明。** 检查精修策略，并把配体 ADP/B-factor 与邻近环境比较；当前 Phenix 文档在 X-ray 验证语境下报告配体与周围 3 Å 环境的 ADP 统计及配体 occupancy。Cryo-EM 模型的 ADP 即使列出，也常受 restraints 约束，不能只视为局部 map 强度。Ligand Challenge 建议结合局部密度的绝对强度和相对周围环境判断，并以 F86 的半强度密度举例支持约 50% occupancy；这是该结构中的个案，不是通用校准式。解释时同时考虑柔性、局部分辨率、多姿势及精修参数。【[pintilie2020] DOI 10.1038/s41592-020-0731-1，Introduction、Discussion；[ligand-challenge2024] DOI 10.1038/s41592-024-02321-7，Discussion、Extended Data Fig. 4B；[Phenix 官方文档](https://www.phenix-online.org/documentation/reference/validate_ligands.html)，“Metrics”，访问于 2026-09-30】

## Mg²⁺：检查配位壳，不凭距离认离子

- **联合判断身份与配位。** 核验 map、配位原子种类/电荷、配位数、几何、邻近水、occupancy/B-factor 及样品缓冲成分；比较 Na⁺、水和其他离子等替代解释。CheckMyMetal 报告 Mg²⁺常见近八面体六配位、Mg—O 距离约 2.08 Å，但也展示近似距离仍可能更符合 Na⁺的例子。典型几何不是身份判定阈值。【[cmm2017] DOI 10.1107/S2059798317001061，§2、§§3.1.1–3.1.2、Fig. 2、Table 1】
- **排查 restraint circularity。** CMM 2017 报告当时 refinement library 的 Mg—O 默认 restraint 为 2.18 Å，而 CSD 统计峰约 2.08 Å。若坐标被 restraint 拉到预期值，该距离不能再作为独立的离子身份证据；核对实际软件/字典版本，并独立看密度、配位化学和替代离子。不要假定论文所报默认值代表当前库。【[cmm2017] DOI 10.1107/S2059798317001061，§3.1.2、Table 2】
- **分清方法适用范围。** CMM 的配位壳/价态/完整性/几何指标与 occupancy、B-factor 指标不同；论文明确后两项为 X-ray 专用。若同步辐射波长可调至金属吸收边附近，异常散射可辅助元素指认；这是有条件的 X-ray 方法，不是 EM 通用检查。【[cmm2017] DOI 10.1107/S2059798317001061，§§1–2】
- **核酸调查不可外推。** Leonarski 等调查截至 2016 年 5 月、分辨率 ≤3 Å 的核酸 PDB 结构，范围聚焦 Mg²⁺与核碱基亚胺 N1/N3/N7 的直接内层接触；没有调查水介导的外层 Mg—N7 接触，也不覆盖全部核酸 Mg²⁺位点或配位模式。许多被报告的直接接触更可能是 Na⁺、K⁺、NH₄⁺、水或噪声峰；结论不可推广至蛋白 Mg 位点。【[leonarski2017] DOI 10.1093/nar/gkw1175，Abstract、Introduction、“PDB survey”、Discussion】

## 来源

- `[read2011]` Read et al. “A new generation of crystallographic validation tools for the Protein Data Bank.” *Structure* 19, 1395–1412 (2011). DOI: 10.1016/j.str.2011.08.006.
- `[polder2017]` Liebschner et al. “Polder maps: improving OMIT maps by excluding bulk solvent.” *Acta Cryst D* 73, 148–157 (2017). DOI: 10.1107/S2059798316018210.
- `[pintilie2020]` Pintilie et al. “Measurement of atom resolvability in cryo-EM maps with Q-scores.” *Nat Methods* 17, 328–334 (2020). DOI: 10.1038/s41592-020-0731-1.
- `[ligand-challenge2024]` Lawson et al. “Outcomes of the EMDataResource cryo-EM Ligand Modeling Challenge.” *Nat Methods* 21, 1340–1348 (2024). DOI: 10.1038/s41592-024-02321-7.
- `[cmm2017]` Zheng et al. “CheckMyMetal: a macromolecular metal-binding validation tool.” *Acta Cryst D* 73, 223–233 (2017). DOI: 10.1107/S2059798317001061.
- `[leonarski2017]` Leonarski, D’Ascenzo & Auffinger. “Mg²⁺ ions: do they bind to nucleobase nitrogens?” *Nucleic Acids Res* 45, 987–1004 (2017). DOI: 10.1093/nar/gkw1175.
- Phenix 官方文档，[“Validating ligands with phenix.validate_ligands”](https://www.phenix-online.org/documentation/reference/validate_ligands.html)，访问于 2026-09-30。仅作为该日期可访问的 X-ray 工具行为来源；不据此声称 cryo-EM RSCC 的具体流程或通用阈值。
