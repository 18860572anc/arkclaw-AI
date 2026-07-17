#!/usr/bin/env python3
"""倍斯特测试数据框架 - Mock/模拟数据生成器
生成合成业务数据：流量数据、客户数据、订单数据、竞品数据等
"""

import json
import os
import random
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOCK_DIR = os.path.join(BASE_DIR, "data", "mock")

def ensure_dirs():
    for d in ["api-responses", "vector-data", "business-data"]:
        os.makedirs(os.path.join(MOCK_DIR, d), exist_ok=True)

def generate_traffic_data(days=30, platforms=None):
    """生成各平台流量数据"""
    if platforms is None:
        platforms = ["wechat", "douyin", "xiaohongshu", "taobao", "jd", "amazon", "shopify", "tiktok", "facebook", "instagram"]
    data = []
    for d in range(days):
        date = (datetime.now() - timedelta(days=days-1-d)).strftime("%Y-%m-%d")
        for p in platforms:
            base_impressions = random.randint(8000, 50000)
            data.append({
                "date": date,
                "platform": p,
                "impressions": base_impressions,
                "clicks": int(base_impressions * random.uniform(0.02, 0.08)),
                "visitors": int(base_impressions * random.uniform(0.01, 0.05)),
                "inquiries": random.randint(5, 80),
                "gmv": round(random.uniform(5000, 80000), 2),
                "trend": random.choice(["up", "down", "stable"]),
                "change_pct": round(random.uniform(-25, 35), 1),
            })
    path = os.path.join(MOCK_DIR, "business-data", "traffic_data.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"traffic": data, "total_records": len(data)}, f, ensure_ascii=False, indent=2)
    print(f"✅ 流量数据：{path} ({len(data)}条记录)")
    return data

def generate_customer_data(count=50):
    """生成客户数据（含沉睡客户）"""
    industries = ["支付", "零售", "餐饮", "娱乐", "交通", "教育", "医疗", "酒店"]
    sales_staff = ["张明", "李华", "王芳", "赵强", "刘洋", "陈静", "周涛", "吴敏"]
    customers = []
    for i in range(count):
        last_order = datetime.now() - timedelta(days=random.randint(30, 500))
        is_dormant = (datetime.now() - last_order).days > 365
        customers.append({
            "id": f"C{1000+i:04d}",
            "name": f"{random.choice(['深圳市','广州市','北京市','上海市','东莞市'])}{random.choice(['华强','鑫达','鼎盛','联合','创新','卓越','恒通','万顺'])}科技有限公司",
            "industry": random.choice(industries),
            "contact_person": f"{random.choice(['张','李','王','赵','刘','陈','周','吴'])}{random.choice(['伟','芳','强','静','洋','敏','涛','明'])}",
            "phone": f"138{random.randint(10000000, 99999999)}",
            "last_order_date": last_order.strftime("%Y-%m-%d"),
            "total_orders": random.randint(1, 80),
            "total_amount": round(random.uniform(10000, 800000), 2),
            "is_dormant": is_dormant,
            "assigned_sales": random.choice(sales_staff),
            "customer_level": random.choice(["S", "A", "B", "C"]),
        })
    path = os.path.join(MOCK_DIR, "business-data", "customer_data.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"customers": customers, "total": len(customers), "dormant_count": sum(1 for c in customers if c["is_dormant"])}, f, ensure_ascii=False, indent=2)
    print(f"✅ 客户数据：{path} ({len(customers)}个客户，{sum(1 for c in customers if c['is_dormant'])}个沉睡客户)")
    return customers

def generate_order_data(count=30):
    """生成订单数据"""
    customers = ["客户A", "客户B", "客户C", "客户D", "客户E", "客户F", "客户G"]
    products = ["C100充电宝", "C200充电宝", "CS12充电柜", "CS24充电柜"]
    statuses = ["pending", "in_production", "quality_check", "shipped", "delivered"]
    orders = []
    for i in range(count):
        created = datetime.now() - timedelta(days=random.randint(1, 90))
        orders.append({
            "id": f"ORD{1000+i:04d}",
            "customer": random.choice(customers),
            "product": random.choice(products),
            "qty": random.randint(100, 10000),
            "unit_price": round(random.uniform(50, 500), 2),
            "total_amount": 0,
            "status": random.choice(statuses),
            "created_at": created.strftime("%Y-%m-%d"),
            "delivery_date": (created + timedelta(days=random.randint(15, 60))).strftime("%Y-%m-%d"),
            "sales_person": random.choice(["张明", "李华", "王芳"]),
        })
    for o in orders:
        o["total_amount"] = round(o["qty"] * o["unit_price"], 2)
    path = os.path.join(MOCK_DIR, "business-data", "order_data.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"orders": orders, "total": len(orders)}, f, ensure_ascii=False, indent=2)
    print(f"✅ 订单数据：{path} ({len(orders)}个订单)")
    return orders

def generate_competitor_data():
    """生成竞品数据"""
    competitors = [
        {"name": "竞品科技A", "products": [{"name": "PA100", "capacity": "10000mAh", "price": 89}, {"name": "PA200", "capacity": "20000mAh", "price": 159}], "market_share": "25%", "strengths": ["价格低", "渠道广"]},
        {"name": "创新科技B", "products": [{"name": "IB100", "capacity": "10000mAh", "price": 129}, {"name": "IB200", "capacity": "20000mAh", "price": 199}], "market_share": "20%", "strengths": ["品牌强", "设计好"]},
        {"name": "电源科技C", "products": [{"name": "PC100", "capacity": "10000mAh", "price": 99}, {"name": "PC200", "capacity": "20000mAh", "price": 179}], "market_share": "15%", "strengths": ["技术领先", "品质好"]},
        {"name": "环球电子D", "products": [{"name": "GE100", "capacity": "10000mAh", "price": 79}, {"name": "GE200", "capacity": "20000mAh", "price": 149}], "market_share": "12%", "strengths": ["价格最低", "覆盖广"]},
        {"name": "智能科技E", "products": [{"name": "SE100", "capacity": "10000mAh", "price": 109}, {"name": "SE200", "capacity": "20000mAh", "price": 189}], "market_share": "10%", "strengths": ["创新功能多", "设计新颖"]},
    ]
    path = os.path.join(MOCK_DIR, "business-data", "competitor_data.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"competitors": competitors, "total": len(competitors)}, f, ensure_ascii=False, indent=2)
    print(f"✅ 竞品数据：{path} ({len(competitors)}个竞品)")
    return competitors

def generate_bom_data():
    """生成BOM物料清单数据"""
    boms = [
        {"project_id": "P001", "materials": [
            {"id": "M001", "name": "锂电池组", "spec": "18650-2600mAh", "qty": 100, "unit": "个", "delivery_date": "2026-08-15", "status": "in_transit"},
            {"id": "M002", "name": "PCBA主板", "spec": "V3.2", "qty": 100, "unit": "片", "delivery_date": "2026-08-10", "status": "arrived"},
            {"id": "M003", "name": "外壳上盖", "spec": "PC+ABS-黑色", "qty": 100, "unit": "个", "delivery_date": "2026-08-20", "status": "pending"},
            {"id": "M004", "name": "外壳底盖", "spec": "PC+ABS-黑色", "qty": 100, "unit": "个", "delivery_date": "2026-08-20", "status": "pending"},
            {"id": "M005", "name": "USB-C接口", "spec": "母座-沉板", "qty": 100, "unit": "个", "delivery_date": "2026-08-12", "status": "arrived"},
        ]},
        {"project_id": "P002", "materials": [
            {"id": "M006", "name": "锂电池组", "spec": "21700-5000mAh", "qty": 200, "unit": "个", "delivery_date": "2026-08-25", "status": "pending"},
            {"id": "M007", "name": "PCBA主板", "spec": "V4.0", "qty": 200, "unit": "片", "delivery_date": "2026-08-20", "status": "in_transit"},
            {"id": "M008", "name": "无线充电线圈", "spec": "Qi标准", "qty": 200, "unit": "个", "delivery_date": "2026-08-30", "status": "pending"},
        ]},
    ]
    path = os.path.join(MOCK_DIR, "business-data", "bom_data.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"boms": boms, "total": len(boms)}, f, ensure_ascii=False, indent=2)
    print(f"✅ BOM数据：{path} ({len(boms)}个BOM)")
    return boms

def generate_inventory_data():
    """生成库存数据"""
    items = [
        {"id": "M001", "name": "锂电池组(18650)", "stock": 5000, "reserved": 2000, "available": 3000, "warehouse": "深圳仓", "min_stock": 1000},
        {"id": "M002", "name": "PCBA主板(V3.2)", "stock": 3000, "reserved": 2500, "available": 500, "warehouse": "深圳仓", "min_stock": 500},
        {"id": "M003", "name": "外壳上盖(黑色)", "stock": 2000, "reserved": 1500, "available": 500, "warehouse": "深圳仓", "min_stock": 300},
        {"id": "M004", "name": "USB-C接口", "stock": 10000, "reserved": 3000, "available": 7000, "warehouse": "深圳仓", "min_stock": 2000},
        {"id": "M005", "name": "包装盒", "stock": 8000, "reserved": 4000, "available": 4000, "warehouse": "深圳仓", "min_stock": 1000},
    ]
    path = os.path.join(MOCK_DIR, "business-data", "inventory_data.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"items": items, "total": len(items)}, f, ensure_ascii=False, indent=2)
    print(f"✅ 库存数据：{path} ({len(items)}个SKU)")
    return items

def generate_material_prices():
    """生成元器件行情数据"""
    materials = [
        {"name": "锂电池(18650)", "unit": "元/个", "current_price": 12.5, "price_change_3m": "+15%", "trend": "up", "supply_status": "紧张"},
        {"name": "内存芯片", "unit": "元/片", "current_price": 8.2, "price_change_3m": "+35%", "trend": "up", "supply_status": "紧缺"},
        {"name": "电感", "unit": "元/个", "current_price": 0.35, "price_change_3m": "+5%", "trend": "stable", "supply_status": "充足"},
        {"name": "电容", "unit": "元/个", "current_price": 0.15, "price_change_3m": "+10%", "trend": "up", "supply_status": "充足"},
        {"name": "PCBA板材", "unit": "元/平方米", "current_price": 85, "price_change_3m": "-3%", "trend": "down", "supply_status": "充足"},
        {"name": "USB-C接口", "unit": "元/个", "current_price": 0.8, "price_change_3m": "+2%", "trend": "stable", "supply_status": "充足"},
    ]
    path = os.path.join(MOCK_DIR, "business-data", "material_prices.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"materials": materials, "total": len(materials)}, f, ensure_ascii=False, indent=2)
    print(f"✅ 元器件行情：{path} ({len(materials)}种)")
    return materials

def main():
    ensure_dirs()
    generate_traffic_data(days=30)
    generate_customer_data(count=50)
    generate_order_data(count=30)
    generate_competitor_data()
    generate_bom_data()
    generate_inventory_data()
    generate_material_prices()
    print(f"\n🎯 Mock数据生成完成！目录：{MOCK_DIR}")

if __name__ == "__main__":
    main()