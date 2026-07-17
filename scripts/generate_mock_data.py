#!/usr/bin/env python3
"""倍斯特测试数据框架 - Mock数据生成器 (完整版52场景+倍用心接口数据)"""
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

    # ===== 供应商数据（含倍用心扩展字段） =====
    suppliers = [
        {"id":"SUP001","name":"供应商A","type":"电池","rating":4.8,"delivery_punctuality":0.95,"price_level":"中等","cooperation_years":5,"certifications":["ISO9001","UL"]},
        {"id":"SUP002","name":"供应商B","type":"电子元件","rating":4.5,"delivery_punctuality":0.88,"price_level":"偏高","cooperation_years":3,"certifications":["ISO9001"]},
        {"id":"SUP003","name":"供应商C","type":"包材","rating":4.2,"delivery_punctuality":0.92,"price_level":"低","cooperation_years":2,"certifications":["ISO14001"]},
        {"id":"SUP004","name":"供应商D","type":"PCB","rating":4.6,"delivery_punctuality":0.90,"price_level":"中等","cooperation_years":4,"certifications":["ISO9001","IPC"]},
        {"id":"SUP005","name":"供应商E","type":"锂电池","rating":4.9,"delivery_punctuality":0.97,"price_level":"偏高","cooperation_years":6,"certifications":["ISO9001","UL","UN38.3"]},
    ]
    # 倍用心扩展：联系方式、银行信息、付款条款
    contact_names = ["王经理","李经理","赵经理","陈经理","刘经理"]
    banks = ["中国银行","工商银行","建设银行","招商银行","农业银行"]
    payment_terms_list = ["月结30天","月结60天","预付30%","预付50%","票据结算"]
    for s in suppliers:
        s["contact_person"] = random.choice(contact_names)
        s["contact_phone"] = f"13{random.choice([8,9,7,6])}{random.randint(10000000,99999999)}"
        s["bank_info"] = {"bank": random.choice(banks), "account": f"6222{random.randint(1000000000000,9999999999999)}"}
        s["payment_terms"] = random.choice(payment_terms_list)
    with open(os.path.join(MOCK_DIR,"business-data","supplier_data.json"),"w",encoding="utf-8") as f:
        json.dump({"suppliers":suppliers,"total":len(suppliers)},f,ensure_ascii=False,indent=2)
    print(f"Suppliers: {len(suppliers)}")

    # ===== 财务数据（含倍用心扩展：出库明细、收款记录、费用支出、工时） =====
    finance = {
        "receivables":[
            {"id":"RCV001","customer_id":"C1001","customer_name":"客户A","amount":150000,"due_date":"2026-06-15","days_overdue":32,"status":"overdue","collection_phase":"second_reminder"},
            {"id":"RCV002","customer_id":"C1002","customer_name":"客户B","amount":85000,"due_date":"2026-07-01","days_overdue":16,"status":"overdue","collection_phase":"first_reminder"},
            {"id":"RCV003","customer_id":"C1003","customer_name":"客户C","amount":200000,"due_date":"2026-07-20","days_overdue":0,"status":"pending","collection_phase":"normal"},
            {"id":"RCV004","customer_id":"C1004","customer_name":"客户D","amount":50000,"due_date":"2026-05-01","days_overdue":77,"status":"overdue","collection_phase":"legal_warning"},
        ],
        "commission_rules":[
            {"rule_id":"R001","name":"标准提成","base_rate":0.03,"target_bonus_rate":0.01,"overdue_deduction_rate":0.005},
            {"rule_id":"R002","name":"高额提成","base_rate":0.05,"target_bonus_rate":0.02,"overdue_deduction_rate":0.01,"min_amount":500000},
        ],
        "commission_records":[
            {"id":"COM001","sales_person":"张明","period":"2026-06","base_commission":15000,"bonus":5000,"deduction":2000,"net_amount":18000},
            {"id":"COM002","sales_person":"李华","period":"2026-06","base_commission":12000,"bonus":3000,"deduction":0,"net_amount":15000},
            {"id":"COM003","sales_person":"王芳","period":"2026-06","base_commission":8000,"bonus":2000,"deduction":500,"net_amount":9500},
        ],
        "accounting_subjects":{
            "资产类":["银行存款","应收账款","库存商品","固定资产","预付账款"],
            "负债类":["应付账款","预收账款","应交税费","短期借款"],
            "权益类":["实收资本","未分配利润","盈余公积"],
            "成本类":["生产成本","制造费用","劳务成本"],
            "损益类":["主营业务收入","主营业务成本","管理费用","销售费用","财务费用","税金及附加"],
        },
        "tax_rates":{
            "VAT":{"rate":0.13,"filing_frequency":"monthly","deadline":"次月15日"},
            "corporate_income_tax":{"rate":0.25,"filing_frequency":"quarterly","deadline":"季度结束后15日内"},
            "stamp_tax":{"rate":0.0003,"filing_frequency":"monthly","deadline":"当月最后一日"},
        },
        # 倍用心扩展字段
        "outbound_details":[
            {"outbound_no":"OB20260701001","order_no":"ORD1001","customer":"客户A","product":"C200充电宝","qty":1000,"unit_price":45.0,"total_amount":45000.0,"outbound_date":"2026-07-10","warehouse":"成品仓"},
            {"outbound_no":"OB20260715001","order_no":"ORD1001","customer":"客户A","product":"C200充电宝","qty":1800,"unit_price":45.0,"total_amount":81000.0,"outbound_date":"2026-07-15","warehouse":"成品仓"},
            {"outbound_no":"OB20260715002","order_no":"ORD1002","customer":"客户B","product":"CS12充电柜","qty":50,"unit_price":3200.0,"total_amount":160000.0,"outbound_date":"2026-07-15","warehouse":"成品仓"},
        ],
        "payment_records":[
            {"payment_no":"PAY20260701001","customer":"客户A","amount":45000.0,"payment_date":"2026-07-01","payment_method":"银行转账","related_invoice":"INV20260701001","status":"confirmed"},
            {"payment_no":"PAY20260710001","customer":"客户B","amount":128000.0,"payment_date":"2026-07-10","payment_method":"承兑汇票","related_invoice":"INV20260710001","status":"confirmed"},
            {"payment_no":"PAY20260715001","customer":"客户A","amount":81000.0,"payment_date":"2026-07-15","payment_method":"银行转账","related_invoice":"INV20260715001","status":"pending"},
        ],
        "expenses":[
            {"expense_no":"EXP20260701001","department":"制造中心","category":"原材料采购","amount":250000.0,"expense_date":"2026-07-01","status":"approved","remark":"7月第一批物料采购"},
            {"expense_no":"EXP20260705001","department":"研发部","category":"设备采购","amount":85000.0,"expense_date":"2026-07-05","status":"approved","remark":"新测试设备采购"},
            {"expense_no":"EXP20260710001","department":"销售部","category":"差旅费","amount":12000.0,"expense_date":"2026-07-10","status":"pending","remark":"客户拜访差旅"},
            {"expense_no":"EXP20260712001","department":"管理中心","category":"办公费用","amount":8000.0,"expense_date":"2026-07-12","status":"approved","remark":"办公用品采购"},
        ],
        "labor_hours":[
            {"department":"制造中心","period":"2026-07","total_hours":8560,"regular_hours":8000,"overtime_hours":560,"headcount":50,"avg_hours_per_person":171.2},
            {"department":"研发部","period":"2026-07","total_hours":3400,"regular_hours":3200,"overtime_hours":200,"headcount":20,"avg_hours_per_person":170.0},
            {"department":"销售部","period":"2026-07","total_hours":1680,"regular_hours":1600,"overtime_hours":80,"headcount":10,"avg_hours_per_person":168.0},
            {"department":"管理中心","period":"2026-07","total_hours":1260,"regular_hours":1200,"overtime_hours":60,"headcount":8,"avg_hours_per_person":157.5},
        ],
    }
    with open(os.path.join(MOCK_DIR,"business-data","finance_data.json"),"w",encoding="utf-8") as f:
        json.dump(finance,f,ensure_ascii=False,indent=2)
    print(f"Finance data: OK")

    # ===== 生产数据（含倍用心扩展：产线入库、进度、产能） =====
    prod = {
        "production_lines":[
            {"id":"PL001","name":"充电宝产线A","factory":"江苏工厂","capacity_per_day":5000,"current_efficiency":0.85,"bottleneck":"SMT贴片工序","status":"running"},
            {"id":"PL002","name":"充电柜产线B","factory":"江苏工厂","capacity_per_day":200,"current_efficiency":0.78,"bottleneck":"组装调试","status":"running"},
            {"id":"PL003","name":"充电宝产线C","factory":"广西工厂","capacity_per_day":3000,"current_efficiency":0.0,"bottleneck":"设备调试中","status":"commissioning"},
        ],
        "quality_metrics":[
            {"period":"2026-06","yield_rate":0.973,"defect_types":{"外观划伤":0.008,"充电异常":0.005,"连接器松动":0.004,"其他":0.010},"improvements":["优化SMT回流焊温度参数","增加外观检测工位"]},
            {"period":"2026-05","yield_rate":0.965,"defect_types":{"外观划伤":0.012,"充电异常":0.007,"连接器松动":0.006,"其他":0.010},"improvements":["引入自动光学检测"]},
        ],
        "complaints":[
            {"id":"CP0001","customer":"客户A","product":"C200充电宝","date":"2026-07-01","description":"充电宝无法为手机充电","root_cause":"USB-C接口焊接不良","impact_scope":"批次20260601-20260615生产","corrective_action":"更换接口模块并全检","status":"closed"},
            {"id":"CP0002","customer":"客户B","product":"CS12充电柜","date":"2026-07-10","description":"充电柜第3槽位无法充电","root_cause":"待分析","impact_scope":"待确认","corrective_action":"待制定","status":"analyzing"},
        ],
        "schedules":[{"id":"SCH001","period":"2026-07-16","orders":["ORD1001","ORD1002"],"factory":"江苏工厂","line_assignments":{"PL001":["ORD1001"],"PL002":["ORD1002"]},"estimated_start":"2026-07-18","estimated_complete":"2026-08-15"}],
        # 倍用心扩展字段
        "warehouse_in_records":[
            {"order_no":"ORD1001","product":"C200充电宝","factory":"江苏工厂","line":"充电宝产线A","planned_qty":5000,"produced_qty":3200,"warehoused_qty":2800,"defect_qty":15,"yield_rate":0.973,"warehouse_date":"2026-07-16"},
            {"order_no":"ORD1002","product":"CS12充电柜","factory":"江苏工厂","line":"充电柜产线B","planned_qty":200,"produced_qty":120,"warehoused_qty":100,"defect_qty":2,"yield_rate":0.983,"warehouse_date":"2026-07-16"},
        ],
        "production_progress":[
            {"order_no":"ORD1001","product":"C200充电宝","total_qty":5000,"completed_qty":3200,"completion_pct":64.0,"current_stage":"组装测试","planned_completion":"2026-08-10","risk":"low"},
            {"order_no":"ORD1002","product":"CS12充电柜","total_qty":200,"completed_qty":120,"completion_pct":60.0,"current_stage":"组装调试","planned_completion":"2026-08-15","risk":"low"},
        ],
        "capacity_data":[
            {"factory":"江苏工厂","line":"充电宝产线A","daily_capacity":5000,"current_load":0.85,"available_capacity":750,"status":"running","bottleneck":"SMT贴片工序"},
            {"factory":"江苏工厂","line":"充电柜产线B","daily_capacity":200,"current_load":0.78,"available_capacity":44,"status":"running","bottleneck":"组装调试"},
            {"factory":"广西工厂","line":"充电宝产线C","daily_capacity":3000,"current_load":0.0,"available_capacity":3000,"status":"commissioning","bottleneck":"设备调试中"},
        ],
    }
    with open(os.path.join(MOCK_DIR,"business-data","production_data.json"),"w",encoding="utf-8") as f:
        json.dump(prod,f,ensure_ascii=False,indent=2)
    print(f"Production data: OK")

    # ===== CRM数据（含倍用心扩展：跟进记录、商机状态） =====
    crm = {
        "crm_dashboard": {"total_customers": 50, "active_customers": 35, "dormant_customers": 15, "new_inquiries_this_week": 8, "collaboration_tasks_pending": 5},
        "collaboration_tasks": [{"id":"T001","title":"客户A报价跟进","department":"销售部","assignee":"张明","due_date":"2026-07-20","status":"in_progress"},{"id":"T002","title":"客户B技术方案","department":"研发部","assignee":"陈工","due_date":"2026-07-18","status":"pending"}],
        # 倍用心扩展字段
        "follow_up_records":[
            {"customer_code":"C1001","customer_name":"深圳市科技有限公司","sales_person":"张明","follow_up_date":"2026-07-15","method":"电话","content":"沟通新订单需求，预计8月下单","next_action":"准备报价单","next_date":"2026-07-18"},
            {"customer_code":"C1001","customer_name":"深圳市科技有限公司","sales_person":"张明","follow_up_date":"2026-07-10","method":"拜访","content":"样品展示，客户对C200充电宝满意","next_action":"跟进合同签订","next_date":"2026-07-14"},
            {"customer_code":"C1002","customer_name":"广州市贸易有限公司","sales_person":"李华","follow_up_date":"2026-07-12","method":"微信","content":"确认CS12充电柜技术参数","next_action":"发送正式报价","next_date":"2026-07-13"},
            {"customer_code":"C1003","customer_name":"深圳市电子有限公司","sales_person":"王芳","follow_up_date":"2026-07-08","method":"邮件","content":"发送季度促销方案","next_action":"确认客户意向","next_date":"2026-07-20"},
        ],
        "opportunities":[
            {"customer_code":"C1001","customer_name":"深圳市科技有限公司","opportunity_name":"C200充电宝批量采购","expected_amount":450000.0,"stage":"商务谈判","probability_pct":70,"expected_close":"2026-08","sales_person":"张明","created_date":"2026-06-20"},
            {"customer_code":"C1002","customer_name":"广州市贸易有限公司","opportunity_name":"CS12充电柜代理","expected_amount":640000.0,"stage":"方案确认","probability_pct":50,"expected_close":"2026-09","sales_person":"李华","created_date":"2026-06-25"},
            {"customer_code":"C1004","customer_name":"客户D","opportunity_name":"OEM充电宝定制","expected_amount":280000.0,"stage":"需求调研","probability_pct":30,"expected_close":"2026-10","sales_person":"赵强","created_date":"2026-07-01"},
        ],
    }
    with open(os.path.join(MOCK_DIR,"business-data","crm_data.json"),"w",encoding="utf-8") as f:
        json.dump(crm,f,ensure_ascii=False,indent=2)
    print(f"CRM data: OK")

    # ===== 订单数据扩展（含倍用心字段） =====
    orders = {"orders":[
        {"id":"ORD1001","customer":"客户A","product":"C200充电宝","qty":5000,"price":45.0,"delivery":"2026-08-15","date":"2026-07-01","status":"生产中","product_model":"C200","work_order_no":"WO20260701001","customer_id":"C1001","unit_price":45.0},
        {"id":"ORD1002","customer":"客户B","product":"CS12充电柜","qty":200,"price":3200.0,"delivery":"2026-08-30","date":"2026-07-05","status":"生产中","product_model":"CS12","work_order_no":"WO20260705001","customer_id":"C1002","unit_price":3200.0},
        {"id":"ORD1003","customer":"客户C","product":"C100充电宝","qty":10000,"price":28.0,"delivery":"2026-09-01","date":"2026-07-10","status":"待审核","product_model":"C100","work_order_no":"","customer_id":"C1003","unit_price":28.0},
    ]}
    with open(os.path.join(MOCK_DIR,"business-data","order_data.json"),"w",encoding="utf-8") as f:
        json.dump(orders,f,ensure_ascii=False,indent=2)
    print(f"Order data: OK")

    # ===== BOM数据扩展（含倍用心字段） =====
    boms = {"boms":[
        {"project_id":"C200","product_code":"C200","bom_version":"V1.0","materials":[
            {"material_code":"MC001","material_name":"锂电池组(18650)","spec":"3.7V 2600mAh","unit":"个","standard_qty":4},
            {"material_code":"MC002","material_name":"PCB主板","spec":"BMS-V3.0","unit":"片","standard_qty":1},
            {"material_code":"MC003","material_name":"外壳(上盖)","spec":"ABS材质 白色","unit":"个","standard_qty":1},
            {"material_code":"MC004","material_name":"外壳(下盖)","spec":"ABS材质 白色","unit":"个","standard_qty":1},
            {"material_code":"MC005","material_name":"USB-C接口模块","spec":"TYPE-C 5A","unit":"个","standard_qty":2},
            {"material_code":"MC006","material_name":"电量显示板","spec":"LED 4格","unit":"片","standard_qty":1},
            {"material_code":"MC007","material_name":"螺丝包","spec":"M2.0*6mm","unit":"包","standard_qty":1},
        ],"substitute_info":[{"material_code":"MC001","substitute_code":"MC001-B","substitute_name":"锂电池组(18650) 替代料","reason":"产能不足"}]},
    ]}
    with open(os.path.join(MOCK_DIR,"business-data","bom_data.json"),"w",encoding="utf-8") as f:
        json.dump(boms,f,ensure_ascii=False,indent=2)
    print(f"BOM data: OK")

    # ===== 其他数据文件 =====
    # 库存数据
    inventory = {"items":[
        {"id":"MC001","material":"MC001","material_code":"MC001","warehouse":"主仓库","available":15000,"min_stock":500,"in_transit":3000,"batch_date":"2026-06-15"},
        {"id":"MC005","material":"MC005","material_code":"MC005","warehouse":"主仓库","available":3000,"min_stock":1000,"in_transit":5000,"batch_date":"2026-06-20"},
        {"id":"MC002","material":"MC002","material_code":"MC002","warehouse":"电子料仓","available":500,"min_stock":2000,"in_transit":8000,"batch_date":"2026-06-10"},
    ]}
    with open(os.path.join(MOCK_DIR,"business-data","inventory_data.json"),"w",encoding="utf-8") as f:
        json.dump(inventory,f,ensure_ascii=False,indent=2)
    print(f"Inventory data: OK")

    # 竞品数据
    competitors = {"competitors":[
        {"name":"竞品科技A","product":"PowerBank200","price":89.0,"capacity":"20000mAh","market_share":0.25,"strength":"品牌知名度高","weakness":"价格高"},
        {"name":"竞品科技B","product":"ChargePro100","price":49.0,"capacity":"10000mAh","market_share":0.18,"strength":"性价比高","weakness":"品控不稳定"},
    ]}
    with open(os.path.join(MOCK_DIR,"business-data","competitor_data.json"),"w",encoding="utf-8") as f:
        json.dump(competitors,f,ensure_ascii=False,indent=2)
    print(f"Competitor data: OK")

    # 物料价格
    prices = {"materials":[
        {"name":"锂电池(18650)","current_price":12.5,"trend":"up","supply_status":"紧张","volatility":"高"},
        {"name":"锂电池组(18650)","current_price":45.0,"trend":"up","supply_status":"紧张","volatility":"高"},
        {"name":"PCB主板","current_price":8.5,"trend":"stable","supply_status":"充足","volatility":"低"},
    ]}
    with open(os.path.join(MOCK_DIR,"business-data","material_prices.json"),"w",encoding="utf-8") as f:
        json.dump(prices,f,ensure_ascii=False,indent=2)
    print(f"Material prices: OK")

    print("All mock data generated (含倍用心接口数据)!")
    print("数据域覆盖：订单与BOM | 库存与物料 | 采购与供应商 | 生产与进度 | 财务与收款 | CRM与客户")

if __name__ == "__main__":
    run()