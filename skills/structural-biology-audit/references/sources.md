# 来源索引

共 **39 条记录：37 篇主文献＋2 条更新**。书目用 Crossref DOI 元数据核对，并匹配 Zotero 本地 PDF；引用量统一为 **OpenAlex，2026-09-30** 快照。完整作者、卷期页码、DOI、引用量 work 链接、更新关系、精确原文位置及局限见 [sources.json](sources.json)。

## 核验口径

- 39 份 PDF 均已核对身份与支撑当前规则的相关章节/图表；逐条记录实际审读页码、版本、SHA-256 与未覆盖内容。状态 `fulltext_sections_verified` 表示相关段落核验，`update_text_verified` 表示更新通知核验。
- 原文审读不是原数据复算，也不保证文中全部结果正确。作者接受稿、扫描文本缺页/单位误识别、外部补充材料及未复算的方法均按条目说明。全文和提取文本不存入技能仓库。
- 高引经典作概念锚，社区建议与专项纠错补充盲点；较低引用量的新文献按实际角色列出。引用数、期刊、年份均不单独裁决冲突。
- `openalex_is_retracted=false` 只表示该快照未标记撤稿，不是穷尽更新审查；遇到新争议应再核期刊/PubMed/Crossmark。

## 按需选择来源

| 主题 | 基础锚点 | 共识、专项验证、边界或更新 |
|---|---|---|
| Cryo-EM 分辨率与可靠性 | `rh2003`、`scheres-chen2012`、`kucukelbir2014`、`vanheel2005`、`relion2012` | `chen2013`、`tan2017`、`kleywegt2024`、`pintilie2020`、`ligand-challenge2024`、`afonine2018`、`em-challenge2021`、`checkmysequence2022` |
| X-ray 数据、精修与精度 | `brunger1992`、`evans2013`、`karplus2012`、`cruickshank1999`、`molprobity2018`、`read2011`、`pisa2007` | `cruickshank1999-erratum`、`polder2017`、`krissinel2011`、`fraser2011` |
| 配体密度、化学与金属 | `kucukelbir2014`、`af3-2024` | `polder2017`、`pintilie2020`、`ligand-challenge2024`、`cmm2017`、`leonarski2017`、`afonine2018` |
| 结构比较 | `carugo2001`、`tmalign2005` | 由相关基础方法交叉支撑 |
| 模型验证与序列错位 | `brunger1992`、`evans2013`、`karplus2012`、`cruickshank1999`、`iupac2011`、`molprobity2018`、`read2011`、`af2-2021`、`af3-2024` | `kleywegt2024`、`cruickshank1999-erratum`、`pintilie2020`、`ligand-challenge2024`、`cmm2017`、`leonarski2017`、`afonine2018`、`em-challenge2021`、`checkmysequence2022`、`register-errors2024`、`akdel2022`、`terwilliger2024` |
| 证据措辞与术语 | `iupac2011` | `cmm2017`、`leonarski2017` |
| 数据处理与模型偏差 | `rh2003`、`scheres-chen2012`、`vanheel2005`、`brunger1992`、`relion2012` | `chen2013`、`tan2017`、`polder2017` |
| 生物学组装与实验条件 | `pisa2007`、`henzler2007`、`motlagh2014` | `krissinel2011`、`fraser2011` |
| 预测模型 | `af2-2021`、`af3-2024` | `register-errors2024`、`af3-2024-addendum`、`akdel2022`、`terwilliger2024` |
| 结构到机制 | `monod1965`、`henzler2007`、`motlagh2014` | `fraser2011`、`hammes2009` |

## 39 条唯一书目

表内链接指向 DOI；精确核验位置按 source ID 在 JSON 中查找。OpenAlex 引用数只作传播度快照。

