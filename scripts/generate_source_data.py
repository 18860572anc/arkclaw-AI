#!/usr/bin/env python3
"""倍斯特测试数据框架 - 源数据生成器
生成公司信息、FAQ、话术模板、品牌调性等源数据
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
            {"year": 2020, "event": "进入海外市场，覆盖欧美东南亚"},
            {"year": 2022, "event": "建立江苏工厂，年产能提升至500万台"},
            {"year": 2024, "event": "与ArkClaw达成战略合作，启动AI数字化升级"},
            {"year": 2025, "event": "建立广西工厂，拓展新能源电池领域"},
        ],
        "culture": "创新、务实、客户至上",
        "brand_guide": {
            "primary_color": "#1A73E8",
            "secondary_color": "#00C853",
            "accent_color": "#FF6D00",
            "font_title": "思源黑体 Bold",
            "font_body": "思源黑体 Regular",
            "font_en": "Inter",
            "design_style": "简洁干净、圆角元素、图标化表达",
        }
    }
    path = os.path.join(SOURCE_DIR, "company", "company_info.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ 公司信息：{path}")
    return data

def generate_faq():
    faq = [
        {"question": "产品保修期多久？", "answer": "标准保修期为12个月，从发货之日起计算。可延长至24个月（需额外购买延长保修服务）。", "category": "after_sale", "tags": ["保修", "售后"]},
        {"question": "充电宝无法开机怎么办？", "answer": "1.检查电源连接 2.确认电池电量 3.长按复位键10秒 4.如仍无法开机请联系技术支持", "category": "tech", "tags": ["故障排查", "开机"]},
        {"question": "充电速度慢的原因？", "answer": "1.检查充电线缆是否完好 2.确认设备温度是否过高 3.检查输出端口是否清洁", "category": "tech", "tags": ["充电慢", "故障"]},
        {"question": "产品防水等级是多少？", "answer": "标准产品防水等级为IPX4，可防溅水。如需更高防水等级可定制（最高IPX7）。", "category": "product", "tags": ["防水", "规格"]},
        {"question": "支持哪些充电协议？", "answer": "支持QC3.0、PD3.0、AFC、FCP等主流快充协议", "category": "product", "tags": ["快充", "协议"]},
        {"question": "最小起订量是多少？", "answer": "标准产品MOQ为100台，定制产品MOQ为500台", "category": "sales", "tags": ["MOQ", "订购"]},
        {"question": "定制产品需要多长时间？", "answer": "ODM定制周期一般为45-60天，含设计评审、开模、打样、试产、量产", "category": "sales", "tags": ["定制", "周期"]},
        {"question": "海外订单如何发货？", "answer": "支持FOB深圳、CIF主要港口、DDP等多种贸易条款，海运周期约20-35天", "category": "sales", "tags": ["海外", "物流"]},
        {"question": "充电柜的安装要求？", "answer": "需AC 220V电源，接地良好，安装环境温度0-40°C，避免阳光直射和潮湿环境", "category": "tech", "tags": ["安装", "充电柜"]},
        {"question": "产品通过哪些认证？", "answer": "CE、FCC、RoHS、UN38.3（电池安全认证）", "category": "product", "tags": ["认证", "合规"]},
    ]
    path = os.path.join(SOURCE_DIR, "faq", "faq_data.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"faq": faq}, f, ensure_ascii=False, indent=2)
    print(f"✅ FAQ数据：{path} ({len(faq)}条)")
    return faq

def generate_templates():
    templates = {
        "communication": [
            {"type": "greeting", "tone": "formal", "text": "您好！欢迎咨询倍斯特，请问有什么可以帮您？"},
            {"type": "greeting", "tone": "casual", "text": "嗨！感谢关注倍斯特，有什么需要了解的？"},
            {"type": "apology", "text": "非常抱歉给您带来不便，我们正在为您加急处理，预计{time}内回复。"},
            {"type": "escalation", "text": "这个问题我需要转给技术支持同事处理，请稍等，他们会尽快联系您。"},
            {"type": "closing", "text": "感谢您的咨询，如有其他问题随时联系我们！祝您生活愉快！"},
            {"type": "price_objection", "text": "我理解您对价格的关注。其实我们的产品采用{feature}技术，相比竞品在{advantage}方面有明显优势，长期来看性价比更高。"},
        ],
        "sales_tips": [
            {"scenario": "客户犹豫不决", "tip": "使用二选一法则：'您看是选择标准款还是升级款？' 而不是 '您要不要？'"},
            {"scenario": "客户拒绝", "tip": "先认可再引导：'我理解您的顾虑，其实很多客户一开始也有同样的担心，后来发现...'"},
            {"scenario": "价格异议", "tip": "价值重构：将价格分解到每天/每次使用，突出长期价值"},
            {"scenario": "客户沉默", "tip": "抛出开放式问题：'您目前在充电宝使用上遇到的最大痛点是什么？'"},
            {"scenario": "竞品对比", "tip": "差异化定位：'我们的优势在于{advantage}，这是竞品不具备的。'"},
        ],
        "customer_forms": {
            "profile": {"fields": ["客户名称", "行业", "联系人", "联系方式", "首次合作日期", "历史订单总额", "客户等级", "备注"]},
            "visit": {"fields": ["客户名称", "拜访日期", "拜访方式", "沟通内容", "客户反馈", "下一步计划", "跟进人"]},
            "opportunity": {"fields": ["客户名称", "商机描述", "预计金额", "当前阶段", "成功率", "预计成交日期", "跟进人"]},
        },
        "email_templates": [
            {"type": "first_contact", "subject": "Introduction - Beste Power Bank Solutions", "body": "Dear {customer_name},\n\nWe are Beste, a leading manufacturer of power bank and charging station solutions...\n\nBest regards,\n{sales_name}"},
            {"type": "quote", "subject": "Quotation for {product_name}", "body": "Dear {customer_name},\n\nPlease find attached the quotation for {product_name}...\n\nBest regards,\n{sales_name}"},
        ]
    }
    path = os.path.join(SOURCE_DIR, "templates", "templates_data.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(templates, f, ensure_ascii=False, indent=2)
    print(f"✅ 模板数据：{path}")
    return templates

def generate_policies():
    policies = [
        {"id": "POL-001", "name": "考勤管理制度", "category": "人事", "effective_date": "2026-01-01", "content": "员工每日工作时间为9:00-18:00，午休1小时，弹性上下班30分钟。"},
        {"id": "POL-002", "name": "报销管理制度", "category": "财务", "effective_date": "2026-01-01", "content": "差旅费报销标准：一线城市住宿500元/天，餐饮200元/天。"},
        {"id": "POL-003", "name": "信息安全管理制度", "category": "IT", "effective_date": "2026-03-01", "content": "所有员工须使用公司统一认证系统登录，密码每90天更换一次。"},
        {"id": "POL-004", "name": "请假管理制度", "category": "人事", "effective_date": "2026-01-01", "content": "年假：入职满1年5天，满10年10天，满20年15天。"},
        {"id": "POL-005", "name": "采购管理制度", "category": "行政", "effective_date": "2026-01-01", "content": "单笔采购金额超过5000元需部门负责人审批，超过50000元需总经理审批。"},
    ]
    path = os.path.join(SOURCE_DIR, "policies", "policies_data.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"policies": policies}, f, ensure_ascii=False, indent=2)
    print(f"✅ 制度文档：{path} ({len(policies)}份)")
    return policies

def main():
    ensure_dirs()
    generate_company()
    generate_faq()
    generate_templates()
    generate_policies()
    print(f"\n🎯 源数据生成完成！目录：{SOURCE_DIR}")

if __name__ == "__main__":
    main()