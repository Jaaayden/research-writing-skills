# 原子模型：几何、局部拟合与序列审计

模型审计分别检查实验数据、坐标模型及模型与数据的拟合。全局评分可能掩盖少见或局部异常，不能替代被论证残基或原子的局部证据；单项异常是调查线索，单项好分数也不是正确性的证明。([afonine2018](https://doi.org/10.1107/S2059798318009324)，§2.1；[read2011](https://doi.org/10.1016/j.str.2011.08.006)，pp. 1396–1397、1407–1410，Fig. 6C、Table 4)

## 几何与构象

- 查看目标区域的键长、键角、平面性、手性、Ramachandran、rotamer、clash 与局部主链构象；按分辨率、模型类型、精修约束和报告所用参考集解释异常。键长/键角残差会受 refinement restraints 影响；常见几何接近理想值本身不是独立验证，Ramachandran 与 rotamer 等通常较少直接受约束。少数异常可能是真实构象，需回到实验数据判断。([read2011](https://doi.org/10.1016/j.str.2011.08.006)，pp. 1397–1401、Fig. 1–3；[afonine2018](https://doi.org/10.1107/S2059798318009324)，§3.1、Fig. 2；[em-challenge2021](https://doi.org/10.1038/s41592-020-01051-w)，§“Overall and local quality of models”、Extended Data Figs. 1–3)
- 同时核对局部密度/模型拟合与构象证据。若几何与密度冲突，报告冲突和具体位置，不用一个全局几何分数裁定；RSR、RSCC 等局部拟合分数也受计算区域、分辨率和所选密度图影响。([read2011](https://doi.org/10.1016/j.str.2011.08.006)，pp. 1404–1405；[afonine2018](https://doi.org/10.1107/S2059798318009324)，§2.1、§3.1、§3.3)
- 检查肽键方向和 ω；约 5% 的脯氨酸肽键为 cis，而非脯氨酸 cis 约占 0.03%；偏离平面的强扭曲肽键更罕见，通常应优先复查。罕见不等于错误，结合局部密度、氢键或同源结构判断是否为真实构象。([molprobity2018](https://doi.org/10.1002/pro.3330)，§“Cis or twisted non-trans peptides”、pp. 305–306、Figs. 9、11B；[em-challenge2021](https://doi.org/10.1038/s41592-020-01051-w)，Results: “Overall and local quality of models”、Extended Data Fig. 1)

## 局部 map/model fit

- 对结论涉及的残基逐点查看密度和局部拟合指标；记录 map、mask、sharpening/contour 条件及所用局部指标。全图相关系数或整体分辨率不能替代单残基拟合。cryo-EM 局部评分优先使用逐残基结果，不以滑动窗口平均掩盖短区域错位。([read2011](https://doi.org/10.1016/j.str.2011.08.006)，pp. 1404–1405；[afonine2018](https://doi.org/10.1107/S2059798318009324)，§§2.1.1、3.3、3.5、Figs. 6–8；[em-challenge2021](https://doi.org/10.1038/s41592-020-01051-w)，Recommendation 2、§“Evaluating metrics: local scoring”)
- 结合几何和拟合两类互补证据。若某指标正是 refinement 优化目标，不把它单独计作独立验证；可用其他局部指标或可用的独立数据/半图交叉检查。占位率、B factor、mask 与 map sharpening 会影响部分拟合分数；Afonine 等也展示过模型几何改善时，CCmask 可能不变或略降，说明拟合数值与几何需联合解释。([read2011](https://doi.org/10.1016/j.str.2011.08.006)，p. 1404；[afonine2018](https://doi.org/10.1107/S2059798318009324)，§§3.3–3.5、3.9、Figs. 6–8、Table 4；[em-challenge2021](https://doi.org/10.1038/s41592-020-01051-w)，Results: “Evaluating metrics: Fit-to-Map”)

## 序列、register 与坐标身份

- 核对 construct/目标序列、沉积 polymer sequence、链断点、残基编号和 map 中的局部侧链/主链支持。记录 accession、`_pdbx_audit_revision_history.revision_date` 或所用文件快照、map/反射数据 accession、`_atom_site.auth_asym_id`/`_atom_site.label_asym_id`、`auth_seq_id`/`label_seq_id`、`pdbx_PDB_ins_code`、`auth_atom_id`/`label_atom_id` 和 `label_alt_id`；需要时说明论文编号到文件编号的映射。([read2011](https://doi.org/10.1016/j.str.2011.08.006)，Fig. 6C、Table 4；[checkmysequence2022](https://doi.org/10.1107/S2059798322005009)，Fig. 1)
- 分清两种 register 筛查的证据来源。checkMySequence 是 map-dependent 方法，需要 cryo-EM map、坐标模型和模型各链序列；它用 map 与主链坐标推断残基类型，再报告序列指派的 p-value。此 p-value 是“随机出现该结果”的估计，不是模型 register 错误的后验概率。作者采用的 99.5% 单侧界限明确属于经验阈值，且作者指出低局部分辨率需加长测试片段（默认 20、最多 60 个残基），因此局部短错位通常不足约 10 个残基时可能漏检。([checkmysequence2022](https://doi.org/10.1107/S2059798322005009)，§2、pp. 807–808；§4.1–4.2、pp. 809–810；§5、p. 815)
- conkit-validate 则是 map-independent 的筛查：将模型中的残基接触与 AlphaFold2 预测的距离/接触图比较。该文分析的是截至 2022-04-05 已沉积、名义分辨率 3–5 Å 的 PDB cryo-EM/MX 结构；作者称结果为 putative register errors。AlphaFold2 预测质量、构象差异和 fold-switching 都可能造成误报。文中人 calcineurin（PDB 5c1v）链 B 的替代折叠受到密度支持，但被标记为潜在错误，自动替换后密度拟合反而较差，是明确假阳性示例。([register-errors2024](https://doi.org/10.1107/S2052252524009114)，§2.1–2.3、pp. 939–941；§3.5.1、p. 945；§3.6.3、pp. 946–948)
- 比较 register 修正前后的模型时，注明坐标替换、局部实空间拟合和重精修使用的实验 map/数据及指标。该文分别重精修原模型与替代模型，再比较同一实验数据下的局部 CC/RSCC；拟合改善可作为支持证据，但因拟合与评估依赖同一实验数据，不能称为独立验证。([register-errors2024](https://doi.org/10.1107/S2052252524009114)，§2.5、p. 941；§3.4、p. 945、Fig. 5)

## 报告边界

逐项注明观察到的证据、证据来源和缺失项；缺图、缺 map 或无法取得验证报告时写“无法核验”。不要将结构模型的静态拟合或接触直接外推为动态、因果或机制已被证明。
