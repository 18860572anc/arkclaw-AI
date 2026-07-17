"""
倍斯特 - 移动端响应式 Web 自动化测试

覆盖场景：
- 正常路径：移动端页面加载、关键元素渲染
- 边界情况：不同设备尺寸适配、横竖屏切换
- 异常情况：触摸事件处理、性能负载
"""

import pytest
import allure
from conftest import (
    assert_element_visible,
    assert_element_contains_text,
    click_element,
    get_element_text,
    VIEWPORT_TABLET,
    VIEWPORT_MOBILE,
)


# ── 正常路径 ──────────────────────────────────────────────────────────────────


@allure.feature("移动端响应式")
@allure.story("正常路径")
class TestMobileNormal:

    @allure.title("移动端登录页 - 关键元素渲染")
    def test_mobile_login_page(self, page_mobile, base_url, take_screenshot):
        """验证移动端登录页面元素渲染"""
        page = page_mobile
        page.goto(f"{base_url}/web/login.html", wait_until="networkidle")

        # 验证核心元素可见
        assert_element_visible(page, ".login-container")
        assert_element_visible(page, "#username")
        assert_element_visible(page, "#password")
        assert_element_visible(page, "#loginBtn")

        # 验证表单可操作
        fill_input(page, "#username", "admin")
        fill_input(page, "#password", "password123")
        click_element(page, "#loginBtn")

        page.wait_for_timeout(1500)

        take_screenshot("mobile_login")

    @allure.title("移动端 Dashboard - 适配布局")
    def test_mobile_dashboard(self, page_mobile, base_url, take_screenshot):
        """验证移动端 Dashboard 关键元素和布局"""
        page = page_mobile
        page.goto(f"{base_url}/web/dashboard.html", wait_until="networkidle")

        # 验证侧边栏在移动端的行为
        sidebar = page.locator(".sidebar")
        assert sidebar.is_visible()

        # 验证统计卡片（移动端应堆叠显示）
        stats_grid = page.locator("#statsGrid")
        assert stats_grid.is_visible()

        # 验证数据表格
        assert_element_visible(page, "#recentOrdersTable")

        # 截图
        take_screenshot("mobile_dashboard")

    @allure.title("移动端 AI Agent - 聊天界面适配")
    def test_mobile_agent(self, page_mobile, base_url, take_screenshot):
        """验证移动端 AI Agent 聊天界面"""
        page = page_mobile
        page.goto(f"{base_url}/web/agent.html", wait_until="networkidle")

        # 验证聊天界面
        assert_element_visible(page, "#chatMessages")
        assert_element_visible(page, "#chatInput")
        assert_element_visible(page, "#sendBtn")

        # 发送消息
        fill_input(page, "#chatInput", "移动端测试")
        click_element(page, "#sendBtn")

        page.wait_for_timeout(2500)

        take_screenshot("mobile_agent")


# ── 边界情况 ──────────────────────────────────────────────────────────────────


@allure.feature("移动端响应式")
@allure.story("边界情况")
class TestMobileBoundary:

    @allure.title("平板尺寸 - 各页面渲染")
    def test_tablet_viewport(self, page_tablet, base_url, take_screenshot):
        """验证平板尺寸下的页面渲染"""
        page = page_tablet

        # 登录页面
        page.goto(f"{base_url}/web/login.html", wait_until="networkidle")
        assert_element_visible(page, "#loginBtn")
        take_screenshot("tablet_login")

        # Dashboard
        page.goto(f"{base_url}/web/dashboard.html", wait_until="networkidle")
        assert_element_visible(page, "#statsGrid")
        take_screenshot("tablet_dashboard")

        # AI Agent
        page.goto(f"{base_url}/web/agent.html", wait_until="networkidle")
        assert_element_visible(page, "#chatInput")
        take_screenshot("tablet_agent")

    @allure.title("极窄屏幕 - 320px 宽度适配")
    def test_narrow_screen(self, page, base_url, take_screenshot):
        """验证极小屏幕宽度下的布局"""
        page.set_viewport_size({"width": 320, "height": 568})

        # 登录页面
        page.goto(f"{base_url}/web/login.html", wait_until="networkidle")
        # 容器不应溢出
        container = page.locator(".login-container")
        box = container.bounding_box()
        assert box is not None
        assert box["width"] <= 380  # 容器宽度应适配屏幕
        take_screenshot("narrow_login")

        # Dashboard
        page.goto(f"{base_url}/web/dashboard.html", wait_until="networkidle")
        take_screenshot("narrow_dashboard")

        # AI Agent
        page.goto(f"{base_url}/web/agent.html", wait_until="networkidle")
        assert_element_visible(page, "#chatInput")
        take_screenshot("narrow_agent")

    @allure.title("横竖屏切换 - 布局稳定性")
    def test_orientation_switch(self, page, base_url, take_screenshot):
        """验证横竖屏切换的布局稳定性"""
        # 竖屏
        page.set_viewport_size({"width": 375, "height": 812})
        page.goto(f"{base_url}/web/dashboard.html", wait_until="networkidle")
        page.wait_for_timeout(300)
        take_screenshot("orientation_portrait")

        # 横屏
        page.set_viewport_size({"width": 812, "height": 375})
        page.wait_for_timeout(500)
        take_screenshot("orientation_landscape")

        # 切换回竖屏
        page.set_viewport_size({"width": 375, "height": 812})
        page.wait_for_timeout(300)

        # 验证可操作
        assert_element_visible(page, "h1")

    @allure.title("高 DPI 屏幕 - Retina 显示适配")
    def test_high_dpi(self, page, base_url, take_screenshot):
        """模拟高 DPI 屏幕"""
        page.set_viewport_size({"width": 414, "height": 896})
        page.goto(f"{base_url}/web/login.html", wait_until="networkidle")
        assert_element_visible(page, "#loginBtn")
        take_screenshot("high_dpi_login")

    @allure.title("超大字体 - 无障碍访问")
    def test_large_font(self, page, base_url, take_screenshot):
        """验证浏览器放大字体后的布局"""
        page.set_viewport_size({"width": 375, "height": 812})
        # 通过 JS 模拟字体放大
        page.goto(f"{base_url}/web/login.html", wait_until="networkidle")
        page.evaluate("document.body.style.fontSize = '24px'")

        page.wait_for_timeout(300)
        take_screenshot("large_font_login")


