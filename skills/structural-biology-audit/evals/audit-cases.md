# 独立行为评估案例

以下13组均为合成材料，只检验审计行为，不代表真实结构的正确性。评估时先读取 SKILL.md，再按主张加载参考文件；不得把未提供的数据写成已经复算。

## Cryo-EM 与化学接触
请使用 structural-biology-audit 审计下列六个独立结构结论。以下为合成案例的完整可用材料，用于技能行为验证，不对应真实沉积结构。仅依据提供的材料判断案例；可以读取技能参考来解释方法，但不能宣称看过未提供的地图或重做计算。每个案例给判定、证据位置、限制、缺失/判别证据。

### E1
原句：The structure was determined at 2.8 Å resolution.
材料E1-M1：两半粒子在精修后期共用未低通的高分辨率参考。作者称其为gold-standard。FSC报告采用0.143；二值紧mask后为2.8 Å，unmasked为3.8 Å；未报告phase-randomization或noise-substitution校正。没有提供half-map文件，仅有曲线和上述方法文字。

### E2
原句：The ligand is clearly resolved.
材料E2-F1说明：全局FSC0.143为2.8 Å；位点局部分辨率约5.0 Å。论文描述在全图显示值0.7时只能见一个团块，调整配体显示值至0.3才有连接外形；一个芳环和两个关键取代基未获分开密度支持。坐标中使用理想配体字典，occupancy固定1.0。未报告局部fit或其他姿势比较；没有原始map可计算。

### E3
原句：Asp54 forms a hydrogen bond with the carbonyl oxygen of ligand L.
材料E3-C1：双方为羧酸根Oδ2和中性酰胺羰基O；测定pH7.4，作者明确将Asp54建模为去质子化羧酸根。两O距离3.0 Å，没有介入水，PyMOL画了一条黄线。未提供质子位置、供受体方向或其他化学证据。

### E4
原句：Mg2+ is definitively identified at site M.
材料E4-M1：坐标中标MG；六个O配位邻居平均距离2.38 Å，缓冲含200mM NaCl及2mM MgCl2。精修使用指定MG restraint和固定occupancy1.0。只有一个球形电子密度峰和全局Rfree，无异常散射、替代离子精修或位点B factor比较。尚未排除Na、水或其他解释。

### E5
原句：The reported gold-standard half-map FSC resolution is 3.1 Å at the 0.143 criterion.
材料E5-M1：处理日志记载粒子从初次三维精修起分为独立半集，低通初始化；噪声替换校正masked曲线过0.143于3.1 Å，unmasked曲线3.2 Å。方法、软mask参数和曲线种类均报告。该句只陈述此报告口径，不声称所有位点3.1 Å、模型完全正确或机制成立。案例未提供实际half-map文件，因此不能独立复算曲线。

### E6
原句：The Lys87–ligand contact is consistent with a hydrogen bond.
材料E6-G1：X-ray局部1.2 Å数据下，Lys Nζ与中性酰胺羰基O的重原子坐标有连续局部密度支持，rotamer无冲突，未发现更好的替代构象。pH7.0及化学环境支持Lys供体和羰基受体。D···A为3.0 Å；添加理想H后H···A为2.0 Å、D-H···A为170度；H坐标为软件添加，未直接解析。原句只称consistent with，并没有声称实验观察到质子。

## 跨方法、冲突与正面案例
请用 structural-biology-audit 核验下列七个独立结论。案例数据为合成文字材料，不对应真实结构；方法来源使用技能内真实论文。不要编辑任何文件、入库或生成文章。每条给判定、证据位置、限制及缺失/判别证据；文献分歧给有条件裁决。

### C1
原句：The complete structures are identical (RMSD=0.4 Å).
材料C1-A1：两条蛋白各320残基，RMSD仅对保守核心84个Cα计算；关键活性环20残基未比对，两结构域相对转动18度。未给被排除区域的密度支持或局部分析。

### C2
原句：The AlphaFold region is experimentally more mobile because its B factor is 95.
材料C2-P1：结构来源为AlphaFold2；PDB B-factor列写的是pLDDT。没有X-ray/EM实验、动力学或热力学测定。该区域pLDDT95、链间PAE高。作者以95和另一段65比较运动。

### C3
原句：The apo and holo structures prove induced fit rather than conformational selection.
材料C3-S1：同一构建体两个晶体模型，apo开放、holo闭合；模型有密度支持，但晶型不同。没有结合动力学、apo少数态群体或路径通量测量。讨论引用Hammes, Chang & Oas2009。

### C4
原句：This protein is a physiological dimer because PISA places the dimer first.
材料C4-B1：PISA输入为完整天然序列晶体坐标，最高排名dimer。独立SEC-MALS在同一缓冲、配体、温度和足以覆盖结构实验相关浓度范围下支持monomer；论文未解释冲突。仅有此溶液测量，不含细胞内计量数据。

### C5
原句：A register error is proven because an AlphaFold-based checker flagged residues120–140.
材料C5-V1：现坐标在该区域几何无明显异常。工具提出+2的替代register；AF2预测与现模型同一序列。地图不可访问，未做替代register对map fit的比较，未获取高分辨率参照。作者引用register-errors2024，并称文中所有putative errors均已实验证实。

### C6
原句A：必须仅按Rosenthal–Henderson2003的固定0.143报告分辨率，van Heel–Schatz2005已被证明错误。
原句B：AF3的2024 Addendum修改了原文准确率，因此所有原文准确率都失效；Cruickshank1999原公式无需勘误即可复用。
材料C6-R1：两组FSC方法讨论、AF3原文/addendum、Cruickshank/erratum均为技能内选定真实DOI，可以核验其原文或索引。请分别评价这些来源冲突/更新结论，不靠引用量投票。

### C7
原句：The aligned catalytic core has a closely matching backbone conformation in these two coordinate models.
材料C7-A1：同一蛋白同一序列与核心边界，提供一致链/残基映射、各84个已建模Cα；无缺失或插入，按该84原子叠合后RMSD0.4 Å，核心逐残基最大偏离0.8 Å。该句限定为坐标模型的核心主链比较，不涉及未比对区、功能或模型实验正确性。
