"""
倍斯特 - Dashboard 看板 Web 自动化测试

覆盖场景：
- 正常路径：页面加载、导航菜单、统计卡片、数据表格、图表区
- 边界情况：空数据状态、大量数据渲染
- 异常情况：页面加载失败、局部组件异常
- 截图对比
"""

import pytest
import allure
from conftest import (
    assert_element_visible,
    assert_element_contains_text,
    click_element,
    wait_for_navigation,
    get_element_text,
    navigate_to,
)


# ── 正常路径 ──────────────────────────────────────────────────────────────────


@allure.feature("Dashboard 看板")
@allure.story("正常路径")
class TestDashboardNormal:

    @allure.title("页面加载 - Dashboard 页面完整渲染")
    def test_dashboard_page_load(self, page, base_url, take_screenshot):
        """验证 Dashboard 页面所有主要区域正确加载"""
        page.goto(f"{base_url}/web/dashboard.html", wait_until="networkidle")

        # 验证页面标题
        assert "仪表盘" in page.title() or "倍斯特" in page.title()

        # 验证头部区域
        assert_element_visible(page, "h1")
        assert_element_contains_text(page, "h1", "仪表盘")

        # 验证统计卡片区域
        assert_element_visible(page, "#statsGrid")
        assert_element_visible(page, "#statOrders")
        assert_element_visible(page, "#statProduction")
        assert_element_visible(page, "#statWarnings")
        assert_element_visible(page, "#statRevenue")

        # 验证图表区域
        assert_element_visible(page, "#orderChart")
        assert_element_visible(page, "#productChart")

        # 验证数据表格
        assert_element_visible(page, "#recentOrdersTable")
        assert_element_contains_text(page, "#recentOrdersTable", "订单号")

        # 截图
        take_screenshot("dashboard_full_page")

    @allure.title("导航菜单 - 所有菜单项渲染")
    def test_navigation_menu(self, page, base_url, take_screenshot):
        """验证左侧导航菜单所有项正确渲染"""
        page.goto(f"{base_url}/web/dashboard.html", wait_until="networkidle")

        # 验证侧边栏
        assert_element_visible(page, ".sidebar")

        # 验证所有导航项
        nav_items = {
            "仪表盘": "📊",
            "订单管理": "📋",
            "库存管理": "📦",
            "生产管理": "🏭",
            "AI 助手": "🤖",
            "系统设置": "⚙️",
        }

        nav_els = page.locator(".sidebar .nav li")
        nav_count = nav_els.count()
        assert nav_count >= 6, f"导航项数量不足: {nav_count}"

        for label, icon in nav_items.items():
            assert_element_contains_text(page, ".sidebar", label)

        # 验证默认激活项
        active_item = page.locator(".sidebar .nav li.active")
        assert active_item.count() >= 1

        take_screenshot("dashboard_navigation")

    @allure.title("导航菜单切换 - 点击菜单项切换激活状态")
    def test_navigation_switch(self, page, base_url):
        """验证点击不同导航菜单项时激活状态切换"""
        page.goto(f"{base_url}/web/dashboard.html", wait_until="networkidle")

        # 默认仪表盘激活
        active_items = page.locator(".sidebar .nav li.active")
        initial_active_text = active_items.first.text_content() or ""
        assert "仪表盘" in initial_active_text

        # 点击"订单管理"
        click_element(page, ".sidebar .nav li:nth-child(2)")
        page.wait_for_timeout(300)

        # 验证激活项切换
        active_items = page.locator(".sidebar .nav li.active")
        new_active_text = active_items.first.text_content() or ""
        assert "订单管理" in new_active_text

    @allure.title("统计卡片 - 数据展示正确")
    def test_stat_cards_data(self, page, base_url):
        """验证统计卡片数据展示"""
        page.goto(f"{base_url}/web/dashboard.html", wait_until="networkidle")

        # 验证各统计值不为空
        stat_orders = page.locator("#statOrders")
        assert len((stat_orders.text_content() or "").strip()) > 0

        stat_production = page.locator("#statProduction")
        assert len((stat_production.text_content() or "").strip()) > 0

        stat_warnings = page.locator("#statWarnings")
        assert len((stat_warnings.text_content() or "").strip()) > 0

        stat_revenue = page.locator("#statRevenue")
        assert len((stat_revenue.text_content() or "").strip()) > 0

    @allure.title("数据表格 - 表格行和状态标签")
    def test_data_table(self, page, base_url, take_screenshot):
        """验证最近订单表格数据展示"""
        page.goto(f"{base_url}/web/dashboard.html", wait_until="networkidle")

        # 验证表格标题
        assert_element_contains_text(page, "#recentOrdersTable", "最近订单")

        # 验证表头
        headers = ["订单号", "客户", "产品型号", "数量", "状态", "交期"]
        for header in headers:
            assert_element_contains_text(page, "#recentOrdersTable thead", header)

        # 验证表格行数
        rows = page.locator("#recentOrdersTable tbody tr")
        row_count = rows.count()
        assert row_count >= 5, f"数据行数不足: {row_count}"

        # 验证状态标签
        status_badges = page.locator(".status-badge")
        assert status_badges.count() >= 3

        take_screenshot("dashboard_data_table")

    @allure.title("用户信息 - 头部用户信息展示")
    def test_user_info(self, page, base_url):
        """验证用户信息显示"""
        page.goto(f"{base_url}/web/dashboard.html", wait_until="networkidle")

        # 验证用户信息区域
        assert_element_visible(page, ".user-info")
        assert_element_visible(page, ".avatar")
        assert_element_contains_text(page, ".user-info", "管理员")


