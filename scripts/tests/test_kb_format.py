#!/usr/bin/env python3
"""
乳腺癌知识库格式验证测试
验证 kb.json 和各个知识图谱文件的格式正确性
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any

# 必需字段
REQUIRED_FIELDS = ["head", "relation", "tail", "source", "evidence", "domain", "confidence"]
OPTIONAL_FIELDS = ["pmid"]

# 置信度范围
MIN_CONFIDENCE = 0.0
MAX_CONFIDENCE = 1.0


class ValidationResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
        self.warnings = []

    def add_pass(self, message: str):
        self.passed += 1
        print(f"  ✓ {message}")

    def add_error(self, message: str):
        self.failed += 1
        self.errors.append(message)
        print(f"  ✗ {message}")

    def add_warning(self, message: str):
        self.warnings.append(message)
        print(f"  ⚠ {message}")


def validate_triplet(triplet: Dict[str, Any], index: int, result: ValidationResult):
    """验证单个三元组"""
    # 检查必需字段
    for field in REQUIRED_FIELDS:
        if field not in triplet:
            result.add_error(f"第{index}条: 缺少必需字段 '{field}'")
            return

    # 检查字段类型
    if not isinstance(triplet["head"], str) or not triplet["head"].strip():
        result.add_error(f"第{index}条: head 必须是非空字符串")

    if not isinstance(triplet["relation"], str) or not triplet["relation"].strip():
        result.add_error(f"第{index}条: relation 必须是非空字符串")

    if not isinstance(triplet["tail"], str) or not triplet["tail"].strip():
        result.add_error(f"第{index}条: tail 必须是字符串")

    # 检查置信度范围
    confidence = triplet.get("confidence")
    if confidence is not None:
        if not isinstance(confidence, (int, float)):
            result.add_error(f"第{index}条: confidence 必须是数字")
        elif confidence < MIN_CONFIDENCE or confidence > MAX_CONFIDENCE:
            result.add_error(f"第{index}条: confidence 必须在0-1之间")
        else:
            result.add_pass(f"第{index}条: 置信度 {confidence} 合法")

    # 检查可选字段
    if "pmid" in triplet:
        pmid = triplet["pmid"]
        if pmid and not str(pmid).isdigit():
            result.add_warning(f"第{index}条: pmid '{pmid}' 格式可能不正确")

    # 检查域有效性
    valid_domains = ["epidemiology", "biomarkers", "csco_2024", "treatment"]
    domain = triplet.get("domain")
    if domain not in valid_domains:
        result.add_warning(f"第{index}条: domain '{domain}' 未在预期列表中")

    # 通过基本验证
    if result.failed == 0:
        result.add_pass(f"第{index}条: 格式验证通过")


def validate_knowledge_file(filepath: Path, result: ValidationResult) -> Tuple[bool, int]:
    """验证单个知识图谱文件"""
    print(f"\n验证文件: {filepath.name}")

    # 检查文件存在
    if not filepath.exists():
        result.add_error(f"文件不存在: {filepath}")
        return False, 0

    # 尝试解析JSON
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        result.add_error(f"JSON格式错误: {e}")
        return False, 0

    # 检查元数据
    if "_meta" not in data:
        result.add_warning("缺少 _meta 元数据")

    # 检查triplets数组
    if "triplets" not in data:
        result.add_error("缺少 triplets 数组")
        return False, 0

    triplets = data["triplets"]
    if not isinstance(triplets, list):
        result.add_error("triplets 必须是数组")
        return False, 0

    if len(triplets) == 0:
        result.add_error("triplets 数组为空")
        return False, 0

    # 验证每个三元组
    for i, triplet in enumerate(triplets, 1):
        validate_triplet(triplet, i, result)

    triplet_count = len(triplets)
    if triplet_count >= 15:
        result.add_pass(f"共 {triplet_count} 条三元组 (≥15，满足要求)")
    else:
        result.add_error(f"仅 {triplet_count} 条三元组 (<15，不满足要求)")

    return result.failed == 0, triplet_count


def validate_schema(filepath: Path, result: ValidationResult):
    """验证JSON Schema文件"""
    print(f"\n验证Schema文件: {filepath.name}")

    if not filepath.exists():
        result.add_error(f"Schema文件不存在: {filepath}")
        return

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        result.add_pass("Schema文件格式正确")
    except json.JSONDecodeError as e:
        result.add_error(f"Schema JSON格式错误: {e}")


def main():
    script_dir = Path(__file__).parent
    repo_dir = script_dir.parent.parent  # scripts/tests/ -> scripts/ -> repo root
    kg_dir = repo_dir / "data" / "knowledge-graph"
    schema_file = repo_dir / "schemas" / "triplet_schema.json"

    print("=" * 60)
    print("乳腺癌知识库格式验证")
    print("=" * 60)

    result = ValidationResult()
    total_triplets = 0

    # 验证知识图谱文件
    kg_files = [
        "epidemiology.json",
        "biomarkers.json",
        "csco_2024.json",
        "treatment.json"
    ]

    print("\n[1] 验证知识图谱文件")
    for filename in kg_files:
        filepath = kg_dir / filename
        success, count = validate_knowledge_file(filepath, result)
        if success:
            total_triplets += count

    # 验证Schema
    print("\n[2] 验证Schema文件")
    validate_schema(schema_file, result)

    # 验证生成的kb.json
    print("\n[3] 验证生成的kb.json")
    kb_file = repo_dir / "data" / "kb.json"
    if kb_file.exists():
        try:
            with open(kb_file, 'r', encoding='utf-8') as f:
                kb_data = json.load(f)
            kb_triplets = len(kb_data.get("triplets", []))
            result.add_pass(f"kb.json 存在，包含 {kb_triplets} 条三元组")
        except json.JSONDecodeError as e:
            result.add_error(f"kb.json JSON格式错误: {e}")
    else:
        result.add_warning("kb.json 不存在（需运行 build_kb.py 生成）")

    # 验证kb_meta.json
    print("\n[4] 验证kb_meta.json")
    meta_file = repo_dir / "data" / "kb_meta.json"
    if meta_file.exists():
        try:
            with open(meta_file, 'r', encoding='utf-8') as f:
                meta = json.load(f)
            result.add_pass(f"kb_meta.json 存在")
            result.add_pass(f"  - 知识库名称: {meta.get('name', 'N/A')}")
            result.add_pass(f"  - 版本: {meta.get('version', 'N/A')}")
            result.add_pass(f"  - 总三元组: {meta.get('total_triplets', 0)}")
            result.add_pass(f"  - 知识域数: {meta.get('total_domains', 0)}")
        except json.JSONDecodeError as e:
            result.add_error(f"kb_meta.json JSON格式错误: {e}")
    else:
        result.add_warning("kb_meta.json 不存在（需运行 build_kb.py 生成）")

    # 总结
    print("\n" + "=" * 60)
    print("验证结果总结")
    print("=" * 60)
    print(f"通过: {result.passed}")
    print(f"失败: {result.failed}")
    print(f"警告: {len(result.warnings)}")

    if result.failed > 0:
        print("\n错误详情:")
        for error in result.errors:
            print(f"  - {error}")

    if result.warnings:
        print("\n警告详情:")
        for warning in result.warnings:
            print(f"  - {warning}")

    print(f"\n总三元组数: {total_triplets}")

    if result.failed == 0:
        print("\n✓ 所有验证通过!")
        return 0
    else:
        print("\n✗ 存在错误，请修复后重试")
        return 1


if __name__ == "__main__":
    sys.exit(main())
