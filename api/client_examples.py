#!/usr/bin/env python3
"""
倍斯特 Mock API 客户端调用示例
================================
演示如何使用 Python requests 调用倍斯特 Mock API 的所有接口。
支持统一响应格式解析、版本化路径和旧路径兼容。

前置条件:
    pip install requests

使用方式:
    python api/client_examples.py

运行前请确保 mock_api_server.py 已在运行:
    python api/mock_api_server.py
"""

import requests
import json
from typing import Optional, Dict, Any

BASE_URL = "http://localhost:3001"
V1_URL = f"{BASE_URL}/api/v1"

# ==================== 统一响应解析 ====================

def parse_response(response: requests.Response) -> Dict[str, Any]:
    """解析统一响应格式，返回 data 字段"""
    result = response.json()
    if result.get("code") == 0:
        return result["data"]
    else:
        raise RuntimeError(f"API Error [{result['code']}]: {result['message']}")

# ==================== 黑云系统接口 (V1 版本) ====================

def get_bom(project_id: str) -> Dict[str, Any]:
    """获取项目BOM物料清单"""
    resp = requests.get(f"{V1_URL}/heiyun/bom/{project_id}")
    return parse_response(resp)

def get_orders(status: Optional[str] = None, customer: Optional[str] = None) -> Dict[str, Any]:
    """获取订单列表"""
    params = {}
    if status: params["status"] = status
    if customer: params["customer"] = customer
    resp = requests.get(f"{V1_URL}/heiyun/orders", params=params)
    return parse_response(resp)

def get_order(order_id: str) -> Dict[str, Any]:
    """获取订单详情"""
    resp = requests.get(f"{V1_URL}/heiyun/orders/{order_id}")
    return parse_response(resp)

def get_customers(status: Optional[str] = None, dormant: Optional[bool] = None) -> Dict[str, Any]:
    """获取客户列表"""
    params = {}
    if status: params["status"] = status
    if dormant is not None: params["dormant"] = dormant
    resp = requests.get(f"{V1_URL}/heiyun/customers", params=params)
    return parse_response(resp)

def get_customer(customer_id: str) -> Dict[str, Any]:
    """获取客户详情"""
    resp = requests.get(f"{V1_URL}/heiyun/customers/{customer_id}")
    return parse_response(resp)

def get_inventory(warehouse: Optional[str] = None, low_stock: Optional[bool] = None) -> Dict[str, Any]:
    """获取库存数据"""
    params = {}
    if warehouse: params["warehouse"] = warehouse
    if low_stock is not None: params["low_stock"] = low_stock
    resp = requests.get(f"{V1_URL}/heiyun/inventory", params=params)
    return parse_response(resp)

# ==================== 倍用心系统接口 (V1 版本) ====================

def byx_bom_query(product_code: str) -> Dict[str, Any]:
    """BOM清单查询"""
    resp = requests.get(f"{V1_URL}/beiyongxin/bom/query", params={"product_code": product_code})
    return parse_response(resp)

def byx_order_query(order_no: Optional[str] = None) -> Dict[str, Any]:
    """订单信息查询"""
    params = {}
    if order_no: params["order_no"] = order_no
    resp = requests.get(f"{V1_URL}/beiyongxin/orders/query", params=params)
    return parse_response(resp)

def byx_status_change(order_no: str, old_status: str, new_status: str) -> Dict[str, Any]:
    """订单状态变更推送"""
    payload = {
        "order_no": order_no,
        "old_status": old_status,
        "new_status": new_status,
        "change_time": "2026-07-16T10:00:00",
        "change_reason": "生产完成"
    }
    resp = requests.post(f"{V1_URL}/beiyongxin/orders/status-change", json=payload)
    return parse_response(resp)

def byx_delivery_data(order_no: str) -> Dict[str, Any]:
    """订单交期数据"""
    resp = requests.get(f"{V1_URL}/beiyongxin/orders/delivery", params={"order_no": order_no})
    return parse_response(resp)

def byx_inventory_query(material_code: str) -> Dict[str, Any]:
    """实时库存查询"""
    resp = requests.get(f"{V1_URL}/beiyongxin/inventory/real-time", params={"material_code": material_code})
    return parse_response(resp)

