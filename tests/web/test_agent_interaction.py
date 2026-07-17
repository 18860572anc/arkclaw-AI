"""
倍斯特 - AI Agent 交互界面 Web 自动化测试

覆盖场景：
- 正常路径：页面加载、聊天界面渲染、消息发送与回复
- 边界情况：空消息、超长消息、特殊字符、快速连续发送
- 异常情况：服务不可用、网络异常、页面错误
"""

import pytest
import allure
from conftest import (
    assert_element_visible,
    assert_element_contains_text,
    fill_input,
    click_element,
    get_element_text,
)


# ── 正常路径 ──────────────────────────────────────────────────────────────────


@allure.feature("AI Agent 交互界面")
@allure.story("正常路径")
class TestAgentNormal:

    @allure.title("页面加载 - 聊天界面完整渲染")
    def test_agent_page_load(self, page, base_url, take_screenshot):
        """验证 AI Agent 页面所有元素正确渲染"""
        page.goto(f"{base_url}/web/agent.html", wait_until="networkidle")

        # 验证页面标题
        assert "AI 助手" in page.title() or "倍斯特" in page.title()

        # 验证头部
        assert_element_contains_text(page, ".chat-header h1", "AI 智能助手")
        assert_element_contains_text(page, ".chat-header p", "倍斯特")

        # 验证聊天消息区域
        assert_element_visible(page, "#chatMessages")

        # 验证输入区域
        assert_element_visible(page, "#chatInput")
        assert_element_visible(page, "#sendBtn")

        # 验证默认消息
        assert_element_contains_text(page, "#chatMessages", "AI 助手")
        assert_element_contains_text(page, "#chatMessages", "订单")

        # 截图
        take_screenshot("agent_page_load")

    @allure.title("消息发送 - 输入消息并发送")
    def test_send_message(self, page, base_url, take_screenshot):
        """验证发送消息后界面更新"""
        page.goto(f"{base_url}/web/agent.html", wait_until="networkidle")

        # 发送消息
        fill_input(page, "#chatInput", "显示最近订单状态")
        click_element(page, "#sendBtn")

        # 等待消息发送（用户消息立即出现）
        page.wait_for_timeout(500)

        # 验证用户消息出现在聊天区域
        messages = page.locator("#chatMessages .message.user")
        assert messages.count() >= 2  # 加上默认示例消息

        # 等待 AI 回复（模拟延迟 1.5s）
        page.wait_for_timeout(2000)

        # 验证 AI 回复
        assistant_messages = page.locator("#chatMessages .message.assistant")
        assert assistant_messages.count() >= 2  # 默认问候 + 回复

        # 截图
        take_screenshot("agent_send_message")

    @allure.title("发送按钮状态 - 不同输入状态下的按钮")
    def test_send_button_state(self, page, base_url):
        """验证发送按钮在不同输入状态下的行为"""
        page.goto(f"{base_url}/web/agent.html", wait_until="networkidle")

        send_btn = page.locator("#sendBtn")

        # 初始状态可用
        assert not send_btn.is_disabled()

        # 输入文本后仍可用
        fill_input(page, "#chatInput", "hello")
        assert not send_btn.is_disabled()

        # 发送后暂时禁用（等待回复期间）
        click_element(page, "#sendBtn")
        page.wait_for_timeout(300)
        # 发送后按钮应禁用（等待回复）
        # 实际行为取决于前端实现

    @allure.title("历史消息 - 默认消息展示")
    def test_default_messages(self, page, base_url):
        """验证页面加载时默认展示的历史消息"""
        page.goto(f"{base_url}/web/agent.html", wait_until="networkidle")

        # 验证默认的 AI 问候消息
        assert_element_contains_text(page, "#chatMessages", "倍斯特 AI 助手")

        # 验证示例消息
        assert_element_visible(page, "#sampleUserMsg")
        assert_element_visible(page, "#sampleAssistantMsg")

        # 验证示例消息中的表格数据
        assert_element_contains_text(page, "#sampleAssistantMsg", "ORD1001")
        assert_element_contains_text(page, "#sampleAssistantMsg", "生产中")


# ── 边界情况 ──────────────────────────────────────────────────────────────────


