"""黑云系统接口测试（过渡期兼容）

覆盖接口：
  - GET /api/heiyun/bom/{project_id}
  - GET /api/heiyun/orders
  - GET /api/heiyun/orders/{order_id}
  - GET /api/heiyun/customers
  - GET /api/heiyun/customers/{customer_id}
  - GET /api/heiyun/inventory
"""
import pytest
import requests
from conftest import (
    API_BASE, assert_response_time, assert_json_schema, extract_data,
)


class TestHeiyunBOM:
    """黑云BOM物料清单接口测试"""

    def test_get_bom_success(self, session):
        """正常路径：获取项目BOM清单"""
        r = session.get(f"{API_BASE}/api/heiyun/bom/C200", timeout=10)
        assert r.status_code == 200, f"期望200，实际{r.status_code}: {r.text}"
        assert_response_time(r)
        data = extract_data(r)
        assert "project_id" in data
        assert "materials" in data

    def test_get_bom_not_found(self, session):
        """边界情况：不存在的项目ID"""
        r = session.get(f"{API_BASE}/api/heiyun/bom/DOES_NOT_EXIST", timeout=10)
        assert r.status_code == 404, f"期望404，实际{r.status_code}"
        assert_response_time(r)
        body = r.json()
        assert "detail" in body or "message" in body


class TestHeiyunOrders:
    """黑云订单接口测试"""

    def test_get_orders_success(self, session):
        """正常路径：获取订单列表"""
        r = session.get(f"{API_BASE}/api/heiyun/orders", timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert "orders" in data
        assert "total" in data
        assert isinstance(data["orders"], list)

    def test_get_orders_with_filter(self, session):
        """正常路径：按状态筛选订单"""
        r = session.get(f"{API_BASE}/api/heiyun/orders", params={"status": "生产中"}, timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        for o in data["orders"]:
            assert o["status"] == "生产中"

    def test_get_order_detail_success(self, session):
        """正常路径：获取单个订单详情"""
        r = session.get(f"{API_BASE}/api/heiyun/orders/ORD1001", timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert data["id"] == "ORD1001"

    def test_get_order_not_found(self, session):
        """边界情况：不存在的订单ID"""
        r = session.get(f"{API_BASE}/api/heiyun/orders/INVALID_ORDER_999", timeout=10)
        assert r.status_code == 404
        assert_response_time(r)

    def test_get_orders_empty_params(self, session):
        """边界情况：空状态筛选"""
        r = session.get(f"{API_BASE}/api/heiyun/orders", params={"status": ""}, timeout=10)
        assert r.status_code == 200

    @pytest.mark.parametrize("order_id", [
        pytest.param("ORD1001", id="正常订单"),
        pytest.param("ORD1002", id="正常订单2"),
    ])
    def test_get_order_multiple_ids(self, session, order_id):
        """参数化：多个订单ID的详情查询"""
        r = session.get(f"{API_BASE}/api/heiyun/orders/{order_id}", timeout=10)
        assert r.status_code == 200
        assert_response_time(r)


class TestHeiyunCustomers:
    """黑云客户接口测试"""

    def test_get_customers_success(self, session):
        """正常路径：获取客户列表"""
        r = session.get(f"{API_BASE}/api/heiyun/customers", timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert "customers" in data
        assert "total" in data

    def test_get_customers_dormant_filter(self, session):
        """正常路径：按休眠状态筛选"""
        r = session.get(f"{API_BASE}/api/heiyun/customers", params={"dormant": "true"}, timeout=10)
        assert r.status_code == 200
        data = extract_data(r)
        for c in data["customers"]:
            assert c["is_dormant"] is True

    def test_get_customer_detail_success(self, session):
        """正常路径：获取单个客户详情"""
        r = session.get(f"{API_BASE}/api/heiyun/customers/C1001", timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert "id" in data

    def test_get_customer_not_found(self, session):
        """边界情况：不存在的客户ID"""
        r = session.get(f"{API_BASE}/api/heiyun/customers/NOBODY", timeout=10)
        assert r.status_code == 404
        assert_response_time(r)


class TestHeiyunInventory:
    """黑云库存接口测试"""

    def test_get_inventory_success(self, session):
        """正常路径：获取库存列表"""
        r = session.get(f"{API_BASE}/api/heiyun/inventory", timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert "items" in data
        assert "total" in data

    def test_get_inventory_low_stock(self, session):
        """正常路径：低库存筛选"""
        r = session.get(f"{API_BASE}/api/heiyun/inventory", params={"low_stock": "true"}, timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        for item in data["items"]:
            assert item["available"] <= item["min_stock"]


class TestHeiyunHealth:
    """黑云健康检查接口测试"""

    def test_health_check(self, session):
        """正常路径：健康检查"""
        r = session.get(f"{API_BASE}/health", timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert data["status"] == "ok"
        assert "service" in data
        assert "version" in data

    def test_api_status(self, session):
        """正常路径：API状态"""
        r = session.get(f"{API_BASE}/api/status", timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert "heiyun" in data
        assert "beiyongxin" in data
        assert "data_loaded" in data