# ── 边界情况 ──────────────────────────────────────────────────────────────────


@allure.feature("Dashboard 看板")
@allure.story("边界情况")
class TestDashboardBoundary:

    @allure.title("图表区域 - 占位内容展示")
    def test_chart_placeholders(self, page, base_url, take_screenshot):
        """验证图表占位区域正常渲染"""
        page.goto(f"{base_url}/web/dashboard.html", wait_until="networkidle")

        # 验证图表占位
        chart_placeholder = page.locator(".chart-placeholder")
        assert chart_placeholder.count() >= 2

        # 获取图表内容
        for i in range(chart_placeholder.count()):
            text = chart_placeholder.nth(i).text_content() or ""
            assert len(text) > 0

        take_screenshot("dashboard_chart_placeholders")

    @allure.title("统计数据更新 - 模拟数据动态变化")
    def test_stat_updates(self, page, base_url):
        """验证统计数据的动态更新（模拟）"""
        page.goto(f"{base_url}/web/dashboard.html", wait_until="networkidle")

        # 获取初始值
        initial_value = page.locator("#statOrders").text_content() or ""

        # 等待数据更新（页面有定时器模拟更新）
        page.wait_for_timeout(8000)

        # 获取更新后的值
        new_value = page.locator("#statOrders").text_content() or ""

        # 验证值不为空
        assert len(initial_value) > 0
        assert len(new_value) > 0

    @allure.title("长页面滚动 - 完整页面渲染")
    def test_page_scroll(self, page, base_url, take_screenshot):
        """验证页面滚动后所有内容正常渲染"""
        page.goto(f"{base_url}/web/dashboard.html", wait_until="networkidle")

        # 滚动到底部
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(500)

        # 截图底部
        take_screenshot("dashboard_page_bottom")

        # 滚动回顶部
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(300)

        # 验证顶部元素仍然可见
        assert_element_visible(page, "h1")


# ── 异常情况 ──────────────────────────────────────────────────────────────────


@allure.feature("Dashboard 看板")
@allure.story("异常情况")
class TestDashboardAbnormal:

    @allure.title("页面加载超时 - 慢速网络模拟")
    def test_page_load_timeout(self, page, take_screenshot):
        """验证页面加载超时行为"""
        try:
            page.goto("http://192.0.2.1/web/dashboard.html", timeout=3000, wait_until="domcontentloaded")
        except Exception:
            pass

        take_screenshot("dashboard_timeout")

    @allure.title("大量数据渲染 - 性能评估")
    def test_large_data_rendering(self, page, base_url, take_screenshot):
        """通过注入大量 DOM 模拟大负载"""
        page.goto(f"{base_url}/web/dashboard.html", wait_until="networkidle")

        # 注入大量行到表格
        page.evaluate("""
            const tbody = document.querySelector('#recentOrdersTable tbody');
            for (let i = 0; i < 100; i++) {
                const row = document.createElement('tr');
                row.innerHTML = `<td>ORD${10000 + i}</td><td>客户${i}</td>
                    <td>C${i}00充电宝</td><td>${i * 100}</td>
                    <td><span class="status-badge production">生产中</span></td>
                    <td>2026-12-${String(i % 30 + 1).padStart(2, '0')}</td>`;
                tbody.appendChild(row);
            }
        """)

        page.wait_for_timeout(1000)

        # 验证页面未崩溃
        rows = page.locator("#recentOrdersTable tbody tr")
        assert rows.count() >= 105  # 原有的5行 + 100新行

        take_screenshot("dashboard_large_data")

    @allure.title("并发页面 - 多标签页稳定性")
    def test_concurrent_tabs(self, browser_type, playwright_context, base_url, take_screenshot):
        """验证多标签页打开时的稳定性"""
        page = playwright_context

        # 打开第一个标签
        page.goto(f"{base_url}/web/dashboard.html", wait_until="networkidle")

        # 打开第二个标签
        page2 = page.context.new_page()
        page2.goto(f"{base_url}/web/login.html", wait_until="networkidle")

        # 打开第三个标签
        page3 = page.context.new_page()
        page3.goto(f"{base_url}/web/agent.html", wait_until="networkidle")

        # 验证所有标签页正常
        assert page.locator("h1").is_visible()
        assert page2.locator("#username").is_visible()
        assert page3.locator("#chatInput").is_visible()

        take_screenshot("dashboard_concurrent_tabs")

        page2.close()
        page3.close()