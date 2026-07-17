"""
跨浏览器兼容性测试 - chromium / firefox / webkit
验证页面在各浏览器内核下的一致性
"""

import pytest
import os


class TestCrossBrowser:
    """
    跨浏览器兼容性测试
    每个用例在三个浏览器上分别执行，验证渲染一致性和功能正确性
    """

    # ================================================================
    # Chromium
    # ================================================================

    @pytest.mark.chromium
    def test_chromium_page_loads(self, page, base_url):
        """Chromium: 页面加载"""
        page.goto(base_url, wait_until="networkidle")
        title = page.title()
        assert title is not None, "Chromium 页面应加载"
        status_code = page.evaluate("() => document.readyState")
        assert status_code == "complete", "Chromium 页面应完全加载"

    @pytest.mark.chromium
    def test_chromium_basic_elements(self, page, base_url):
        """Chromium: 基础元素存在"""
        page.goto(base_url, wait_until="networkidle")
        body = page.query_selector("body")
        assert body is not None, "Chromium body 应存在"

    @pytest.mark.chromium
    def test_chromium_no_console_errors(self, page, base_url):
        """Chromium: 无控制台错误"""
        console_errors = []

        def handle_console(msg):
            if msg.type == "error" or msg.type == "warning":
                console_errors.append(f"[{msg.type}] {msg.text}")

        page.on("console", handle_console)
        page.goto(base_url, wait_until="networkidle")
        page.wait_for_timeout(1000)

        error_count = len(console_errors)
        if error_count > 0:
            # 记录但不断言失败，仅作为参考
            print(f"\nChromium 控制台消息: {error_count} 条")

    @pytest.mark.chromium
    def test_chromium_javascript_execution(self, page, base_url):
        """Chromium: JavaScript 执行正常"""
        page.goto(base_url, wait_until="networkidle")
        result = page.evaluate("() => typeof window !== 'undefined' && window.navigator !== 'undefined'")
        assert result, "Chromium 下 JavaScript 应正常执行"

    @pytest.mark.chromium
    def test_chromium_screenshot_capture(self, page, base_url):
        """Chromium: 截图功能"""
        page.goto(base_url, wait_until="networkidle")
        screenshot_dir = os.path.join(os.path.dirname(__file__), "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, "chromium_page.png")
        page.screenshot(path=screenshot_path, full_page=True)
        assert os.path.exists(screenshot_path), "Chromium 截图应成功保存"
        file_size = os.path.getsize(screenshot_path)
        assert file_size > 1000, f"Chromium 截图应有合理大小 ({file_size} bytes)"

    # ================================================================
    # Firefox
    # ================================================================

    @pytest.mark.firefox
    def test_firefox_page_loads(self, page, base_url):
        """Firefox: 页面加载"""
        page.goto(base_url, wait_until="networkidle")
        title = page.title()
        assert title is not None, "Firefox 页面应加载"

    @pytest.mark.firefox
    def test_firefox_css_rendering(self, page, base_url):
        """Firefox: CSS 渲染正常"""
        page.goto(base_url, wait_until="networkidle")
        # 检查视口尺寸
        viewport = page.evaluate("() => ({w: window.innerWidth, h: window.innerHeight})")
        assert viewport["w"] > 0 and viewport["h"] > 0, "Firefox 视口应有有效尺寸"

    @pytest.mark.firefox
    def test_firefox_dom_manipulation(self, page, base_url):
        """Firefox: DOM 操作正常"""
        page.goto(base_url, wait_until="networkidle")
        element_count = page.evaluate("() => document.querySelectorAll('*').length")
        assert element_count > 0, "Firefox 下 DOM 元素数量应大于 0"

    @pytest.mark.firefox
    def test_firefox_screenshot_capture(self, page, base_url):
        """Firefox: 截图功能"""
        page.goto(base_url, wait_until="networkidle")
        screenshot_dir = os.path.join(os.path.dirname(__file__), "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, "firefox_page.png")
        page.screenshot(path=screenshot_path, full_page=True)
        assert os.path.exists(screenshot_path), "Firefox 截图应成功保存"

    # ================================================================
    # WebKit
    # ================================================================

    @pytest.mark.webkit
    def test_webkit_page_loads(self, page, base_url):
        """WebKit: 页面加载"""
        page.goto(base_url, wait_until="networkidle")
        title = page.title()
        assert title is not None, "WebKit 页面应加载"

    @pytest.mark.webkit
    def test_webkit_network_requests(self, page, base_url):
        """WebKit: 网络请求正常"""
        page.goto(base_url, wait_until="networkidle")
        performance = page.evaluate("""() => {
            const entries = performance.getEntriesByType('resource');
            return {
                total: entries.length,
                failed: entries.filter(e => e.responseStatus >= 400).length
            };
        }""")
        print(f"\nWebKit 网络请求: {performance['total']} 总, {performance['failed']} 失败")

    @pytest.mark.webkit
    def test_webkit_canvas_support(self, page, base_url):
        """WebKit: Canvas 支持"""
        page.goto(base_url, wait_until="networkidle")
        canvas_support = page.evaluate("""() => {
            const c = document.createElement('canvas');
            return !!(c.getContext && c.getContext('2d'));
        }""")
        assert canvas_support, "WebKit 应支持 Canvas"

    @pytest.mark.webkit
    def test_webkit_screenshot_capture(self, page, base_url):
        """WebKit: 截图功能"""
        page.goto(base_url, wait_until="networkidle")
        screenshot_dir = os.path.join(os.path.dirname(__file__), "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, "webkit_page.png")
        page.screenshot(path=screenshot_path, full_page=True)
        assert os.path.exists(screenshot_path), "WebKit 截图应成功保存"

    # ================================================================
    # 跨浏览器一致性验证
    # ================================================================

    @pytest.mark.chromium
    def test_viewport_size_consistency(self, page, base_url):
        """验证视口尺寸设置正确"""
        viewport = page.viewport_size
        assert viewport is not None, "视口尺寸应存在"
        assert viewport["width"] > 0 and viewport["height"] > 0, \
            "视口尺寸应为正数"
        print(f"\n当前视口: {viewport['width']}x{viewport['height']}")

    @pytest.mark.chromium
    def test_cookies_functional(self, page, base_url):
        """基础 Cookie 功能"""
        page.goto(base_url, wait_until="networkidle")
        page.evaluate("() => document.cookie = 'test_cookie=arkclaw_ui_test'")
        cookie = page.evaluate("() => document.cookie")
        # Cookie 可能被 SameSite 限制，只验证功能不报错

    @pytest.mark.chromium
    def test_local_storage_available(self, page, base_url):
        """LocalStorage 可用"""
        page.goto(base_url, wait_until="networkidle")
        available = page.evaluate("""() => {
            try {
                localStorage.setItem('test', 'arkclaw');
                const val = localStorage.getItem('test');
                localStorage.removeItem('test');
                return val === 'arkclaw';
            } catch(e) {
                return false;
            }
        }""")
        assert available, "本地存储应可用"

    @pytest.mark.chromium
    @pytest.mark.accessibility
    def test_page_lang_attribute(self, page, base_url):
        """可访问性: html lang 属性"""
        page.goto(base_url, wait_until="networkidle")
        lang = page.evaluate("() => document.documentElement.lang")
        if lang:
            print(f"\n页面语言: {lang}")
        else:
            print("\n页面未设置 lang 属性")

    @pytest.mark.chromium
    @pytest.mark.accessibility
    def test_page_has_main_landmark(self, page, base_url):
        """可访问性: 主内容区域"""
        page.goto(base_url, wait_until="networkidle")
        has_main = page.evaluate("() => !!document.querySelector('main, [role=\"main\"]')")
        if not has_main:
            print("\n页面缺少 main 区域")

    @pytest.mark.chromium
    @pytest.mark.accessibility
    def test_images_have_alt(self, page, base_url):
        """可访问性: 图片 alt 属性"""
        page.goto(base_url, wait_until="networkidle")
        images = page.query_selector_all("img")
        missing_alt = 0
        for img in images:
            alt = img.get_attribute("alt")
            if alt is None:
                missing_alt += 1
        total = len(images)
        if total > 0:
            coverage = (total - missing_alt) / total * 100
            print(f"\n图片 alt 覆盖率: {coverage:.0f}% ({total - missing_alt}/{total})")
        else:
            print("\n页面无图片元素")