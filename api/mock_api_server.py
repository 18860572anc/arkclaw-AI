#!/usr/bin/env python3
"""倍斯特Mock API服务 - 模拟黑云系统及各平台接口 + 倍用心系统接口
FastAPI 服务，提供所有测试场景所需的Mock接口
"""

import json
import os
import random
import uvicorn
from fastapi import FastAPI, HTTPException, Query, APIRouter
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import Optional

app = FastAPI(
    title="倍斯特Mock API",
    version="2.0.0",
    description="倍斯特测试数据框架Mock API服务（含倍用心系统接口）",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ==================== 统一响应格式 ====================

def api_response(data=None, code=0, message="success", http_status=200):
    """统一API成功响应格式"""
    return JSONResponse(
        content={
            "code": code,
            "message": message,
            "data": data,
            "timestamp": datetime.now().isoformat()
        },
        status_code=http_status
    )

def api_error(code="ERROR", message="Unknown error", http_status=400):
    """统一API错误响应格式"""
    return JSONResponse(
        content={
            "code": code,
            "message": message,
            "data": None,
            "timestamp": datetime.now().isoformat()
        },
        status_code=http_status
    )

# ==================== API 版本路由器 ====================
v1_router = APIRouter(prefix="/api/v1")

# ==================== 黑云系统 V1 接口路由 ====================

@v1_router.get("/heiyun/bom/{project_id}", tags=["倍斯特-黑云系统"],
    summary="获取项目BOM物料清单",
    description="V1版本，根据项目ID查询BOM物料清单")
async def get_bom_v1(project_id: str):
    """获取项目BOM物料清单 - V1版本"""
    if _boms:
        for b in _boms.get("boms", []):
            if b["project_id"] == project_id:
                return api_response(data=b)
    return api_error("PROJECT_NOT_FOUND", f"项目{project_id}不存在", http_status=404)

@v1_router.get("/heiyun/orders", tags=["倍斯特-黑云系统"],
    summary="获取订单列表",
    description="V1版本，获取订单列表，支持按状态和客户筛选")
async def get_orders_v1(status: Optional[str] = None, customer: Optional[str] = None):
    """获取订单列表 - V1版本"""
    orders = _orders.get("orders", [])
    if status:
        orders = [o for o in orders if o["status"] == status]
    if customer:
        orders = [o for o in orders if o["customer"] == customer]
    return api_response(data={"orders": orders, "total": len(orders)})

@v1_router.get("/heiyun/orders/{order_id}", tags=["倍斯特-黑云系统"],
    summary="获取订单详情",
    description="V1版本，根据订单ID获取订单详细信息")
async def get_order_v1(order_id: str):
    """获取订单详情 - V1版本"""
    for o in _orders.get("orders", []):
        if o["id"] == order_id:
            return api_response(data=o)
    return api_error("ORDER_NOT_FOUND", f"订单{order_id}不存在", http_status=404)

@v1_router.get("/heiyun/customers", tags=["倍斯特-黑云系统"],
    summary="获取客户列表",
    description="V1版本，获取客户列表，支持按状态和休眠状态筛选")
async def get_customers_v1(status: Optional[str] = None, dormant: Optional[bool] = None):
    """获取客户列表 - V1版本"""
    customers = _customers.get("customers", [])
    if dormant is not None:
        customers = [c for c in customers if c["is_dormant"] == dormant]
    return api_response(data={"customers": customers, "total": len(customers)})

@v1_router.get("/heiyun/customers/{customer_id}", tags=["倍斯特-黑云系统"],
    summary="获取客户详情",
    description="V1版本，根据客户ID获取客户详细信息")
async def get_customer_v1(customer_id: str):
    """获取客户详情 - V1版本"""
    for c in _customers.get("customers", []):
        if c["id"] == customer_id:
            return api_response(data=c)
    return api_error("CUSTOMER_NOT_FOUND", f"客户{customer_id}不存在", http_status=404)

@v1_router.get("/heiyun/inventory", tags=["倍斯特-黑云系统"],
    summary="获取库存数据",
    description="V1版本，获取库存数据，支持按仓库和低库存预警筛选")
async def get_inventory_v1(warehouse: Optional[str] = None, low_stock: Optional[bool] = None):
    """获取库存数据 - V1版本"""
    items = _inventory.get("items", [])
    if warehouse:
        items = [i for i in items if i["warehouse"] == warehouse]
    if low_stock:
        items = [i for i in items if i["available"] <= i["min_stock"]]
    return api_response(data={"items": items, "total": len(items)})


# ==================== 倍用心系统 V1 接口路由 ====================

@v1_router.get("/beiyongxin/bom/query", tags=["倍斯特-倍用心系统"],
    summary="BOM清单查询",
    description="[V1] 获取产品BOM清单 - 采购需求智能分析(P0)、物料齐套协调(P0)")
async def byx_bom_query_v1(product_code: str = Query(..., description="成品编号/产品型号")):
    """[倍用心] BOM清单查询 - V1版本"""
    if _boms:
        for b in _boms.get("boms", []):
            if b.get("project_id") == product_code or b.get("product_code") == product_code:
                return api_response(data={
                    "product_code": product_code, "bom_version": b.get("bom_version", "V1.0"),
                    "materials": b.get("materials", []),
                    "optional_fields": {"material_types": ["结构件", "电子件", "包材"], "bom_version": b.get("bom_version", "V1.0"), "substitute_info": b.get("substitute_info", [])},
                    "dependency": "partial", "transition_note": "10月前可人工导出BOM过渡"
                })
    return api_response(data={
        "product_code": product_code, "bom_version": "V1.0",
        "materials": [
            {"material_code": "MC001", "material_name": "锂电池组(18650)", "spec": "3.7V 2600mAh", "unit": "个", "standard_qty": 4},
            {"material_code": "MC002", "material_name": "PCB主板", "spec": "BMS-V3.0", "unit": "片", "standard_qty": 1},
            {"material_code": "MC003", "material_name": "外壳(上盖)", "spec": "ABS材质 白色", "unit": "个", "standard_qty": 1},
            {"material_code": "MC004", "material_name": "外壳(下盖)", "spec": "ABS材质 白色", "unit": "个", "standard_qty": 1},
            {"material_code": "MC005", "material_name": "USB-C接口模块", "spec": "TYPE-C 5A", "unit": "个", "standard_qty": 2},
            {"material_code": "MC006", "material_name": "电量显示板", "spec": "LED 4格", "unit": "片", "standard_qty": 1},
            {"material_code": "MC007", "material_name": "螺丝包", "spec": "M2.0*6mm", "unit": "包", "standard_qty": 1}
        ],
        "optional_fields": {
            "material_types": {"MC001": "电子件", "MC002": "电子件", "MC003": "结构件", "MC004": "结构件", "MC005": "电子件", "MC006": "电子件", "MC007": "结构件"},
            "bom_version": "V1.0",
            "substitute_info": [{"material_code": "MC001", "substitute_code": "MC001-B", "substitute_name": "锂电池组(18650) 替代料", "reason": "产能不足"}]
        },
        "dependency": "partial", "transition_note": "10月前可人工导出BOM过渡"
    })

@v1_router.get("/beiyongxin/orders/query", tags=["倍斯特-倍用心系统"],
    summary="订单信息查询",
    description="[V1] 获取订单主数据及明细（●强依赖）")
async def byx_order_query_v1(
    order_no: Optional[str] = Query(None, description="订单号"),
    date_from: Optional[str] = Query(None, description="开始日期"),
    date_to: Optional[str] = Query(None, description="结束日期"),
    customer_code: Optional[str] = Query(None, description="客户编号")):
    """[倍用心] 订单信息查询 - V1版本"""
    orders = _orders.get("orders", [])
    if order_no:
        orders = [o for o in orders if o.get("id") == order_no]
    if not orders:
        orders = [
            {"id": "ORD1001", "customer": "客户A", "product_model": "C200充电宝", "quantity": 5000, "unit_price": 45.0, "delivery_date": "2026-08-15", "order_date": "2026-07-01", "status": "生产中", "work_order_no": "WO20260701001"},
            {"id": "ORD1002", "customer": "客户B", "product_model": "CS12充电柜", "quantity": 200, "unit_price": 3200.0, "delivery_date": "2026-08-30", "order_date": "2026-07-05", "status": "生产中", "work_order_no": "WO20260705001"},
            {"id": "ORD1003", "customer": "客户C", "product_model": "C100充电宝", "quantity": 10000, "unit_price": 28.0, "delivery_date": "2026-09-01", "order_date": "2026-07-10", "status": "待审核", "work_order_no": ""},
        ]
    result = []
    for o in orders:
        result.append({
            "order_no": o.get("id", ""), "customer_name": o.get("customer", ""),
            "product_model": o.get("product_model", o.get("product", "")), "quantity": o.get("quantity", o.get("qty", 0)),
            "unit_price": o.get("unit_price", o.get("price", 0)), "delivery_date": o.get("delivery_date", o.get("delivery", "")),
            "order_date": o.get("order_date", o.get("date", "")),
            "optional_fields": {"order_status": o.get("status", "生产中"), "work_order_no": o.get("work_order_no", "")}
        })
    return api_response(data={"orders": result, "total": len(result), "dependency": "strong"})

@v1_router.post("/beiyongxin/orders/status-change", tags=["倍斯特-倍用心系统"],
    summary="订单状态变更推送",
    description="[V1] 订单状态变更主动推送（事件触发）（●强依赖）")
async def byx_status_change_v1(payload: dict):
    """[倍用心] 订单状态变更推送 - V1版本"""
    order_no = payload.get("order_no", "")
    if not order_no:
        return api_error("INVALID_ORDER", "订单号不能为空", http_status=400)
    return api_response(data={
        "acknowledged": True, "order_no": order_no,
        "old_status": payload.get("old_status", ""), "new_status": payload.get("new_status", ""),
        "change_time": payload.get("change_time", datetime.now().isoformat()),
        "change_reason": payload.get("change_reason", ""),
        "processed_at": datetime.now().isoformat(), "dependency": "strong"
    })

@v1_router.get("/beiyongxin/orders/delivery", tags=["倍斯特-倍用心系统"],
    summary="订单交期数据",
    description="[V1] 获取订单交期及进度（●强依赖）")
async def byx_delivery_data_v1(order_no: str = Query(..., description="订单编号")):
    """[倍用心] 订单交期数据 - V1版本"""
    if not order_no:
        return api_error("INVALID_ORDER", "订单号不能为空", http_status=400)
    return api_response(data={
        "order_no": order_no, "promised_delivery": "2026-08-15", "current_progress_pct": 45,
        "milestones": [
            {"node": "物料齐套", "planned": "2026-07-10", "actual": "2026-07-08"},
            {"node": "SMT贴片", "planned": "2026-07-15", "actual": None},
            {"node": "组装测试", "planned": "2026-07-25", "actual": None},
            {"node": "成品入库", "planned": "2026-08-10", "actual": None},
        ],
        "actual_completion": None, "dependency": "strong"
    })

@v1_router.get("/beiyongxin/inventory/real-time", tags=["倍斯特-倍用心系统"],
    summary="实时库存查询",
    description="[V1] 查询物料实时库存（●强依赖）")
async def byx_inventory_query_v1(
    material_code: str = Query(..., description="物料编码"),
    warehouse_code: Optional[str] = Query(None, description="仓库编码")):
    if not material_code:
        return api_error("INVALID_MATERIAL", "物料编码不能为空", http_status=400)
    return api_response(data={
        "material_code": material_code, "available_qty": random.randint(1000, 30000), "in_transit_qty": random.randint(500, 5000),
        "optional_fields": {"warehouse_name": "主仓库", "safety_stock": 500, "batch_date": "2026-06-15"},
        "dependency": "strong"
    })

@v1_router.get("/beiyongxin/inventory/shortage", tags=["倍斯特-倍用心系统"],
    summary="欠料明细查询",
    description="[V1] 查询订单欠料明细（●强依赖）")
async def byx_shortage_query_v1(order_no: str = Query(..., description="订单编号/工单编号")):
    if not order_no:
        return api_error("INVALID_ORDER", "订单编号不能为空", http_status=400)
    return api_response(data={
        "order_no": order_no,
        "shortage_details": [
            {"material_code": "MC001", "material_name": "锂电池组(18650)", "required_qty": 20000, "received_qty": 15000, "shortage_qty": 5000, "expected_arrival": "2026-07-20", "optional_fields": {"current_status": "在途", "supplier_name": "供应商A"}},
            {"material_code": "MC005", "material_name": "USB-C接口模块", "required_qty": 5000, "received_qty": 3000, "shortage_qty": 2000, "expected_arrival": "2026-07-18", "optional_fields": {"current_status": "在途", "supplier_name": "供应商B"}},
        ],
        "total_shortage_items": 2, "dependency": "strong"
    })

@v1_router.get("/beiyongxin/inventory/slow-moving", tags=["倍斯特-倍用心系统"],
    summary="呆滞物料清单",
    description="[V1] 获取呆滞物料清单（180天以上未使用）（●强依赖）")
async def byx_slow_moving_v1():
    return api_response(data={
        "slow_moving_items": [
            {"material_code": "SM001", "material_name": "Micro-USB接口模块(旧版)", "stock_qty": 5000, "inbound_date": "2025-06-10", "last_used_date": "2025-12-01", "purchase_order_no": "PO20250601001", "batch_no": "B20250601"},
            {"material_code": "SM002", "material_name": "外壳(旧款黑色)", "stock_qty": 3000, "inbound_date": "2025-08-15", "last_used_date": "2026-01-10", "purchase_order_no": "PO20250815002", "batch_no": "B20250815"},
        ],
        "total_items": 2, "dependency": "strong"
    })

@v1_router.get("/beiyongxin/purchase/orders", tags=["倍斯特-倍用心系统"],
    summary="采购订单查询",
    description="[V1] 获取采购订单及明细（●强依赖）")
async def byx_purchase_orders_v1(
    po_no: Optional[str] = Query(None), supplier_code: Optional[str] = Query(None),
    date_from: Optional[str] = Query(None), date_to: Optional[str] = Query(None)):
    return api_response(data={
        "purchase_orders": [
            {"po_no": "PO20260701001", "supplier_name": "供应商A", "material_code": "MC001", "material_name": "锂电池组(18650)", "purchase_qty": 20000, "delivered_qty": 15000, "undelivered_qty": 5000, "promised_delivery": "2026-07-20", "optional_fields": {"order_status": "部分交货"}},
            {"po_no": "PO20260705002", "supplier_name": "供应商B", "material_code": "MC005", "material_name": "USB-C接口模块", "purchase_qty": 10000, "delivered_qty": 3000, "undelivered_qty": 7000, "promised_delivery": "2026-07-18", "optional_fields": {"order_status": "部分交货"}},
        ],
        "total": 2, "dependency": "strong"
    })

@v1_router.get("/beiyongxin/suppliers/master-data", tags=["倍斯特-倍用心系统"],
    summary="供应商主数据",
    description="[V1] 获取供应商主数据（●强依赖）")
async def byx_supplier_master_v1(
    supplier_code: Optional[str] = Query(None), material_type: Optional[str] = Query(None)):
    supps = _suppliers.get("suppliers", [])
    if not supps:
        supps = [{"id": "SUP001", "name": "供应商A", "type": "电池", "rating": 4.8}]
    if supplier_code:
        supps = [s for s in supps if s.get("id") == supplier_code]
    result = []
    for s in supps:
        result.append({
            "supplier_code": s.get("id", ""), "supplier_name": s.get("name", ""),
            "material_type": s.get("type", ""), "rating": s.get("rating", 0.0),
        })
    return api_response(data={"suppliers": result, "total": len(result), "dependency": "strong"})

@v1_router.get("/beiyongxin/purchase/delivery-status", tags=["倍斯特-倍用心系统"],
    summary="采购交期状态",
    description="[V1] 获取采购订单交期及在途状态（●强依赖）")
async def byx_purchase_delivery_status_v1(po_no: Optional[str] = Query(None)):
    return api_response(data={
        "delivery_statuses": [
            {"po_no": "PO20260701001", "supplier": "供应商A", "material": "锂电池组(18650)", "qty": 20000, "remaining_qty": 5000, "status": "partial", "next_delivery": "2026-07-20", "risk_level": "中"},
        ],
        "total": 1, "dependency": "strong"
    })

@v1_router.get("/beiyongxin/purchase/history", tags=["倍斯特-倍用心系统"],
    summary="历史交易记录",
    description="[V1] 获取供应商历史交易记录（▲部分依赖）")
async def byx_purchase_history_v1(supplier_code: str = Query(..., description="供应商编码"), months: int = Query(12, description="回溯月数")):
    if not supplier_code:
        return api_error("INVALID_SUPPLIER", "供应商编码不能为空", http_status=400)
    return api_response(data={
        "supplier_code": supplier_code, "history_period_months": months,
        "transaction_records": [
            {"date": "2026-06-15", "material": "锂电池组(18650)", "qty": 5000, "unit_price": 12.5, "total_amount": 62500.0, "delivery_status": "completed"},
        ],
        "total_transactions": 1, "total_amount": 62500.0, "avg_delivery_delay_days": 2,
        "dependency": "partial"
    })

@v1_router.get("/beiyongxin/production/warehouse-in", tags=["倍斯特-倍用心系统"],
    summary="产线入库状态",
    description="[V1] 获取产线入库状态（●强依赖）")
async def byx_prod_warehouse_in_v1(factory_code: Optional[str] = Query(None), date: Optional[str] = Query(None)):
    return api_response(data={
        "warehouse_in_records": [
            {"order_no": "ORD1001", "product": "C200充电宝", "factory": "江苏工厂", "line": "充电宝产线A", "planned_qty": 5000, "produced_qty": 3200, "warehoused_qty": 2800, "defect_qty": 15, "yield_rate": 0.973, "warehouse_date": "2026-07-16"},
        ],
        "total": 1, "dependency": "strong"
    })

@v1_router.get("/beiyongxin/production/progress", tags=["倍斯特-倍用心系统"],
    summary="生产进度",
    description="[V1] 获取生产进度（▲部分依赖）")
async def byx_prod_progress_v1(order_no: Optional[str] = Query(None)):
    return api_response(data={
        "production_progress": [
            {"order_no": "ORD1001", "product": "C200充电宝", "total_qty": 5000, "completed_qty": 3200, "completion_pct": 64.0, "current_stage": "组装测试", "planned_completion": "2026-08-10", "risk": "low"},
        ],
        "total": 1, "dependency": "partial"
    })

@v1_router.get("/beiyongxin/production/capacity", tags=["倍斯特-倍用心系统"],
    summary="产能数据",
    description="[V1] 获取产能数据（▲部分依赖）")
async def byx_prod_capacity_v1(factory_code: Optional[str] = Query(None)):
    return api_response(data={
        "capacity_data": [
            {"factory": "江苏工厂", "line": "充电宝产线A", "daily_capacity": 5000, "current_load": 0.85, "available_capacity": 750, "status": "running", "bottleneck": "SMT贴片工序"},
        ],
        "total_lines": 1, "total_daily_capacity": 5000, "dependency": "partial"
    })

@v1_router.get("/beiyongxin/finance/outbound-detail", tags=["倍斯特-倍用心系统"],
    summary="出库明细",
    description="[V1] 获取出库明细（●强依赖）")
async def byx_fin_outbound_v1(customer_code: Optional[str] = Query(None), date_from: Optional[str] = Query(None), date_to: Optional[str] = Query(None)):
    return api_response(data={
        "outbound_details": [
            {"outbound_no": "OB20260701001", "order_no": "ORD1001", "customer": "客户A", "product": "C200充电宝", "qty": 1000, "unit_price": 45.0, "total_amount": 45000.0, "outbound_date": "2026-07-10", "warehouse": "成品仓"},
        ],
        "total": 1, "dependency": "strong"
    })

@v1_router.get("/beiyongxin/finance/payment-records", tags=["倍斯特-倍用心系统"],
    summary="收款记录",
    description="[V1] 获取收款记录（●强依赖）")
async def byx_fin_payment_records_v1(customer_code: Optional[str] = Query(None), date_from: Optional[str] = Query(None), date_to: Optional[str] = Query(None)):
    return api_response(data={
        "payment_records": [
            {"payment_no": "PAY20260701001", "customer": "客户A", "amount": 45000.0, "payment_date": "2026-07-01", "payment_method": "银行转账", "related_invoice": "INV20260701001", "status": "confirmed"},
        ],
        "total": 1, "dependency": "strong"
    })

@v1_router.get("/beiyongxin/finance/expenses", tags=["倍斯特-倍用心系统"],
    summary="费用支出",
    description="[V1] 获取费用支出（▲部分依赖）")
async def byx_fin_expenses_v1(dept_code: Optional[str] = Query(None), period: Optional[str] = Query(None)):
    return api_response(data={
        "expenses": [
            {"expense_no": "EXP20260701001", "department": "制造中心", "category": "原材料采购", "amount": 250000.0, "expense_date": "2026-07-01", "status": "approved", "remark": "7月第一批物料采购"},
        ],
        "total": 1, "total_amount": 250000.0, "dependency": "partial"
    })

@v1_router.get("/beiyongxin/finance/labor-hours", tags=["倍斯特-倍用心系统"],
    summary="工时数据",
    description="[V1] 获取工时数据（▲部分依赖）")
async def byx_fin_labor_hours_v1(dept_code: Optional[str] = Query(None), period: Optional[str] = Query(None)):
    return api_response(data={
        "labor_hours": [
            {"department": "制造中心", "period": "2026-07", "total_hours": 8560, "regular_hours": 8000, "overtime_hours": 560, "headcount": 50, "avg_hours_per_person": 171.2},
        ],
        "total": 1, "dependency": "partial"
    })

@v1_router.get("/beiyongxin/crm/customer-info", tags=["倍斯特-倍用心系统"],
    summary="客户信息",
    description="[V1] 获取客户信息（●强依赖）")
async def byx_crm_customer_info_v1(customer_code: Optional[str] = Query(None)):
    return api_response(data={
        "customers": _customers.get("customers", [{"id": "C1001", "name": "客户A"}]), "total": 1, "dependency": "strong"
    })

@v1_router.get("/beiyongxin/crm/follow-up", tags=["倍斯特-倍用心系统"],
    summary="跟进记录",
    description="[V1] 获取客户跟进记录（▲部分依赖）")
async def byx_crm_follow_up_v1(customer_code: Optional[str] = Query(None), sales_person: Optional[str] = Query(None)):
    return api_response(data={
        "follow_up_records": [
            {"customer_code": "C1001", "customer_name": "客户A", "sales_person": "张明", "follow_up_date": "2026-07-15", "method": "电话", "content": "沟通新订单需求", "next_action": "准备报价单", "next_date": "2026-07-18"},
        ],
        "total": 1, "dependency": "partial"
    })

@v1_router.get("/beiyongxin/crm/opportunity", tags=["倍斯特-倍用心系统"],
    summary="商机状态",
    description="[V1] 获取商机状态（●强依赖）")
async def byx_crm_opportunity_v1(customer_code: Optional[str] = Query(None)):
    return api_response(data={
        "opportunities": [
            {"customer_code": "C1001", "customer_name": "客户A", "opportunity_name": "C200充电宝批量采购", "expected_amount": 450000.0, "stage": "商务谈判", "probability_pct": 70, "expected_close": "2026-08", "sales_person": "张明", "created_date": "2026-06-20"},
        ],
        "total": 1, "total_expected_amount": 450000.0, "dependency": "strong"
    })


app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# ==================== 数据加载 ====================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOCK_DATA_DIR = os.path.join(BASE_DIR, "data", "mock", "business-data")

def load_json(filename):
    path = os.path.join(MOCK_DATA_DIR, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return api_response(data={})
# 缓存数据
_customers = {}
_orders = {}
_traffic = {}
_competitors = {}
_boms = {}
_inventory = {}
_prices = {}
_suppliers = {}
_finance = {}
_production = {}
_crm = {}
_hr = {}

def reload_data():
    global _customers, _orders, _traffic, _competitors, _boms, _inventory, _prices
    global _suppliers, _finance, _production, _crm, _hr
    _customers = load_json("customer_data.json")
    _orders = load_json("order_data.json")
    _traffic = load_json("traffic_data.json")
    _competitors = load_json("competitor_data.json")
    _boms = load_json("bom_data.json")
    _inventory = load_json("inventory_data.json")
    _prices = load_json("material_prices.json")
    _suppliers = load_json("supplier_data.json")
    _finance = load_json("finance_data.json")
    _production = load_json("production_data.json")
    _crm = load_json("crm_data.json")
    _hr = load_json("hr_data.json")

reload_data()

# ==================== 黑云系统接口（保留现有，过渡期兼容） ====================

@app.get("/api/heiyun/bom/{project_id}", tags=["倍斯特-黑云系统"])
async def get_bom(project_id: str):
    """获取项目BOM物料清单"""
    if _boms:
        for b in _boms.get("boms", []):
            if b["project_id"] == project_id:
                return b
    return api_error("PROJECT_NOT_FOUND", f"项目{project_id}不存在", http_status=404)

@app.get("/api/heiyun/orders", tags=["倍斯特-黑云系统"])
async def get_orders(status: Optional[str] = None, customer: Optional[str] = None):
    """获取订单列表"""
    orders = _orders.get("orders", [])
    if status:
        orders = [o for o in orders if o["status"] == status]
    if customer:
        orders = [o for o in orders if o["customer"] == customer]
    return api_response(data={"orders": orders, "total": len(orders)})
@app.get("/api/heiyun/orders/{order_id}", tags=["倍斯特-黑云系统"])
async def get_order(order_id: str):
    """获取单个订单详情"""
    for o in _orders.get("orders", []):
        if o["id"] == order_id:
            return o
    return api_error("ORDER_NOT_FOUND", f"订单{order_id}不存在", http_status=404)

@app.get("/api/heiyun/customers", tags=["倍斯特-黑云系统"])
async def get_customers(status: Optional[str] = None, dormant: Optional[bool] = None):
    """获取客户列表"""
    customers = _customers.get("customers", [])
    if dormant is not None:
        customers = [c for c in customers if c["is_dormant"] == dormant]
    return api_response(data={"customers": customers, "total": len(customers)})
@app.get("/api/heiyun/customers/{customer_id}", tags=["倍斯特-黑云系统"])
async def get_customer(customer_id: str):
    """获取单个客户详情"""
    for c in _customers.get("customers", []):
        if c["id"] == customer_id:
            return c
    return api_error("CUSTOMER_NOT_FOUND", f"客户{customer_id}不存在", http_status=404)

@app.get("/api/heiyun/inventory", tags=["倍斯特-黑云系统"])
async def get_inventory(warehouse: Optional[str] = None, low_stock: Optional[bool] = None):
    """获取库存数据"""
    items = _inventory.get("items", [])
    if warehouse:
        items = [i for i in items if i["warehouse"] == warehouse]
    if low_stock:
        items = [i for i in items if i["available"] <= i["min_stock"]]
    return api_response(data={"items": items, "total": len(items)})
# ==================== 平台流量接口 ====================

@app.get("/api/platform/{platform}/metrics", tags=["倍斯特-平台流量"])
async def get_platform_metrics(platform: str, date: Optional[str] = None):
    """获取平台流量数据"""
    if _traffic:
        records = _traffic.get("traffic", [])
        filtered = [r for r in records if r["platform"] == platform]
        if date:
            filtered = [r for r in filtered if r["date"] == date]
        if filtered:
            return api_response(data={"platform": platform, "records": filtered, "total": len(filtered)})
    return api_response(data={
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
    })

# ==================== 竞品分析接口 ====================

@app.get("/api/competitors", tags=["倍斯特-竞品分析"])
async def get_competitors():
    return api_response(data=_competitors)

@app.get("/api/competitors/{name}", tags=["倍斯特-竞品分析"])
async def get_competitor(name: str):
    for c in _competitors.get("competitors", []):
        if c["name"] == name:
            return c
    return api_error("COMPETITOR_NOT_FOUND", f"竞品{name}不存在", http_status=404)

# ==================== 元器件行情接口 ====================

@app.get("/api/market/prices", tags=["倍斯特-市场行情"])
async def get_market_prices(material: Optional[str] = None):
    materials = _prices.get("materials", [])
    if material:
        materials = [m for m in materials if m["name"] == material]
    return api_response(data={"materials": materials, "total": len(materials)})
# ==================== 健康检查 ====================

@app.get("/health")
async def health_check():
    return api_response(data={"status": "ok", "service": "beste-mock-api", "version": "2.0.0", "timestamp": datetime.now().isoformat()})
@app.get("/api/status", tags=["倍斯特-其他"])
async def api_status():
    return api_response(data={
        "heiyun": bool(_orders.get("orders")),
        "beiyongxin": True,
        "customers": bool(_customers.get("customers")),
        "traffic": bool(_traffic.get("traffic")),
        "competitors": bool(_competitors.get("competitors")),
        "inventory": bool(_inventory.get("items")),
        "prices": bool(_prices.get("materials")),
        "suppliers": bool(_suppliers.get("suppliers")),
        "finance": bool(_finance.get("receivables")),
        "production": bool(_production.get("production_lines")),
        "data_loaded": all([_orders, _customers, _traffic]),
    })

@app.post("/api/admin/reload", tags=["倍斯特-系统管理"])
async def reload_mock_data():
    reload_data()
    return api_response(data={"status": "ok", "message": "数据已重新加载"})
# ====================================================================
# 倍用心系统接口（新ERP，2026年10月上线）
# ====================================================================
# 文档参考：倍斯特×倍用心系统接口对接需求文档一
# 共21个接口，覆盖6大数据域
# 依赖类型标注：●强依赖 ▲部分依赖

# ==================== 1. 订单与BOM数据域（4个接口） ====================

# 接口1：BOM清单查询（▲部分依赖 - 10月前可人工导出BOM过渡）
@app.get("/api/beiyongxin/bom/query", tags=["倍斯特-倍用心系统"])
async def byx_bom_query(product_code: str = Query(..., description="成品编号/产品型号")):
    """[倍用心] 获取产品BOM清单 - 采购需求智能分析(P0)、物料齐套协调(P0)、智能报价(P1)"""
    if _boms:
        for b in _boms.get("boms", []):
            if b.get("project_id") == product_code or b.get("product_code") == product_code:
                return api_response(data={
                    "product_code": product_code,
                    "bom_version": b.get("bom_version", "V1.0"),
                    "materials": b.get("materials", []),
                    "optional_fields": {"material_types": ["结构件", "电子件", "包材"], "bom_version": b.get("bom_version", "V1.0"), "substitute_info": b.get("substitute_info", [])},
                    "dependency": "partial", "transition_note": "10月前可人工导出BOM过渡"
                })
    return api_response(data={
        "product_code": product_code, "bom_version": "V1.0",
        "materials": [
            {"material_code": "MC001", "material_name": "锂电池组(18650)", "spec": "3.7V 2600mAh", "unit": "个", "standard_qty": 4},
            {"material_code": "MC002", "material_name": "PCB主板", "spec": "BMS-V3.0", "unit": "片", "standard_qty": 1},
            {"material_code": "MC003", "material_name": "外壳(上盖)", "spec": "ABS材质 白色", "unit": "个", "standard_qty": 1},
            {"material_code": "MC004", "material_name": "外壳(下盖)", "spec": "ABS材质 白色", "unit": "个", "standard_qty": 1},
            {"material_code": "MC005", "material_name": "USB-C接口模块", "spec": "TYPE-C 5A", "unit": "个", "standard_qty": 2},
            {"material_code": "MC006", "material_name": "电量显示板", "spec": "LED 4格", "unit": "片", "standard_qty": 1},
            {"material_code": "MC007", "material_name": "螺丝包", "spec": "M2.0*6mm", "unit": "包", "standard_qty": 1}
        ],
        "optional_fields": {
            "material_types": {"MC001": "电子件", "MC002": "电子件", "MC003": "结构件", "MC004": "结构件", "MC005": "电子件", "MC006": "电子件", "MC007": "结构件"},
            "bom_version": "V1.0",
            "substitute_info": [{"material_code": "MC001", "substitute_code": "MC001-B", "substitute_name": "锂电池组(18650) 替代料", "reason": "产能不足"}]
        },
        "dependency": "partial", "transition_note": "10月前可人工导出BOM过渡"
    })

# 接口2：订单信息查询（●强依赖）
@app.get("/api/beiyongxin/orders/query", tags=["倍斯特-倍用心系统"])
async def byx_order_query(order_no: Optional[str] = Query(None, description="订单号"), date_from: Optional[str] = Query(None, description="开始日期"), date_to: Optional[str] = Query(None, description="结束日期"), customer_code: Optional[str] = Query(None, description="客户编号")):
    """[倍用心] 获取订单主数据及明细"""
    orders = _orders.get("orders", [])
    if order_no:
        orders = [o for o in orders if o.get("id") == order_no]
    if not orders:
        orders = [
            {"id": "ORD1001", "customer": "客户A", "product_model": "C200充电宝", "quantity": 5000, "unit_price": 45.0, "delivery_date": "2026-08-15", "order_date": "2026-07-01", "status": "生产中", "work_order_no": "WO20260701001"},
            {"id": "ORD1002", "customer": "客户B", "product_model": "CS12充电柜", "quantity": 200, "unit_price": 3200.0, "delivery_date": "2026-08-30", "order_date": "2026-07-05", "status": "生产中", "work_order_no": "WO20260705001"},
            {"id": "ORD1003", "customer": "客户C", "product_model": "C100充电宝", "quantity": 10000, "unit_price": 28.0, "delivery_date": "2026-09-01", "order_date": "2026-07-10", "status": "待审核", "work_order_no": ""},
        ]
    result = []
    for o in orders:
        result.append({
            "order_no": o.get("id", ""), "customer_name": o.get("customer", ""),
            "product_model": o.get("product_model", o.get("product", "")), "quantity": o.get("quantity", o.get("qty", 0)),
            "unit_price": o.get("unit_price", o.get("price", 0)), "delivery_date": o.get("delivery_date", o.get("delivery", "")),
            "order_date": o.get("order_date", o.get("date", "")),
            "optional_fields": {"order_status": o.get("status", "生产中"), "work_order_no": o.get("work_order_no", "")}
        })
    return api_response(data={"orders": result, "total": len(result), "dependency": "strong"})
# 接口3：订单状态变更推送（●强依赖）- 事件触发
@app.post("/api/beiyongxin/orders/status-change", tags=["倍斯特-倍用心系统"])
async def byx_status_change(payload: dict):
    """[倍用心] 订单状态变更主动推送（事件触发）"""
    order_no = payload.get("order_no", "")
    if not order_no:
        return api_error("INVALID_ORDER", "订单号不能为空", http_status=400)
    return api_response(data={
        "acknowledged": True, "order_no": order_no,
        "old_status": payload.get("old_status", ""), "new_status": payload.get("new_status", ""),
        "change_time": payload.get("change_time", datetime.now().isoformat()),
        "change_reason": payload.get("change_reason", ""),
        "processed_at": datetime.now().isoformat(), "dependency": "strong"
    })

# 接口4：订单交期数据（●强依赖）
@app.get("/api/beiyongxin/orders/delivery", tags=["倍斯特-倍用心系统"])
async def byx_delivery_data(order_no: str = Query(..., description="订单编号")):
    """[倍用心] 获取订单交期及进度"""
    if not order_no:
        return api_error("INVALID_ORDER", "订单号不能为空", http_status=400)
    return api_response(data={
        "order_no": order_no, "promised_delivery": "2026-08-15", "current_progress_pct": 45,
        "milestones": [
            {"node": "物料齐套", "planned": "2026-07-10", "actual": "2026-07-08"},
            {"node": "SMT贴片", "planned": "2026-07-15", "actual": None},
            {"node": "组装测试", "planned": "2026-07-25", "actual": None},
            {"node": "成品入库", "planned": "2026-08-10", "actual": None},
        ],
        "actual_completion": None, "dependency": "strong"
    })

# ==================== 2. 库存与物料数据域（3个接口） ====================

# 接口5：实时库存查询（●强依赖）
@app.get("/api/beiyongxin/inventory/real-time", tags=["倍斯特-倍用心系统"])
async def byx_inventory_query(material_code: str = Query(..., description="物料编码"), warehouse_code: Optional[str] = Query(None, description="仓库编码")):
    if not material_code:
        return api_error("INVALID_MATERIAL", "物料编码不能为空", http_status=400)
    return api_response(data={
        "material_code": material_code, "available_qty": random.randint(1000, 30000), "in_transit_qty": random.randint(500, 5000),
        "optional_fields": {"warehouse_name": "主仓库", "safety_stock": 500, "batch_date": "2026-06-15"},
        "dependency": "strong"
    })

# 接口6：欠料明细查询（●强依赖）
@app.get("/api/beiyongxin/inventory/shortage", tags=["倍斯特-倍用心系统"])
async def byx_shortage_query(order_no: str = Query(..., description="订单编号/工单编号")):
    """[倍用心] 查询订单欠料明细"""
    if not order_no:
        return api_error("INVALID_ORDER", "订单编号不能为空", http_status=400)
    return api_response(data={
        "order_no": order_no,
        "shortage_details": [
            {"material_code": "MC001", "material_name": "锂电池组(18650)", "required_qty": 20000, "received_qty": 15000, "shortage_qty": 5000, "expected_arrival": "2026-07-20", "optional_fields": {"current_status": "在途", "supplier_name": "供应商A"}},
            {"material_code": "MC005", "material_name": "USB-C接口模块", "required_qty": 5000, "received_qty": 3000, "shortage_qty": 2000, "expected_arrival": "2026-07-18", "optional_fields": {"current_status": "在途", "supplier_name": "供应商B"}},
        ],
        "total_shortage_items": 2, "dependency": "strong"
    })

# 接口7：呆滞物料清单（●强依赖）
@app.get("/api/beiyongxin/inventory/slow-moving", tags=["倍斯特-倍用心系统"])
async def byx_slow_moving():
    """[倍用心] 获取呆滞物料清单（180天以上未使用）"""
    return api_response(data={
        "slow_moving_items": [
            {"material_code": "SM001", "material_name": "Micro-USB接口模块(旧版)", "stock_qty": 5000, "inbound_date": "2025-06-10", "last_used_date": "2025-12-01", "purchase_order_no": "PO20250601001", "batch_no": "B20250601"},
            {"material_code": "SM002", "material_name": "外壳(旧款黑色)", "stock_qty": 3000, "inbound_date": "2025-08-15", "last_used_date": "2026-01-10", "purchase_order_no": "PO20250815002", "batch_no": "B20250815"},
            {"material_code": "SM003", "material_name": "电池保护板(旧版BMS)", "stock_qty": 2000, "inbound_date": "2025-03-20", "last_used_date": "2025-09-05", "purchase_order_no": "PO20250320003", "batch_no": "B20250320"},
            {"material_code": "SM004", "material_name": "LED指示灯(红色,旧版)", "stock_qty": 8000, "inbound_date": "2025-05-01", "last_used_date": "2025-10-15", "purchase_order_no": "PO20250501004", "batch_no": "B20250501"},
        ],
        "total_items": 4, "dependency": "strong"
    })

# ==================== 3. 采购与供应商数据域（4个接口：8-11） ====================

# 接口8：采购订单查询（●强依赖）
@app.get("/api/beiyongxin/purchase/orders", tags=["倍斯特-倍用心系统"])
async def byx_purchase_orders(po_no: Optional[str] = Query(None), supplier_code: Optional[str] = Query(None), date_from: Optional[str] = Query(None), date_to: Optional[str] = Query(None)):
    """[倍用心] 获取采购订单及明细"""
    return api_response(data={
        "purchase_orders": [
            {"po_no": "PO20260701001", "supplier_name": "供应商A", "material_code": "MC001", "material_name": "锂电池组(18650)", "purchase_qty": 20000, "delivered_qty": 15000, "undelivered_qty": 5000, "promised_delivery": "2026-07-20", "optional_fields": {"order_status": "部分交货"}},
            {"po_no": "PO20260705002", "supplier_name": "供应商B", "material_code": "MC005", "material_name": "USB-C接口模块", "purchase_qty": 10000, "delivered_qty": 3000, "undelivered_qty": 7000, "promised_delivery": "2026-07-18", "optional_fields": {"order_status": "部分交货"}},
            {"po_no": "PO20260710003", "supplier_name": "供应商C", "material_code": "MC003", "material_name": "外壳(上盖)", "purchase_qty": 5000, "delivered_qty": 5000, "undelivered_qty": 0, "promised_delivery": "2026-07-15", "optional_fields": {"order_status": "已交货"}},
            {"po_no": "PO20260712004", "supplier_name": "供应商D", "material_code": "MC002", "material_name": "PCB主板", "purchase_qty": 8000, "delivered_qty": 0, "undelivered_qty": 8000, "promised_delivery": "2026-07-25", "optional_fields": {"order_status": "待交货"}},
        ],
        "total": 4, "dependency": "strong"
    })

# 接口9：供应商主数据（●强依赖）
@app.get("/api/beiyongxin/suppliers/master-data", tags=["倍斯特-倍用心系统"])
async def byx_supplier_master(supplier_code: Optional[str] = Query(None), material_type: Optional[str] = Query(None)):
    """[倍用心] 获取供应商主数据"""
    supps = _suppliers.get("suppliers", [])
    if not supps:
        supps = [
            {"id": "SUP001", "name": "供应商A", "type": "电池", "rating": 4.8, "delivery_punctuality": 0.95, "price_level": "中等", "cooperation_years": 5, "certifications": ["ISO9001", "UL"], "contact_person": "王经理", "contact_phone": "13812345678", "bank_info": {"bank": "中国银行", "account": "6222000000000001"}, "payment_terms": "月结30天"},
            {"id": "SUP002", "name": "供应商B", "type": "电子元件", "rating": 4.5, "delivery_punctuality": 0.88, "price_level": "偏高", "cooperation_years": 3, "certifications": ["ISO9001"], "contact_person": "李经理", "contact_phone": "13812345679", "bank_info": {"bank": "工商银行", "account": "6222000000000002"}, "payment_terms": "月结60天"},
            {"id": "SUP003", "name": "供应商C", "type": "包材", "rating": 4.2, "delivery_punctuality": 0.92, "price_level": "低", "cooperation_years": 2, "certifications": ["ISO14001"], "contact_person": "赵经理", "contact_phone": "13812345680", "bank_info": {"bank": "建设银行", "account": "6222000000000003"}, "payment_terms": "月结30天"},
            {"id": "SUP004", "name": "供应商D", "type": "PCB", "rating": 4.6, "delivery_punctuality": 0.90, "price_level": "中等", "cooperation_years": 4, "certifications": ["ISO9001", "IPC"], "contact_person": "陈经理", "contact_phone": "13812345681", "bank_info": {"bank": "招商银行", "account": "6222000000000004"}, "payment_terms": "月结45天"},
            {"id": "SUP005", "name": "供应商E", "type": "锂电池", "rating": 4.9, "delivery_punctuality": 0.97, "price_level": "偏高", "cooperation_years": 6, "certifications": ["ISO9001", "UL", "UN38.3"], "contact_person": "刘经理", "contact_phone": "13812345682", "bank_info": {"bank": "中国银行", "account": "6222000000000005"}, "payment_terms": "月结60天"},
        ]
    if supplier_code:
        supps = [s for s in supps if s.get("id") == supplier_code]
    if material_type:
        supps = [s for s in supps if material_type in s.get("type", "")]
    result = []
    for s in supps:
        result.append({
            "supplier_code": s.get("id", ""), "supplier_name": s.get("name", ""),
            "material_type": s.get("type", ""), "rating": s.get("rating", 0.0),
            "delivery_punctuality_rate": s.get("delivery_punctuality", 0.0),
            "price_level": s.get("price_level", ""), "cooperation_years": s.get("cooperation_years", 0),
            "certifications": s.get("certifications", []),
            "contact_person": s.get("contact_person", "张经理"), "contact_phone": s.get("contact_phone", ""),
            "bank_info": s.get("bank_info", {}), "payment_terms": s.get("payment_terms", "月结30天"),
        })
    return api_response(data={"suppliers": result, "total": len(result), "dependency": "strong"})
# 接口10：采购交期状态（●强依赖）
@app.get("/api/beiyongxin/purchase/delivery-status", tags=["倍斯特-倍用心系统"])
async def byx_purchase_delivery_status(po_no: Optional[str] = Query(None)):
    """[倍用心] 获取采购订单交期及在途状态"""
    statuses = [
        {"po_no": "PO20260701001", "supplier": "供应商A", "material": "锂电池组(18650)", "qty": 20000, "remaining_qty": 5000, "status": "partial", "next_delivery": "2026-07-20", "risk_level": "中", "transport_mode": "公路运输", "tracking_no": "SF20260701001"},
        {"po_no": "PO20260705002", "supplier": "供应商B", "material": "USB-C接口模块", "qty": 10000, "remaining_qty": 7000, "status": "partial", "next_delivery": "2026-07-18", "risk_level": "高", "transport_mode": "快递", "tracking_no": "SF20260705002"},
        {"po_no": "PO20260712004", "supplier": "供应商D", "material": "PCB主板", "qty": 8000, "remaining_qty": 8000, "status": "pending", "next_delivery": "2026-07-25", "risk_level": "低", "transport_mode": "公路运输", "tracking_no": ""},
    ]
    if po_no:
        statuses = [s for s in statuses if s["po_no"] == po_no]
    return api_response(data={"delivery_statuses": statuses, "total": len(statuses), "dependency": "strong"})
# 接口11：历史交易记录（▲部分依赖）
@app.get("/api/beiyongxin/purchase/history", tags=["倍斯特-倍用心系统"])
async def byx_purchase_history(supplier_code: str = Query(..., description="供应商编码"), months: int = Query(12, description="回溯月数")):
    """[倍用心] 获取供应商历史交易记录"""
    if not supplier_code:
        return api_error("INVALID_SUPPLIER", "供应商编码不能为空", http_status=400)
    return api_response(data={
        "supplier_code": supplier_code, "history_period_months": months,
        "transaction_records": [
            {"date": "2026-06-15", "material": "锂电池组(18650)", "qty": 5000, "unit_price": 12.5, "total_amount": 62500.0, "delivery_status": "completed"},
            {"date": "2026-06-01", "material": "锂电池组(18650)", "qty": 10000, "unit_price": 12.5, "total_amount": 125000.0, "delivery_status": "completed"},
            {"date": "2026-05-15", "material": "锂电池组(18650)", "qty": 8000, "unit_price": 12.8, "total_amount": 102400.0, "delivery_status": "completed"},
            {"date": "2026-04-20", "material": "锂电池组(18650)", "qty": 6000, "unit_price": 13.0, "total_amount": 78000.0, "delivery_status": "completed"},
        ],
        "total_transactions": 4, "total_amount": 367900.0, "avg_delivery_delay_days": 2,
        "dependency": "partial"
    })

# ==================== 4. 生产与进度数据域（3个接口：12-14） ====================

# 接口12：产线入库状态（●强依赖）
@app.get("/api/beiyongxin/production/warehouse-in", tags=["倍斯特-倍用心系统"])
async def byx_prod_warehouse_in(factory_code: Optional[str] = Query(None), date: Optional[str] = Query(None)):
    """[倍用心] 获取产线入库状态"""
    return api_response(data={
        "warehouse_in_records": [
            {"order_no": "ORD1001", "product": "C200充电宝", "factory": "江苏工厂", "line": "充电宝产线A", "planned_qty": 5000, "produced_qty": 3200, "warehoused_qty": 2800, "defect_qty": 15, "yield_rate": 0.973, "warehouse_date": "2026-07-16"},
            {"order_no": "ORD1002", "product": "CS12充电柜", "factory": "江苏工厂", "line": "充电柜产线B", "planned_qty": 200, "produced_qty": 120, "warehoused_qty": 100, "defect_qty": 2, "yield_rate": 0.983, "warehouse_date": "2026-07-16"},
        ],
        "total": 2, "dependency": "strong"
    })

# 接口13：生产进度（▲部分依赖）
@app.get("/api/beiyongxin/production/progress", tags=["倍斯特-倍用心系统"])
async def byx_prod_progress(order_no: Optional[str] = Query(None)):
    """[倍用心] 获取生产进度"""
    return api_response(data={
        "production_progress": [
            {"order_no": "ORD1001", "product": "C200充电宝", "total_qty": 5000, "completed_qty": 3200, "completion_pct": 64.0, "current_stage": "组装测试", "planned_completion": "2026-08-10", "risk": "low"},
            {"order_no": "ORD1002", "product": "CS12充电柜", "total_qty": 200, "completed_qty": 120, "completion_pct": 60.0, "current_stage": "组装调试", "planned_completion": "2026-08-15", "risk": "low"},
        ],
        "total": 2, "dependency": "partial"
    })

# 接口14：产能数据（▲部分依赖）
@app.get("/api/beiyongxin/production/capacity", tags=["倍斯特-倍用心系统"])
async def byx_prod_capacity(factory_code: Optional[str] = Query(None)):
    """[倍用心] 获取产能数据"""
    return api_response(data={
        "capacity_data": [
            {"factory": "江苏工厂", "line": "充电宝产线A", "daily_capacity": 5000, "current_load": 0.85, "available_capacity": 750, "status": "running", "bottleneck": "SMT贴片工序"},
            {"factory": "江苏工厂", "line": "充电柜产线B", "daily_capacity": 200, "current_load": 0.78, "available_capacity": 44, "status": "running", "bottleneck": "组装调试"},
            {"factory": "广西工厂", "line": "充电宝产线C", "daily_capacity": 3000, "current_load": 0.0, "available_capacity": 3000, "status": "commissioning", "bottleneck": "设备调试中"},
        ],
        "total_lines": 3, "total_daily_capacity": 8200, "dependency": "partial"
    })

# ==================== 5. 财务与收款数据域（4个接口：15-18） ====================

# 接口15：出库明细（●强依赖）
@app.get("/api/beiyongxin/finance/outbound-detail", tags=["倍斯特-倍用心系统"])
async def byx_fin_outbound(customer_code: Optional[str] = Query(None), date_from: Optional[str] = Query(None), date_to: Optional[str] = Query(None)):
    """[倍用心] 获取出库明细"""
    return api_response(data={
        "outbound_details": [
            {"outbound_no": "OB20260701001", "order_no": "ORD1001", "customer": "客户A", "product": "C200充电宝", "qty": 1000, "unit_price": 45.0, "total_amount": 45000.0, "outbound_date": "2026-07-10", "warehouse": "成品仓"},
            {"outbound_no": "OB20260715001", "order_no": "ORD1001", "customer": "客户A", "product": "C200充电宝", "qty": 1800, "unit_price": 45.0, "total_amount": 81000.0, "outbound_date": "2026-07-15", "warehouse": "成品仓"},
            {"outbound_no": "OB20260715002", "order_no": "ORD1002", "customer": "客户B", "product": "CS12充电柜", "qty": 50, "unit_price": 3200.0, "total_amount": 160000.0, "outbound_date": "2026-07-15", "warehouse": "成品仓"},
        ],
        "total": 3, "dependency": "strong"
    })

# 接口16：收款记录（●强依赖）
@app.get("/api/beiyongxin/finance/payment-records", tags=["倍斯特-倍用心系统"])
async def byx_fin_payment_records(customer_code: Optional[str] = Query(None), date_from: Optional[str] = Query(None), date_to: Optional[str] = Query(None)):
    """[倍用心] 获取收款记录"""
    return api_response(data={
        "payment_records": [
            {"payment_no": "PAY20260701001", "customer": "客户A", "amount": 45000.0, "payment_date": "2026-07-01", "payment_method": "银行转账", "related_invoice": "INV20260701001", "status": "confirmed"},
            {"payment_no": "PAY20260710001", "customer": "客户B", "amount": 128000.0, "payment_date": "2026-07-10", "payment_method": "承兑汇票", "related_invoice": "INV20260710001", "status": "confirmed"},
            {"payment_no": "PAY20260715001", "customer": "客户A", "amount": 81000.0, "payment_date": "2026-07-15", "payment_method": "银行转账", "related_invoice": "INV20260715001", "status": "pending"},
        ],
        "total": 3, "dependency": "strong"
    })

# 接口17：费用支出（▲部分依赖）
@app.get("/api/beiyongxin/finance/expenses", tags=["倍斯特-倍用心系统"])
async def byx_fin_expenses(dept_code: Optional[str] = Query(None), period: Optional[str] = Query(None)):
    """[倍用心] 获取费用支出"""
    return api_response(data={
        "expenses": [
            {"expense_no": "EXP20260701001", "department": "制造中心", "category": "原材料采购", "amount": 250000.0, "expense_date": "2026-07-01", "status": "approved", "remark": "7月第一批物料采购"},
            {"expense_no": "EXP20260705001", "department": "研发部", "category": "设备采购", "amount": 85000.0, "expense_date": "2026-07-05", "status": "approved", "remark": "新测试设备采购"},
            {"expense_no": "EXP20260710001", "department": "销售部", "category": "差旅费", "amount": 12000.0, "expense_date": "2026-07-10", "status": "pending", "remark": "客户拜访差旅"},
            {"expense_no": "EXP20260712001", "department": "管理中心", "category": "办公费用", "amount": 8000.0, "expense_date": "2026-07-12", "status": "approved", "remark": "办公用品采购"},
        ],
        "total": 4, "total_amount": 355000.0, "dependency": "partial"
    })

# 接口18：工时数据（▲部分依赖）
@app.get("/api/beiyongxin/finance/labor-hours", tags=["倍斯特-倍用心系统"])
async def byx_fin_labor_hours(dept_code: Optional[str] = Query(None), period: Optional[str] = Query(None)):
    """[倍用心] 获取工时数据"""
    return api_response(data={
        "labor_hours": [
            {"department": "制造中心", "period": "2026-07", "total_hours": 8560, "regular_hours": 8000, "overtime_hours": 560, "headcount": 50, "avg_hours_per_person": 171.2},
            {"department": "研发部", "period": "2026-07", "total_hours": 3400, "regular_hours": 3200, "overtime_hours": 200, "headcount": 20, "avg_hours_per_person": 170.0},
            {"department": "销售部", "period": "2026-07", "total_hours": 1680, "regular_hours": 1600, "overtime_hours": 80, "headcount": 10, "avg_hours_per_person": 168.0},
            {"department": "管理中心", "period": "2026-07", "total_hours": 1260, "regular_hours": 1200, "overtime_hours": 60, "headcount": 8, "avg_hours_per_person": 157.5},
        ],
        "total": 4, "dependency": "partial"
    })

# ==================== 6. CRM与客户数据域（3个接口：19-21） ====================

# 接口19：客户信息（●强依赖）
@app.get("/api/beiyongxin/crm/customer-info", tags=["倍斯特-倍用心系统"])
async def byx_crm_customer_info(customer_code: Optional[str] = Query(None)):
    """[倍用心] 获取客户信息"""
    custs = _customers.get("customers", [])
    if not custs:
        custs = [
            {"id": "C1001", "name": "深圳市科技有限公司", "industry": "零售", "contact_person": "张经理", "phone": "13812345678", "total_orders": 25, "total_amount": 650000.0, "is_dormant": False, "customer_level": "A"},
            {"id": "C1002", "name": "广州市贸易有限公司", "industry": "贸易", "contact_person": "李经理", "phone": "13812345679", "total_orders": 12, "total_amount": 320000.0, "is_dormant": False, "customer_level": "B"},
            {"id": "C1003", "name": "深圳市电子有限公司", "industry": "电子", "contact_person": "王经理", "phone": "13812345680", "total_orders": 8, "total_amount": 180000.0, "is_dormant": True, "customer_level": "C"},
        ]
    if customer_code:
        custs = [c for c in custs if c.get("id") == customer_code]
    return api_response(data={"customers": custs, "total": len(custs), "dependency": "strong"})
# 接口20：跟进记录（▲部分依赖）
@app.get("/api/beiyongxin/crm/follow-up", tags=["倍斯特-倍用心系统"])
async def byx_crm_follow_up(customer_code: Optional[str] = Query(None), sales_person: Optional[str] = Query(None)):
    """[倍用心] 获取客户跟进记录"""
    return api_response(data={
        "follow_up_records": [
            {"customer_code": "C1001", "customer_name": "深圳市科技有限公司", "sales_person": "张明", "follow_up_date": "2026-07-15", "method": "电话", "content": "沟通新订单需求，预计8月下单", "next_action": "准备报价单", "next_date": "2026-07-18"},
            {"customer_code": "C1001", "customer_name": "深圳市科技有限公司", "sales_person": "张明", "follow_up_date": "2026-07-10", "method": "拜访", "content": "样品展示，客户对C200充电宝满意", "next_action": "跟进合同签订", "next_date": "2026-07-14"},
            {"customer_code": "C1002", "customer_name": "广州市贸易有限公司", "sales_person": "李华", "follow_up_date": "2026-07-12", "method": "微信", "content": "确认CS12充电柜技术参数", "next_action": "发送正式报价", "next_date": "2026-07-13"},
            {"customer_code": "C1003", "customer_name": "深圳市电子有限公司", "sales_person": "王芳", "follow_up_date": "2026-07-08", "method": "邮件", "content": "发送季度促销方案", "next_action": "确认客户意向", "next_date": "2026-07-20"},
        ],
        "total": 4, "dependency": "partial"
    })

# 接口21：商机状态（●强依赖）
@app.get("/api/beiyongxin/crm/opportunity", tags=["倍斯特-倍用心系统"])
async def byx_crm_opportunity(customer_code: Optional[str] = Query(None)):
    """[倍用心] 获取商机状态"""
    return api_response(data={
        "opportunities": [
            {"customer_code": "C1001", "customer_name": "深圳市科技有限公司", "opportunity_name": "C200充电宝批量采购", "expected_amount": 450000.0, "stage": "商务谈判", "probability_pct": 70, "expected_close": "2026-08", "sales_person": "张明", "created_date": "2026-06-20"},
            {"customer_code": "C1002", "customer_name": "广州市贸易有限公司", "opportunity_name": "CS12充电柜代理", "expected_amount": 640000.0, "stage": "方案确认", "probability_pct": 50, "expected_close": "2026-09", "sales_person": "李华", "created_date": "2026-06-25"},
            {"customer_code": "C1004", "customer_name": "客户D", "opportunity_name": "OEM充电宝定制", "expected_amount": 280000.0, "stage": "需求调研", "probability_pct": 30, "expected_close": "2026-10", "sales_person": "赵强", "created_date": "2026-07-01"},
        ],
        "total": 3, "total_expected_amount": 1370000.0, "dependency": "strong"
    })

# ==================== 新增场景API端点（保留原有） ====================

@app.get("/api/oem/supported-capacities", tags=["倍斯特-OEM定制"])
async def oem_supported_capacities():
    data = load_json("oem_data.json")
    return api_response(data={"supported_capacities": data.get("supported_capacities", []), "supported_colors": data.get("supported_colors", [])})
@app.get("/api/oem/design-template", tags=["倍斯特-OEM定制"])
async def oem_design_template(product_type: str, capacity: str):
    data = load_json("oem_data.json")
    for t in data.get("design_templates", []):
        if t["product_type"] == product_type and t["capacity"] == capacity:
            return t
    return api_error("TEMPLATE_NOT_FOUND", f"产品{product_type}容量{capacity}的设计模板不存在", http_status=404)

@app.post("/api/oem/scheme", tags=["倍斯特-OEM定制"])
async def oem_generate_scheme():
    data = load_json("oem_data.json")
    schemes = data.get("schemes", [])
    if schemes:
        return schemes[0]
    return api_error("DESIGN_SERVICE_DOWN", "设计服务暂时不可用", http_status=500)

@app.get("/api/overseas/supported-regions", tags=["倍斯特-海外业务"])
async def overseas_regions():
    data = load_json("overseas_data.json")
    return api_response(data={"regions": data.get("supported_regions", []), "delivery_terms": data.get("delivery_terms", [])})
@app.get("/api/overseas/price-factors/{region}", tags=["倍斯特-海外业务"])
async def overseas_price_factors(region: str):
    data = load_json("overseas_data.json")
    factors = data.get("price_factors", {})
    if region in factors:
        return factors[region]
    return api_error("REGION_NOT_SUPPORTED", f"区域{region}不支持", http_status=404)

@app.get("/api/overseas/inquiries", tags=["倍斯特-海外业务"])
async def overseas_inquiries():
    data = load_json("overseas_data.json")
    return api_response(data={"inquiries": data.get("overseas_inquiries", [])})
@app.post("/api/orders/dispatch", tags=["倍斯特-订单管理"])
async def order_dispatch(order_id: str, factory: str):
    orders = load_json("order_data.json").get("orders", [])
    order = None
    for o in orders:
        if o["id"] == order_id:
            order = o
            break
    if not order:
        return api_error("ORDER_NOT_FOUND", f"订单{order_id}不存在", http_status=404)
    prod = load_json("production_data.json")
    factories = set(pl["factory"] for pl in prod.get("production_lines", []))
    if factory not in factories:
        return api_error("FACTORY_NOT_FOUND", f"工厂{factory}不存在", http_status=400)
    return api_response(data={"dispatched": True, "order_id": order_id, "factory": factory, "assigned_line": "PL001", "estimated_start": "2026-07-18"})
@app.get("/api/orders/{order_id}/progress", tags=["倍斯特-订单管理"])
async def order_progress(order_id: str):
    risk = load_json("order_risk_data.json")
    for tl in risk.get("order_timelines", []):
        if tl["order_id"] == order_id:
            return tl
    return api_error("ORDER_NOT_FOUND", f"订单{order_id}不存在", http_status=404)

@app.get("/api/orders/risk-alerts", tags=["倍斯特-订单管理"])
async def order_risk_alerts(time_range: str):
    if not time_range:
        return api_error("INVALID_PARAM", "时间范围不能为空", http_status=400)
    risk = load_json("order_risk_data.json")
    return api_response(data={"risk_alerts": risk.get("risk_alerts", []), "total": len(risk.get("risk_alerts", []))})
@app.get("/api/finance/receivables", tags=["倍斯特-财务"])
async def get_receivables(customer_id: Optional[str] = None):
    fin = load_json("finance_data.json")
    rcv = fin.get("receivables", [])
    if customer_id:
        rcv = [r for r in rcv if r["customer_id"] == customer_id]
    return api_response(data={"receivables": rcv, "total": len(rcv)})
@app.get("/api/finance/receivables/{customer_id}/collection-plan", tags=["倍斯特-财务"])
async def collection_plan(customer_id: str, overdue_days: int):
    if overdue_days < 0:
        return api_error("INVALID_PARAM", "逾期天数不能为负", http_status=400)
    fin = load_json("finance_data.json")
    for r in fin.get("receivables", []):
        if r["customer_id"] == customer_id:
            return api_response(data={"customer_id": customer_id, "amount": r["amount"], "overdue_days": overdue_days, "suggested_action": "发送催收函" if overdue_days < 60 else "法律警告"})
    return api_error("CUSTOMER_NOT_FOUND", f"客户{customer_id}不存在", http_status=404)

@app.get("/api/department/{department}/report", tags=["倍斯特-部门报表"])
async def department_report(department: str, period: str):
    valid_depts = ["商务部", "制造中心", "销售部", "研发部", "管理中心"]
    if department not in valid_depts:
        return api_error("DEPARTMENT_NOT_FOUND", f"部门{department}不存在", http_status=400)
    return api_response(data={"department": department, "period": period, "contract_amount": 2500000, "signed_count": 8, "collection_rate": 0.75, "active_projects": 12})
@app.get("/api/commission/calculate", tags=["倍斯特-佣金"])
async def calculate_commission(sales_person: str, period: str):
    fin = load_json("finance_data.json")
    for rec in fin.get("commission_records", []):
        if rec["sales_person"] == sales_person and rec["period"] == period:
            return rec
    hr_data = load_json("hr_data.json")
    emp_names = [e["name"] for e in hr_data.get("employees", [])]
    if sales_person not in emp_names:
        return api_error("EMPLOYEE_NOT_FOUND", f"员工{sales_person}不存在", http_status=404)
    return api_response(data={"sales_person": sales_person, "period": period, "base_commission": 0, "bonus": 0, "deduction": 0, "net_amount": 0})
@app.get("/api/pricing/quote", tags=["倍斯特-定价"])
async def generate_quote(product_id: str, qty: int, customer_level: str = "B"):
    if qty <= 0:
        return api_error("INVALID_QTY", "数量必须大于0", http_status=400)
    pricing_data = load_json("pricing_data.json")
    base_prices = pricing_data.get("base_prices", {})
    if product_id not in base_prices:
        return api_error("PRODUCT_NOT_FOUND", f"产品{product_id}不存在", http_status=404)
    base_price = base_prices[product_id]
    discount_rules = pricing_data.get("discount_rules", {})
    discount = discount_rules.get(customer_level, {}).get("discount_rate", 0)
    unit_price = round(base_price * (1 - discount), 2)
    total = round(unit_price * qty, 2)
    return api_response(data={"product_id": product_id, "unit_price": unit_price, "qty": qty, "total": total, "discount": discount, "valid_until": "2026-08-15"})
@app.get("/api/crm/dashboard", tags=["倍斯特-CRM"])
async def crm_dashboard(time_range: str):
    crm_data = load_json("crm_data.json")
    return crm_data.get("crm_dashboard", {})

@app.get("/api/crm/collaboration-tasks", tags=["倍斯特-CRM"])
async def collaboration_tasks():
    crm_data = load_json("crm_data.json")
    return api_response(data={"tasks": crm_data.get("collaboration_tasks", [])})
@app.get("/api/hr/performance/{department}", tags=["倍斯特-人力资源"])
async def performance_analysis(department: str, period: str):
    hr_data = load_json("hr_data.json")
    if department not in hr_data.get("departments", []):
        return api_error("DEPARTMENT_NOT_FOUND", f"部门{department}不存在", http_status=400)
    emps = [e for e in hr_data.get("employees", []) if e["department"] == department]
    if not emps:
        return api_error("NO_DATA", "该部门无员工数据", http_status=404)
    avg_score = sum(e["kpi_score"] for e in emps) / len(emps)
    return api_response(data={"department": department, "period": period, "avg_kpi_score": round(avg_score, 1), "employee_count": len(emps), "employees": emps})
@app.get("/api/gallery/search", tags=["倍斯特-图库"])
async def search_gallery(keyword: str, category: str = "产品图"):
    gallery = load_json("gallery_data.json")
    results = [img for img in gallery.get("images", []) if keyword.lower() in img["name"].lower() or any(keyword.lower() in t.lower() for t in img.get("tags", []))]
    if not results:
        return api_error("MATCH_NOT_FOUND", "未找到匹配图片", http_status=404)
    return api_response(data={"results": results, "total": len(results)})
@app.post("/api/production/schedule", tags=["倍斯特-生产管理"])
async def schedule_production():
    prod = load_json("production_data.json")
    schedules = prod.get("schedules", [])
    if schedules:
        return schedules[0]
    return api_response(data={"message": "无排产计划"})
@app.get("/api/quality/monthly/{period}", tags=["倍斯特-品质管理"])
async def quality_monthly(period: str):
    if period >= "2099":
        return api_error("INVALID_PERIOD", "时间段无效", http_status=400)
    prod = load_json("production_data.json")
    for qm in prod.get("quality_metrics", []):
        if qm["period"] == period:
            return qm
    return api_error("NO_DATA", "该时间段无品质数据", http_status=404)

@app.get("/api/production/process-analysis", tags=["倍斯特-生产管理"])
async def process_analysis(product_line: str, period: str):
    prod = load_json("production_data.json")
    for pl in prod.get("production_lines", []):
        if pl["name"] == product_line:
            return api_response(data={"product_line": product_line, "period": period, "current_efficiency": pl["current_efficiency"], "bottleneck": pl["bottleneck"], "improvement_suggestions": ["优化瓶颈工序", "增加自动化设备"]})
    return api_error("LINE_NOT_FOUND", f"产线{product_line}不存在", http_status=404)

@app.get("/api/quality/complaint/{complaint_id}", tags=["倍斯特-品质管理"])
async def complaint_analysis(complaint_id: str):
    prod = load_json("production_data.json")
    for c in prod.get("complaints", []):
        if c["id"] == complaint_id:
            return c
    return api_error("COMPLAINT_NOT_FOUND", f"投诉{complaint_id}不存在", http_status=404)

@app.get("/api/amoeba/accounting", tags=["倍斯特-阿米巴"])
async def amoeba_accounting(unit: str, period: str):
    hr_data = load_json("hr_data.json")
    for u in hr_data.get("amoeba_units", []):
        if u["unit"] == unit and u["period"] == period:
            return u
    return api_error("UNIT_NOT_FOUND", f"阿米巴单元{unit}不存在", http_status=404)

@app.get("/api/hr/culture-summary/{period}", tags=["倍斯特-人力资源"])
async def culture_summary(period: str):
    hr_data = load_json("hr_data.json")
    activities = [a for a in hr_data.get("culture_activities", []) if a["period"] == period]
    if not activities:
        return api_error("NO_ACTIVITIES", "该期间无活动记录", http_status=404)
    total_participants = sum(a["participants"] for a in activities)
    avg_score = sum(a["feedback_score"] for a in activities) / len(activities)
    return api_response(data={"period": period, "activity_count": len(activities), "total_participants": total_participants, "avg_feedback_score": round(avg_score, 1), "activities": activities})
@app.get("/api/policy/check", tags=["倍斯特-政策"])
async def policy_check(document: str, policy_id: str):
    src_path = os.path.join(BASE_DIR, "data/source/policies", "policies_data.json")
    if os.path.exists(src_path):
        with open(src_path, "r", encoding="utf-8") as f:
            policies = json.load(f)
    for p in policies.get("policies", []):
        if p["id"] == policy_id:
            return api_response(data={"document": document, "policy_id": policy_id, "policy_name": p["name"], "is_compliant": True, "detail": "报销单符合报销管理制度规定"})
    return api_error("POLICY_NOT_FOUND", f"政策{policy_id}不存在", http_status=404)

@app.get("/api/gov/policy-match", tags=["倍斯特-政策匹配"])
async def policy_match(company_industry: str, company_region: str, revenue: str):
    if not company_industry:
        return api_error("INVALID_INDUSTRY", "行业不能为空", http_status=400)
    gov = load_json("gov_policy_data.json")
    matched = [p for p in gov.get("policies", []) if company_industry.lower() in p["industry"].lower() or company_region.lower() in p["region"].lower()]
    return api_response(data={"matched_policies": matched, "matched_count": len(matched)})
@app.get("/api/gov/qualification-plan", tags=["倍斯特-政策匹配"])
async def qualification_plan(company_stage: str, target_markets: str):
    if not target_markets:
        return api_error("INVALID_MARKETS", "目标市场不能为空", http_status=400)
    gov = load_json("gov_policy_data.json")
    quals = gov.get("qualifications", {})
    return api_response(data={"company_stage": company_stage, "current_qualifications": quals.get("current", []), "needed_qualifications": quals.get("needed", []), "roadmap": quals.get("roadmap", [])})
@app.get("/api/hr/talent-review/{department}", tags=["倍斯特-人力资源"])
async def talent_review(department: str):
    hr_data = load_json("hr_data.json")
    if department not in hr_data.get("departments", []):
        return api_error("DEPARTMENT_NOT_FOUND", f"部门{department}不存在", http_status=400)
    emps = [e for e in hr_data.get("employees", []) if e["department"] == department]
    key_talents = [e for e in emps if e["is_key_talent"]]
    return api_response(data={"department": department, "total_employees": len(emps), "key_talents": key_talents, "avg_tenure": round(sum(e["tenure_years"] for e in emps) / len(emps), 1) if emps else 0, "risk_analysis": "低流失风险"})
@app.post("/api/finance/voucher", tags=["倍斯特-财务"])
async def generate_voucher():
    return api_response(data={"voucher_id": "VCH20260716001", "entries": [{"account": "应收账款", "debit": 50000, "credit": 0}, {"account": "主营业务收入", "debit": 0, "credit": 50000}], "summary": "销售商品确认收入"})
@app.get("/api/finance/tax-filing", tags=["倍斯特-财务"])
async def tax_filing(tax_type: str, period: str):
    if not tax_type:
        return api_error("INVALID_TAX_TYPE", "税种不能为空", http_status=400)
    fin = load_json("finance_data.json")
    rates = fin.get("tax_rates", {})
    tax_info = rates.get(tax_type, {})
    return api_response(data={"tax_type": tax_type, "period": period, "output_tax": 65000, "input_tax": 45000, "tax_due": 20000, "deadline": tax_info.get("deadline", "次月15日")})
@app.get("/api/market/forecast", tags=["倍斯特-市场行情"])
async def market_forecast(material: str, horizon_months: int):
    prices = load_json("material_prices.json")
    for m in prices.get("materials", []):
        if m["name"] == material:
            return api_response(data={"material": material, "current_price": m["current_price"], "trend": m["trend"], "supply_status": m["supply_status"], "forecast": f"预计未来{horizon_months}个月价格上涨10-15%", "suggestion": "建议增加采购库存"})
    return api_error("MATERIAL_NOT_FOUND", f"材料{material}不存在", http_status=404)

@app.get("/api/suppliers/compare", tags=["倍斯特-供应商管理"])
async def supplier_compare(material: str, qty: int):
    suppliers = load_json("supplier_data.json").get("suppliers", [])
    if not suppliers:
        return api_error("NO_SUPPLIERS", "供应商列表为空", http_status=400)
    results = []
    for s in suppliers:
        est_price = round(random.uniform(10, 50) * (1 - (s["rating"] - 4) * 0.05), 2)
        results.append({"supplier_id": s["id"], "name": s["name"], "unit_price": est_price, "total": round(est_price * qty, 2), "delivery_days": random.randint(15, 45), "rating": s["rating"], "score": round(s["rating"] * 0.4 + (1 - est_price / 50) * 0.3 + s["delivery_punctuality"] * 0.3, 2)})
    results.sort(key=lambda x: x["score"], reverse=True)
    for i, r in enumerate(results):
        r["rank"] = i + 1
    return api_response(data={"material": material, "qty": qty, "comparison": results})
@app.get("/api/suppliers/{supplier_id}/evaluate", tags=["倍斯特-供应商管理"])
async def supplier_evaluate(supplier_id: str, dimensions: str):
    if not dimensions:
        return api_error("INVALID_DIMENSIONS", "评价维度不能为空", http_status=400)
    suppliers = load_json("supplier_data.json").get("suppliers", [])
    for s in suppliers:
        if s["id"] == supplier_id:
            dims = [d.strip() for d in dimensions.split(",")]
            scores = {d: round(random.uniform(3.5, 5.0), 1) for d in dims}
            avg_score = round(sum(scores.values()) / len(scores), 1)
            level = "A" if avg_score >= 4.5 else "B" if avg_score >= 4.0 else "C"
            return api_response(data={"supplier_id": supplier_id, "name": s["name"], "dimension_scores": scores, "overall_score": avg_score, "level": level})
    return api_error("SUPPLIER_NOT_FOUND", f"供应商{supplier_id}不存在", http_status=404)

@app.get("/api/logistics/quote", tags=["倍斯特-物流"])
async def logistics_quote(origin: str, destination: str, weight_kg: float, volume_cbm: float):
    log = load_json("logistics_data.json")
    routes = [r for r in log.get("shipping_routes", []) if r["destination"] == destination]
    if not routes:
        return api_error("DESTINATION_NOT_SUPPORTED", f"目的地{destination}不支持", http_status=404)
    options = []
    for r in routes:
        if weight_kg >= r.get("min_kg", 0):
            freight = round(r["cost_per_kg"] * weight_kg + r.get("cost_per_cbm", 0) * volume_cbm, 2)
            options.append({"mode": r["mode"], "carrier": r["carrier"], "freight": freight, "transit_days": r["transit_days"], "total_cost": freight})
    return api_response(data={"origin": origin, "destination": destination, "weight_kg": weight_kg, "volume_cbm": volume_cbm, "options": options})

# ==================== 注册 V1 路由 ====================
app.include_router(v1_router)

# ==================== 旧路径重定向 ====================

@app.get("/api/heiyun/{rest:path}", include_in_schema=False, tags=["倍斯特-黑云系统"])
async def redirect_heiyun_old(rest: str):
    """旧路径 /api/heiyun/* → 重定向到 /api/v1/heiyun/*"""
    return RedirectResponse(url=f"/api/v1/heiyun/{rest}")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)
