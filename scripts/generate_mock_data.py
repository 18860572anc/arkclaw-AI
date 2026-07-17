#!/usr/bin/env python3
"""倍斯特测试数据框架 - Mock数据生成器 (完整版52场景)"""
import json, os, random
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOCK_DIR = os.path.join(BASE_DIR, "data", "mock")

def ensure_dirs():
    for d in ["api-responses", "vector-data", "business-data"]:
        os.makedirs(os.path.join(MOCK_DIR, d), exist_ok=True)

def run():
    ensure_dirs()
    # ===== Existing generators =====
    platforms = ["wechat","douyin","xiaohongshu","taobao","jd","amazon","shopify","tiktok","facebook","instagram"]
    traffic = []
    for d in range(30):
        date = (datetime.now() - timedelta(days=29-d)).strftime("%Y-%m-%d")
        for p in platforms:
            bi = random.randint(8000,50000)
            traffic.append({"date":date,"platform":p,"impressions":bi,"clicks":int(bi*random.uniform(0.02,0.08)),"visitors":int(bi*random.uniform(0.01,0.05)),"inquiries":random.randint(5,80),"gmv":round(random.uniform(5000,80000),2),"trend":random.choice(["up","down","stable"]),"change_pct":round(random.uniform(-25,35),1)})
    with open(os.path.join(MOCK_DIR,"business-data","traffic_data.json"),"w",encoding="utf-8") as f:
        json.dump({"traffic":traffic,"total_records":len(traffic)},f,ensure_ascii=False,indent=2)
    print(f"Traffic: {len(traffic)} records")

    industries = ["支付","零售","餐饮","娱乐","交通","教育","医疗","酒店"]
    sales_staff = ["张明","李华","王芳","赵强","刘洋","陈静","周涛","吴敏"]
    customers = []
    for i in range(50):
        lo = datetime.now() - timedelta(days=random.randint(30,500))
        is_d = (datetime.now()-lo).days > 365
        customers.append({"id":f"C{1000+i:04d}","name":f"{random.choice([chr(0x6DF1)+chr(0x5733)+chr(0x5E02),chr(0x5E7F)+chr(0x5DDE)+chr(0x5E02)])}科技有限公司","industry":random.choice(industries),"contact_person":"张经理","phone":f"138{random.randint(10000000,99999999)}","last_order_date":lo.strftime("%Y-%m-%d"),"total_orders":random.randint(1,80),"total_amount":round(random.uniform(10000,800000),2),"is_dormant":is_d,"assigned_sales":random.choice(sales_staff),"customer_level":random.choice(["S","A","B","C"])})
    with open(os.path.join(MOCK_DIR,"business-data","customer_data.json"),"w",encoding="utf-8") as f:
        json.dump({"customers":customers,"total":len(customers),"dormant_count":sum(1 for c in customers if c["is_dormant"])},f,ensure_ascii=False,indent=2)
    print(f"Customers: {len(customers)}")

    # ===== New generators =====
    # Supplier data
    suppliers = [{"id":"SUP001","name":"供应商A","type":"电池","rating":4.8,"delivery_punctuality":0.95,"price_level":"中等","cooperation_years":5,"certifications":["ISO9001","UL"]},{"id":"SUP002","name":"供应商B","type":"电子元件","rating":4.5,"delivery_punctuality":0.88,"price_level":"偏高","cooperation_years":3,"certifications":["ISO9001"]},{"id":"SUP003","name":"供应商C","type":"包材","rating":4.2,"delivery_punctuality":0.92,"price_level":"低","cooperation_years":2,"certifications":["ISO14001"]},{"id":"SUP004","name":"供应商D","type":"PCB","rating":4.6,"delivery_punctuality":0.90,"price_level":"中等","cooperation_years":4,"certifications":["ISO9001","IPC"]},{"id":"SUP005","name":"供应商E","type":"锂电池","rating":4.9,"delivery_punctuality":0.97,"price_level":"偏高","cooperation_years":6,"certifications":["ISO9001","UL","UN38.3"]}]
    with open(os.path.join(MOCK_DIR,"business-data","supplier_data.json"),"w",encoding="utf-8") as f:
        json.dump({"suppliers":suppliers,"total":len(suppliers)},f,ensure_ascii=False,indent=2)
    print(f"Suppliers: {len(suppliers)}")

    # Finance data
    finance = {"receivables":[{"id":"RCV001","customer_id":"C1001","customer_name":"客户A","amount":150000,"due_date":"2026-06-15","days_overdue":32,"status":"overdue","collection_phase":"second_reminder"},{"id":"RCV002","customer_id":"C1002","customer_name":"客户B","amount":85000,"due_date":"2026-07-01","days_overdue":16,"status":"overdue","collection_phase":"first_reminder"},{"id":"RCV003","customer_id":"C1003","customer_name":"客户C","amount":200000,"due_date":"2026-07-20","days_overdue":0,"status":"pending","collection_phase":"normal"},{"id":"RCV004","customer_id":"C1004","customer_name":"客户D","amount":50000,"due_date":"2026-05-01","days_overdue":77,"status":"overdue","collection_phase":"legal_warning"}],"commission_rules":[{"rule_id":"R001","name":"标准提成","base_rate":0.03,"target_bonus_rate":0.01,"overdue_deduction_rate":0.005},{"rule_id":"R002","name":"高额提成","base_rate":0.05,"target_bonus_rate":0.02,"overdue_deduction_rate":0.01,"min_amount":500000}],"commission_records":[{"id":"COM001","sales_person":"张明","period":"2026-06","base_commission":15000,"bonus":5000,"deduction":2000,"net_amount":18000},{"id":"COM002","sales_person":"李华","period":"2026-06","base_commission":12000,"bonus":3000,"deduction":0,"net_amount":15000},{"id":"COM003","sales_person":"王芳","period":"2026-06","base_commission":8000,"bonus":2000,"deduction":500,"net_amount":9500}],"accounting_subjects":{"资产类":["银行存款","应收账款","库存商品","固定资产","预付账款"],"负债类":["应付账款","预收账款","应交税费","短期借款"],"权益类":["实收资本","未分配利润","盈余公积"],"成本类":["生产成本","制造费用","劳务成本"],"损益类":["主营业务收入","主营业务成本","管理费用","销售费用","财务费用","税金及附加"]},"tax_rates":{"VAT":{"rate":0.13,"filing_frequency":"monthly","deadline":"次月15日"},"corporate_income_tax":{"rate":0.25,"filing_frequency":"quarterly","deadline":"季度结束后15日内"},"stamp_tax":{"rate":0.0003,"filing_frequency":"monthly","deadline":"当月最后一日"}}}
    with open(os.path.join(MOCK_DIR,"business-data","finance_data.json"),"w",encoding="utf-8") as f:
        json.dump(finance,f,ensure_ascii=False,indent=2)
    print(f"Finance data: OK")

    # Production data
    prod = {"production_lines":[{"id":"PL001","name":"充电宝产线A","factory":"江苏工厂","capacity_per_day":5000,"current_efficiency":0.85,"bottleneck":"SMT贴片工序","status":"running"},{"id":"PL002","name":"充电柜产线B","factory":"江苏工厂","capacity_per_day":200,"current_efficiency":0.78,"bottleneck":"组装调试","status":"running"},{"id":"PL003","name":"充电宝产线C","factory":"广西工厂","capacity_per_day":3000,"current_efficiency":0.0,"bottleneck":"设备调试中","status":"commissioning"}],"quality_metrics":[{"period":"2026-06","yield_rate":0.973,"defect_types":{"外观划伤":0.008,"充电异常":0.005,"连接器松动":0.004,"其他":0.010},"improvements":["优化SMT回流焊温度参数","增加外观检测工位"]},{"period":"2026-05","yield_rate":0.965,"defect_types":{"外观划伤":0.012,"充电异常":0.007,"连接器松动":0.006,"其他":0.010},"improvements":["引入自动光学检测"]}],"complaints":[{"id":"CP0001","customer":"客户A","product":"C200充电宝","date":"2026-07-01","description":"充电宝无法为手机充电","root_cause":"USB-C接口焊接不良","impact_scope":"批次20260601-20260615生产","corrective_action":"更换接口模块并全检","status":"closed"},{"id":"CP0002","customer":"客户B","product":"CS12充电柜","date":"2026-07-10","description":"充电柜第3槽位无法充电","root_cause":"待分析","impact_scope":"待确认","corrective_action":"待制定","status":"analyzing"}],"schedules":[{"id":"SCH001","period":"2026-07-16","orders":["ORD1001","ORD1002"],"factory":"江苏工厂","line_assignments":{"PL001":["ORD1001"],"PL002":["ORD1002"]},"estimated_start":"2026-07-18","estimated_complete":"2026-08-15"}]}
    with open(os.path.join(MOCK_DIR,"business-data","production_data.json"),"w",encoding="utf-8") as f:
        json.dump(prod,f,ensure_ascii=False,indent=2)
    print(f"Production data: OK")
    print("All mock data generated!")

if __name__ == "__main__":
    run()
