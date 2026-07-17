#!/usr/bin/env python3
"""倍斯特测试数据框架 - 源数据生成器 (完整版)
生成公司信息、FAQ、话术模板、品牌调性、知识库、制度政策等源数据
"""

import json
import os
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(BASE_DIR, "data", "source")

def ensure_dirs():
    for d in ["company", "faq", "templates", "references", "policies"]:
        os.makedirs(os.path.join(SOURCE_DIR, d), exist_ok=True)

def generate_company():
    data = {
        "name": "倍斯特科技股份有限公司",
        "founded_year": 2008,
        "founded_date": "2008-05-27",
        "industry": "共享充电宝/充电柜研发制造",
        "employees": 500,
        "offices": ["深圳总部", "江苏工厂", "广西工厂"],
        "products": [
            {"name": "C100充电宝", "capacity": "10000mAh", "output": "5V/2A", "protocol": "QC3.0", "weight": "200g", "waterproof": "IPX4"},
            {"name": "C200充电宝", "capacity": "20000mAh", "output": "5V/3A", "protocol": "QC3.0+PD3.0", "weight": "350g", "waterproof": "IPX4"},
            {"name": "CS12充电柜", "capacity": "12槽位", "input": "AC 220V", "output": "5V/2A per port", "dimensions": "600x400x1800mm"},
            {"name": "CS24充电柜", "capacity": "24槽位", "input": "AC 220V", "output": "5V/2A per port", "dimensions": "800x500x1800mm"},
            {"name": "CS36充电柜", "capacity": "36槽位", "input": "AC 380V", "output": "5V/2A per port", "dimensions": "1000x600x1800mm"},
        ],
        "milestones": [
            {"year": 2008, "event": "倍斯特在深圳成立"},
            {"year": 2015, "event": "推出第一代共享充电宝产品"},
            {"year": 2018, "event": "年出货量突破100万台"},
            {"year": 2020, "event": "进入海外市场, 覆盖欧美东南亚"},
            {"year": 2022, "event": "建立江苏工厂, 年产能提升至500万台"},
            {"year": 2024, "event": "与ArkClaw达成战略合作, 启动AI数字化升级"},
            {"year": 2025, "event": "建立广西工厂, 拓展新能源电池领域"},
        ],
        "culture": "创新, 务实, 客户至上",
        "brand_guide": {
            "primary_color": "#1A73E8",
            "secondary_color": "#00C853",
            "accent_color": "#FF6D00",
            "font_title": "思源黑体 Bold",
            "font_body": "思源黑体 Regular",
            "font_en": "Inter",
            "design_style": "简洁干净, 圆角元素, 图标化表达",
        }
    }
    path = os.path.join(SOURCE_DIR, "company", "company_info.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Company info: {path}")

