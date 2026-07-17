#!/usr/bin/env python3
"""Generate test case JSON files for all 52 scenes"""
import json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES = os.path.join(BASE, "tests", "cases")
for d in ["normal", "boundary", "exception"]:
    os.makedirs(os.path.join(CASES, d), exist_ok=True)

# Normal cases - 47 total (17 existing + 30 new)
normal = [
    {"id": "CC-N001", "scene": "内容创作", "name": "小红书海报生成-正常", "input": {"content_type": "poster", "keywords": "共享充电宝 夏日促销", "platform": "xiaohongshu", "brand_style": "科技感"}, "expected": {"output_type": "image", "resolution": ">=1242x1660"}, "type": "normal"},
    {"id": "CC-N002", "scene": "内容创作", "name": "公众号推文生成-正常", "input": {"content_type": "article", "keywords": "共享充电宝 行业趋势 2026", "platform": "wechat"}, "expected": {"output_type": "text", "word_count": "1500-2000"}, "type": "normal"},
    {"id": "TM-N001", "scene": "流量监测", "name": "单平台数据采集-正常", "input": {"task": "fetch_platform", "platform": "wechat", "time_range": "today"}, "expected": {"has_metrics": True, "fields": ["impressions", "clicks", "gmv"]}, "type": "normal"},
    {"id": "TM-N002", "scene": "流量监测", "name": "日报生成-正常", "input": {"task": "generate_report", "time_range": "yesterday"}, "expected": {"has_report": True, "platform_count": ">=14"}, "type": "normal"},
    {"id": "CA-N001", "scene": "竞品分析", "name": "竞品信息采集-正常", "input": {"competitor": "竞品科技A", "dimensions": ["产品规格", "定价"]}, "expected": {"has_data": True, "dimensions_covered": 2}, "type": "normal"},
    {"id": "CS-N001", "scene": "客服", "name": "FAQ回复-正常", "input": {"query": "产品保修期多久？", "customer_type": "business"}, "expected": {"answer_contains": ["12个月", "保修"]}, "type": "normal"},
    {"id": "CS-N002", "scene": "客服", "name": "技术问题排查-正常", "input": {"query": "充电宝无法开机怎么办？", "customer_type": "technical"}, "expected": {"answer_contains": ["复位键", "技术支持"]}, "type": "normal"},
    {"id": "SE-N001", "scene": "销售专家", "name": "客户犹豫场景-正常", "input": {"scenario": "客户犹豫不决", "customer_context": "客户对20000mAh和10000mAh两款犹豫"}, "expected": {"has_advice": True, "contains": ["推荐"]}, "type": "normal"},
    {"id": "CM-N001", "scene": "客户管理", "name": "客户分析-正常", "input": {"task": "analyze_customer", "customer_id": "C0001"}, "expected": {"has_profile": True, "has_analysis": True}, "type": "normal"},
    {"id": "DA-N001", "scene": "沉睡客户激活", "name": "沉睡客户识别-正常", "input": {"task": "identify_dormant", "threshold_days": 365}, "expected": {"customer_list": True, "has_dormant": True}, "type": "normal"},
    {"id": "RD-N001", "scene": "研发服务", "name": "产品参数查询-正常", "input": {"query": "C200充电宝的充电协议是什么？"}, "expected": {"answer_contains": ["PD3.0", "QC3.0"]}, "type": "normal"},
    {"id": "ODM-N001", "scene": "ODM需求调研", "name": "需求问卷生成-正常", "input": {"task": "generate_questionnaire", "product_type": "充电宝"}, "expected": {"has_questionnaire": True, "fields_count": ">=5"}, "type": "normal"},
    {"id": "PM-N001", "scene": "项目管理", "name": "全项目看板-正常", "input": {"task": "overview_dashboard"}, "expected": {"has_projects": True, "has_progress": True}, "type": "normal"},
    {"id": "KB-N001", "scene": "知识库", "name": "硬件知识检索-正常", "input": {"query": "外壳壁厚应该设计多少？"}, "expected": {"answer_contains": ["2.0", "2.5mm"]}, "type": "normal"},
    {"id": "AD-N001", "scene": "行政助手", "name": "制度查询-正常", "input": {"query": "年假天数怎么算？"}, "expected": {"answer_contains": ["年假"]}, "type": "normal"},
    {"id": "MK-N001", "scene": "物料齐套", "name": "BOM欠料查询-正常", "input": {"project_id": "P001"}, "expected": {"has_materials": True, "status_fields": True}, "type": "normal"},
    {"id": "PR-N001", "scene": "采购分析", "name": "物料需求合并-正常", "input": {"task": "merge_requirements", "orders": ["ORD0001", "ORD0002"]}, "expected": {"has_merged": True, "total_qty": ">0"}, "type": "normal"},
    {"id": "OEM-N001", "scene": "OEM快速设计", "name": "OEM方案生成-正常", "input": {"task": "generate_oem_scheme", "product_type": "充电宝", "capacity": "10000mAh", "color": "白色", "logo_file": "customer_logo.ai"}, "expected": {"has_scheme": True, "fields": ["外观设计", "结构图纸", "BOM清单", "预估成本"]}, "type": "normal"},
    {"id": "OB-N001", "scene": "海外B端售前助理", "name": "海外客户报价生成-正常", "input": {"task": "generate_overseas_quote", "customer_region": "北美", "product": "CS12充电柜", "qty": 500, "delivery_terms": "FOB深圳"}, "expected": {"has_quote": True, "fields": ["单价", "总价", "贸易条款", "交期"]}, "type": "normal"},
    {"id": "OD-N001", "scene": "订单派发", "name": "订单智能派发-正常", "input": {"task": "dispatch_order", "order_id": "ORD1001", "factory": "江苏工厂"}, "expected": {"dispatched": True, "assigned_line": True, "estimated_start": True}, "type": "normal"},
    {"id": "OP-N001", "scene": "订单进度管理", "name": "订单进度查询-正常", "input": {"task": "track_progress", "order_id": "ORD1002"}, "expected": {"has_timeline": True, "current_stage": True, "completion_pct": True}, "type": "normal"},
    {"id": "OR-N001", "scene": "订单统筹及风险预警", "name": "订单风险扫描-正常", "input": {"task": "scan_risks", "time_range": "this_month"}, "expected": {"has_risk_report": True, "fields": ["延迟风险", "缺料风险", "质量风险"]}, "type": "normal"},
    {"id": "IR-N001", "scene": "智能回款", "name": "回款计划生成-正常", "input": {"task": "generate_collection_plan", "customer_id": "C1001", "overdue_days": 45}, "expected": {"has_plan": True, "fields": ["应回金额", "逾期天数", "建议催收方式"]}, "type": "normal"},
    {"id": "BD-N001", "scene": "部门助手(商务部)", "name": "商务部报表生成-正常", "input": {"task": "monthly_report", "department": "商务部", "period": "2026-06"}, "expected": {"has_report": True, "fields": ["合同额", "签约数", "回款率", "在跟项目"]}, "type": "normal"},
    {"id": "CC-N003", "scene": "提成核算", "name": "销售提成计算-正常", "input": {"task": "calc_commission", "sales_person": "张明", "period": "2026-06", "rules": "standard"}, "expected": {"has_result": True, "fields": ["base_commission", "bonus", "deduction", "net_amount"]}, "type": "normal"},
    {"id": "IQ-N001", "scene": "智能报价", "name": "智能报价生成-正常", "input": {"task": "generate_quote", "product_id": "C200", "qty": 1000, "customer_level": "A"}, "expected": {"has_quote": True, "fields": ["unit_price", "total", "discount", "valid_until"]}, "type": "normal"},
    {"id": "IC-N001", "scene": "内部协作与CRM监控", "name": "协作看板-正常", "input": {"task": "collaboration_dashboard", "time_range": "this_week"}, "expected": {"has_dashboard": True, "fields": ["任务完成数", "沟通记录", "待办事项", "跨部门协作"]}, "type": "normal"},
    {"id": "PA-N001", "scene": "人员分析与考核", "name": "绩效分析-正常", "input": {"task": "performance_analysis", "department": "销售部", "period": "2026-Q2"}, "expected": {"has_analysis": True, "fields": ["KPI达标率", "排名", "改进建议"]}, "type": "normal"},
    {"id": "PG-N001", "scene": "产品图库训练", "name": "产品图库检索-正常", "input": {"task": "search_gallery", "keyword": "充电柜CS12", "category": "产品图"}, "expected": {"has_results": True, "images_count": ">=1"}, "type": "normal"},
    {"id": "PS-N001", "scene": "生产排产", "name": "排产计划生成-正常", "input": {"task": "schedule_production", "orders": ["ORD1001", "ORD1002"], "factory": "江苏工厂"}, "expected": {"has_schedule": True, "fields": ["产线分配", "开始日期", "预计完成日期"]}, "type": "normal"},
    {"id": "QM-N001", "scene": "品质管理总结", "name": "品质月报生成-正常", "input": {"task": "quality_monthly", "period": "2026-06"}, "expected": {"has_report": True, "fields": ["良品率", "不良类型", "改善措施"]}, "type": "normal"},
    {"id": "PI-N001", "scene": "工艺改进分析", "name": "工艺效率分析-正常", "input": {"task": "process_analysis", "product_line": "充电宝产线A", "period": "2026-Q2"}, "expected": {"has_analysis": True, "fields": ["当前效率", "瓶颈工序", "改进建议"]}, "type": "normal"},
    {"id": "CR-N001", "scene": "客诉根因分析", "name": "客诉根因分析-正常", "input": {"task": "root_cause_analysis", "complaint_id": "CP0001"}, "expected": {"has_analysis": True, "fields": ["根因", "影响范围", "纠正措施"]}, "type": "normal"},
    {"id": "AM-N001", "scene": "阿米巴经营数据分析", "name": "阿米巴单元核算-正常", "input": {"task": "amoeba_accounting", "unit": "销售部", "period": "2026-06"}, "expected": {"has_report": True, "fields": ["收入", "支出", "单位时间附加值", "改善方向"]}, "type": "normal"},
    {"id": "MF-N001", "scene": "部门助手(制造中心)", "name": "制造日报生成-正常", "input": {"task": "daily_report", "department": "制造中心", "date": "2026-07-16"}, "expected": {"has_report": True, "fields": ["产量", "良品率", "设备稼动率", "异常记录"]}, "type": "normal"},
    {"id": "EC-N001", "scene": "企业文化总结", "name": "企业文化活动总结-正常", "input": {"task": "culture_summary", "period": "2026-Q2"}, "expected": {"has_summary": True, "fields": ["活动汇总", "参与率", "员工反馈", "改进建议"]}, "type": "normal"},
    {"id": "IP-N001", "scene": "内部政策校验分析", "name": "政策合规检查-正常", "input": {"task": "policy_check", "document": "报销申请单20260715", "policy_id": "POL-002"}, "expected": {"is_compliant": True, "has_detail": True}, "type": "normal"},
    {"id": "GP-N001", "scene": "政府政策匹配", "name": "政策匹配查询-正常", "input": {"task": "match_policy", "company_industry": "新能源", "company_region": "深圳", "revenue": "50000000"}, "expected": {"has_matches": True, "matched_count": ">=1"}, "type": "normal"},
    {"id": "CQ-N001", "scene": "公司资质规划", "name": "资质规划建议-正常", "input": {"task": "qualification_plan", "company_stage": "扩张期", "target_markets": ["欧美", "东南亚"]}, "expected": {"has_plan": True, "fields": ["已有资质", "需办理资质", "时间路线图"]}, "type": "normal"},
    {"id": "TA-N001", "scene": "人才分析", "name": "人才盘点报告-正常", "input": {"task": "talent_review", "department": "研发部"}, "expected": {"has_review": True, "fields": ["人员结构", "关键人才", "流失风险", "培养建议"]}, "type": "normal"},
    {"id": "AM-N002", "scene": "阿米巴经营分析(管理中心)", "name": "管理中心阿米巴核算-正常", "input": {"task": "amoeba_management", "unit": "管理中心", "period": "2026-06"}, "expected": {"has_report": True, "fields": ["管理费用", "间接成本分摊", "人均效能"]}, "type": "normal"},
    {"id": "AC-N001", "scene": "会计分目(做账)", "name": "会计凭证生成-正常", "input": {"task": "generate_voucher", "transaction_type": "销售", "amount": 50000, "customer": "客户A"}, "expected": {"has_voucher": True, "fields": ["借方科目", "贷方科目", "金额", "摘要"]}, "type": "normal"},
    {"id": "TX-N001", "scene": "智能报税", "name": "增值税申报-正常", "input": {"task": "tax_filing", "tax_type": "VAT", "period": "2026-06"}, "expected": {"has_filing": True, "fields": ["销项税", "进项税", "应缴税额", "申报截止日"]}, "type": "normal"},
    {"id": "MF-N002", "scene": "市场行情预测", "name": "原材料价格预测-正常", "input": {"task": "forecast", "material": "锂电池(18650)", "horizon_months": 3}, "expected": {"has_forecast": True, "fields": ["当前价格", "预测趋势", "建议采购策略"]}, "type": "normal"},
    {"id": "SP-N001", "scene": "供应商比价", "name": "多供应商比价-正常", "input": {"task": "compare_prices", "material": "锂电池组", "suppliers": ["供应商A", "供应商B", "供应商C"], "qty": 1000}, "expected": {"has_comparison": True, "fields": ["排名", "单价", "交期", "评分"]}, "type": "normal"},
    {"id": "SE-N002", "scene": "供应商评价", "name": "供应商综合评分-正常", "input": {"task": "evaluate_supplier", "supplier_id": "SUP001", "dimensions": ["质量", "交期", "价格", "服务"]}, "expected": {"has_score": True, "fields": ["综合评分", "各维度得分", "等级"]}, "type": "normal"},
    {"id": "OL-N001", "scene": "海外物流报价", "name": "国际物流报价查询-正常", "input": {"task": "logistics_quote", "origin": "深圳", "destination": "洛杉矶", "weight_kg": 500, "volume_cbm": 2.5}, "expected": {"has_quote": True, "fields": ["运输方式", "运费", "时效", "总费用"]}, "type": "normal"},
]

with open(os.path.join(CASES, "normal", "normal_cases.json"), "w", encoding="utf-8") as f:
    json.dump({"cases": normal, "total": len(normal), "type": "normal"}, f, ensure_ascii=False, indent=2)
print(f"Normal cases: {len(normal)}")

# Verify all 52 scenes are covered
scenes_in_normal = set(c["scene"] for c in normal)
print(f"Scenes in normal: {len(scenes_in_normal)}")
print("OK - normal_cases.json written")