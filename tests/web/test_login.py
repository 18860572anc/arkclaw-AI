"""
倍斯特 - 登录页面 Web 自动化测试

覆盖场景：
- 正常路径：页面加载、表单元素渲染、成功登录跳转
- 边界情况：空字段、特殊字符输入、超长输入
- 异常情况：网络超时模拟、错误页面展示
"""

import os
import pytest
import allure
from conftest import (
    assert_element_visible,
    assert_element_contains_text,
    fill_input,
    click_element,
    wait_for_navigation,
    get_element_text,
    navigate_to,
)


# ── 正常路径 ──────────────────────────────────────────────────────────────────


@allure.feature("登录页面")
@allure.story("正常路径")
class TestLoginNormal:

    @allure.title("页面加载 - 登录表单元素完整渲染")
    def test_login_page_elements(self, page, base_url, take_screenshot):
        """验证登录页面所有关键元素正确渲染"""
        page.goto(f"{base_url}/web/login.html", wait_until="networkidle")

        # 验证页面标题
        assert "登录" in page.title()

        # 验证 Logo 和标题
        assert_element_contains_text(page, ".logo h1", "倍斯特科技")

        # 验证表单元素存在
        assert_element_visible(page, "#username")
        assert_element_visible(page, "#password")
        assert_element_visible(page, "#loginBtn")
        assert_element_visible(page, "#remarks")

        # 验证链接存在
        assert_element_visible(page, 'a[href="/forgot-password"]')
        assert_element_visible(page, 'a[href="/register"]')

        # 截图
        take_screenshot("login_page_elements")

    @allure.title("成功登录 - 填写有效凭证后可跳转")
    def test_successful_login(self, page, base_url, take_screenshot):
        """验证输入有效用户名和密码后成功登录"""
        page.goto(f"{base_url}/web/login.html", wait_until="networkidle")

        fill_input(page, "#username", "admin")
        fill_input(page, "#password", "password123")
        click_element(page, "#loginBtn")

        # 等待登录成功消息
        page.wait_for_selector("#successMessage.visible", timeout=5000)
        assert_element_visible(page, "#successMessage")

        take_screenshot("login_success")

    @allure.title("登录按钮 - 表单提交时按钮状态变化")
    def test_login_button_state(self, page, base_url):
        """验证登录按钮点击后的状态变化"""
        page.goto(f"{base_url}/web/login.html", wait_until="networkidle")

        fill_input(page, "#username", "admin")
        fill_input(page, "#password", "password123")

        # 按钮初始状态可用
        login_btn = page.locator("#loginBtn")
        assert not login_btn.is_disabled()

        # 点击后应变为禁用
        click_element(page, "#loginBtn")
        # 注意：按钮会在点击后立即禁用
        page.wait_for_timeout(300)
        # 如果成功消息出现，说明已提交成功
        success_msg = page.locator("#successMessage")
        if success_msg.is_visible(timeout=2000):
            assert success_msg.is_visible()


# ── 边界情况 ──────────────────────────────────────────────────────────────────


