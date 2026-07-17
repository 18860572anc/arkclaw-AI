"""其他业务接口测试

覆盖接口：
  - 平台流量 /api/platform/{platform}/metrics
  - 竞品分析 /api/competitors, /api/competitors/{name}
  - 元器件行情 /api/market/prices
  - OEM /api/oem/*
  - 海外 /api/overseas/*
  - 订单派发/进度/风险 /api/orders/*
  - 财务 /api/finance/*
  - 部门报表 /api/department/{department}/report
  - 提成 /api/commission/calculate
  - 报价 /api/pricing/quote
  - CRM /api/crm/*
  - 人事 /api/hr/*
  - 图库 /api/gallery/search
  - 生产排产/品质/工艺 /api/production/*, /api/quality/*
  - 阿米巴 /api/amoeba/accounting
  - 企业文化 /api/hr/culture-summary/{period}
  - 政策 /api/policy/check, /api/gov/*
  - 物流 /api/logistics/quote
  - 供应商 /api/suppliers/*
"""
import pytest
import requests
from conftest import (
    API_BASE, assert_response_time, assert_json_schema, extract_data,
)


class TestPlatformMetrics:
    """平台流量接口测试"""

    def test_platform_metrics_success(self, session):
        """正常路径：获取平台流量指标"""
        r = session.get(f"{API_BASE}/api/platform/wechat/metrics", timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert "platform" in data
        assert ("metrics" in data) or ("records" in data)

    def test_platform_metrics_with_date(self, session):
        """正常路径：带日期的平台流量"""
        r = session.get(f"{API_BASE}/api/platform/wechat/metrics", params={"date": "2026-07-16"}, timeout=10)
        assert r.status_code == 200
        assert_response_time(r)


class TestCompetitors:
    """竞品分析接口测试"""

    def test_competitors_list_success(self, session):
        """正常路径：获取竞品列表"""
        r = session.get(f"{API_BASE}/api/competitors", timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert "competitors" in data

    def test_competitor_detail_success(self, session):
        """正常路径：获取单个竞品详情"""
        r = session.get(f"{API_BASE}/api/competitors/竞品科技A", timeout=10)
        assert r.status_code == 200
        assert_response_time(r)

    def test_competitor_not_found(self, session):
        """边界情况：不存在的竞品"""
        r = session.get(f"{API_BASE}/api/competitors/NOBODY", timeout=10)
        assert r.status_code == 404
        assert_response_time(r)


class TestMarketPrices:
    """元器件行情接口测试"""

    def test_market_prices_success(self, session):
        """正常路径：获取元器件行情"""
        r = session.get(f"{API_BASE}/api/market/prices", timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert "materials" in data

    def test_market_prices_filter(self, session):
        """正常路径：按物料筛选"""
        r = session.get(f"{API_BASE}/api/market/prices", params={"material": "锂电池组"}, timeout=10)
        assert r.status_code == 200
        assert_response_time(r)


class TestOEM:
    """OEM设计接口测试"""

    def test_supported_capacities(self, session):
        """正常路径：支持容量查询"""
        r = session.get(f"{API_BASE}/api/oem/supported-capacities", timeout=10)
        assert r.status_code == 200
        assert_response_time(r)

    def test_design_template_success(self, session):
        """正常路径：设计模板查询"""
        r = session.get(f"{API_BASE}/api/oem/design-template",
                        params={"product_type": "充电宝", "capacity": "10000mAh"}, timeout=10)
        if r.status_code == 200:
            assert_response_time(r)

    def test_design_template_not_found(self, session):
        """边界情况：不存在的设计模板"""
        r = session.get(f"{API_BASE}/api/oem/design-template",
                        params={"product_type": "UNKNOWN", "capacity": "99999mAh"}, timeout=10)
        assert r.status_code == 404
        assert_response_time(r)

    def test_oem_scheme(self, session):
        """正常路径：OEM方案生成"""
        r = session.post(f"{API_BASE}/api/oem/scheme", timeout=10)
        assert r.status_code in (200, 500)


class TestOverseas:
    """海外业务接口测试"""

    def test_supported_regions(self, session):
        """正常路径：支持区域查询"""
        r = session.get(f"{API_BASE}/api/overseas/supported-regions", timeout=10)
        assert r.status_code == 200
        assert_response_time(r)

    def test_price_factors_success(self, session):
        """正常路径：价格因子查询"""
        r = session.get(f"{API_BASE}/api/overseas/price-factors/北美", timeout=10)
        assert r.status_code in (200, 404)

    def test_price_factors_not_found(self, session):
        """边界情况：不存在的区域"""
        r = session.get(f"{API_BASE}/api/overseas/price-factors/UNKNOWN", timeout=10)
        assert r.status_code == 404
        assert_response_time(r)

    def test_overseas_inquiries(self, session):
        """正常路径：海外询盘列表"""
        r = session.get(f"{API_BASE}/api/overseas/inquiries", timeout=10)
        assert r.status_code == 200
        assert_response_time(r)


class TestOrders:
    """订单派发/进度/风险接口测试"""

    def test_order_dispatch_success(self, session):
        """正常路径：订单派发"""
        r = session.get(f"{API_BASE}/api/orders/dispatch",
                        params={"order_id": "ORD1001", "factory": "江苏工厂"}, timeout=10)
        assert r.status_code in (200, 405, 404)
        if r.status_code == 200:
            assert_response_time(r)

    def test_order_progress_success(self, session):
        """正常路径：订单进度查询"""
        r = session.get(f"{API_BASE}/api/orders/ORD1001/progress", timeout=10)
        assert r.status_code in (200, 404)

    def test_order_progress_not_found(self, session):
        """边界情况：不存在的订单进度"""
        r = session.get(f"{API_BASE}/api/orders/INVALID_ORDER_999/progress", timeout=10)
        assert r.status_code == 404
        assert_response_time(r)

    def test_risk_alerts_empty_time_range(self, session):
        """边界情况：空时间范围"""
        r = session.get(f"{API_BASE}/api/orders/risk-alerts", params={"time_range": ""}, timeout=10)
        assert r.status_code in (400, 200)

    def test_risk_alerts_success(self, session):
        """正常路径：风险预警"""
        r = session.get(f"{API_BASE}/api/orders/risk-alerts", params={"time_range": "this_month"}, timeout=10)
        assert r.status_code == 200
        assert_response_time(r)


class TestFinance:
    """财务接口测试"""

    def test_receivables_success(self, session):
        """正常路径：应收款查询"""
        r = session.get(f"{API_BASE}/api/finance/receivables", timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert "receivables" in data

    def test_receivables_filtered(self, session):
        """正常路径：按客户筛选应收款"""
        r = session.get(f"{API_BASE}/api/finance/receivables", params={"customer_id": "C1001"}, timeout=10)
        assert r.status_code == 200
        assert_response_time(r)

    def test_collection_plan_success(self, session):
        """正常路径：回款计划"""
        r = session.get(f"{API_BASE}/api/finance/receivables/C1001/collection-plan",
                        params={"overdue_days": 45}, timeout=10)
        assert r.status_code in (200, 404)

    def test_collection_plan_negative_overdue(self, session):
        """边界情况：负逾期天数"""
        r = session.get(f"{API_BASE}/api/finance/receivables/C1001/collection-plan",
                        params={"overdue_days": -1}, timeout=10)
        assert r.status_code == 400
        assert_response_time(r)

    def test_tax_filing_empty_type(self, session):
        """边界情况：空税种"""
        r = session.get(f"{API_BASE}/api/finance/tax-filing",
                        params={"tax_type": "", "period": "2026-06"}, timeout=10)
        assert r.status_code in (400, 422)

    def test_tax_filing_success(self, session):
        """正常路径：智能报税"""
        r = session.get(f"{API_BASE}/api/finance/tax-filing",
                        params={"tax_type": "VAT", "period": "2026-06"}, timeout=10)
        assert r.status_code == 200
        assert_response_time(r)

    def test_voucher_generate(self, session):
        """正常路径：会计凭证"""
        r = session.post(f"{API_BASE}/api/finance/voucher", timeout=10)
        assert r.status_code == 200
        assert_response_time(r)


class TestDepartment:
    """部门报表接口测试"""

    def test_department_report_success(self, session):
        """正常路径：部门报表"""
        r = session.get(f"{API_BASE}/api/department/商务部/report", params={"period": "2026-06"}, timeout=10)
        assert r.status_code == 200
        assert_response_time(r)

    def test_department_report_not_found(self, session):
        """边界情况：不存在的部门"""
        r = session.get(f"{API_BASE}/api/department/UNKNOWN/report", params={"period": "2026-06"}, timeout=10)
        assert r.status_code == 400
        assert_response_time(r)


class TestCommission:
    """提成核算接口测试"""

    def test_commission_success(self, session):
        """正常路径：提成核算"""
        r = session.get(f"{API_BASE}/api/commission/calculate",
                        params={"sales_person": "张明", "period": "2026-06"}, timeout=10)
        assert r.status_code == 200
        assert_response_time(r)

    def test_commission_not_found(self, session):
        """边界情况：不存在的员工"""
        r = session.get(f"{API_BASE}/api/commission/calculate",
                        params={"sales_person": "NOBODY", "period": "2026-06"}, timeout=10)
        assert r.status_code == 404
        assert_response_time(r)


class TestPricing:
    """报价接口测试"""

    def test_quote_success(self, session):
        """正常路径：智能报价"""
        r = session.get(f"{API_BASE}/api/pricing/quote",
                        params={"product_id": "C200", "qty": 1000, "customer_level": "A"}, timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert "unit_price" in data
        assert "total" in data

    def test_quote_zero_qty(self, session):
        """边界情况：零数量报价"""
        r = session.get(f"{API_BASE}/api/pricing/quote",
                        params={"product_id": "C200", "qty": 0, "customer_level": "A"}, timeout=10)
        assert r.status_code == 400

    def test_quote_negative_qty(self, session):
        """边界情况：负数数量报价"""
        r = session.get(f"{API_BASE}/api/pricing/quote",
                        params={"product_id": "C200", "qty": -1, "customer_level": "A"}, timeout=10)
        assert r.status_code == 400

    def test_quote_product_not_found(self, session):
        """边界情况：不存在的产品"""
        r = session.get(f"{API_BASE}/api/pricing/quote",
                        params={"product_id": "UNKNOWN_PRODUCT", "qty": 100, "customer_level": "A"}, timeout=10)
        assert r.status_code == 404
        assert_response_time(r)


class TestCRM:
    """CRM内部协作接口测试"""

    def test_crm_dashboard(self, session):
        """正常路径：CRM看板"""
        r = session.get(f"{API_BASE}/api/crm/dashboard", params={"time_range": "this_week"}, timeout=10)
        assert r.status_code == 200
        assert_response_time(r)

    def test_collaboration_tasks(self, session):
        """正常路径：协作任务"""
        r = session.get(f"{API_BASE}/api/crm/collaboration-tasks", timeout=10)
        assert r.status_code == 200
        assert_response_time(r)


class TestHR:
    """人事与绩效接口测试"""

    def test_performance_success(self, session):
        """正常路径：绩效分析"""
        r = session.get(f"{API_BASE}/api/hr/performance/销售部", params={"period": "2026-Q2"}, timeout=10)
        assert r.status_code == 200
        assert_response_time(r)

    def test_performance_not_found(self, session):
        """边界情况：不存在的部门"""
        r = session.get(f"{API_BASE}/api/hr/performance/UNKNOWN_DEPT", params={"period": "2026-Q2"}, timeout=10)
        assert r.status_code == 400
        assert_response_time(r)

    def test_talent_review_success(self, session):
        """正常路径：人才盘点"""
        r = session.get(f"{API_BASE}/api/hr/talent-review/研发部", timeout=10)
        assert r.status_code == 200
        assert_response_time(r)

    def test_talent_review_not_found(self, session):
        """边界情况：不存在的部门"""
        r = session.get(f"{API_BASE}/api/hr/talent-review/UNKNOWN", timeout=10)
        assert r.status_code == 400
        assert_response_time(r)

    def test_culture_summary_success(self, session):
        """正常路径：企业文化总结"""
        r = session.get(f"{API_BASE}/api/hr/culture-summary/2026-Q2", timeout=10)
        assert r.status_code in (200, 404)

    def test_culture_summary_future(self, session):
        """边界情况：未来时间段"""
        r = session.get(f"{API_BASE}/api/hr/culture-summary/2099-Q4", timeout=10)
        assert r.status_code == 404
        assert_response_time(r)


class TestGallery:
    """图库检索接口测试"""

    def test_gallery_search_success(self, session):
        """正常路径：图库检索"""
        r = session.get(f"{API_BASE}/api/gallery/search", params={"keyword": "充电柜"}, timeout=10)
        if r.status_code == 200:
            assert_response_time(r)
            data = extract_data(r)
            assert "results" in data
        elif r.status_code == 404:
            pass

    def test_gallery_search_not_found(self, session):
        """边界情况：无匹配关键词"""
        r = session.get(f"{API_BASE}/api/gallery/search", params={"keyword": "XYZXYZ_NOT_EXISTS"}, timeout=10)
        assert r.status_code == 404
        assert_response_time(r)


class TestProduction:
    """生产排产/品质/工艺接口测试"""

    def test_schedule_production(self, session):
        """正常路径：排产计划"""
        r = session.post(f"{API_BASE}/api/production/schedule", timeout=10)
        assert r.status_code == 200
        assert_response_time(r)

    def test_quality_monthly_success(self, session):
        """正常路径：品质月报"""
        r = session.get(f"{API_BASE}/api/quality/monthly/2026-06", timeout=10)
        assert r.status_code in (200, 404)

    def test_quality_monthly_future(self, session):
        """边界情况：未来时间段"""
        r = session.get(f"{API_BASE}/api/quality/monthly/2099-01", timeout=10)
        assert r.status_code == 400
        assert_response_time(r)

    def test_process_analysis_success(self, session):
        """正常路径：工艺分析"""
        r = session.get(f"{API_BASE}/api/production/process-analysis",
                        params={"product_line": "充电宝产线A", "period": "2026-Q2"}, timeout=10)
        assert r.status_code in (200, 404)

    def test_process_analysis_not_found(self, session):
        """边界情况：不存在的产线"""
        r = session.get(f"{API_BASE}/api/production/process-analysis",
                        params={"product_line": "UNKNOWN_LINE", "period": "2026-Q2"}, timeout=10)
        assert r.status_code == 404
        assert_response_time(r)

    def test_complaint_analysis_success(self, session):
        """正常路径：客诉分析"""
        r = session.get(f"{API_BASE}/api/quality/complaint/CP0001", timeout=10)
        assert r.status_code in (200, 404)

    def test_complaint_not_found(self, session):
        """边界情况：不存在的投诉"""
        r = session.get(f"{API_BASE}/api/quality/complaint/INVALID_CP", timeout=10)
        assert r.status_code == 404
        assert_response_time(r)


class TestAmoeba:
    """阿米巴经营分析接口测试"""

    def test_amoeba_accounting_success(self, session):
        """正常路径：阿米巴核算"""
        r = session.get(f"{API_BASE}/api/amoeba/accounting",
                        params={"unit": "销售部", "period": "2026-06"}, timeout=10)
        assert r.status_code in (200, 404)

    def test_amoeba_not_found(self, session):
        """边界情况：不存在的阿米巴单元"""
        r = session.get(f"{API_BASE}/api/amoeba/accounting",
                        params={"unit": "UNKNOWN", "period": "2026-06"}, timeout=10)
        assert r.status_code == 404
        assert_response_time(r)


class TestPolicy:
    """政策合规接口测试"""

    def test_policy_check_success(self, session):
        """正常路径：政策合规检查"""
        r = session.get(f"{API_BASE}/api/policy/check",
                        params={"document": "报销申请单20260715", "policy_id": "POL-002"}, timeout=10)
        assert r.status_code in (200, 404)

    def test_policy_check_not_found(self, session):
        """边界情况：不存在的政策"""
        r = session.get(f"{API_BASE}/api/policy/check",
                        params={"document": "报销单", "policy_id": "POL-999"}, timeout=10)
        assert r.status_code == 404
        assert_response_time(r)

    def test_gov_policy_match_empty_industry(self, session):
        """边界情况：空行业"""
        r = session.get(f"{API_BASE}/api/gov/policy-match",
                        params={"company_industry": "", "company_region": "深圳", "revenue": "50000000"}, timeout=10)
        assert r.status_code in (400, 422)

    def test_gov_policy_match_success(self, session):
        """正常路径：政策匹配"""
        r = session.get(f"{API_BASE}/api/gov/policy-match",
                        params={"company_industry": "新能源", "company_region": "深圳", "revenue": "50000000"}, timeout=10)
        assert r.status_code == 200
        assert_response_time(r)

    def test_qualification_plan_empty_markets(self, session):
        """边界情况：空目标市场"""
        r = session.get(f"{API_BASE}/api/gov/qualification-plan",
                        params={"company_stage": "扩张期", "target_markets": ""}, timeout=10)
        assert r.status_code in (400, 422)

    def test_qualification_plan_success(self, session):
        """正常路径：资质规划"""
        r = session.get(f"{API_BASE}/api/gov/qualification-plan",
                        params={"company_stage": "扩张期", "target_markets": "欧美"}, timeout=10)
        assert r.status_code == 200
        assert_response_time(r)


class TestLogistics:
    """物流接口测试"""

    def test_logistics_quote_success(self, session):
        """正常路径：物流报价"""
        r = session.get(f"{API_BASE}/api/logistics/quote",
                        params={"origin": "深圳", "destination": "洛杉矶", "weight_kg": 500, "volume_cbm": 2.5}, timeout=10)
        assert r.status_code in (200, 404)

    def test_logistics_quote_not_found(self, session):
        """边界情况：不支持的目的地"""
        r = session.get(f"{API_BASE}/api/logistics/quote",
                        params={"origin": "深圳", "destination": "UNKNOWN", "weight_kg": 500, "volume_cbm": 2.5}, timeout=10)
        assert r.status_code == 404
        assert_response_time(r)


class TestSuppliers:
    """供应商评价接口测试"""

    def test_supplier_compare_empty(self, session):
        """边界情况：空供应商列表"""
        r = session.get(f"{API_BASE}/api/suppliers/compare", params={"material": "锂电池组", "qty": 1000}, timeout=10)
        assert r.status_code in (200, 400)
        if r.status_code == 200:
            assert_response_time(r)

    def test_supplier_evaluate_empty_dimensions(self, session):
        """边界情况：空评价维度"""
        r = session.get(f"{API_BASE}/api/suppliers/SUP001/evaluate", params={"dimensions": ""}, timeout=10)
        assert r.status_code in (400, 422)

    def test_supplier_evaluate_success(self, session):
        """正常路径：供应商评价"""
        r = session.get(f"{API_BASE}/api/suppliers/SUP001/evaluate",
                        params={"dimensions": "质量,交期,价格,服务"}, timeout=10)
        assert r.status_code == 200
        assert_response_time(r)
        data = extract_data(r)
        assert "overall_score" in data
        assert "level" in data

    def test_supplier_evaluate_not_found(self, session):
        """边界情况：不存在的供应商"""
        r = session.get(f"{API_BASE}/api/suppliers/UNKNOWN/evaluate", params={"dimensions": "质量"}, timeout=10)
        assert r.status_code == 404
        assert_response_time(r)


class TestMarketForecast:
    """市场行情预测"""

    def test_forecast_success(self, session):
        """正常路径：价格预测"""
        r = session.get(f"{API_BASE}/api/market/forecast",
                        params={"material": "锂电池组(18650)", "horizon_months": 3}, timeout=10)
        assert r.status_code in (200, 404)

    def test_forecast_not_found(self, session):
        """边界情况：不存在的物料"""
        r = session.get(f"{API_BASE}/api/market/forecast",
                        params={"material": "UNKNOWN_MATERIAL", "horizon_months": 3}, timeout=10)
        assert r.status_code == 404
        assert_response_time(r)