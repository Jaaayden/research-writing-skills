# X-ray 晶体学：数据与精度审计

用于核验 X-ray 结构的分辨率、数据质量、精修与坐标精度主张。优先读取论文、PDB 条目及其验证报告；若反射数据不可访问，注明哪些数据级检查无法完成，不把缺失信息判成错误。

## 数据完整度、各向异性与分辨率界限

- 检查总体和最高分辨率壳层的 completeness、冗余度及信噪指标；若结论依赖 anomalous signal，也记录 anomalous completeness。严重缺失的壳层或方向会限制相应结论，但单凭完整度不能判定模型错误。([evans2013](https://doi.org/10.1107/S0907444913000061)，§3.1、图 1 及 §3.2.3)
- 查看 CC1/2 随分辨率壳层的变化；明显各向异性时，尽可能比较主要方向或方向扇区的数据支持，不能把一个各向同性 cutoff 当作每个方向都同等有信息。Rmerge/Rmeas 不适合作为唯一的高分辨率截断标准。([evans2013](https://doi.org/10.1107/S0907444913000061)，§§3.2.2–3.2.3、图 2；[karplus2012](https://doi.org/10.1126/science.1218231)，图 2)
- 对争议 cutoff，比较相邻 cutoff 的 paired refinement：为保证可比性，使用同一起始模型、相同 free flags 和相同精修流程，并在较差 cutoff 的共同分辨率范围计算两种模型的 Rwork、Rfree。结合 CC1/2、差值图和模型变化判断新增数据是否有用；不套用单一普适 CC1/2 阈值。Karplus 与 Diederichs 用共同分辨率范围的 Rwork/Rfree 比较展示 paired refinement；Evans 与 Murshudov 也建议将其作为分辨率决策的补充检验。([karplus2012](https://doi.org/10.1126/science.1218231)，图 1、p. 1031；[evans2013](https://doi.org/10.1107/S0907444913000061)，§5、p. 1211)

## Rwork、Rfree 与独立性

- 并列核对 Rwork、Rfree、精修分辨率和 free-set 规模。Rfree 的交叉验证含义依赖未参与模型拟合的 test reflections；重精修和模型比较应保留同一组 free flags，不重新抽签，也不把反复用于挑选模型的 test set 当作独立检验。还要检查 flags 是否与晶格对称性及孪晶律兼容；否则工作集与 test set 可能产生统计依赖并人为压低 Rfree。([brunger1992](https://doi.org/10.1038/355472a0)，pp. 472–475；[read2011](https://doi.org/10.1016/j.str.2011.08.006)，p. 1404；[karplus2012](https://doi.org/10.1126/science.1218231)，p. 1031)
- Rwork/Rfree 的差值、绝对值或某一轮下降都不能单独证明局部结构正确；将它们作为全局指标，与数据质量、精修流程和被主张的局部证据一并审计。无法确认 free-set 历史时，标为“独立性无法核验”。([evans2013](https://doi.org/10.1107/S0907444913000061)，§5、p. 1211；[read2011](https://doi.org/10.1016/j.str.2011.08.006)，p. 1404)

## 分辨率不等于坐标精度

- 将分辨率（反射数据最高空间频率）与坐标精度/坐标不确定度分开。名义分辨率描述数据截断，不是每个原子的定位误差，也不能单独支持“坐标准确至 X Å”。([evans2013](https://doi.org/10.1107/S0907444913000061)，§5；[cruickshank1999](https://doi.org/10.1107/S0907444998012645)，§6.4、Eq. 30；§10.2)
- 若讨论 DPI 或 σ(r)，按原文把 DPI 解释为粗略的衍射数据精度指标，不把它当成每个原子的实测误差。引用或重算前须使用勘误版本：Eq. 30 中 C 的指数由 −1/2 更正为 −1/3；Eq. 49 的残差平方和项须包含权重 w。勘误还更正了原文 p. 589 §4.2 的符号和 Fig. 7 图注。([cruickshank1999](https://doi.org/10.1107/S0907444998012645)，§6.4、Eq. 30、§7.1、§10.2、Appendix A1 Eq. 49；[cruickshank1999-erratum](https://doi.org/10.1107/S0907444999004308)，p. 1108)

## 审计记录

记录 PDB accession、所用坐标/反射文件的版本或修订日期、数据来源、报告的分辨率界限和验证报告位置。涉及特定原子时，记录 `_atom_site.auth_asym_id`/`_atom_site.label_asym_id`、`auth_seq_id`/`label_seq_id`、`pdbx_PDB_ins_code`、`auth_atom_id`/`label_atom_id` 与 `label_alt_id`；论文编号与沉积文件不一致时，明确映射关系。