def generate_faq():
    faq = [
        {"question": "产品保修期多久?", "answer": "标准保修期为12个月, 从发货之日起计算. 可延长至24个月.", "category": "after_sale", "tags": ["保修", "售后"]},
        {"question": "充电宝无法开机怎么办?", "answer": "1.检查电源连接 2.确认电池电量 3.长按复位键10秒 4.如仍无法开机请联系技术支持", "category": "tech", "tags": ["故障排查", "开机"]},
        {"question": "充电速度慢的原因?", "answer": "1.检查充电线缆是否完好 2.确认设备温度是否过高 3.检查输出端口是否清洁", "category": "tech", "tags": ["充电慢", "故障"]},
        {"question": "产品防水等级是多少?", "answer": "标准产品防水等级为IPX4, 可防溅水. 如需更高防水等级可定制.", "category": "product", "tags": ["防水", "规格"]},
        {"question": "支持哪些充电协议?", "answer": "支持QC3.0, PD3.0, AFC, FCP等主流快充协议", "category": "product", "tags": ["快充", "协议"]},
        {"question": "最小起订量是多少?", "answer": "标准产品MOQ为100台, 定制产品MOQ为500台", "category": "sales", "tags": ["MOQ", "订购"]},
        {"question": "定制产品需要多长时间?", "answer": "ODM定制周期一般为45-60天, 含设计评审, 开模, 打样, 试产, 量产", "category": "sales", "tags": ["定制", "周期"]},
        {"question": "海外订单如何发货?", "answer": "支持FOB深圳, CIF主要港口, DDP等多种贸易条款, 海运周期约20-35天", "category": "sales", "tags": ["海外", "物流"]},
        {"question": "充电柜的安装要求?", "answer": "需AC 220V电源, 接地良好, 安装环境温度0-40度, 避免阳光直射和潮湿环境", "category": "tech", "tags": ["安装", "充电柜"]},
        {"question": "产品通过哪些认证?", "answer": "CE, FCC, RoHS, UN38.3", "category": "product", "tags": ["认证", "合规"]},
    ]
    path = os.path.join(SOURCE_DIR, "faq", "faq_data.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"faq": faq}, f, ensure_ascii=False, indent=2)
    print(f"FAQ: {path} ({len(faq)}条)")

def generate_templates():
    templates = {
        "communication": [
            {"type": "greeting", "tone": "formal", "text": "您好! 欢迎咨询倍斯特, 请问有什么可以帮您?"},
            {"type": "greeting", "tone": "casual", "text": "嗨! 感谢关注倍斯特, 有什么需要了解的?"},
            {"type": "apology", "text": "非常抱歉给您带来不便, 我们正在为您加急处理, 预计{time}内回复."},
            {"type": "escalation", "text": "这个问题我需要转给技术支持同事处理, 请稍等, 他们会尽快联系您."},
            {"type": "closing", "text": "感谢您的咨询, 如有其他问题随时联系我们! 祝您生活愉快!"},
            {"type": "price_objection", "text": "我理解您对价格的关注. 其实我们的产品采用{feature}技术, 相比竞品在{advantage}方面有明显优势, 长期来看性价比更高."},
        ],
        "sales_tips": [
            {"scenario": "客户犹豫不决", "tip": "使用二选一法则: 您看是选择标准款还是升级款? 而不是您要不要?"},
            {"scenario": "客户拒绝", "tip": "先认可再引导: 我理解您的顾虑, 其实很多客户一开始也有同样的担心, 后来发现..."},
            {"scenario": "价格异议", "tip": "价值重构: 将价格分解到每天/每次使用, 突出长期价值"},
            {"scenario": "客户沉默", "tip": "抛出开放式问题: 您目前在充电宝使用上遇到的最大痛点是什么?"},
            {"scenario": "竞品对比", "tip": "差异化定位: 我们的优势在于{advantage}, 这是竞品不具备的."},
        ],
        "customer_forms": {
            "profile": {"fields": ["客户名称", "行业", "联系人", "联系方式", "首次合作日期", "历史订单总额", "客户等级", "备注"]},
            "visit": {"fields": ["客户名称", "拜访日期", "拜访方式", "沟通内容", "客户反馈", "下一步计划", "跟进人"]},
            "opportunity": {"fields": ["客户名称", "商机描述", "预计金额", "当前阶段", "成功率", "预计成交日期", "跟进人"]},
        },
        "email_templates": [
            {"type": "first_contact", "subject": "Introduction - Beste Power Bank Solutions", "body": "Dear {customer_name}, We are Beste, a leading manufacturer of power bank and charging station solutions..."},
            {"type": "quote", "subject": "Quotation for {product_name}", "body": "Dear {customer_name}, Please find attached the quotation for {product_name}..."},
            {"type": "overseas_quote", "subject": "Overseas Quotation - {product_name}", "body": "Dear {customer_name}, Thank you for your interest in our products. Please find the FOB quotation below..."},
        ]
    }
    path = os.path.join(SOURCE_DIR, "templates", "templates_data.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(templates, f, ensure_ascii=False, indent=2)
    print(f"Templates: {path}")

def generate_policies():
    policies = [
        {"id": "POL-001", "name": "考勤管理制度", "category": "人事", "effective_date": "2026-01-01", "content": "员工每日工作时间为9:00-18:00, 午休1小时, 弹性上下班30分钟."},
        {"id": "POL-002", "name": "报销管理制度", "category": "财务", "effective_date": "2026-01-01", "content": "差旅费报销标准: 一线城市住宿500元/天, 餐饮200元/天. 单笔采购金额超过5000元需部门负责人审批, 超过50000元需总经理审批."},
        {"id": "POL-003", "name": "信息安全管理制度", "category": "IT", "effective_date": "2026-03-01", "content": "所有员工须使用公司统一认证系统登录, 密码每90天更换一次."},
        {"id": "POL-004", "name": "请假管理制度", "category": "人事", "effective_date": "2026-01-01", "content": "年假: 入职满1年5天, 满10年10天, 满20年15天."},
        {"id": "POL-005", "name": "采购管理制度", "category": "行政", "effective_date": "2026-01-01", "content": "单笔采购金额超过5000元需部门负责人审批, 超过50000元需总经理审批."},
        {"id": "POL-006", "name": "销售提成管理办法", "category": "销售", "effective_date": "2026-01-01", "content": "销售提成按回款金额的3%计算, 超额完成目标奖励1%, 逾期回款扣减0.5%."},
        {"id": "POL-007", "name": "加班管理制度", "category": "人事", "effective_date": "2026-01-01", "content": "加班需提前申请, 工作日加班1.5倍工资, 休息日2倍, 法定节假日3倍."},
        {"id": "POL-008", "name": "品质管理制度", "category": "品质", "effective_date": "2026-01-01", "content": "来料检验AQL=0.65, 制程检验每2小时抽检一次, 出货检验全检."},
    ]
    path = os.path.join(SOURCE_DIR, "policies", "policies_data.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"policies": policies}, f, ensure_ascii=False, indent=2)
    print(f"Policies: {path} ({len(policies)}份)")

def generate_knowledge_base():
    kb = [
        {"id": "KB001", "category": "结构设计", "question": "外壳壁厚应该设计多少?", "answer": "ABS/PC+ABS材质壁厚推荐2.0-2.5mm, PP材质推荐2.5-3.0mm."},
        {"id": "KB002", "category": "电路设计", "question": "USB-C接口的焊接温度?", "answer": "回流焊峰值温度245度, 波峰焊温度260度."},
        {"id": "KB003", "category": "电池", "question": "18650电池的配对要求?", "answer": "同一电池组内电芯容量差<=1%, 内阻差<=5mOhm, 电压差<=10mV."},
        {"id": "KB004", "category": "认证", "question": "产品出口美国需要哪些认证?", "answer": "FCC, UL, UN38.3."},
        {"id": "KB005", "category": "品质", "question": "AQL抽样标准是什么?", "answer": "AQL=0.65, 正常检验水平II, 一次抽样方案."},
        {"id": "KB006", "category": "模具", "question": "模具保养周期?", "answer": "每生产5000次后进行一级保养, 每20000次后进行二级保养."},
        {"id": "KB007", "category": "测试", "question": "充电宝过充保护测试要求?", "answer": "过充保护电压4.35V, 恢复电压4.15V."},
        {"id": "KB008", "category": "物料", "question": "PCBA板材的常用厚度?", "answer": "常用1.6mm, 可根据需求定制0.8mm/1.0mm/2.0mm."},
        {"id": "KB009", "category": "工艺", "question": "SMT贴片精度要求?", "answer": "CHIP元件精度+/-0.1mm, IC精度+/-0.05mm."},
        {"id": "KB010", "category": "销售", "question": "最小起订量MOQ是多少?", "answer": "标准产品MOQ为100台, 定制产品MOQ为500台."},
    ]
    path = os.path.join(SOURCE_DIR, "references", "knowledge_base.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"knowledge_base": kb, "total": len(kb)}, f, ensure_ascii=False, indent=2)
    print(f"Knowledge base: {path} ({len(kb)}条)")

def generate_gov_source():
    gov_source = {
        "policies_raw": [
            {"id": "GOV001", "title": "深圳市新能源产业扶持政策", "content": "对注册在深圳的新能源企业, 年营收超1000万且注册满2年, 可申请最高500万元补贴."},
            {"id": "GOV002", "title": "国家高新技术企业认定管理办法", "content": "国家重点支持的高新技术领域企业, 研发投入占比超5%, 可申请认定, 享受15%所得税率."},
            {"id": "GOV003", "title": "广东省制造业数字化转型实施方案", "content": "支持制造业企业数字化改造, 投入超100万的可申请最高200万元补贴."},
        ],
        "qualification_standards": {
            "高新技术企业": {"requirements": ["研发投入占比>5%", "知识产权>5项", "高新收入占比>60%"], "benefits": ["所得税率15%", "人才引进优惠", "项目优先支持"]},
            "专精特新": {"requirements": ["成立满2年", "营收超1000万", "细分市场占有率>5%"], "benefits": ["补贴50-100万", "融资支持", "品牌背书"]},
        }
    }
    path = os.path.join(SOURCE_DIR, "references", "gov_source.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(gov_source, f, ensure_ascii=False, indent=2)
    print(f"Gov source: {path}")

def generate_oem_source():
    oem_source = {
        "design_standards": {
            "充电宝": {"wall_thickness": "2.0-2.5mm", "material_options": ["PC+ABS", "ABS", "PC"], "surface_treatment": ["磨砂", "亮面", "橡胶漆", "UV喷涂"]},
            "充电柜": {"material": "SPCC冷轧板+静电喷涂", "thickness": "1.0-1.5mm", "surface_treatment": ["静电喷涂", "拉丝", "烤漆"]},
        },
        "logo_processes": ["丝印", "烫金", "UV打印", "激光雕刻", "模内装饰"],
        "packaging_options": ["彩盒", "白盒", "展示盒", "航空箱"],
    }
    path = os.path.join(SOURCE_DIR, "references", "oem_source.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(oem_source, f, ensure_ascii=False, indent=2)
    print(f"OEM source: {path}")

def generate_finance_source():
    finance_source = {
        "accounting_rules": {
            "销售收入确认": "产品发出且客户签收后确认收入, 附有安装义务的待安装完成后确认.",
            "成本核算方法": "采用加权平均法计算发出存货成本, 制造费用按工时分配.",
            "折旧政策": "固定资产采用直线法折旧, 电子设备5年, 机械设备10年, 房屋20年.",
        },
        "tax_calculation_rules": {
            "VAT": "销项税额-进项税额, 一般纳税人税率13%, 小规模3%.",
            "corporate_income_tax": "应纳税所得额*25%, 高新技术企业15%.",
            "withholding_tax": "境外供应商技术服务费预提所得税10%.",
        }
    }
    path = os.path.join(SOURCE_DIR, "references", "finance_source.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(finance_source, f, ensure_ascii=False, indent=2)
    print(f"Finance source: {path}")

def main():
    ensure_dirs()
    generate_company()
    generate_faq()
    generate_templates()
    generate_policies()
    generate_knowledge_base()
    generate_gov_source()
    generate_oem_source()
    generate_finance_source()
    print(f"\nSource data generation complete! Directory: {SOURCE_DIR}")

if __name__ == "__main__":
    main()
