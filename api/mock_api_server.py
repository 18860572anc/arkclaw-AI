#!/usr/bin/env python3
"""倍斯特Mock API服务 - 模拟黑云系统及各平台接口
FastAPI 服务，提供所有测试场景所需的Mock接口
"""

import json
import os
import random
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import Optional

app = FastAPI(title="倍斯特Mock API", version="1.0.0", description="倍斯特测试数据框架Mock API服务")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# ==================== 数据加载 ====================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOCK_DATA_DIR = os.path.join(BASE_DIR, "data", "mock", "business-data")

def load_json(filename):
    path = os.path.join(MOCK_DATA_DIR, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# 缓存数据
_customers = {}
_orders = {}
_traffic = {}
_competitors = {}
_boms = {}
_inventory = {}
_prices = {}

def reload_data():
    global _customers, _orders, _traffic, _competitors, _boms, _inventory, _prices
    _customers = load_json("customer_data.json")
    _orders = load_json("order_data.json")
    _traffic = load_json("traffic_data.json")
    _competitors = load_json("competitor_data.json")
    _boms = load_json("bom_data.json")
    _inventory = load_json("inventory_data.json")
    _prices = load_json("material_prices.json")

reload_data()

# ==================== 黑云系统接口 ====================

@app.get("/api/heiyun/bom/{project_id}")
async def get_bom(project_id: str):
    """获取项目BOM物料清单"""
    if _boms:
        for b in _boms.get("boms", []):
            if b["project_id"] == project_id:
                return b
    raise HTTPException(status_code=404, detail={"code": "PROJECT_NOT_FOUND", "message": f"项目{project_id}不存在"})

@app.get("/api/heiyun/orders")
async def get_orders(status: Optional[str] = None, customer: Optional[str] = None):
    """获取订单列表"""
    orders = _orders.get("orders", [])
    if status:
        orders = [o for o in orders if o["status"] == status]
    if customer:
        orders = [o for o in orders if o["customer"] == customer]
    return {"orders": orders, "total": len(orders)}

@app.get("/api/heiyun/orders/{order_id}")
async def get_order(order_id: str):
    """获取单个订单详情"""
    for o in _orders.get("orders", []):
        if o["id"] == order_id:
            return o
    raise HTTPException(status_code=404, detail={"code": "ORDER_NOT_FOUND", "message": f"订单{order_id}不存在"})

@app.get("/api/heiyun/customers")
async def get_customers(status: Optional[str] = None, dormant: Optional[bool] = None):
    """获取客户列表"""
    customers = _customers.get("customers", [])
    if dormant is not None:
        customers = [c for c in customers if c["is_dormant"] == dormant]
    return {"customers": customers, "total": len(customers)}

@app.get("/api/heiyun/customers/{customer_id}")
async def get_customer(customer_id: str):
    """获取单个客户详情"""
    for c in _customers.get("customers", []):
        if c["id"] == customer_id:
            return c
    raise HTTPException(status_code=404, detail={"code": "CUSTOMER_NOT_FOUND", "message": f"客户{customer_id}不存在"})

@app.get("/api/heiyun/inventory")
async def get_inventory(warehouse: Optional[str] = None, low_stock: Optional[bool] = None):
    """获取库存数据"""
    items = _inventory.get("items", [])
    if warehouse:
        items = [i for i in items if i["warehouse"] == warehouse]
    if low_stock:
        items = [i for i in items if i["available"] <= i["min_stock"]]
    return {"items": items, "total": len(items)}

# ==================== 平台流量接口 ====================

@app.get("/api/platform/{platform}/metrics")
async def get_platform_metrics(platform: str, date: Optional[str] = None):
    """获取平台流量数据"""
    if _traffic:
        records = _traffic.get("traffic", [])
        filtered = [r for r in records if r["platform"] == platform]
        if date:
            filtered = [r for r in filtered if r["date"] == date]
        if filtered:
            return {"platform": platform, "records": filtered, "total": len(filtered)}
    # 返回动态生成数据
    return {
        "platform": platform,
        "date": date or datetime.now().strftime("%Y-%m-%d"),
        "metrics": {
            "impressions": random.randint(10000, 100000),
            "clicks": random.randint(500, 5000),
            "visitors": random.randint(300, 3000),
            "inquiries": random.randint(5, 100),
            "gmv": round(random.uniform(5000, 80000), 2),
        },
        "trend": random.choice(["up", "down", "stable"]),
        "change_pct": round(random.uniform(-25, 35), 1),
    }

# ==================== 竞品分析接口 ====================

@app.get("/api/competitors")
async def get_competitors():
    """获取竞品列表"""
    return _competitors

@app.get("/api/competitors/{name}")
async def get_competitor(name: str):
    """获取单个竞品详情"""
    for c in _competitors.get("competitors", []):
        if c["name"] == name:
            return c
    raise HTTPException(status_code=404, detail={"code": "COMPETITOR_NOT_FOUND", "message": f"竞品{name}不存在"})

# ==================== 元器件行情接口 ====================

@app.get("/api/market/prices")
async def get_market_prices(material: Optional[str] = None):
    """获取元器件行情"""
    materials = _prices.get("materials", [])
    if material:
        materials = [m for m in materials if m["name"] == material]
    return {"materials": materials, "total": len(materials)}

# ==================== 健康检查 ====================

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "beste-mock-api", "version": "1.0.0", "timestamp": datetime.now().isoformat()}

