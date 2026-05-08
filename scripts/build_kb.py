#!/usr/bin/env python3
"""
乳腺癌知识库构建脚本
构建知识图谱三元组，生成 kb.json 和 kb_meta.json
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# 知识域映射
DOMAIN_NAMES = {
    "epidemiology": "流行病学",
    "biomarkers": "分子分型与生物标志物",
    "csco_2024": "CSCO 2024指南推荐",
    "treatment": "治疗方案"
}

def load_knowledge_files(kg_dir: Path) -> Dict[str, Any]:
    """加载所有知识图谱文件"""
    files = {
        "epidemiology.json": "epidemiology",
        "biomarkers.json": "biomarkers",
        "csco_2024.json": "csco_2024",
        "treatment.json": "treatment"
    }

    knowledge_data = {}
    for filename, domain in files.items():
        filepath = kg_dir / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                knowledge_data[domain] = json.load(f)
            print(f"✓ 已加载: {filename}")
        else:
            print(f"✗ 缺失: {filename}")

    return knowledge_data


def build_knowledge_base(knowledge_data: Dict[str, Any]) -> Dict[str, Any]:
    """构建知识库"""
    all_triplets = []
    domain_stats = {}
    source_stats = {}

    for domain, data in knowledge_data.items():
        triplets = data.get("triplets", [])
        domain_stats[domain] = {
            "name": DOMAIN_NAMES.get(domain, domain),
            "count": len(triplets)
        }

        for triplet in triplets:
            triplet["domain"] = domain
            all_triplets.append(triplet)

            # 统计来源
            source = triplet.get("source", "未知")
            if source not in source_stats:
                source_stats[source] = 0
            source_stats[source] += 1

    return {
        "triplets": all_triplets,
        "stats": {
            "total": len(all_triplets),
            "domains": len(domain_stats),
            "domain_stats": domain_stats,
            "source_stats": source_stats
        }
    }


def generate_metadata(kb_data: Dict[str, Any], output_dir: Path) -> Dict[str, Any]:
    """生成知识库元数据"""
    stats = kb_data["stats"]

    meta = {
        "name": "乳腺癌知识库",
        "name_en": "Breast Cancer Knowledge Base",
        "version": "1.0.0",
        "build_date": datetime.now().isoformat(),
        "total_triplets": stats["total"],
        "total_domains": stats["domains"],
        "domains": []
    }

    for domain_id, domain_info in stats["domain_stats"].items():
        meta["domains"].append({
            "id": domain_id,
            "name": domain_info["name"],
            "triplet_count": domain_info["count"]
        })

    # 计算置信度统计
    confidences = [t.get("confidence", 1.0) for t in kb_data["triplets"]]
    meta["confidence_stats"] = {
        "average": round(sum(confidences) / len(confidences), 3),
        "min": min(confidences),
        "max": max(confidences)
    }

    # PMIDs统计
    pmids = [t.get("pmid") for t in kb_data["triplets"] if t.get("pmid")]
    meta["citation_stats"] = {
        "total_papers": len(set(pmids)),
        "papers_with_pmid": len(pmids)
    }

    return meta


def main():
    # 路径设置
    script_dir = Path(__file__).parent
    repo_dir = script_dir.parent
    kg_dir = repo_dir / "data" / "knowledge-graph"
    data_dir = repo_dir / "data"

    print("=" * 50)
    print("乳腺癌知识库构建程序")
    print("=" * 50)
    print()

    # 1. 加载知识文件
    print("[1/4] 加载知识图谱文件...")
    knowledge_data = load_knowledge_files(kg_dir)
    print()

    if not knowledge_data:
        print("错误: 未找到任何知识图谱文件")
        return 1

    # 2. 构建知识库
    print("[2/4] 构建知识库...")
    kb_data = build_knowledge_base(knowledge_data)
    print(f"  - 总三元组数: {kb_data['stats']['total']}")
    print(f"  - 知识域数: {kb_data['stats']['domains']}")
    for domain_id, info in kb_data['stats']['domain_stats'].items():
        print(f"    · {info['name']}: {info['count']}条")
    print()

    # 3. 生成元数据
    print("[3/4] 生成元数据...")
    meta = generate_metadata(kb_data, data_dir)
    print(f"  - 平均置信度: {meta['confidence_stats']['average']}")
    print(f"  - 引用文献数: {meta['citation_stats']['total_papers']}")
    print()

    # 4. 保存文件
    print("[4/4] 保存文件...")
    kb_output = data_dir / "kb.json"
    meta_output = data_dir / "kb_meta.json"

    # 保存kb.json（不含stats）
    kb_save = {"triplets": kb_data["triplets"]}
    with open(kb_output, 'w', encoding='utf-8') as f:
        json.dump(kb_save, f, ensure_ascii=False, indent=2)
    print(f"  ✓ 已保存: {kb_output}")

    # 保存kb_meta.json
    with open(meta_output, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"  ✓ 已保存: {meta_output}")
    print()

    print("=" * 50)
    print("构建完成!")
    print(f"共生成 {kb_data['stats']['total']} 条知识三元组")
    print(f"覆盖 {kb_data['stats']['domains']} 个知识域")
    print("=" * 50)

    return 0


if __name__ == "__main__":
    exit(main())
