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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)