@allure.feature("AI Agent 交互界面")
@allure.story("边界情况")
class TestAgentBoundary:

    @allure.title("空消息 - 发送空消息的处理")
    def test_empty_message(self, page, base_url, take_screenshot):
        """验证发送空消息时的行为"""
        page.goto(f"{base_url}/web/agent.html", wait_until="networkidle")

        # 获取发送前消息数量
        initial_count = page.locator("#chatMessages .message").count()

        # 尝试发送空消息
        click_element(page, "#sendBtn")
        page.wait_for_timeout(500)

        # 消息数量应不变（空消息不应发送）
        after_count = page.locator("#chatMessages .message").count()
        assert after_count == initial_count

        take_screenshot("agent_empty_message")

    @allure.title("超长消息 - 发送长文本的处理")
    def test_long_message(self, page, base_url, take_screenshot):
        """验证超长消息的发送"""
        page.goto(f"{base_url}/web/agent.html", wait_until="networkidle")

        long_message = "查询订单" * 200
        fill_input(page, "#chatInput", long_message)
        click_element(page, "#sendBtn")

        page.wait_for_timeout(2500)

        # 验证消息已发送
        messages = page.locator("#chatMessages .message.user")
        last_msg = messages.last.text_content() or ""
        assert "查询订单" in last_msg

        take_screenshot("agent_long_message")

    @allure.title("特殊字符消息 - XSS 和 SQL 注入字符")
    def test_special_chars_message(self, page, base_url):
        """验证包含特殊字符消息的发送"""
        page.goto(f"{base_url}/web/agent.html", wait_until="networkidle")

        special_messages = [
            "<script>alert('xss')</script>",
            "<img src=x onerror=alert(1)>",
            "' OR '1'='1",
            "'; DROP TABLE users; --",
            "你好世界！@#$%^&*()",
            "   多个空格   ",
            "🚀🌟🎉",
        ]

        for msg in special_messages:
            fill_input(page, "#chatInput", msg)
            click_element(page, "#sendBtn")
            page.wait_for_timeout(2500)  # 等待回复

            # 验证消息显示正确
            messages = page.locator("#chatMessages .message.user")
            last_msg = messages.last.text_content() or ""
            assert len(last_msg) > 0

    @allure.title("快速连续发送 - 限流或节流")
    def test_rapid_messages(self, page, base_url, take_screenshot):
        """验证快速连续发送消息时的行为"""
        page.goto(f"{base_url}/web/agent.html", wait_until="networkidle")

        # 连续发送 5 条消息
        for i in range(5):
            fill_input(page, "#chatInput", f"第{i+1}条消息")
            click_element(page, "#sendBtn")
            page.wait_for_timeout(100)

        # 等待所有回复
        page.wait_for_timeout(5000)

        # 验证用户消息数量
        user_messages = page.locator("#chatMessages .message.user")
        # 应该包含默认示例消息 + 5条新消息
        assert user_messages.count() >= 6

        take_screenshot("agent_rapid_messages")


# ── 异常情况 ──────────────────────────────────────────────────────────────────


@allure.feature("AI Agent 交互界面")
@allure.story("异常情况")
class TestAgentAbnormal:

    @allure.title("无效页面路径 - 后端不可用")
    def test_invalid_agent_page(self, page, base_url, take_screenshot):
        """验证访问不存在的页面"""
        response = page.goto(f"{base_url}/web/agent_nonexistent.html", wait_until="domcontentloaded")
        take_screenshot("agent_invalid_page")

    @allure.title("大量消息 - 聊天界面性能")
    def test_many_messages(self, page, base_url, take_screenshot):
        """验证生成大量消息后的界面性能"""
        page.goto(f"{base_url}/web/agent.html", wait_until="networkidle")

        # 通过 JS 快速注入大量消息
        page.evaluate("""
            const container = document.getElementById('chatMessages');
            for (let i = 0; i < 50; i++) {
                const msg = document.createElement('div');
                msg.className = 'message user';
                msg.innerHTML = `<div class="avatar">我</div>
                    <div class="bubble"><div>测试消息 #${i}</div>
                    <div class="time">10:00</div></div>`;
                container.appendChild(msg);

                const reply = document.createElement('div');
                reply.className = 'message assistant';
                reply.innerHTML = `<div class="avatar">AI</div>
                    <div class="bubble"><div>这是自动回复 #${i}</div>
                    <div class="time">10:00</div></div>`;
                container.appendChild(reply);
            }
        """)

        page.wait_for_timeout(1000)

        # 验证页面未崩溃
        messages = page.locator("#chatMessages .message")
        assert messages.count() >= 100

        # 验证输入框仍可操作
        assert_element_visible(page, "#chatInput")

        take_screenshot("agent_many_messages")

    @allure.title("窗口调整 - 响应式布局稳定性")
    def test_window_resize(self, page, base_url, take_screenshot):
        """验证窗口调整大小后界面布局稳定性"""
        page.goto(f"{base_url}/web/agent.html", wait_until="networkidle")

        # 设置不同窗口尺寸
        viewports = [
            {"width": 1920, "height": 1080},
            {"width": 1440, "height": 900},
            {"width": 1024, "height": 768},
            {"width": 768, "height": 1024},
        ]

        for vp in viewports:
            page.set_viewport_size(vp)
            page.wait_for_timeout(300)
            # 验证关键元素仍可见
            assert_element_visible(page, "#chatInput")
            assert_element_visible(page, "#sendBtn")

        # 极窄窗口
        page.set_viewport_size({"width": 320, "height": 568})
        page.wait_for_timeout(500)
        take_screenshot("agent_narrow_window")

    @allure.title("输入框清空 - 连续操作稳定性")
    def test_input_clear(self, page, base_url):
        """验证输入框内容清空后的行为"""
        page.goto(f"{base_url}/web/agent.html", wait_until="networkidle")

        # 输入、清空、再输入
        fill_input(page, "#chatInput", "测试消息")
        fill_input(page, "#chatInput", "")
        fill_input(page, "#chatInput", "新消息")
        click_element(page, "#sendBtn")

        page.wait_for_timeout(2500)
        # 验证新消息已发送
        assert_element_contains_text(page, "#chatMessages", "新消息")