@app.get("/api/status")
async def api_status():
    """数据源状态检查"""
    return {
        "heiyun": bool(_orders.get("orders")),
        "customers": bool(_customers.get("customers")),
        "traffic": bool(_traffic.get("traffic")),
        "competitors": bool(_competitors.get("competitors")),
        "inventory": bool(_inventory.get("items")),
        "prices": bool(_prices.get("materials")),
        "data_loaded": all([_orders, _customers, _traffic]),
    }

# ==================== 数据重置接口 ====================

@app.post("/api/admin/reload")
async def reload_mock_data():
    """重新加载Mock数据"""
    reload_data()
    return {"status": "ok", "message": "数据已重新加载"}


# ==================== 新增场景API端点 ====================

# --- OEM快速设计 ---
@app.get("/api/oem/supported-capacities")
async def oem_supported_capacities():
    data = load_json("oem_data.json")
    return {"supported_capacities": data.get("supported_capacities", []), "supported_colors": data.get("supported_colors", [])}

@app.get("/api/oem/design-template")
async def oem_design_template(product_type: str, capacity: str):
    data = load_json("oem_data.json")
    for t in data.get("design_templates", []):
        if t["product_type"] == product_type and t["capacity"] == capacity:
            return t
    raise HTTPException(status_code=404, detail={"code": "TEMPLATE_NOT_FOUND", "message": f"产品{product_type}容量{capacity}的设计模板不存在"})

@app.post("/api/oem/scheme")
async def oem_generate_scheme():
    data = load_json("oem_data.json")
    schemes = data.get("schemes", [])
    if schemes:
        return schemes[0]
    raise HTTPException(status_code=500, detail={"code": "DESIGN_SERVICE_DOWN", "message": "设计服务暂时不可用"})

# --- 海外B端售前助理 ---
@app.get("/api/overseas/supported-regions")
async def overseas_regions():
    data = load_json("overseas_data.json")
    return {"regions": data.get("supported_regions", []), "delivery_terms": data.get("delivery_terms", [])}

@app.get("/api/overseas/price-factors/{region}")
async def overseas_price_factors(region: str):
    data = load_json("overseas_data.json")
    factors = data.get("price_factors", {})
    if region in factors:
        return factors[region]
    raise HTTPException(status_code=404, detail={"code": "REGION_NOT_SUPPORTED", "message": f"区域{region}不支持"})

@app.get("/api/overseas/inquiries")
async def overseas_inquiries():
    data = load_json("overseas_data.json")
    return {"inquiries": data.get("overseas_inquiries", [])}

