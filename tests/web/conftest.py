"""
倍斯特 Web 自动化测试框架 - 公共配置和 Fixtures

使用 Playwright + pytest 实现浏览器自动化测试。
测试目标：http://localhost:80（Nginx 代理入口）
浏览器引擎：browserless/chrome（通过 websocket 连接）
"""

import os
import json
import pytest
import allure
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# ── 全局配置 ──────────────────────────────────────────────────────────────────

# 测试目标 URL（Nginx 代理入口）
BASE_URL = os.environ.get("WEB_TEST_BASE_URL", "http://nginx:80")

# browserless websocket endpoint
BROWSERLESS_WS = os.environ.get(
    "BROWSERLESS_WS",
    "ws://browser:3000",
)

# 截图目录
SCREENSHOT_DIR = Path(os.environ.get("SCREENSHOT_DIR", "/app/results/screenshots"))

# 隐式等待超时（毫秒）
DEFAULT_TIMEOUT = int(os.environ.get("PLAYWRIGHT_TIMEOUT", "30000"))

# 浏览器窗口尺寸
VIEWPORT_DESKTOP = {"width": 1920, "height": 1080}
VIEWPORT_TABLET = {"width": 768, "height": 1024}
VIEWPORT_MOBILE = {"width": 375, "height": 812}


# ── Fixtures ───────────────────────────────────────────────────────────────────


def pytest_configure(config):
    """pytest 初始化：创建截图目录"""
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


def pytest_runtest_makereport(item, call):
    """测试失败时自动截图"""
    if call.when == "call" and call.excinfo is not None:
        # 获取当前 browser 实例并截图
        browser = item.funcargs.get("browser")
        if browser:
            try:
                context = browser.contexts[0]
                page = context.pages[0]
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = SCREENSHOT_DIR / f"failure_{item.name}_{timestamp}.png"
                page.screenshot(path=str(screenshot_path))
                # 附加到 Allure 报告
                allure.attach.file(
                    str(screenshot_path),
                    name=f"失败截图_{item.name}",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception:
                pass  # 截图失败不阻塞测试


@pytest.fixture(scope="session")
def browser_type():
    """返回使用的浏览器类型标识"""
    return "chromium"


@pytest.fixture(scope="session")
def playwright_context():
    """创建 Playwright 上下文（通过 browserless 连接）"""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as pw:
        try:
            browser = pw.chromium.connect_over_cdp(BROWSERLESS_WS)
        except Exception as e:
            # 如果 browserless 不可用，回退到本地浏览器
            browser = pw.chromium.launch(
                headless=os.environ.get("PLAYWRIGHT_HEADLESS", "true").lower() == "true",
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                ],
            )
        context = browser.new_context(
            viewport=VIEWPORT_DESKTOP,
            locale="zh-CN",
            timezone_id="Asia/Shanghai",
            ignore_https_errors=True,
        )
        page = context.new_page()
        page.set_default_timeout(DEFAULT_TIMEOUT)
        yield page
        page.close()
        context.close()
        browser.close()


@pytest.fixture(scope="session")
def playwright_context_tablet():
    """创建平板尺寸的 Playwright 上下文"""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as pw:
        try:
            browser = pw.chromium.connect_over_cdp(BROWSERLESS_WS)
        except Exception:
            browser = pw.chromium.launch(
                headless=os.environ.get("PLAYWRIGHT_HEADLESS", "true").lower() == "true",
                args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"],
            )
        context = browser.new_context(
            viewport=VIEWPORT_TABLET,
            locale="zh-CN",
            timezone_id="Asia/Shanghai",
        )
        page = context.new_page()
        page.set_default_timeout(DEFAULT_TIMEOUT)
        yield page
        page.close()
        context.close()
        browser.close()


