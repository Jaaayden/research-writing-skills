# 结构结论的用词证据门槛

用于把结构观察、模型指认和生物化学解释分开表述。先写证据实际支持的层级，再决定用词；不把自动标线、单一指标或受 restraint 的坐标写成直接观测。

| 观察/证据 | 建议写法 | 暂不支持的强写法 |
|---|---|---|
| 局部图有峰，但形状、化学或替代物未排除 | “该位点有密度，模型暂指认为 X”；“密度与 X 相容，但身份仍不确定” | “X 已被明确解析/确定结合” |
| 配体多个关键基团有连续局部密度，地图与 contour/处理透明，几何化学合理；存在现实歧义时已比较替代姿势/部分占有 | “局部密度支持该配体姿势”；只有证据相互吻合时才写“配体清楚解析” | 仅凭全局分辨率、颜色表面或 RSCC/Q-score 一个数字写“清楚解析” |
| 只有近接，或供受体身份/关键质子化歧义尚未排除 | “存在与氢键相容的几何”；“可能形成氢键” | 将有歧义的相互作用断言为确定氢键 |
| 只有两个重原子距离或 PyMOL/可视化软件画出虚线 | “存在近距离接触” | “形成氢键” |
| 金属峰经多项化学/几何/密度及实验信息支持 | “Mg²⁺由……配位”；报告配位数、几何与关键距离 | 仅按最近原子距离写“Mg²⁺由……配位” |
| 金属峰仍可能为 Na⁺/水/其他离子 | “该密度峰被模型指认为 Mg²⁺；身份未排除替代解释” | “Mg²⁺存在/结合于此” |

## “氢键”何时可以作为结论

- **原文结论：** IUPAC 将氢键定义为有证据显示键形成的吸引相互作用，并列出多类实验/理论证据；方向性和较短的 H···受体距离是常见特征，而非适用于所有体系的单一硬阈值。【[iupac2011] DOI 10.1351/PAC-REC-10-01-02，“Definition”及氢键存在判据】
- **原文结论：** IUPAC 定义中的供体是 X—H（X 比 H 更具电负性），受体可以是原子或原子团。【[iupac2011] DOI 10.1351/PAC-REC-10-01-02，“Definition”】**审计判断：** 若 His、Asp/Glu、配体可电离基团或水的质子化状态会改变 donor/acceptor 身份，核对化学状态并说明未排除的歧义。
- **审计判断：** 检查 donor/acceptor 化学、IUPAC 所述方向性、局部环境、供体侧链 rotamer、密度和竞争构象。MolProbity 会添加/优化 H 原子以进行全原子接触分析；因此若模型中的 H 坐标由软件生成，应将 D—H···A 方向视为模型几何证据，不写成直接观察到质子或氢键。【[iupac2011] DOI 10.1351/PAC-REC-10-01-02，“Definition”及氢键存在判据；[molprobity2018] DOI 10.1002/pro.3330，“Hydrogen addition and NQH flips”】
- **审计记录：** 报告具体供受体原子、D···A 与可获得的 H···A 距离、D—H···A 角度，并标明 H 是实验定位还是软件添加；没有 H 时不能伪造角度。结合坐标不确定性解释，不能用一条黄线或普适距离/角度截点裁决。并不要求每条结构氢键都直接解析 H；化学与局部几何足以支持推断时可给“支持”，但标明这是模型与化学证据支持的解释。
- **审计判断：** Asn/Gln/His 末端翻转会改变供体/受体身份与接触网络；比较翻转前后密度、全原子 clashes 和氢键网络。MolProbity 指出这些末端在电子密度中近似对称，并以 clash/缺失氢键模式辅助识别翻转候选；不要只凭密度外形裁决。【[molprobity2018] DOI 10.1002/pro.3330，Introduction、“Better-idealized output coordinates from NQH flips”】

## “已解析”“结合”“配位”的范围

- **“resolved/已解析”** 指局部地图支持可辨识的形状/细节，不等于分子身份、化学状态或功能机制已被证明。写配体结论时附局部 map、contour、局部分辨率/原子可解析性及图处理信息；多指标和局部证据优先于全图均分。【[ligand-challenge2024] DOI 10.1038/s41592-024-02321-7，Discussion Recommendations 1–3、Fig. 2；[pintilie2020] DOI 10.1038/s41592-020-0731-1，Figs. 2–3、Discussion】
- **“RSCC 支持”** 必须交代数据类型、map、软件与计算定义。wwPDB X-ray VTF 讨论 ligand RSR/RSCC 作为局部 fit 指标，但指出整分子分数可能掩盖大型配体的局部问题。当前 Phenix `validate_ligands` 文档（2026-09-30 查阅）说明的是 X-ray RSCC 流程，并建议把配体分数与其周围 `sites` 分数比较；页面没有建立 cryo-EM RSCC 的具体计算流程。不要套用一个跨分辨率/数据集的通过阈值，也不要把 X-ray RSCC 定义外推为 cryo-EM 通用指标。【[read2011] DOI 10.1016/j.str.2011.08.006，“Ligands”；[Phenix 官方文档](https://www.phenix-online.org/documentation/reference/validate_ligands.html)，“Metrics”“Possible Problems”，访问于 2026-09-30】
- **“Mg²⁺由……配位”** 比“该峰被指认为 Mg²⁺”强：前者同时断言身份和配位几何。若 map、配位壳、化学环境或样品条件不足，先报告为模型指认并列出 Na⁺/水/缓冲离子等替代解释。经典 Mg 几何/距离只能作典型预期，且需核对 refinement restraints。【[cmm2017] DOI 10.1107/S2059798317001061，§§3.1.1–3.1.2、Fig. 2、Tables 1–2；[leonarski2017] DOI 10.1093/nar/gkw1175，Abstract、§“PDB survey”】
- **“结合/稳定/催化”** 属于更强的生物化学解释。结构可以支持位置和几何，不自动证明亲和力、稳定作用或催化机制；如文章要提出此类机制，需把结构证据与独立实验/功能证据分开。

## 来源

- `[iupac2011]` Arunan et al. “Definition of the hydrogen bond (IUPAC Recommendations 2011).” *Pure Appl Chem* 83, 1637–1641. DOI: 10.1351/PAC-REC-10-01-02.
- `[molprobity2018]` Williams et al. “MolProbity: More and better reference data for improved all-atom structure validation.” *Protein Sci* 27, 293–315 (2018). DOI: 10.1002/pro.3330.
- `[read2011]` Read et al. “A new generation of crystallographic validation tools for the Protein Data Bank.” *Structure* 19, 1395–1412 (2011). DOI: 10.1016/j.str.2011.08.006.
- Phenix 官方文档，[“Validating ligands with phenix.validate_ligands”](https://www.phenix-online.org/documentation/reference/validate_ligands.html)，访问于 2026-09-30；该引用仅支持文档所述 X-ray 工具行为。
- 其他来源见 [ligand-density.md](ligand-density.md)。