# --- 订单派发 ---
@app.post("/api/orders/dispatch")
async def order_dispatch(order_id: str, factory: str):
    orders = load_json("order_data.json").get("orders", [])
    order = None
    for o in orders:
        if o["id"] == order_id:
            order = o
            break
    if not order:
        raise HTTPException(status_code=404, detail={"code": "ORDER_NOT_FOUND", "message": f"订单{order_id}不存在"})
    # Check factory exists
    prod = load_json("production_data.json")
    factories = set(pl["factory"] for pl in prod.get("production_lines", []))
    if factory not in factories:
        raise HTTPException(status_code=400, detail={"code": "FACTORY_NOT_FOUND", "message": f"工厂{factory}不存在"})
    return {"dispatched": True, "order_id": order_id, "factory": factory, "assigned_line": "PL001", "estimated_start": "2026-07-18"}

# --- 订单进度管理 ---
@app.get("/api/orders/{order_id}/progress")
async def order_progress(order_id: str):
    risk = load_json("order_risk_data.json")
    for tl in risk.get("order_timelines", []):
        if tl["order_id"] == order_id:
            return tl
    raise HTTPException(status_code=404, detail={"code": "ORDER_NOT_FOUND", "message": f"订单{order_id}不存在"})

# --- 订单统筹及风险预警 ---
@app.get("/api/orders/risk-alerts")
async def order_risk_alerts(time_range: str):
    if not time_range:
        raise HTTPException(status_code=400, detail={"code": "INVALID_PARAM", "message": "时间范围不能为空"})
    risk = load_json("order_risk_data.json")
    return {"risk_alerts": risk.get("risk_alerts", []), "total": len(risk.get("risk_alerts", []))}

# --- 智能回款 ---
@app.get("/api/finance/receivables")
async def get_receivables(customer_id: Optional[str] = None):
    fin = load_json("finance_data.json")
    rcv = fin.get("receivables", [])
    if customer_id:
        rcv = [r for r in rcv if r["customer_id"] == customer_id]
    return {"receivables": rcv, "total": len(rcv)}

@app.get("/api/finance/receivables/{customer_id}/collection-plan")
async def collection_plan(customer_id: str, overdue_days: int):
    if overdue_days < 0:
        raise HTTPException(status_code=400, detail={"code": "INVALID_PARAM", "message": "逾期天数不能为负"})
    fin = load_json("finance_data.json")
    for r in fin.get("receivables", []):
        if r["customer_id"] == customer_id:
            return {"customer_id": customer_id, "amount": r["amount"], "overdue_days": overdue_days, "suggested_action": "发送催收函" if overdue_days < 60 else "法律警告"}
    raise HTTPException(status_code=404, detail={"code": "CUSTOMER_NOT_FOUND", "message": f"客户{customer_id}不存在"})

# --- 商务部门报表 ---
@app.get("/api/department/{department}/report")
async def department_report(department: str, period: str):
    valid_depts = ["商务部", "制造中心", "销售部", "研发部", "管理中心"]
    if department not in valid_depts:
        raise HTTPException(status_code=400, detail={"code": "DEPARTMENT_NOT_FOUND", "message": f"部门{department}不存在"})
    return {"department": department, "period": period, "contract_amount": 2500000, "signed_count": 8, "collection_rate": 0.75, "active_projects": 12}

# --- 提成核算 ---
@app.get("/api/commission/calculate")
async def calculate_commission(sales_person: str, period: str):
    fin = load_json("finance_data.json")
    for rec in fin.get("commission_records", []):
        if rec["sales_person"] == sales_person and rec["period"] == period:
            return rec
    # Check if sales person exists
    hr_data = load_json("hr_data.json")
    emp_names = [e["name"] for e in hr_data.get("employees", [])]
    if sales_person not in emp_names:
        raise HTTPException(status_code=404, detail={"code": "EMPLOYEE_NOT_FOUND", "message": f"员工{sales_person}不存在"})
    return {"sales_person": sales_person, "period": period, "base_commission": 0, "bonus": 0, "deduction": 0, "net_amount": 0}

