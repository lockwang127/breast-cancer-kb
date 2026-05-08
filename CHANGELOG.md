# Changelog

所有重要的知识库变更都会记录在此。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)。

## [1.0.0] - 2025-01-15

### Added

#### 流行病学数据 (epidemiology)
- 中国2022年新发病例数据 (35.72万)
- 中国2022年死亡人数 (约8万)
- 病死比 (约22%)
- 发病率趋势分析
- 高发年龄分布 (45-55岁)
- 城市/农村地区差异
- 五年生存率数据 (83.2%)
- 全球发病排名
- 危险因素和保护因素
- 遗传性乳腺癌比例
- BRCA突变携带者风险
- 筛查项目信息

#### 分子分型与生物标志物 (biomarkers)
- 分子亚型分布比例
- HR+/HER2- (70%)
- HER2+ (15-20%)
- 三阴性 (15%)
- Ki-67判定标准
- BRCA1/BRCA2突变特征
- ER/PR/HER2阳性判定标准
- TP53/PIK3CA突变分布
- PARP抑制剂适应证
- CDK4/6抑制剂应用
- 双靶向治疗地位
- NGS基因检测意义

#### CSCO 2024指南推荐 (csco_2024)
- HR+早期乳腺癌内分泌治疗推荐
- HR+晚期乳腺癌CDK4/6抑制剂推荐
- HER2+一线标准治疗 (曲帕双靶+紫杉类)
- 三阴性化疗方案 (蒽环类+紫杉类)
- PARP抑制剂适应证
- T-DM1/T-DXd推荐
- 绝经前OFS治疗
- 免疫治疗推荐 (帕博利珠单抗)
- 新辅助治疗后强化治疗
- 骨改良药物推荐
- 生育保护建议

#### 治疗方案 (treatment)
- 保乳手术适应证
- 前哨淋巴结活检适应证
- 新辅助治疗适应证
- 辅助治疗分层依据
- 全乳切除术适应证
- 放疗适应证
- 化疗方案 (AC/TC方案)
- 内分泌治疗疗程
- 曲妥珠单抗疗程
- 心脏毒性监测
- 戈舍瑞林作用机制
- CDK4/6抑制剂药物

### Created
- `schemas/triplet_schema.json` - 三元组JSON Schema定义
- `scripts/build_kb.py` - 知识库构建脚本
- `scripts/tests/test_kb_format.py` - 格式验证测试
- `docs/domain_guide.md` - 知识域说明文档
- `UPDATE_POLICY.md` - 更新策略文档

### Documentation
- `README.md` - 仓库说明文档
- `DEPLOY.md` - GitHub部署说明
