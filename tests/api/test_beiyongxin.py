"""倍用心系统接口测试（6大数据域，21个接口）

覆盖接口：
  1. 订单与BOM数据域：BOM清单、订单查询、订单状态变更、交期数据
  2. 库存与物料数据域：实时库存、欠料明细、呆滞物料
  3. 采购与供应商数据域：采购订单、供应商主数据、交期状态、历史交易
  4. 生产与进度数据域：产线入库、生产进度、产能数据
  5. 财务与收款数据域：出库明细、收款记录、费用支出、工时数据
  6. CRM与客户数据域：客户信息、跟进记录、商机状态
"""
import pytest
import requests
from conftest import (
    API_BASE, assert_response_time, assert_json_schema, extract_data,
)


# ==================== 1. 订单与BOM数据域 ====================

class TestBeiyongxinBOM:
    """倍用心-BOM清单查询"""

    def test_bom_query_success(self, session):
        """正常路径：查询产品BOM清单"""
        r = session.get(f"{API_BASE}/api/beiyongxin/bom/query", params={"product_code": "C200"}, timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert "product_code" in data
        assert "materials" in data
        assert "dependency" in data

    def test_bom_query_empty_product_code(self, session):
        """边界情况：空物料编码"""
        r = session.get(f"{API_BASE}/api/beiyongxin/bom/query", params={"product_code": ""}, timeout=10)
        assert r.status_code in (200, 422)


class TestBeiyongxinOrders:
    """倍用心-订单查询"""

    def test_order_query_success(self, session):
        """正常路径：查询订单信息"""
        r = session.get(f"{API_BASE}/api/beiyongxin/orders/query", params={"order_no": "ORD1001"}, timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert "orders" in data
        assert "dependency" in data
        assert data["dependency"] == "strong"

    def test_order_query_all(self, session):
        """正常路径：查询全部订单"""
        r = session.get(f"{API_BASE}/api/beiyongxin/orders/query", timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert data["total"] >= 0

    def test_status_change_success(self, session):
        """正常路径：订单状态变更推送"""
        payload = {
            "order_no": "ORD1001",
            "old_status": "生产中",
            "new_status": "已入库",
            "change_time": "2026-07-16T10:00:00",
            "change_reason": "生产完成"
        }
        r = session.post(f"{API_BASE}/api/beiyongxin/orders/status-change", json=payload, timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert data["acknowledged"] is True
        assert data["order_no"] == "ORD1001"

    def test_status_change_empty_order_no(self, session):
        """边界情况：空订单号状态变更"""
        r = session.post(f"{API_BASE}/api/beiyongxin/orders/status-change", json={}, timeout=10)
        assert r.status_code == 400

    def test_delivery_data_success(self, session):
        """正常路径：订单交期数据"""
        r = session.get(f"{API_BASE}/api/beiyongxin/orders/delivery", params={"order_no": "ORD1001"}, timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert "promised_delivery" in data
        assert "milestones" in data
        assert "current_progress_pct" in data

    def test_delivery_data_empty_order_no(self, session):
        """边界情况：空订单号查询交期"""
        r = session.get(f"{API_BASE}/api/beiyongxin/orders/delivery", params={"order_no": ""}, timeout=10)
        assert r.status_code in (400, 422)


# ==================== 2. 库存与物料数据域 ====================

class TestBeiyongxinInventory:
    """倍用心-库存与物料"""

    def test_real_time_inventory_success(self, session):
        """正常路径：实时库存查询"""
        r = session.get(f"{API_BASE}/api/beiyongxin/inventory/real-time", params={"material_code": "MC001"}, timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert "available_qty" in data
        assert "in_transit_qty" in data
        assert "dependency" in data

    def test_real_time_inventory_empty_material(self, session):
        """边界情况：空物料编码"""
        r = session.get(f"{API_BASE}/api/beiyongxin/inventory/real-time", params={"material_code": ""}, timeout=10)
        assert r.status_code in (400, 422)

    def test_shortage_query_success(self, session):
        """正常路径：欠料明细查询"""
        r = session.get(f"{API_BASE}/api/beiyongxin/inventory/shortage", params={"order_no": "ORD1001"}, timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert "shortage_details" in data
        assert "total_shortage_items" in data

    def test_shortage_query_empty_order(self, session):
        """边界情况：空订单编号"""
        r = session.get(f"{API_BASE}/api/beiyongxin/inventory/shortage", params={"order_no": ""}, timeout=10)
        assert r.status_code in (400, 422)

    def test_slow_moving_success(self, session):
        """正常路径：呆滞物料清单"""
        r = session.get(f"{API_BASE}/api/beiyongxin/inventory/slow-moving", timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert "slow_moving_items" in data
        assert "total_items" in data


# ==================== 3. 采购与供应商数据域 ====================

class TestBeiyongxinPurchase:
    """倍用心-采购与供应商"""

    def test_purchase_orders_success(self, session):
        """正常路径：采购订单查询"""
        r = session.get(f"{API_BASE}/api/beiyongxin/purchase/orders", timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert "purchase_orders" in data
        assert "total" in data

    def test_supplier_master_success(self, session):
        """正常路径：供应商主数据查询"""
        r = session.get(f"{API_BASE}/api/beiyongxin/suppliers/master-data", params={"supplier_code": "SUP001"}, timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert "suppliers" in data
        assert len(data["suppliers"]) > 0
        assert data["suppliers"][0]["supplier_code"] == "SUP001"

    def test_supplier_master_empty_code(self, session):
        """边界情况：不指定供应商编码"""
        r = session.get(f"{API_BASE}/api/beiyongxin/suppliers/master-data", timeout=10)
        assert r.status_code == 200
        assert_response_time(r)

    def test_delivery_status_success(self, session):
        """正常路径：采购交期状态"""
        r = session.get(f"{API_BASE}/api/beiyongxin/purchase/delivery-status", params={"po_no": "PO20260701001"}, timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert "delivery_statuses" in data
        assert "dependency" in data

    def test_purchase_history_success(self, session):
        """正常路径：历史交易记录"""
        r = session.get(f"{API_BASE}/api/beiyongxin/purchase/history", params={"supplier_code": "SUP001", "months": 12}, timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert "transaction_records" in data
        assert "total_amount" in data

    def test_purchase_history_empty_supplier(self, session):
        """边界情况：空供应商编码"""
        r = session.get(f"{API_BASE}/api/beiyongxin/purchase/history", params={"supplier_code": "", "months": 12}, timeout=10)
        assert r.status_code in (400, 422)


# ==================== 4. 生产与进度数据域 ====================

class TestBeiyongxinProduction:
    """倍用心-生产与进度"""

    def test_warehouse_in_success(self, session):
        """正常路径：产线入库状态"""
        r = session.get(f"{API_BASE}/api/beiyongxin/production/warehouse-in", timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert "warehouse_in_records" in data

    def test_production_progress_success(self, session):
        """正常路径：生产进度查询"""
        r = session.get(f"{API_BASE}/api/beiyongxin/production/progress", params={"order_no": "ORD1001"}, timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert "production_progress" in data

    def test_capacity_success(self, session):
        """正常路径：产能数据查询"""
        r = session.get(f"{API_BASE}/api/beiyongxin/production/capacity", timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert "capacity_data" in data
        assert "total_lines" in data


# ==================== 5. 财务与收款数据域 ====================

class TestBeiyongxinFinance:
    """倍用心-财务与收款"""

    def test_outbound_detail_success(self, session):
        """正常路径：出库明细查询"""
        r = session.get(f"{API_BASE}/api/beiyongxin/finance/outbound-detail", timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert "outbound_details" in data

    def test_payment_records_success(self, session):
        """正常路径：收款记录查询"""
        r = session.get(f"{API_BASE}/api/beiyongxin/finance/payment-records", timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert "payment_records" in data

    def test_expenses_success(self, session):
        """正常路径：费用支出查询"""
        r = session.get(f"{API_BASE}/api/beiyongxin/finance/expenses", params={"dept_code": "制造中心"}, timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert "expenses" in data
        assert "total_amount" in data

    def test_labor_hours_success(self, session):
        """正常路径：工时数据查询"""
        r = session.get(f"{API_BASE}/api/beiyongxin/finance/labor-hours", params={"dept_code": "制造中心"}, timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert "labor_hours" in data


# ==================== 6. CRM与客户数据域 ====================

class TestBeiyongxinCRM:
    """倍用心-CRM与客户"""

    def test_customer_info_success(self, session):
        """正常路径：客户信息查询"""
        r = session.get(f"{API_BASE}/api/beiyongxin/crm/customer-info", params={"customer_code": "C1001"}, timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert "customers" in data
        assert data["customers"][0]["id"] == "C1001"

    def test_customer_info_all(self, session):
        """正常路径：查询全部客户"""
        r = session.get(f"{API_BASE}/api/beiyongxin/crm/customer-info", timeout=10)
        assert r.status_code == 200
        assert_response_time(r)

    def test_follow_up_success(self, session):
        """正常路径：客户跟进记录"""
        r = session.get(f"{API_BASE}/api/beiyongxin/crm/follow-up", params={"customer_code": "C1001"}, timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert "follow_up_records" in data

    def test_opportunity_success(self, session):
        """正常路径：商机状态查询"""
        r = session.get(f"{API_BASE}/api/beiyongxin/crm/opportunity", params={"customer_code": "C1001"}, timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert "opportunities" in data
        assert "total_expected_amount" in data