# --- 智能报价 ---
@app.get("/api/pricing/quote")
async def generate_quote(product_id: str, qty: int, customer_level: str = "B"):
    if qty <= 0:
        raise HTTPException(status_code=400, detail={"code": "INVALID_QTY", "message": "数量必须大于0"})
    pricing_data = load_json("pricing_data.json")
    base_prices = pricing_data.get("base_prices", {})
    if product_id not in base_prices:
        raise HTTPException(status_code=404, detail={"code": "PRODUCT_NOT_FOUND", "message": f"产品{product_id}不存在"})
    base_price = base_prices[product_id]
    discount_rules = pricing_data.get("discount_rules", {})
    discount = discount_rules.get(customer_level, {}).get("discount_rate", 0)
    unit_price = round(base_price * (1 - discount), 2)
    total = round(unit_price * qty, 2)
    return {"product_id": product_id, "unit_price": unit_price, "qty": qty, "total": total, "discount": discount, "valid_until": "2026-08-15"}

# --- 内部协作与CRM监控 ---
@app.get("/api/crm/dashboard")
async def crm_dashboard(time_range: str):
    crm_data = load_json("crm_data.json")
    return crm_data.get("crm_dashboard", {})

@app.get("/api/crm/collaboration-tasks")
async def collaboration_tasks():
    crm_data = load_json("crm_data.json")
    return {"tasks": crm_data.get("collaboration_tasks", [])}

# --- 人员分析与考核 ---
@app.get("/api/hr/performance/{department}")
async def performance_analysis(department: str, period: str):
    hr_data = load_json("hr_data.json")
    if department not in hr_data.get("departments", []):
        raise HTTPException(status_code=400, detail={"code": "DEPARTMENT_NOT_FOUND", "message": f"部门{department}不存在"})
    emps = [e for e in hr_data.get("employees", []) if e["department"] == department]
    if not emps:
        raise HTTPException(status_code=404, detail={"code": "NO_DATA", "message": "该部门无员工数据"})
    avg_score = sum(e["kpi_score"] for e in emps) / len(emps)
    return {"department": department, "period": period, "avg_kpi_score": round(avg_score, 1), "employee_count": len(emps), "employees": emps}

# --- 产品图库检索 ---
@app.get("/api/gallery/search")
async def search_gallery(keyword: str, category: str = "产品图"):
    gallery = load_json("gallery_data.json")
    results = [img for img in gallery.get("images", []) if keyword.lower() in img["name"].lower() or any(keyword.lower() in t.lower() for t in img.get("tags", []))]
    if not results:
        raise HTTPException(status_code=404, detail={"code": "MATCH_NOT_FOUND", "message": "未找到匹配图片"})
    return {"results": results, "total": len(results)}

# --- 生产排产 ---
@app.post("/api/production/schedule")
async def schedule_production():
    prod = load_json("production_data.json")
    schedules = prod.get("schedules", [])
    if schedules:
        return schedules[0]
    return {"message": "无排产计划"}

# --- 品质管理总结 ---
@app.get("/api/quality/monthly/{period}")
async def quality_monthly(period: str):
    if period >= "2099":
        raise HTTPException(status_code=400, detail={"code": "INVALID_PERIOD", "message": "时间段无效"})
    prod = load_json("production_data.json")
    for qm in prod.get("quality_metrics", []):
        if qm["period"] == period:
            return qm
    raise HTTPException(status_code=404, detail={"code": "NO_DATA", "message": "该时间段无品质数据"})

# --- 工艺改进分析 ---
@app.get("/api/production/process-analysis")
async def process_analysis(product_line: str, period: str):
    prod = load_json("production_data.json")
    for pl in prod.get("production_lines", []):
        if pl["name"] == product_line:
            return {"product_line": product_line, "period": period, "current_efficiency": pl["current_efficiency"], "bottleneck": pl["bottleneck"], "improvement_suggestions": ["优化瓶颈工序", "增加自动化设备"]}
    raise HTTPException(status_code=404, detail={"code": "LINE_NOT_FOUND", "message": f"产线{product_line}不存在"})

# --- 客诉根因分析 ---
@app.get("/api/quality/complaint/{complaint_id}")
async def complaint_analysis(complaint_id: str):
    prod = load_json("production_data.json")
    for c in prod.get("complaints", []):
        if c["id"] == complaint_id:
            return c
    raise HTTPException(status_code=404, detail={"code": "COMPLAINT_NOT_FOUND", "message": f"投诉{complaint_id}不存在"})