@pytest.fixture(scope="session")
def playwright_context_mobile():
    """创建移动端尺寸的 Playwright 上下文"""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as pw:
        try:
            browser = pw.chromium.connect_over_cdp(BROWSERLESS_WS)
        except Exception:
            browser = pw.chromium.launch(
                headless=os.environ.get("PLAYWRIGHT_HEADLESS", "true").lower() == "true",
                args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"],
            )
        context = browser.new_context(
            viewport=VIEWPORT_MOBILE,
            locale="zh-CN",
            timezone_id="Asia/Shanghai",
            is_mobile=True,
            user_agent=(
                "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 "
                "Mobile/15E148 Safari/604.1"
            ),
        )
        page = context.new_page()
        page.set_default_timeout(DEFAULT_TIMEOUT)
        yield page
        page.close()
        context.close()
        browser.close()


@pytest.fixture
def page(playwright_context):
    """提供 main page 实例（桌面端）"""
    return playwright_context


@pytest.fixture
def page_tablet(playwright_context_tablet):
    """提供平板尺寸 page 实例"""
    return playwright_context_tablet


@pytest.fixture
def page_mobile(playwright_context_mobile):
    """提供移动端尺寸 page 实例"""
    return playwright_context_mobile


@pytest.fixture
def base_url():
    """测试基础 URL"""
    return BASE_URL


@pytest.fixture
def screenshot_dir():
    """截图保存目录"""
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    return SCREENSHOT_DIR


@pytest.fixture
def take_screenshot(page, screenshot_dir, request):
    """截图辅助函数"""
    def _screenshot(name: str = None):
        filename = name or f"{request.node.name}_{datetime.now().strftime('%H%M%S')}"
        path = screenshot_dir / f"{filename}.png"
        page.screenshot(path=str(path))
        allure.attach.file(
            str(path),
            name=filename,
            attachment_type=allure.attachment_type.PNG,
        )
        return path
    return _screenshot


@pytest.fixture
def navigate_to(page, base_url):
    """导航到指定路径的辅助函数"""
    def _navigate(path: str = "/", wait_until: str = "networkidle"):
        url = f"{base_url}{path}"
        page.goto(url, wait_until=wait_until)
        return page
    return _navigate


# ── 辅助函数 ──────────────────────────────────────────────────────────────────


def get_element_text(page, selector: str) -> str:
    """获取元素文本内容"""
    element = page.wait_for_selector(selector, timeout=DEFAULT_TIMEOUT)
    return element.text_content() or ""


def assert_element_visible(page, selector: str, msg: str = ""):
    """断言元素可见"""
    element = page.wait_for_selector(selector, state="visible", timeout=DEFAULT_TIMEOUT)
    assert element is not None, f"元素未可见: {selector}. {msg}"
    assert element.is_visible(), f"元素不可见: {selector}. {msg}"


def assert_element_contains_text(page, selector: str, expected_text: str):
    """断言元素包含指定文本"""
    element = page.wait_for_selector(selector, state="visible", timeout=DEFAULT_TIMEOUT)
    text = element.text_content() or ""
    assert expected_text in text, (
        f"元素 [{selector}] 不包含预期文本.\n"
        f"预期包含: {expected_text}\n"
        f"实际内容: {text}"
    )


def fill_input(page, selector: str, value: str):
    """填充输入框（先清空再输入）"""
    element = page.wait_for_selector(selector, state="visible", timeout=DEFAULT_TIMEOUT)
    element.fill("")
    element.fill(value)


def click_element(page, selector: str):
    """点击元素"""
    element = page.wait_for_selector(selector, state="visible", timeout=DEFAULT_TIMEOUT)
    element.click()


def wait_for_navigation(page, timeout: int = DEFAULT_TIMEOUT):
    """等待页面导航完成"""
    page.wait_for_load_state("networkidle", timeout=timeout)


def wait_for_selector(page, selector: str, state: str = "visible", timeout: int = DEFAULT_TIMEOUT):
    """等待元素出现"""
    return page.wait_for_selector(selector, state=state, timeout=timeout)