| Source ID | 作者、年份与题名 | OpenAlex | 证据角色 |
|---|---|---:|---|
| `rh2003` | Rosenthal & Henderson (2003) · [Optimal Determination of Particle Orientation, Absolute Hand, and Contrast Loss in Single-particle Electron Cryomicroscopy](https://doi.org/10.1016/j.jmb.2003.07.013) | [2,706](https://openalex.org/W2152562710) | 基础, 方法分歧 |
| `scheres-chen2012` | Scheres & Chen (2012) · [Prevention of overfitting in cryo-EM structure determination](https://doi.org/10.1038/nmeth.2115) | [1,365](https://openalex.org/W2075824676) | 基础, 专项验证 |
| `chen2013` | Chen et al. (2013) · [High-resolution noise substitution to measure overfitting and validate resolution in 3D structure determination by single particle electron cryomicroscopy](https://doi.org/10.1016/j.ultramic.2013.06.004) | [1,125](https://openalex.org/W2054770020) | 专项验证 |
| `kucukelbir2014` | Kucukelbir et al. (2014) · [Quantifying the local resolution of cryo-EM density maps](https://doi.org/10.1038/nmeth.2727) | [2,055](https://openalex.org/W2086812659) | 基础, 专项验证 |
| `tan2017` | Tan et al. (2017) · [Addressing preferred specimen orientation in single-particle cryo-EM through tilting](https://doi.org/10.1038/nmeth.4347) | [1,073](https://openalex.org/W2728385286) | 专项验证 |
| `vanheel2005` | van Heel & Schatz (2005) · [Fourier shell correlation threshold criteria](https://doi.org/10.1016/j.jsb.2005.05.009) | [950](https://openalex.org/W2058716938) | 基础, 方法分歧 |
| `kleywegt2024` | Kleywegt et al. (2024) · [Community recommendations on cryoEM data archiving and validation](https://doi.org/10.1107/s2052252524001246) | [36](https://openalex.org/W4389217803) | 社区建议 |
| `brunger1992` | Brünger (1992) · [Free R value: a novel statistical quantity for assessing the accuracy of crystal structures](https://doi.org/10.1038/355472a0) | [3,909](https://openalex.org/W1996607909) | 基础 |
| `evans2013` | Evans & Murshudov (2013) · [How good are my data and what is the resolution?](https://doi.org/10.1107/s0907444913000061) | [5,141](https://openalex.org/W2110808180) | 基础 |
| `karplus2012` | Karplus & Diederichs (2012) · [Linking Crystallographic Model and Data Quality](https://doi.org/10.1126/science.1218231) | [1,872](https://openalex.org/W2108959691) | 基础, 方法分歧 |
| `cruickshank1999` | Cruickshank (1999) · [Remarks about protein structure precision](https://doi.org/10.1107/s0907444998012645) | [490](https://openalex.org/W2020429677) | 基础 |
| `cruickshank1999-erratum` | Cruickshank (1999) · [Remarks about protein structure precision. Erratum](https://doi.org/10.1107/s0907444999004308) | [14](https://openalex.org/W2144643488) | 勘误 |
| `polder2017` | Liebschner et al. (2017) · [Polder maps: improving OMIT maps by excluding bulk solvent](https://doi.org/10.1107/s2059798316018210) | [706](https://openalex.org/W2585093856) | 专项验证 |
| `pintilie2020` | Pintilie et al. (2020) · [Measurement of atom resolvability in cryo-EM maps with Q-scores](https://doi.org/10.1038/s41592-020-0731-1) | [462](https://openalex.org/W3005016287) | 专项验证 |
| `ligand-challenge2024` | Lawson et al. (2024) · [Outcomes of the EMDataResource cryo-EM Ligand Modeling Challenge](https://doi.org/10.1038/s41592-024-02321-7) | [19](https://openalex.org/W4400007706) | 专项验证, 社区建议 |
| `iupac2011` | Arunan et al. (2011) · [Definition of the hydrogen bond (IUPAC Recommendations 2011)](https://doi.org/10.1351/pac-rec-10-01-02) | [1,984](https://openalex.org/W2053227378) | 基础, 社区建议 |
| `cmm2017` | Zheng et al. (2017) · [CheckMyMetal : a macromolecular metal-binding validation tool](https://doi.org/10.1107/s2059798317001061) | [352](https://openalex.org/W2589875042) | 专项验证 |
| `leonarski2017` | Leonarski et al. (2017) · [Mg2+ions: do they bind to nucleobase nitrogens?](https://doi.org/10.1093/nar/gkw1175) | [107](https://openalex.org/W2574750764) | 适用边界, 方法分歧 |
| `molprobity2018` | Williams et al. (2018) · [MolProbity: More and better reference data for improved all‐atom structure validation](https://doi.org/10.1002/pro.3330) | [5,172](https://openalex.org/W2765322245) | 基础, 专项验证 |
| `read2011` | Read et al. (2011) · [A New Generation of Crystallographic Validation Tools for the Protein Data Bank](https://doi.org/10.1016/j.str.2011.08.006) | [480](https://openalex.org/W2124464974) | 基础, 社区建议 |
| `afonine2018` | Afonine et al. (2018) · [New tools for the analysis and validation of cryo-EM maps and atomic models](https://doi.org/10.1107/s2059798318009324) | [879](https://openalex.org/W2791670278) | 专项验证 |
| `em-challenge2021` | Lawson et al. (2021) · [Cryo-EM model validation recommendations based on outcomes of the 2019 EMDataResource challenge](https://doi.org/10.1038/s41592-020-01051-w) | [122](https://openalex.org/W3127623024) | 专项验证, 社区建议 |
| `checkmysequence2022` | Chojnowski (2022) · [Sequence-assignment validation in cryo-EM models with checkMySequence](https://doi.org/10.1107/s2059798322005009) | [21](https://openalex.org/W4281697297) | 专项验证 |
| `register-errors2024` | Sánchez Rodríguez et al. (2024) · [Using deep-learning predictions reveals a large number of register errors in PDB depositions](https://doi.org/10.1107/s2052252524009114) | [8](https://openalex.org/W4403284158) | 专项验证, 适用边界 |
| `carugo2001` | Carugo & Pongor (2001) · [A normalized root‐mean‐spuare distance for comparing protein three‐dimensional structures](https://doi.org/10.1110/ps.690101) | [421](https://openalex.org/W2063581254) | 基础 |
| `tmalign2005` | Zhang & Skolnick (2005) · [TM-align: a protein structure alignment algorithm based on the TM-score](https://doi.org/10.1093/nar/gki524) | [4,092](https://openalex.org/W2102245393) | 基础 |
| `relion2012` | Scheres (2012) · [RELION: Implementation of a Bayesian approach to cryo-EM structure determination](https://doi.org/10.1016/j.jsb.2012.09.006) | [6,184](https://openalex.org/W2104234755) | 基础 |
| `pisa2007` | Krissinel & Henrick (2007) · [Inference of Macromolecular Assemblies from Crystalline State](https://doi.org/10.1016/j.jmb.2007.05.022) | [10,604](https://openalex.org/W2035503835) | 基础 |
| `krissinel2011` | Krissinel (2011) · [Macromolecular complexes in crystals and solutions](https://doi.org/10.1107/s0907444911007232) | [77](https://openalex.org/W2107996913) | 适用边界, 方法分歧 |
| `fraser2011` | Fraser et al. (2011) · [Accessing protein conformational ensembles using room-temperature X-ray crystallography](https://doi.org/10.1073/pnas.1111325108) | [666](https://openalex.org/W2087432921) | 专项验证, 适用边界 |
| `af2-2021` | Jumper et al. (2021) · [Highly accurate protein structure prediction with AlphaFold](https://doi.org/10.1038/s41586-021-03819-2) | [47,705](https://openalex.org/W3177828909) | 基础 |
| `af3-2024` | Abramson et al. (2024) · [Accurate structure prediction of biomolecular interactions with AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w) | [16,085](https://openalex.org/W4396721167) | 基础 |
| `af3-2024-addendum` | Abramson et al. (2024) · [Addendum: Accurate structure prediction of biomolecular interactions with AlphaFold 3](https://doi.org/10.1038/s41586-024-08416-7) | [349](https://openalex.org/W4404755712) | 补充说明 |
| `akdel2022` | Akdel et al. (2022) · [A structural biology community assessment of AlphaFold2 applications](https://doi.org/10.1038/s41594-022-00849-w) | [756](https://openalex.org/W4308463927) | 专项验证, 适用边界 |
| `terwilliger2024` | Terwilliger et al. (2024) · [AlphaFold predictions are valuable hypotheses and accelerate but do not replace experimental structure determination](https://doi.org/10.1038/s41592-023-02087-4) | [388](https://openalex.org/W4389174567) | 专项验证, 适用边界 |
| `monod1965` | Monod et al. (1965) · [On the nature of allosteric transitions: A plausible model](https://doi.org/10.1016/s0022-2836(65)80285-6) | [8,942](https://openalex.org/W1998093640) | 基础, 适用边界 |
| `hammes2009` | Hammes et al. (2009) · [Conformational selection or induced fit: A flux description of reaction mechanism](https://doi.org/10.1073/pnas.0907195106) | [595](https://openalex.org/W2041000185) | 适用边界 |
| `henzler2007` | Henzler-Wildman & Kern (2007) · [Dynamic personalities of proteins](https://doi.org/10.1038/nature06522) | [2,614](https://openalex.org/W2048822589) | 基础, 适用边界 |
| `motlagh2014` | Motlagh et al. (2014) · [The ensemble nature of allostery](https://doi.org/10.1038/nature13001) | [1,310](https://openalex.org/W1964439982) | 基础, 适用边界 |

## 已核验的冲突与更新边界

- **FSC 阈值：** Rosenthal–Henderson 2003 的 0.143 推导与 van Heel–Schatz 2005 的信息/统计准则并读。按 half-map 独立性、shell 样本、mask 与目标统计量说明适用条件；现行社区报告口径不能证明另一准则“已被证伪”，也不能把一个阈值当作局部正确性。见 `rh2003`、`vanheel2005`、`kleywegt2024` 的原文位置及 [cryo-em.md](cryo-em.md)。
- **X-ray 截断与坐标精度：** R-free、CC½ 和 paired refinement 回答互补问题；不能把一个信号阈值机械设成所有数据集的截断标准。Cruickshank 的精度公式需并读勘误，涉及原式 (30)、(49)、符号和交叉引用的更正；不要只复用原文公式。见 [xray.md](xray.md)。
- **晶体与溶液组装：** PISA 推断和条件匹配的直接溶液测量不回答完全相同的问题；冲突时以被声称状态的直接证据为重点，再核构建体、浓度、盐、配体和温度。Krissinel 2011 的摘要为 Kd ≥ 100 μM，PDF 提取的 `mM` 经 IUCr 官方全文纠正。见 [biological-context.md](biological-context.md)。
- **预测与实验：** 高置信度预测可提出替代解释，不能投票压过实验地图；但实验模型也须核数据质量。register 检查是候选筛查，不是错误后验概率或自动定案。见 [predicted-models.md](predicted-models.md)、[model-validation.md](model-validation.md)。
- **AF3 Addendum：** 核验的通知说明推理代码公开，没有修改原文准确率；不能按页面栏目“Corrections & amendments”推断所有原文指标失效。与原文的 DOI 双向关系保留在 JSON 的 `updates`。

## 工具文档与书目说明

- [Phenix `validate_ligands` 当前官方文档](https://www.phenix-online.org/documentation/reference/validate_ligands.html) 于 2026-09-30 核验，仅支持该页陈述的 X-ray 行为。该页不是固定软件版本的保证，也不从参数名推导 EM RSCC 算法。它单列为工具资料，不增加 39 条论文记录。
- TM-align 的 Crossref 作者字段不完整，作者序列按 Oxford Academic 正式记录补齐。Carugo 2001 的题名在出版方/Crossref 中写作 “root-mean-spuare”，书目保留这一字样；Chen 2013 的 Crossref 未给 issue，如实留空。