# --- 阿米巴经营数据分析 ---
@app.get("/api/amoeba/accounting")
async def amoeba_accounting(unit: str, period: str):
    hr_data = load_json("hr_data.json")
    for u in hr_data.get("amoeba_units", []):
        if u["unit"] == unit and u["period"] == period:
            return u
    raise HTTPException(status_code=404, detail={"code": "UNIT_NOT_FOUND", "message": f"阿米巴单元{unit}不存在"})

# --- 企业文化总结 ---
@app.get("/api/hr/culture-summary/{period}")
async def culture_summary(period: str):
    hr_data = load_json("hr_data.json")
    activities = [a for a in hr_data.get("culture_activities", []) if a["period"] == period]
    if not activities:
        raise HTTPException(status_code=404, detail={"code": "NO_ACTIVITIES", "message": "该期间无活动记录"})
    total_participants = sum(a["participants"] for a in activities)
    avg_score = sum(a["feedback_score"] for a in activities) / len(activities)
    return {"period": period, "activity_count": len(activities), "total_participants": total_participants, "avg_feedback_score": round(avg_score, 1), "activities": activities}

# --- 内部政策校验分析 ---
@app.get("/api/policy/check")
async def policy_check(document: str, policy_id: str):
    policies = load_json("../data/source/policies/policies_data.json") if os.path.exists(os.path.join(BASE_DIR, "data/source/policies/policies_data.json")) else {"policies": []}
    # Actually load from source
    src_path = os.path.join(BASE_DIR, "data/source/policies", "policies_data.json")
    if os.path.exists(src_path):
        with open(src_path, "r", encoding="utf-8") as f:
            policies = json.load(f)
    for p in policies.get("policies", []):
        if p["id"] == policy_id:
            return {"document": document, "policy_id": policy_id, "policy_name": p["name"], "is_compliant": True, "detail": "报销单符合报销管理制度规定"}
    raise HTTPException(status_code=404, detail={"code": "POLICY_NOT_FOUND", "message": f"政策{policy_id}不存在"})

# --- 政府政策匹配 ---
@app.get("/api/gov/policy-match")
async def policy_match(company_industry: str, company_region: str, revenue: str):
    if not company_industry:
        raise HTTPException(status_code=400, detail={"code": "INVALID_INDUSTRY", "message": "行业不能为空"})
    gov = load_json("gov_policy_data.json")
    matched = [p for p in gov.get("policies", []) if company_industry.lower() in p["industry"].lower() or company_region.lower() in p["region"].lower()]
    return {"matched_policies": matched, "matched_count": len(matched)}

# --- 公司资质规划 ---
@app.get("/api/gov/qualification-plan")
async def qualification_plan(company_stage: str, target_markets: str):
    if not target_markets:
        raise HTTPException(status_code=400, detail={"code": "INVALID_MARKETS", "message": "目标市场不能为空"})
    gov = load_json("gov_policy_data.json")
    quals = gov.get("qualifications", {})
    return {"company_stage": company_stage, "current_qualifications": quals.get("current", []), "needed_qualifications": quals.get("needed", []), "roadmap": quals.get("roadmap", [])}

# --- 人才分析 ---
@app.get("/api/hr/talent-review/{department}")
async def talent_review(department: str):
    hr_data = load_json("hr_data.json")
    if department not in hr_data.get("departments", []):
        raise HTTPException(status_code=400, detail={"code": "DEPARTMENT_NOT_FOUND", "message": f"部门{department}不存在"})
    emps = [e for e in hr_data.get("employees", []) if e["department"] == department]
    key_talents = [e for e in emps if e["is_key_talent"]]
    return {"department": department, "total_employees": len(emps), "key_talents": key_talents, "avg_tenure": round(sum(e["tenure_years"] for e in emps) / len(emps), 1) if emps else 0, "risk_analysis": "低流失风险"}

# --- 会计分目(做账) ---
@app.post("/api/finance/voucher")
async def generate_voucher():
    return {"voucher_id": "VCH20260716001", "entries": [{"account": "应收账款", "debit": 50000, "credit": 0}, {"account": "主营业务收入", "debit": 0, "credit": 50000}], "summary": "销售商品确认收入"}