def byx_shortage_query(order_no: str) -> Dict[str, Any]:
    """欠料明细查询"""
    resp = requests.get(f"{V1_URL}/beiyongxin/inventory/shortage", params={"order_no": order_no})
    return parse_response(resp)

def byx_slow_moving() -> Dict[str, Any]:
    """呆滞物料清单"""
    resp = requests.get(f"{V1_URL}/beiyongxin/inventory/slow-moving")
    return parse_response(resp)

def byx_purchase_orders() -> Dict[str, Any]:
    """采购订单查询"""
    resp = requests.get(f"{V1_URL}/beiyongxin/purchase/orders")
    return parse_response(resp)

def byx_supplier_master() -> Dict[str, Any]:
    """供应商主数据"""
    resp = requests.get(f"{V1_URL}/beiyongxin/suppliers/master-data")
    return parse_response(resp)

def byx_purchase_delivery_status(po_no: Optional[str] = None) -> Dict[str, Any]:
    """采购交期状态"""
    params = {}
    if po_no: params["po_no"] = po_no
    resp = requests.get(f"{V1_URL}/beiyongxin/purchase/delivery-status", params=params)
    return parse_response(resp)

def byx_purchase_history(supplier_code: str, months: int = 12) -> Dict[str, Any]:
    """历史交易记录"""
    resp = requests.get(f"{V1_URL}/beiyongxin/purchase/history",
                        params={"supplier_code": supplier_code, "months": months})
    return parse_response(resp)

def byx_prod_warehouse_in() -> Dict[str, Any]:
    """产线入库状态"""
    resp = requests.get(f"{V1_URL}/beiyongxin/production/warehouse-in")
    return parse_response(resp)

def byx_prod_progress() -> Dict[str, Any]:
    """生产进度"""
    resp = requests.get(f"{V1_URL}/beiyongxin/production/progress")
    return parse_response(resp)

def byx_prod_capacity() -> Dict[str, Any]:
    """产能数据"""
    resp = requests.get(f"{V1_URL}/beiyongxin/production/capacity")
    return parse_response(resp)

def byx_fin_outbound() -> Dict[str, Any]:
    """出库明细"""
    resp = requests.get(f"{V1_URL}/beiyongxin/finance/outbound-detail")
    return parse_response(resp)

def byx_fin_payment_records() -> Dict[str, Any]:
    """收款记录"""
    resp = requests.get(f"{V1_URL}/beiyongxin/finance/payment-records")
    return parse_response(resp)

def byx_fin_expenses() -> Dict[str, Any]:
    """费用支出"""
    resp = requests.get(f"{V1_URL}/beiyongxin/finance/expenses")
    return parse_response(resp)

def byx_fin_labor_hours() -> Dict[str, Any]:
    """工时数据"""
    resp = requests.get(f"{V1_URL}/beiyongxin/finance/labor-hours")
    return parse_response(resp)

def byx_crm_customer_info() -> Dict[str, Any]:
    """客户信息"""
    resp = requests.get(f"{V1_URL}/beiyongxin/crm/customer-info")
    return parse_response(resp)

def byx_crm_follow_up() -> Dict[str, Any]:
    """跟进记录"""
    resp = requests.get(f"{V1_URL}/beiyongxin/crm/follow-up")
    return parse_response(resp)

def byx_crm_opportunity() -> Dict[str, Any]:
    """商机状态"""
    resp = requests.get(f"{V1_URL}/beiyongxin/crm/opportunity")
    return parse_response(resp)

# ==================== 原始路径兼容 (旧路径) ====================

def get_bom_old(project_id: str) -> Dict[str, Any]:
    """使用旧路径获取BOM"""
    resp = requests.get(f"{BASE_URL}/api/heiyun/bom/{project_id}")
    return parse_response(resp)

# ==================== 其他接口示例 ====================

def get_platform_metrics(platform: str) -> Dict[str, Any]:
    """获取平台流量数据"""
    resp = requests.get(f"{BASE_URL}/api/platform/{platform}/metrics")
    return parse_response(resp)

def get_competitors() -> Dict[str, Any]:
    """获取竞品列表"""
    resp = requests.get(f"{BASE_URL}/api/competitors")
    return parse_response(resp)

def get_market_prices(material: Optional[str] = None) -> Dict[str, Any]:
    """获取元器件行情"""
    params = {}
    if material: params["material"] = material
    resp = requests.get(f"{BASE_URL}/api/market/prices", params=params)
    return parse_response(resp)

