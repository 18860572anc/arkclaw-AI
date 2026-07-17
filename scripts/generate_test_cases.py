#!/usr/bin/env python3
"""倍斯特测试数据框架 - 测试用例生成器
为每个场景生成 normal/boundary/exception 三类测试用例
"""

import json
import os
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES_DIR = os.path.join(BASE_DIR, "tests", "cases")

def ensure_dirs():
    for d in ["normal", "boundary", "exception"]:
        os.makedirs(os.path.join(CASES_DIR, d), exist_ok=True)

def generate_normal_cases():
    """正常场景测试用例"""
    cases = []
    # 内容创作场景
    cases.append({"id": "CC-N001", "scene": "内容创作", "name": "小红书海报生成-正常", "input": {"content_type": "poster", "keywords": "共享充电宝 夏日促销", "platform": "xiaohongshu", "brand_style": "科技感"}, "expected": {"output_type": "image", "resolution": ">=1242x1660"}, "type": "normal"})
    cases.append({"id": "CC-N002", "scene": "内容创作", "name": "公众号推文生成-正常", "input": {"content_type": "article", "keywords": "共享充电宝 行业趋势 2026", "platform": "wechat"}, "expected": {"output_type": "text", "word_count": "1500-2000"}, "type": "normal"})
    # 流量监测
    cases.append({"id": "TM-N001", "scene": "流量监测", "name": "单平台数据采集-正常", "input": {"task": "fetch_platform", "platform": "wechat", "time_range": "today"}, "expected": {"has_metrics": True, "fields": ["impressions", "clicks", "gmv"]}, "type": "normal"})
    cases.append({"id": "TM-N002", "scene": "流量监测", "name": "日报生成-正常", "input": {"task": "generate_report", "time_range": "yesterday"}, "expected": {"has_report": True, "platform_count": ">=14"}, "type": "normal"})
    # 竞品分析
    cases.append({"id": "CA-N001", "scene": "竞品分析", "name": "竞品信息采集-正常", "input": {"competitor": "竞品科技A", "dimensions": ["产品规格", "定价"]}, "expected": {"has_data": True, "dimensions_covered": 2}, "type": "normal"})
    # 客服
    cases.append({"id": "CS-N001", "scene": "客服", "name": "FAQ回复-正常", "input": {"query": "产品保修期多久？", "customer_type": "business"}, "expected": {"answer_contains": ["12个月", "保修"]}, "type": "normal"})
    cases.append({"id": "CS-N002", "scene": "客服", "name": "技术问题排查-正常", "input": {"query": "充电宝无法开机怎么办？", "customer_type": "technical"}, "expected": {"answer_contains": ["复位键", "技术支持"]}, "type": "normal"})
    # 销售
    cases.append({"id": "SE-N001", "scene": "销售专家", "name": "客户犹豫场景-正常", "input": {"scenario": "客户犹豫不决", "customer_context": "客户对20000mAh和10000mAh两款犹豫"}, "expected": {"has_advice": True, "contains": ["推荐"]}, "type": "normal"})
    # 客户管理
    cases.append({"id": "CM-N001", "scene": "客户管理", "name": "客户分析-正常", "input": {"task": "analyze_customer", "customer_id": "C0001"}, "expected": {"has_profile": True, "has_analysis": True}, "type": "normal"})
    # 沉睡客户
    cases.append({"id": "DA-N001", "scene": "沉睡客户激活", "name": "沉睡客户识别-正常", "input": {"task": "identify_dormant", "threshold_days": 365}, "expected": {"customer_list": True, "has_dormant": True}, "type": "normal"})
    # 研发服务
    cases.append({"id": "RD-N001", "scene": "研发服务", "name": "产品参数查询-正常", "input": {"query": "C200充电宝的充电协议是什么？"}, "expected": {"answer_contains": ["PD3.0", "QC3.0"]}, "type": "normal"})
    # ODM需求
    cases.append({"id": "ODM-N001", "scene": "ODM需求调研", "name": "需求问卷生成-正常", "input": {"task": "generate_questionnaire", "product_type": "充电宝"}, "expected": {"has_questionnaire": True, "fields_count": ">=5"}, "type": "normal"})
    # 项目管理
    cases.append({"id": "PM-N001", "scene": "项目管理", "name": "全项目看板-正常", "input": {"task": "overview_dashboard"}, "expected": {"has_projects": True, "has_progress": True}, "type": "normal"})
    # 知识库
    cases.append({"id": "KB-N001", "scene": "知识库", "name": "硬件知识检索-正常", "input": {"query": "外壳壁厚应该设计多少？"}, "expected": {"answer_contains": ["2.0", "2.5mm"]}, "type": "normal"})
    # 行政
    cases.append({"id": "AD-N001", "scene": "行政助手", "name": "制度查询-正常", "input": {"query": "年假天数怎么算？"}, "expected": {"answer_contains": ["年假"]}, "type": "normal"})
    # 物料
    cases.append({"id": "MK-N001", "scene": "物料齐套", "name": "BOM欠料查询-正常", "input": {"project_id": "P001"}, "expected": {"has_materials": True, "status_fields": True}, "type": "normal"})
    # 采购
    cases.append({"id": "PR-N001", "scene": "采购分析", "name": "物料需求合并-正常", "input": {"task": "merge_requirements", "orders": ["ORD0001", "ORD0002"]}, "expected": {"has_merged": True, "total_qty": ">0"}, "type": "normal"})

    path = os.path.join(CASES_DIR, "normal", "normal_cases.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"cases": cases, "total": len(cases), "type": "normal"}, f, ensure_ascii=False, indent=2)
    print(f"✅ 正常用例：{path} ({len(cases)}个)")
    return cases

def generate_boundary_cases():
    """边界场景测试用例"""
    cases = [
        {"id": "CC-B001", "scene": "内容创作", "name": "空关键词输入", "input": {"content_type": "poster", "keywords": "", "platform": "xiaohongshu"}, "expected": {"error": True, "message_contains": ["关键词"]}, "type": "boundary"},
        {"id": "CC-B002", "scene": "内容创作", "name": "超长关键词输入(1000字)", "input": {"content_type": "article", "keywords": "空" * 500, "platform": "wechat"}, "expected": {"error": True, "message_contains": ["过长"]}, "type": "boundary"},
        {"id": "TM-B001", "scene": "流量监测", "name": "不支持的平台", "input": {"task": "fetch_platform", "platform": "unknown_platform", "time_range": "today"}, "expected": {"error": True, "code": "PLATFORM_NOT_SUPPORTED"}, "type": "boundary"},
        {"id": "TM-B002", "scene": "流量监测", "name": "空时间范围", "input": {"task": "generate_report", "time_range": ""}, "expected": {"error": True, "message_contains": ["时间范围"]}, "type": "boundary"},
        {"id": "CS-B001", "scene": "客服", "name": "空问题输入", "input": {"query": "", "customer_type": "business"}, "expected": {"error": True, "message_contains": ["问题"]}, "type": "boundary"},
        {"id": "CS-B002", "scene": "客服", "name": "超长问题(5000字)", "input": {"query": "测" * 5000, "customer_type": "technical"}, "expected": {"error": True, "message_contains": ["过长"]}, "type": "boundary"},
        {"id": "DA-B001", "scene": "沉睡客户激活", "name": "阈值为0天", "input": {"task": "identify_dormant", "threshold_days": 0}, "expected": {"error": True, "message_contains": ["阈值"]}, "type": "boundary"},
        {"id": "DA-B002", "scene": "沉睡客户激活", "name": "阈值为负值", "input": {"task": "identify_dormant", "threshold_days": -1}, "expected": {"error": True, "message_contains": ["无效"]}, "type": "boundary"},
        {"id": "ODM-B001", "scene": "ODM需求调研", "name": "空产品类型", "input": {"task": "generate_questionnaire", "product_type": ""}, "expected": {"error": True, "message_contains": ["产品类型"]}, "type": "boundary"},
        {"id": "PM-B001", "scene": "项目管理", "name": "不存在的项目ID", "input": {"task": "gantt_chart", "project_id": "NONEXIST"}, "expected": {"error": True, "code": "PROJECT_NOT_FOUND"}, "type": "boundary"},
        {"id": "KB-B001", "scene": "知识库", "name": "不存在的查询内容", "input": {"query": "aksjdhflaksjdhflaksjdhf"}, "expected": {"error": True, "message_contains": ["未找到"]}, "type": "boundary"},
        {"id": "MK-B001", "scene": "物料齐套", "name": "不存在的项目ID", "input": {"project_id": "INVALID001"}, "expected": {"error": True, "code": "PROJECT_NOT_FOUND"}, "type": "boundary"},
    ]
    path = os.path.join(CASES_DIR, "boundary", "boundary_cases.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"cases": cases, "total": len(cases), "type": "boundary"}, f, ensure_ascii=False, indent=2)
    print(f"✅ 边界用例：{path} ({len(cases)}个)")
    return cases

def generate_exception_cases():
    """异常场景测试用例"""
    cases = [
        {"id": "CC-E001", "scene": "内容创作", "name": "AI服务超时", "input": {"content_type": "poster", "keywords": "测试", "platform": "xiaohongshu"}, "mock_scenario": "api_timeout", "expected": {"error": True, "code": "SERVICE_TIMEOUT", "fallback": "请稍后重试"}, "type": "exception"},
        {"id": "CC-E002", "scene": "内容创作", "name": "图片生成失败", "input": {"content_type": "poster", "keywords": "测试", "platform": "xiaohongshu"}, "mock_scenario": "generate_failure", "expected": {"error": True, "code": "GENERATION_FAILED", "fallback": "请检查参数后重试"}, "type": "exception"},
        {"id": "TM-E001", "scene": "流量监测", "name": "平台API不可用", "input": {"task": "fetch_platform", "platform": "wechat", "time_range": "today"}, "mock_scenario": "api_unavailable", "expected": {"error": True, "code": "API_UNAVAILABLE", "fallback": "使用缓存数据"}, "type": "exception"},
        {"id": "CS-E001", "scene": "客服", "name": "知识库无匹配", "input": {"query": "一个非常特殊的问题没有任何匹配", "customer_type": "technical"}, "mock_scenario": "no_match", "expected": {"error": False, "fallback": "转人工"}, "type": "exception"},
        {"id": "DA-E001", "scene": "沉睡客户激活", "name": "黑云系统不可用", "input": {"task": "identify_dormant", "threshold_days": 365}, "mock_scenario": "heiyun_down", "expected": {"error": True, "code": "DATA_SOURCE_UNAVAILABLE", "fallback": "使用缓存数据"}, "type": "exception"},
        {"id": "MK-E001", "scene": "物料齐套", "name": "BOM数据格式异常", "input": {"project_id": "P001"}, "mock_scenario": "data_format_error", "expected": {"error": True, "code": "DATA_FORMAT_ERROR", "fallback": "请检查数据源"}, "type": "exception"},
        {"id": "PR-E001", "scene": "采购分析", "name": "库存数据缺失", "input": {"task": "merge_requirements", "orders": ["ORD0001"]}, "mock_scenario": "missing_inventory", "expected": {"error": False, "warning": "部分库存数据缺失", "fallback": "使用预估数据"}, "type": "exception"},
        {"id": "PM-E001", "scene": "项目管理", "name": "并发更新冲突", "input": {"task": "update_progress", "project_id": "P001", "progress": 50}, "mock_scenario": "concurrent_update", "expected": {"error": True, "code": "CONCURRENT_UPDATE", "fallback": "刷新后重试"}, "type": "exception"},
    ]
    path = os.path.join(CASES_DIR, "exception", "exception_cases.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"cases": cases, "total": len(cases), "type": "exception"}, f, ensure_ascii=False, indent=2)
    print(f"✅ 异常用例：{path} ({len(cases)}个)")
    return cases

def main():
    ensure_dirs()
    normal = generate_normal_cases()
    boundary = generate_boundary_cases()
    exception = generate_exception_cases()
    total = len(normal) + len(boundary) + len(exception)
    print(f"\n🎯 测试用例生成完成！共 {total} 个用例（正常{len(normal)}/边界{len(boundary)}/异常{len(exception)})")

if __name__ == "__main__":
    main()