# --- 智能报税 ---
@app.get("/api/finance/tax-filing")
async def tax_filing(tax_type: str, period: str):
    if not tax_type:
        raise HTTPException(status_code=400, detail={"code": "INVALID_TAX_TYPE", "message": "税种不能为空"})
    fin = load_json("finance_data.json")
    rates = fin.get("tax_rates", {})
    tax_info = rates.get(tax_type, {})
    return {"tax_type": tax_type, "period": period, "output_tax": 65000, "input_tax": 45000, "tax_due": 20000, "deadline": tax_info.get("deadline", "次月15日")}

# --- 市场行情预测 ---
@app.get("/api/market/forecast")
async def market_forecast(material: str, horizon_months: int):
    prices = load_json("material_prices.json")
    for m in prices.get("materials", []):
        if m["name"] == material:
            return {"material": material, "current_price": m["current_price"], "trend": m["trend"], "supply_status": m["supply_status"], "forecast": f"预计未来{horizon_months}个月价格上涨10-15%", "suggestion": "建议增加采购库存"}
    raise HTTPException(status_code=404, detail={"code": "MATERIAL_NOT_FOUND", "message": f"材料{material}不存在"})

# --- 供应商比价 ---
@app.get("/api/suppliers/compare")
async def supplier_compare(material: str, qty: int):
    suppliers = load_json("supplier_data.json").get("suppliers", [])
    if not suppliers:
        raise HTTPException(status_code=400, detail={"code": "NO_SUPPLIERS", "message": "供应商列表为空"})
    results = []
    for s in suppliers:
        est_price = round(random.uniform(10, 50) * (1 - (s["rating"] - 4) * 0.05), 2)
        results.append({"supplier_id": s["id"], "name": s["name"], "unit_price": est_price, "total": round(est_price * qty, 2), "delivery_days": random.randint(15, 45), "rating": s["rating"], "score": round(s["rating"] * 0.4 + (1 - est_price / 50) * 0.3 + s["delivery_punctuality"] * 0.3, 2)})
    results.sort(key=lambda x: x["score"], reverse=True)
    for i, r in enumerate(results):
        r["rank"] = i + 1
    return {"material": material, "qty": qty, "comparison": results}

# --- 供应商评价 ---
@app.get("/api/suppliers/{supplier_id}/evaluate")
async def supplier_evaluate(supplier_id: str, dimensions: str):
    if not dimensions:
        raise HTTPException(status_code=400, detail={"code": "INVALID_DIMENSIONS", "message": "评价维度不能为空"})
    suppliers = load_json("supplier_data.json").get("suppliers", [])
    for s in suppliers:
        if s["id"] == supplier_id:
            dims = [d.strip() for d in dimensions.split(",")]
            scores = {d: round(random.uniform(3.5, 5.0), 1) for d in dims}
            avg_score = round(sum(scores.values()) / len(scores), 1)
            level = "A" if avg_score >= 4.5 else "B" if avg_score >= 4.0 else "C"
            return {"supplier_id": supplier_id, "name": s["name"], "dimension_scores": scores, "overall_score": avg_score, "level": level}
    raise HTTPException(status_code=404, detail={"code": "SUPPLIER_NOT_FOUND", "message": f"供应商{supplier_id}不存在"})

# --- 海外物流报价 ---
@app.get("/api/logistics/quote")
async def logistics_quote(origin: str, destination: str, weight_kg: float, volume_cbm: float):
    log = load_json("logistics_data.json")
    routes = [r for r in log.get("shipping_routes", []) if r["destination"] == destination]
    if not routes:
        raise HTTPException(status_code=404, detail={"code": "DESTINATION_NOT_SUPPORTED", "message": f"目的地{destination}不支持"})
    options = []
    for r in routes:
        if weight_kg >= r.get("min_kg", 0):
            freight = round(r["cost_per_kg"] * weight_kg + r.get("cost_per_cbm", 0) * volume_cbm, 2)
            options.append({"mode": r["mode"], "carrier": r["carrier"], "freight": freight, "transit_days": r["transit_days"], "total_cost": freight})
    return {"origin": origin, "destination": destination, "weight_kg": weight_kg, "volume_cbm": volume_cbm, "options": options}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)