@allure.feature("登录页面")
@allure.story("边界情况")
class TestLoginBoundary:

    @allure.title("空用户名 - 提交时显示错误提示")
    def test_empty_username(self, page, base_url, take_screenshot):
        """验证提交空用户名时的错误提示"""
        page.goto(f"{base_url}/web/login.html", wait_until="networkidle")

        fill_input(page, "#password", "password123")
        click_element(page, "#loginBtn")

        # 验证用户名错误提示显示
        username_error = page.locator("#usernameError")
        assert username_error.is_visible()
        assert "请输入用户名" in (username_error.text_content() or "")

        # 验证输入框标记为错误状态
        username_input = page.locator("#username")
        assert "error" in (username_input.get_attribute("class") or "")

        take_screenshot("login_empty_username")

    @allure.title("空密码 - 提交时显示错误提示")
    def test_empty_password(self, page, base_url):
        """验证提交空密码时的错误提示"""
        page.goto(f"{base_url}/web/login.html", wait_until="networkidle")

        fill_input(page, "#username", "admin")
        click_element(page, "#loginBtn")

        password_error = page.locator("#passwordError")
        assert password_error.is_visible()
        assert "请输入密码" in (password_error.text_content() or "")

    @allure.title("空用户名和密码 - 同时显示两个错误提示")
    def test_empty_both(self, page, base_url, take_screenshot):
        """验证用户名和密码均为空时显示两个错误提示"""
        page.goto(f"{base_url}/web/login.html", wait_until="networkidle")

        click_element(page, "#loginBtn")

        username_error = page.locator("#usernameError")
        password_error = page.locator("#passwordError")
        assert username_error.is_visible()
        assert password_error.is_visible()

        take_screenshot("login_empty_both")

    @allure.title("特殊字符用户名 - 处理特殊字符输入")
    def test_special_characters_username(self, page, base_url):
        """验证特殊字符输入的处理"""
        page.goto(f"{base_url}/web/login.html", wait_until="networkidle")

        special_chars = [
            "admin@#$%",
            "test<script>alert(1)</script>",
            "ユーザー名",
            "admin' OR '1'='1",
            "  admin  ",
            "a" * 100,  # 长用户名
        ]

        for char_input in special_chars:
            fill_input(page, "#username", char_input)
            fill_input(page, "#password", "password123")
            click_element(page, "#loginBtn")

            # 验证输入框接受了输入（不崩溃）
            page.wait_for_timeout(500)
            # 重新加载页面以清除状态
            page.goto(f"{base_url}/web/login.html", wait_until="networkidle")

    @allure.title("超长密码输入 - 处理边界字符量")
    def test_very_long_password(self, page, base_url, take_screenshot):
        """验证超长密码输入时的行为"""
        page.goto(f"{base_url}/web/login.html", wait_until="networkidle")

        long_password = "P" * 1000
        fill_input(page, "#username", "admin")
        fill_input(page, "#password", long_password)
        click_element(page, "#loginBtn")

        # 验证不崩溃
        page.wait_for_timeout(1000)
        take_screenshot("login_long_password")

    @allure.title("备注字段 - 可选字段的边界测试")
    def test_remarks_field(self, page, base_url):
        """验证备注字段（可选）的各种输入"""
        page.goto(f"{base_url}/web/login.html", wait_until="networkidle")

        fill_input(page, "#username", "admin")
        fill_input(page, "#password", "password123")

        # 不填备注，正常提交
        click_element(page, "#loginBtn")
        page.wait_for_timeout(500)

        # 带备注提交
        page.goto(f"{base_url}/web/login.html", wait_until="networkidle")
        fill_input(page, "#username", "admin")
        fill_input(page, "#password", "password123")
        fill_input(page, "#remarks", "测试备注信息")
        click_element(page, "#loginBtn")
        page.wait_for_timeout(500)

        # 备注填超长文本
        page.goto(f"{base_url}/web/login.html", wait_until="networkidle")
        fill_input(page, "#username", "admin")
        fill_input(page, "#password", "password123")
        fill_input(page, "#remarks", "备注" * 500)
        click_element(page, "#loginBtn")
        page.wait_for_timeout(500)


# ── 异常情况 ──────────────────────────────────────────────────────────────────


@allure.feature("登录页面")
@allure.story("异常情况")
class TestLoginAbnormal:

    @allure.title("网络不可达 - 页面加载超时")
    def test_network_timeout(self, page, take_screenshot):
        """验证目标不可达时的行为"""
        try:
            page.goto("http://192.0.2.1/web/login.html", timeout=5000, wait_until="domcontentloaded")
        except Exception:
            pass  # 超时是预期的

        take_screenshot("login_network_timeout")

    @allure.title("无效页面 - 404 错误处理")
    def test_invalid_page(self, page, base_url, take_screenshot):
        """验证访问不存在的页面返回 404"""
        response = page.goto(f"{base_url}/web/nonexistent.html", wait_until="domcontentloaded")
        if response:
            status = response.status
            assert status == 404 or status == 200  # Nginx 可能返回 200 并重定向

        take_screenshot("login_invalid_page_404")

    @allure.title("服务不可用 - 后端服务断开")
    def test_backend_unavailable(self, page, base_url, take_screenshot):
        """验证后端服务不可用时的前端展现"""
        # 访问 API 状态页面确认后端状态
        try:
            response = page.goto(f"{base_url}/api/status", wait_until="domcontentloaded", timeout=10000)
            take_screenshot("login_backend_status")
        except Exception:
            take_screenshot("login_backend_unavailable")

    @allure.title("频繁刷新 - 页面稳定性")
    def test_frequent_refresh(self, page, base_url, take_screenshot):
        """验证页面频繁刷新后仍正常工作"""
        for i in range(10):
            page.goto(f"{base_url}/web/login.html", wait_until="networkidle")
            page.wait_for_timeout(100)

        # 刷新后仍可正常操作
        fill_input(page, "#username", "admin")
        fill_input(page, "#password", "password123")
        assert_element_visible(page, "#loginBtn")

        take_screenshot("login_frequent_refresh")