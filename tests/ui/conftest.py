"""
倍斯特前端 UI 组件测试框架 - Playwright 浏览器配置
支持 chromium / firefox / webkit 多浏览器并行测试

使用方式:
  pytest tests/ui/ --browser chromium          # 仅 Chromium
  pytest tests/ui/ --browser firefox            # 仅 Firefox
  pytest tests/ui/ --browser webkit             # 仅 WebKit
  pytest tests/ui/ --browser chromium --browser firefox  # 多浏览器并行
"""

import os
import pytest
from datetime import datetime
from typing import Dict, Any

# ============ 全局常量 ============

BASE_URL = os.environ.get("UI_TEST_BASE_URL", "http://localhost:80")
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
DEFAULT_TIMEOUT = int(os.environ.get("UI_TEST_TIMEOUT", "30000"))
VIEWPORT_DESKTOP = {"width": 1920, "height": 1080}
VIEWPORT_TABLET = {"width": 768, "height": 1024}
VIEWPORT_MOBILE = {"width": 375, "height": 667}

# ============ CLI 参数 ============


def pytest_addoption(parser):
    """添加 UI 测试 CLI 参数"""
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="以有头模式运行浏览器（默认无头）",
    )
    parser.addoption(
        "--slowmo",
        type=int,
        default=0,
        help="操作间延迟（毫秒），用于调试",
    )
    parser.addoption(
        "--screenshot",
        action="store_true",
        default=False,
        help="测试失败时自动截图",
    )
    parser.addoption(
        "--viewport",
        type=str,
        default="desktop",
        choices=["desktop", "tablet", "mobile"],
        help="视口尺寸预设",
    )


# ============ 浏览器启动配置 ============


def pytest_configure(config):
    """pytest 配置初始化"""
    config.addinivalue_line(
        "markers",
        "chromium: 仅在 chromium 浏览器中运行的测试",
    )
    config.addinivalue_line(
        "markers",
        "firefox: 仅在 firefox 浏览器中运行的测试",
    )
    config.addinivalue_line(
        "markers",
        "webkit: 仅在 webkit 浏览器中运行的测试",
    )
    config.addinivalue_line(
        "markers",
        "accessibility: 可访问性测试标记",
    )

    # 确保截图目录存在
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)


# ============ 浏览器 Fixture ============


@pytest.fixture(scope="session")
def browser_context_args(request):
    """浏览器上下文参数"""
    viewport_name = request.config.getoption("--viewport")
    viewports = {
        "desktop": VIEWPORT_DESKTOP,
        "tablet": VIEWPORT_TABLET,
        "mobile": VIEWPORT_MOBILE,
    }
    return {
        "viewport": viewports.get(viewport_name, VIEWPORT_DESKTOP),
        "ignore_https_errors": True,
        "locale": "zh-CN",
        "timezone_id": "Asia/Shanghai",
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(request):
    """浏览器启动参数"""
    headed = request.config.getoption("--headed")
    slowmo = request.config.getoption("--slowmo")
    return {
        "headless": not headed,
        "slow_mo": slowmo,
    }


# ============ 页面对象 Fixture ============


@pytest.fixture
def base_url() -> str:
    """基础 URL"""
    return BASE_URL


@pytest.fixture
def api_base_url(base_url: str) -> str:
    """API 基础 URL"""
    return f"{base_url}/api"


@pytest.fixture
def navigation_page(page) -> "NavigationPage":
    """导航页面对象"""
    from tests.ui.pages.navigation import NavigationPage
    return NavigationPage(page)


@pytest.fixture
def data_table_page(page) -> "DataTablePage":
    """数据表格页面对象"""
    from tests.ui.pages.data_table import DataTablePage
    return DataTablePage(page)


@pytest.fixture
def form_page(page) -> "FormInteractionPage":
    """表单交互页面对象"""
    from tests.ui.pages.form_interaction import FormInteractionPage
    return FormInteractionPage(page)


# ============ 失败截图 Hook ============


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """获取测试报告信息，用于截图判断"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def _take_failure_screenshot(request, page, browser_name: str = ""):
    """测试失败时自动截图"""
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = request.node.name
        browser_tag = f"_{browser_name}" if browser_name else ""
        filename = f"{test_name}{browser_tag}_{timestamp}.png"
        screenshot_path = os.path.join(SCREENSHOT_DIR, filename)
        try:
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"\n[截图已保存] {screenshot_path}")
        except Exception as e:
            print(f"\n[截图失败] {e}")


@pytest.fixture(autouse=True)
def _auto_screenshot_on_failure(request):
    """自动在测试失败时截图（通过 page fixture）"""
    yield
    # 截图由各个 page fixture 的 teardown 处理


# 覆盖 pytest-playwright 的 page fixture 以添加截图能力
@pytest.fixture
def page(page, request):
    """
    增强的 page fixture，自动添加失败截图功能。
    标记 @pytest.mark.chromium / firefox / webkit 用于跨浏览器并行。
    """
    yield page
    # 获取当前使用的浏览器类型
    browser_type = ""
    for marker_name in ("chromium", "firefox", "webkit"):
        if request.node.get_closest_marker(marker_name):
            browser_type = marker_name
            break
    _take_failure_screenshot(request, page, browser_type)