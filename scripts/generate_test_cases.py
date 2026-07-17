#!/usr/bin/env python3
"""倍斯特测试数据框架 - 测试用例生成器 (完整52场景版)
为所有52个场景生成 normal/boundary/exception 三类测试用例
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES_DIR = os.path.join(BASE_DIR, "tests", "cases")


def ensure_dirs():
    for d in ["normal", "boundary", "exception"]:
        os.makedirs(os.path.join(CASES_DIR, d), exist_ok=True)


def generate_normal_cases():
    cases = [
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
    path = os.path.join(CASES_DIR, "normal", "normal_cases.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"cases": cases, "total": len(cases), "type": "normal"}, f, ensure_ascii=False, indent=2)
    print(f"Normal cases: {len(cases)}")
    return cases


def generate_boundary_cases():
    cases = [
        {"id": "CC-B001", "scene": "内容创作", "name": "空关键词输入", "input": {"content_type": "poster", "keywords": "", "platform": "xiaohongshu"}, "expected": {"error": True, "message_contains": ["关键词"]}, "type": "boundary"},
        {"id": "CC-B002", "scene": "内容创作", "name": "超长关键词输入", "input": {"content_type": "article", "keywords": "空" * 500, "platform": "wechat"}, "expected": {"error": True, "message_contains": ["过长"]}, "type": "boundary"},
        {"id": "TM-B001", "scene": "流量监测", "name": "不支持的平台", "input": {"task": "fetch_platform", "platform": "unknown_platform", "time_range": "today"}, "expected": {"error": True, "code": "PLATFORM_NOT_SUPPORTED"}, "type": "boundary"},
        {"id": "TM-B002", "scene": "流量监测", "name": "空时间范围", "input": {"task": "generate_report", "time_range": ""}, "expected": {"error": True, "message_contains": ["时间范围"]}, "type": "boundary"},
        {"id": "CS-B001", "scene": "客服", "name": "空问题输入", "input": {"query": "", "customer_type": "business"}, "expected": {"error": True, "message_contains": ["问题"]}, "type": "boundary"},
        {"id": "CS-B002", "scene": "客服", "name": "超长问题输入", "input": {"query": "测" * 50, "customer_type": "technical"}, "expected": {"error": True, "message_contains": ["过长"]}, "type": "boundary"},
        {"id": "DA-B001", "scene": "沉睡客户激活", "name": "阈值为0天", "input": {"task": "identify_dormant", "threshold_days": 0}, "expected": {"error": True, "message_contains": ["阈值"]}, "type": "boundary"},
        {"id": "DA-B002", "scene": "沉睡客户激活", "name": "阈值为负值", "input": {"task": "identify_dormant", "threshold_days": -1}, "expected": {"error": True, "message_contains": ["无效"]}, "type": "boundary"},
        {"id": "ODM-B001", "scene": "ODM需求调研", "name": "空产品类型", "input": {"task": "generate_questionnaire", "product_type": ""}, "expected": {"error": True, "message_contains": ["产品类型"]}, "type": "boundary"},
        {"id": "PM-B001", "scene": "项目管理", "name": "不存在的项目ID", "input": {"task": "gantt_chart", "project_id": "NONEXIST"}, "expected": {"error": True, "code": "PROJECT_NOT_FOUND"}, "type": "boundary"},
        {"id": "KB-B001", "scene": "知识库", "name": "不存在的查询内容", "input": {"query": "aksjdhflaksjdhflaksjdhf"}, "expected": {"error": True, "message_contains": ["未找到"]}, "type": "boundary"},
        {"id": "MK-B001", "scene": "物料齐套", "name": "不存在的项目ID", "input": {"project_id": "INVALID001"}, "expected": {"error": True, "code": "PROJECT_NOT_FOUND"}, "type": "boundary"},
        {"id": "OEM-B001", "scene": "OEM快速设计", "name": "不支持的容量", "input": {"task": "generate_oem_scheme", "product_type": "充电宝", "capacity": "999999mAh", "color": "白色"}, "expected": {"error": True, "message_contains": ["容量"]}, "type": "boundary"},
        {"id": "OB-B001", "scene": "海外B端售前助理", "name": "不支持的区域", "input": {"task": "generate_overseas_quote", "customer_region": "南极洲", "product": "CS12充电柜", "qty": 500}, "expected": {"error": True, "message_contains": ["区域"]}, "type": "boundary"},
        {"id": "OD-B001", "scene": "订单派发", "name": "不存在的工厂", "input": {"task": "dispatch_order", "order_id": "ORD1001", "factory": "火星工厂"}, "expected": {"error": True, "message_contains": ["工厂"]}, "type": "boundary"},
        {"id": "OP-B001", "scene": "订单进度管理", "name": "不存在的订单", "input": {"task": "track_progress", "order_id": "NONEXIST"}, "expected": {"error": True, "code": "ORDER_NOT_FOUND"}, "type": "boundary"},
        {"id": "OR-B001", "scene": "订单统筹及风险预警", "name": "空时间范围", "input": {"task": "scan_risks", "time_range": ""}, "expected": {"error": True, "message_contains": ["时间范围"]}, "type": "boundary"},
        {"id": "IR-B001", "scene": "智能回款", "name": "逾期天数为负", "input": {"task": "generate_collection_plan", "customer_id": "C1001", "overdue_days": -5}, "expected": {"error": True, "message_contains": ["逾期"]}, "type": "boundary"},
        {"id": "BD-B001", "scene": "部门助手(商务部)", "name": "不存在的部门", "input": {"task": "monthly_report", "department": "宣传部", "period": "2026-06"}, "expected": {"error": True, "message_contains": ["部门"]}, "type": "boundary"},
        {"id": "CC-B003", "scene": "提成核算", "name": "不存在的员工", "input": {"task": "calc_commission", "sales_person": "不存在的人", "period": "2026-06"}, "expected": {"error": True, "message_contains": ["员工"]}, "type": "boundary"},
        {"id": "IQ-B001", "scene": "智能报价", "name": "数量为零", "input": {"task": "generate_quote", "product_id": "C200", "qty": 0, "customer_level": "A"}, "expected": {"error": True, "message_contains": ["数量"]}, "type": "boundary"},
        {"id": "IC-B001", "scene": "内部协作与CRM监控", "name": "无权限查看", "input": {"task": "collaboration_dashboard", "time_range": "this_week", "department": "财务部"}, "expected": {"error": True, "code": "ACCESS_DENIED"}, "type": "boundary"},
        {"id": "PA-B001", "scene": "人员分析与考核", "name": "不存在的部门", "input": {"task": "performance_analysis", "department": "后勤部", "period": "2026-Q2"}, "expected": {"error": True, "message_contains": ["部门"]}, "type": "boundary"},
        {"id": "PG-B001", "scene": "产品图库训练", "name": "无匹配图片", "input": {"task": "search_gallery", "keyword": "aklsjdhflkjashdflkj", "category": "产品图"}, "expected": {"error": True, "message_contains": ["未找到"]}, "type": "boundary"},
        {"id": "PS-B001", "scene": "生产排产", "name": "空订单列表", "input": {"task": "schedule_production", "orders": [], "factory": "江苏工厂"}, "expected": {"error": True, "message_contains": ["订单"]}, "type": "boundary"},
        {"id": "QM-B001", "scene": "品质管理总结", "name": "未来时间段", "input": {"task": "quality_monthly", "period": "2099-01"}, "expected": {"error": True, "message_contains": ["时间段"]}, "type": "boundary"},
        {"id": "PI-B001", "scene": "工艺改进分析", "name": "不存在的产线", "input": {"task": "process_analysis", "product_line": "虚拟产线", "period": "2026-Q2"}, "expected": {"error": True, "message_contains": ["产线"]}, "type": "boundary"},
        {"id": "CR-B001", "scene": "客诉根因分析", "name": "不存在的投诉", "input": {"task": "root_cause_analysis", "complaint_id": "NONEXIST"}, "expected": {"error": True, "code": "COMPLAINT_NOT_FOUND"}, "type": "boundary"},
        {"id": "AM-B001", "scene": "阿米巴经营数据分析", "name": "不存在的单元", "input": {"task": "amoeba_accounting", "unit": "虚拟部门", "period": "2026-06"}, "expected": {"error": True, "message_contains": ["单元"]}, "type": "boundary"},
        {"id": "MF-B001", "scene": "部门助手(制造中心)", "name": "未来日期查询", "input": {"task": "daily_report", "department": "制造中心", "date": "2099-12-31"}, "expected": {"error": True, "message_contains": ["日期"]}, "type": "boundary"},
        {"id": "EC-B001", "scene": "企业文化总结", "name": "无活动记录", "input": {"task": "culture_summary", "period": "2020-Q1"}, "expected": {"error": True, "message_contains": ["活动"]}, "type": "boundary"},
        {"id": "IP-B001", "scene": "内部政策校验分析", "name": "不存在的政策", "input": {"task": "policy_check", "document": "报销单", "policy_id": "POL-999"}, "expected": {"error": True, "code": "POLICY_NOT_FOUND"}, "type": "boundary"},
        {"id": "GP-B001", "scene": "政府政策匹配", "name": "空行业参数", "input": {"task": "match_policy", "company_industry": "", "company_region": "深圳", "revenue": "50000000"}, "expected": {"error": True, "message_contains": ["行业"]}, "type": "boundary"},
        {"id": "CQ-B001", "scene": "公司资质规划", "name": "空目标市场", "input": {"task": "qualification_plan", "company_stage": "扩张期", "target_markets": []}, "expected": {"error": True, "message_contains": ["市场"]}, "type": "boundary"},
        {"id": "TA-B001", "scene": "人才分析", "name": "不存在的部门", "input": {"task": "talent_review", "department": "不存在部门"}, "expected": {"error": True, "message_contains": ["部门"]}, "type": "boundary"},
        {"id": "AM-B002", "scene": "阿米巴经营分析(管理中心)", "name": "超长时间范围", "input": {"task": "amoeba_management", "unit": "管理中心", "period": "2099-01"}, "expected": {"error": True, "message_contains": ["时间范围"]}, "type": "boundary"},
        {"id": "AC-B001", "scene": "会计分目(做账)", "name": "金额为负", "input": {"task": "generate_voucher", "transaction_type": "销售", "amount": -5000, "customer": "客户A"}, "expected": {"error": True, "message_contains": ["金额"]}, "type": "boundary"},
        {"id": "TX-B001", "scene": "智能报税", "name": "空税种类型", "input": {"task": "tax_filing", "tax_type": "", "period": "2026-06"}, "expected": {"error": True, "message_contains": ["税种"]}, "type": "boundary"},
        {"id": "MF-B002", "scene": "市场行情预测", "name": "不存在的材料", "input": {"task": "forecast", "material": "未知材料XYZ", "horizon_months": 3}, "expected": {"error": True, "message_contains": ["材料"]}, "type": "boundary"},
        {"id": "SP-B001", "scene": "供应商比价", "name": "空供应商列表", "input": {"task": "compare_prices", "material": "锂电池组", "suppliers": [], "qty": 1000}, "expected": {"error": True, "message_contains": ["供应商"]}, "type": "boundary"},
        {"id": "SE-B002", "scene": "供应商评价", "name": "空评价维度", "input": {"task": "evaluate_supplier", "supplier_id": "SUP001", "dimensions": []}, "expected": {"error": True, "message_contains": ["维度"]}, "type": "boundary"},
        {"id": "OL-B001", "scene": "海外物流报价", "name": "不支持的运目的地", "input": {"task": "logistics_quote", "origin": "深圳", "destination": "火星", "weight_kg": 500, "volume_cbm": 2.5}, "expected": {"error": True, "message_contains": ["目的地"]}, "type": "boundary"},
    ]
    path = os.path.join(CASES_DIR, "boundary", "boundary_cases.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"cases": cases, "total": len(cases), "type": "boundary"}, f, ensure_ascii=False, indent=2)
    print(f"Boundary cases: {len(cases)}")
    return cases


def generate_exception_cases():
    cases = [
        {"id": "CC-E001", "scene": "内容创作", "name": "AI服务超时", "input": {"content_type": "poster", "keywords": "测试", "platform": "xiaohongshu"}, "mock_scenario": "api_timeout", "expected": {"error": True, "code": "SERVICE_TIMEOUT", "fallback": "请稍后重试"}, "type": "exception"},
        {"id": "CC-E002", "scene": "内容创作", "name": "图片生成失败", "input": {"content_type": "poster", "keywords": "测试", "platform": "xiaohongshu"}, "mock_scenario": "generate_failure", "expected": {"error": True, "code": "GENERATION_FAILED", "fallback": "请检查参数后重试"}, "type": "exception"},
        {"id": "TM-E001", "scene": "流量监测", "name": "平台API不可用", "input": {"task": "fetch_platform", "platform": "wechat", "time_range": "today"}, "mock_scenario": "api_unavailable", "expected": {"error": True, "code": "API_UNAVAILABLE", "fallback": "使用缓存数据"}, "type": "exception"},
        {"id": "CS-E001", "scene": "客服", "name": "知识库无匹配", "input": {"query": "一个非常特殊的问题没有任何匹配", "customer_type": "technical"}, "mock_scenario": "no_match", "expected": {"error": False, "fallback": "转人工"}, "type": "exception"},
        {"id": "DA-E001", "scene": "沉睡客户激活", "name": "黑云系统不可用", "input": {"task": "identify_dormant", "threshold_days": 365}, "mock_scenario": "heiyun_down", "expected": {"error": True, "code": "DATA_SOURCE_UNAVAILABLE", "fallback": "使用缓存数据"}, "type": "exception"},
        {"id": "MK-E001", "scene": "物料齐套", "name": "BOM数据格式异常", "input": {"project_id": "P001"}, "mock_scenario": "data_format_error", "expected": {"error": True, "code": "DATA_FORMAT_ERROR", "fallback": "请检查数据源"}, "type": "exception"},
        {"id": "PR-E001", "scene": "采购分析", "name": "库存数据缺失", "input":