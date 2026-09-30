# 预测模型审计

当文章把 AlphaFold 等预测坐标用于实验结构、配体结合、界面或机制结论时按需调用。预测模型可提出结构假设或辅助解释；没有实验数据支持时，不称为“测定的结构”。

## 模型来源与问题范围

- 记录模型家族/代际、使用的输出、目标序列和残基范围；复合物还要核对伙伴、构建体、突变/修饰及配体输入。数据库、权重、代码、运行日期和采样细节只在影响模型身份、复现或当前主张时记录。
- AlphaFold 2、AlphaFold-Multimer 与 AlphaFold 3 的任务、输入和评分不同，不能混用。只写“AlphaFold”且无法从上下文辨认版本时，标注版本不明。
- 引用论文评测时，说明具体任务、测试集、同源过滤、训练截止和取样/排名流程。基准成功率描述的是那组测试，不是某一目标的正确概率。

## 置信度与坐标字段

- pLDDT 是模型对局部准确度的估计；PAE 描述残基/链间相对位置的预测对齐误差；pTM/ipTM 是模型的整体或界面分数。它们都不是实验观测、结合亲和力、占有率或单个目标的正确概率。
- 高链内 pLDDT 不保证域间排布、侧链或界面正确；按主张涉及的局部检查，不用平均分掩盖薄弱区域，也不套用统一阈值宣布结构正确。
- 不把预测置信度当作实验 B 因子。若预测文件把置信度写入 PDB/mmCIF 的 B-factor 字段，先查生成程序和文件来源，再标注该字段含义；实验 B 因子也受数据和精修条件影响。

## 预测先验与实验支持

- 若预测坐标参与分子置换、初始建模、缺失区补模、约束或 refinement，记录其用途。预测模型与它辅助拟合的同一份数据相符，不构成两份独立证据；检查实验数据能否区分原模型和合理替代模型。
- 预测模型放入 cryo-EM 或 X-ray 密度时，检查实际实验地图的局部支持，并记录相关分辨率、地图处理和拟合条件。对不符之处还要考虑构建体、配体、修饰、晶体接触及构象状态；高置信冲突应报告，不能单凭分数裁决。
- 预测出的配体或离子位置不是结合、占有率、化学计量或功能的实验依据。机制或结合主张需由相应实验支持。

## Register 检查工具

- checkMySequence 需要 cryo-EM map、坐标模型和链序列，按 map 支持的残基指派提示可能的 register 问题。论文的 p-value 界限是基于片段基准的经验选择，不是模型出错概率；测试片段可从20延长到60个残基，作者指出可检出的错位通常应超过约10个残基，较短错位可能漏检。把结果当候选并回看 map、序列和替代 register。
- conkit-validate 等联系图筛查比较模型中的接触与 AF2 预测接触，是 map-independent 的计算信号，不是实验验证；论文先要求错位至少连续5个残基，再通过过滤，最终称为 putative error。它依赖接触预测质量，构象差异或 fold-switch 也可能触发旗标，应以局部实验数据和序列复核。

## 代际、评测与代码边界

- AF2 2021 论文报告的是该版本在 CASP14 及特定 PDB 基准上的表现；其 pLDDT/pTM 与实测结构误差的基准关系不能无条件移植到后续 AF2 流程或 AF3。
- AF3 2024 论文覆盖蛋白、核酸、配体、离子和修饰等特定评测任务，仍报告有构象覆盖、无序区 hallucination、手性/碰撞和部分目标准确度方面的限制。需要复述其数字时，核对该任务的训练截止及输出排名；例如 PoseBusters 使用 2019-09-30 截止模型，其它主要评测使用 2021-09-30 截止；常规结果从5个模型种子、每种子5个扩散样本中选 top-confidence，抗体分析的特定结果使用1,000个种子。
- AF3 Addendum 说明底层推理代码在原文发表后发布；它没有更正原论文的准确率或科学结论。代码可用性与许可条件应按所用版本另核。

## 参考文献与原文定位

- Jumper et al. (2021), [DOI: 10.1038/s41586-021-03819-2](https://doi.org/10.1038/s41586-021-03819-2)：Fig. 2c,d 对照 pLDDT/pTM 与 PDB 基准中的 lDDT/TM-score（PDF p. 3）；“MSA depth and cross-chain contacts”及 Discussion（p. 6）；Methods “Inference regimen”, “Metrics”, “Test set of recent PDB sequences”（pp. 9–10）。
- Abramson et al. (2024), [DOI: 10.1038/s41586-024-07487-w](https://doi.org/10.1038/s41586-024-07487-w)：Fig. 1 与架构（PDF pp. 2–4）；“Accuracy across complex types”, “Predicted confidences track accuracy”, “Model limitations”及 Fig. 4–5（pp. 5–7）；Methods “Inference regime”, “Metrics”, “Recent PDB evaluation set”, “PoseBusters”（pp. 9–10）；Extended Data Figs. 7–8、Table 1（pp. 18–19、21）。
- Abramson et al. (2024), [Addendum DOI: 10.1038/s41586-024-08416-7](https://doi.org/10.1038/s41586-024-08416-7)：全文短文（PDF p. 1），说明 inference code 后续发布。
- Akdel et al. (2022), [DOI: 10.1038/s41594-022-00849-w](https://doi.org/10.1038/s41594-022-00849-w)：Fig. 1、3–6 与相应结果（PDF pp. 2–10）；Methods 中 oligomerization 与 experimental model building（pp. 13–15）。口袋分析提到高置信子集可能受模板偏倚；寡聚体测试允许潜在训练集重叠。
- Terwilliger et al. (2024), [DOI: 10.1038/s41592-023-02087-4](https://doi.org/10.1038/s41592-023-02087-4)：“Comparing AlphaFold predictions with density maps”及 Fig. 1（PDF p. 2）；Fig. 4、Table 1 和 “Using confidence (pLDDT) to estimate errors”（p. 5）；Methods 与 “Control experiments and limitations”（pp. 8–9）。所选 102 个高质量晶体学模型/map 中，约 10% 的 pLDDT >90 Cα 坐标与参照结构相差超过 2 Å；该比例受样本构成和晶体条件限制。
- Chojnowski (2022), [DOI: 10.1107/S2059798322005009](https://doi.org/10.1107/S2059798322005009)：§2 的输入与片段指派、§§3.1–3.4 的数据与方法、§§4.1–4.7 和 Conclusions（PDF pp. 2–10），Fig. 1、2、7–9。作者将高置信错配称为可能 register 问题；阈值选择、低分辨率补偿及短错位限制见 §4.1、§4.2 和 Conclusions。
- Sánchez Rodríguez et al. (2024), [DOI: 10.1107/S2052252524009114](https://doi.org/10.1107/S2052252524009114)：§§2.1–2.6 的数据集/筛查，§§3.1–3.6 的结果、交叉检查和局限及 Figs. 1–11（PDF pp. 2–12）。范围为截至 2022-04-05、3–5 Å 的 cryo-EM 与 X-ray PDB 条目；作者称输出为 putative register errors，并在 Fig. 11 展示 calcineurin fold-switch 假阳性。

这些来源支持把预测作为可审计的假设，不提供对当前目标的免检通行证。