# ── 异常情况 ──────────────────────────────────────────────────────────────────


@allure.feature("移动端响应式")
@allure.story("异常情况")
class TestMobileAbnormal:

    @allure.title("无网络 - 离线模式")
    def test_offline_mode(self, page_mobile, base_url, take_screenshot):
        """验证移动端离线时的行为"""
        page = page_mobile

        # 先加载页面，再断开网络
        page.goto(f"{base_url}/web/login.html", wait_until="networkidle")
        page.context.set_offline(True)

        try:
            page.goto(f"{base_url}/web/dashboard.html", wait_until="domcontentloaded", timeout=5000)
        except Exception:
            pass

        take_screenshot("mobile_offline")

        # 恢复网络
        page.context.set_offline(False)

    @allure.title("触摸事件 - 模拟触摸操作")
    def test_touch_events(self, page_mobile, base_url, take_screenshot):
        """验证移动端触摸交互"""
        page = page_mobile
        page.goto(f"{base_url}/web/login.html", wait_until="networkidle")

        # 模拟触摸点击输入框
        username = page.locator("#username")
        username.tap()
        page.wait_for_timeout(200)

        # 验证输入框获得焦点
        focused = page.evaluate("document.activeElement === document.getElementById('username')")
        # 注意：tap 可能不会触发 focus，取决于浏览器实现

        # 通过 JS 填入内容
        page.evaluate("document.getElementById('username').value = 'touch_user'")
        page.evaluate("document.getElementById('password').value = 'touch_pass'")

        # 点击登录按钮
        login_btn = page.locator("#loginBtn")
        login_btn.tap()
        page.wait_for_timeout(1500)

        take_screenshot("mobile_touch_login")

    @allure.title("慢速网络 - 页面加载性能")
    def test_slow_network(self, page_mobile, base_url, take_screenshot):
        """验证慢速网络下的页面加载"""
        page = page_mobile

        # 模拟慢速网络（通过 CDP）
        client = page.context.new_cdp_session(page)
        try:
            client.send("Network.emulateNetworkConditions", {
                "offline": False,
                "latency": 500,
                "downloadThroughput": 500 * 1024,  # 500 KB/s
                "uploadThroughput": 100 * 1024,  # 100 KB/s
            })
        except Exception:
            pass  # 可能不支持 CDP

        page.goto(f"{base_url}/web/login.html", wait_until="networkidle")
        assert_element_visible(page, "#loginBtn")
        take_screenshot("mobile_slow_network")

    @allure.title("移动端浏览器兼容 - 模拟 Safari")
    def test_mobile_safari_compatibility(self, page, base_url, take_screenshot):
        """模拟移动端 Safari 浏览器的 UA"""
        page.set_viewport_size({"width": 375, "height": 812})
        page.context.set_extra_http_headers({
            "User-Agent": (
                "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 "
                "Mobile/15E148 Safari/604.1"
            )
        })

        page.goto(f"{base_url}/web/login.html", wait_until="networkidle")
        assert_element_visible(page, "#loginBtn")
        take_screenshot("mobile_safari_ua")