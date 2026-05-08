# 乳腺癌知识库 (Breast Cancer Knowledge Base)

结构化的乳腺癌医学知识图谱，基于知识三元组（head-relation-tail）构建，支持RAG/LLM应用集成。

## 仓库结构

```
breast-cancer-kb/
├── data/
│   ├── knowledge-graph/      # 知识图谱源文件
│   │   ├── epidemiology.json   # 流行病学数据
│   │   ├── biomarkers.json     # 分子分型与生物标志物
│   │   ├── csco_2024.json      # CSCO 2024指南推荐
│   │   └── treatment.json       # 治疗方案
│   ├── kb.json                 # 构建后生成的知识库
│   └── kb_meta.json            # 知识库元数据
├── scripts/
│   ├── build_kb.py            # 知识库构建脚本
│   └── tests/
│       └── test_kb_format.py  # 格式验证测试
├── schemas/
│   └── triplet_schema.json    # 三元组JSON Schema
├── docs/
│   └── domain_guide.md        # 知识域说明文档
├── README.md
├── UPDATE_POLICY.md           # 更新策略
├── CHANGELOG.md               # 变更日志
└── DEPLOY.md                  # 部署说明
```

## 知识域

| 域ID | 名称 | 描述 | 三元组数 |
|------|------|------|----------|
| epidemiology | 流行病学 | 发病率、死亡率、危险因素、地区分布等 | ~17 |
| biomarkers | 分子分型与生物标志物 | ER/PR/HER2/Ki-67、BRCA突变、分子亚型等 | ~17 |
| csco_2024 | CSCO 2024指南推荐 | CSCO指南的治疗推荐、分层依据等 | ~17 |
| treatment | 治疗方案 | 手术、放疗、化疗、内分泌治疗、靶向治疗等 | ~17 |

## 知识三元组格式

每个知识条目以三元组（Triplet）形式存储：

```json
{
  "head": "乳腺癌",
  "relation": "2022年中国新发病例数",
  "tail": "35.72万",
  "source": "GLOBOCAN 2022",
  "evidence": "中国女性乳腺癌新发病例数占全部恶性肿瘤新发病例的9.1%",
  "domain": "epidemiology",
  "confidence": 0.95,
  "pmid": "35622778"
}
```

### 字段说明

| 字段 | 类型 | 必需 | 描述 |
|------|------|------|------|
| head | string | 是 | 三元组头实体 |
| relation | string | 是 | 关系类型 |
| tail | string | 是 | 三元组尾实体 |
| source | string | 是 | 信息来源 |
| evidence | string | 是 | 证据描述 |
| domain | string | 是 | 知识域分类 |
| confidence | number | 是 | 置信度 (0-1) |
| pmid | string | 否 | PubMed文献ID |

## 快速开始

### 构建知识库

```bash
cd breast-cancer-kb
python3 scripts/build_kb.py
```

### 验证格式

```bash
python3 scripts/tests/test_kb_format.py
```

### 查看元数据

```json
{
  "name": "乳腺癌知识库",
  "version": "1.0.0",
  "total_triplets": 68,
  "total_domains": 4,
  "domains": [
    {"id": "epidemiology", "name": "流行病学", "triplet_count": 17},
    {"id": "biomarkers", "name": "分子分型与生物标志物", "triplet_count": 17},
    {"id": "csco_2024", "name": "CSCO 2024指南推荐", "triplet_count": 17},
    {"id": "treatment", "name": "治疗方案", "triplet_count": 17}
  ]
}
```

## 应用场景

- **RAG系统**: 作为医学知识检索增强的参考源
- **LLM训练**: 用于医学大模型的领域知识注入
- **临床决策支持**: 提供规范化的治疗指南参考
- **医学教育**: 结构化的乳腺癌知识学习资源

## 数据来源

- GLOBOCAN 2022 全球癌症统计数据
- CSCO 乳腺癌诊疗指南 2024
- NCCN Guidelines Breast Cancer 2024
- ASCO/CAP 免疫组化检测指南
- 相关PubMed文献

## 致谢

本知识库基于公开的医学指南和文献构建，仅供学术研究和AI应用参考，不构成临床诊疗建议。

## License

本项目采用 MIT License。