def health_check() -> Dict[str, Any]:
    """健康检查"""
    resp = requests.get(f"{BASE_URL}/health")
    return parse_response(resp)

def api_status() -> Dict[str, Any]:
    """API状态概览"""
    resp = requests.get(f"{BASE_URL}/api/status")
    return parse_response(resp)

def reload_data() -> Dict[str, Any]:
    """重新加载Mock数据"""
    resp = requests.post(f"{BASE_URL}/api/admin/reload")
    return parse_response(resp)

# ==================== 主入口 ====================

def main():
    print("=" * 60)
    print("  倍斯特 Mock API 客户端调用示例")
    print("=" * 60)
    print(f"\n服务地址: {BASE_URL}")
    print(f"Swagger 文档: {BASE_URL}/docs")
    print(f"ReDoc 文档: {BASE_URL}/redoc")
    print(f"\n{'─' * 60}")
    print("📌 使用说明")
    print(f"{'─' * 60}")
    print("""
    1. 先启动 Mock API 服务:
       python api/mock_api_server.py

    2. 运行本示例:
       pip install requests
       python api/client_examples.py

    3. 查看 Swagger 文档:
       打开浏览器访问 http://localhost:3001/docs

    4. 接口路径说明:
       - V1版本路径: /api/v1/heiyun/*  (推荐)
       - 旧路径兼容: /api/heiyun/*     (自动重定向)
       - 倍用心接口: /api/v1/beiyongxin/*  (推荐)
    """)

    # 尝试实际调用
    try:
        print(f"{'─' * 60}")
        print("  🔍 健康检查")
        print(f"{'─' * 60}")
        h = health_check()
        print(f"  Status: {h}")
        
        print(f"\n{'─' * 60}")
        print("  📋 API 状态概览")
        print(f"{'─' * 60}")
        s = api_status()
        print(f"  黑云系统: {'✅' if s.get('heiyun') else '❌'}")
        print(f"  倍用心系统: {'✅' if s.get('beiyongxin') else '❌'}")
        print(f"  客户数据: {'✅' if s.get('customers') else '❌'}")
        print(f"  库存数据: {'✅' if s.get('inventory') else '❌'}")
        print(f"  数据加载状态: {'✅' if s.get('data_loaded') else '❌'}")

        print(f"\n{'─' * 60}")
        print("  📦 黑云系统 - 订单列表 (V1)")
        print(f"{'─' * 60}")
        orders = get_orders()
        print(f"  共 {orders['total']} 个订单")
        for o in orders['orders'][:3]:
            print(f"  - {o.get('id', 'N/A')}: {o.get('customer', 'N/A')} | {o.get('status', 'N/A')}")

        print(f"\n{'─' * 60}")
        print("  📦 倍用心系统 - BOM清单查询 (V1)")
        print(f"{'─' * 60}")
        bom = byx_bom_query("C200")
        print(f"  产品: {bom.get('product_code')}")
        print(f"  BOM版本: {bom.get('bom_version')}")
        print(f"  物料数: {len(bom.get('materials', []))}")

        print(f"\n{'─' * 60}")
        print("  📦 倍用心系统 - 实时库存查询 (V1)")
        print(f"{'─' * 60}")
        inv = byx_inventory_query("MC001")
        print(f"  物料: {inv.get('material_code')}")
        print(f"  可用量: {inv.get('available_qty')}")
        print(f"  在途量: {inv.get('in_transit_qty')}")

        print(f"\n{'─' * 60}")
        print("  📦 倍用心系统 - 订单状态变更 (V1)")
        print(f"{'─' * 60}")
        sc = byx_status_change("ORD1001", "待审核", "生产中")
        print(f"  确认: {sc.get('acknowledged')}")
        print(f"  状态: {sc.get('old_status')} → {sc.get('new_status')}")

        print(f"\n{'─' * 60}")
        print("  ✅ 全部示例调用成功!")
        print(f"{'─' * 60}")

    except requests.exceptions.ConnectionError:
        print(f"\n  ⚠️  无法连接到 {BASE_URL}，请先启动 Mock API 服务:")
        print("      python api/mock_api_server.py")
    except Exception as e:
        print(f"\n  ⚠️  调用出现异常: {e}")

if __name__ == "__main__":
    main()