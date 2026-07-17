"""
导航页面对象模型 (Page Object Model)
封装导航菜单的交互操作和断言
"""

from typing import List, Optional


class NavigationPage:
    """导航页面对象"""

    # 选择器
    SIDEBAR = "#sidebar, .sidebar, nav.sidebar, .nav-sidebar, aside"
    MENU_ITEM = (
        "#sidebar a, .sidebar a, .menu-item, "
        "nav.sidebar a, .nav-item, "
        "[role='menuitem'], [role='tab']"
    )
    SUBMENU = ".submenu, .sub-menu, .nav-children, [role='menu']"
    SUBMENU_ITEM = ".submenu a, .sub-menu a, .nav-children a, [role='menu'] [role='menuitem']"
    ACTIVE_MENU = (
        ".menu-item.active, .nav-item.active, "
        ".sidebar a.active, a.active, "
        "[aria-current='page']"
    )
    TOGGLE_BTN = (
        ".menu-toggle, .sidebar-toggle, "
        ".hamburger, .nav-toggle, "
        "[aria-label*='toggle'], [aria-label*='menu'], "
        "button.navbar-toggler"
    )
    PAGE_TITLE = "h1, h2, .page-title, .header-title"
    BREADCRUMB = ".breadcrumb, nav[aria-label='breadcrumb']"
    LOGO = ".logo, .navbar-brand, [aria-label='logo'] img, header img"

    # 预期的菜单项
    EXPECTED_MENU_ITEMS = [
        "首页", "Dashboard", "概览",
        "业务数据", "Business",
        "配置管理", "Settings",
        "帮助", "Help",
    ]

    def __init__(self, page):
        self.page = page

    def navigate_to(self, url: str):
        """导航到指定页面"""
        self.page.goto(url, wait_until="networkidle")
        self.page.wait_for_load_state("networkidle")

    def open_base_page(self):
        """打开根路径"""
        self.navigate_to("/")
        self.page.wait_for_load_state("networkidle")

    def get_menu_items(self) -> List[str]:
        """获取所有菜单项文本"""
        self.page.wait_for_selector(self.MENU_ITEM, timeout=5000)
        items = self.page.query_selector_all(self.MENU_ITEM)
        texts = []
        for item in items:
            text = item.inner_text().strip()
            if text:
                texts.append(text)
        return texts

    def click_menu(self, menu_name: str):
        """点击指定菜单项"""
        # 尝试精确匹配
        menu_link = self.page.locator(self.MENU_ITEM).filter(has_text=menu_name).first
        if menu_link.is_visible():
            menu_link.click()
            self.page.wait_for_load_state("networkidle")
            return

        # 尝试使用可见文本
        link = self.page.get_by_role("link", name=menu_name).first
        if link.is_visible():
            link.click()
            self.page.wait_for_load_state("networkidle")
            return

        # 兜底：寻找包含文本的元素
        element = self.page.locator(f"text={menu_name}").first
        if element.is_visible():
            element.click()
            self.page.wait_for_load_state("networkidle")

    def toggle_sidebar(self):
        """切换侧边栏展开/收起"""
        toggle = self.page.locator(self.TOGGLE_BTN).first
        if toggle.is_visible():
            toggle.click()
            self.page.wait_for_timeout(300)  # 等待动画

    def get_active_menu_text(self) -> str:
        """获取当前高亮菜单文本"""
        active = self.page.locator(self.ACTIVE_MENU).first
        if active.is_visible():
            return active.inner_text().strip()
        return ""

    def is_menu_visible(self, menu_name: str) -> bool:
        """检查菜单项是否可见"""
        item = self.page.locator(self.MENU_ITEM).filter(has_text=menu_name).first
        return item.is_visible()

    def is_sidebar_visible(self) -> bool:
        """侧边栏是否可见"""
        sidebar = self.page.locator(self.SIDEBAR).first
        return sidebar.is_visible()

    def get_page_title(self) -> str:
        """获取当前页面标题"""
        title = self.page.locator(self.PAGE_TITLE).first
        if title.is_visible():
            return title.inner_text().strip()
        return self.page.title()

    def get_current_url_path(self) -> str:
        """获取当前 URL 路径"""
        return self.page.url

    def has_breadcrumb(self) -> bool:
        """是否存在面包屑导航"""
        return self.page.locator(self.BREADCRUMB).first.is_visible()

    def is_logo_visible(self) -> bool:
        """Logo 是否可见"""
        return self.page.locator(self.LOGO).first.is_visible()

    def verify_menu_highlights(self, expected_menu: str) -> bool:
        """验证指定菜单是否高亮"""
        active_text = self.get_active_menu_text()
        return expected_menu.lower() in active_text.lower()

    def get_all_submenu_items(self) -> List[str]:
        """获取所有子菜单项"""
        items = self.page.query_selector_all(self.SUBMENU_ITEM)
        return [item.inner_text().strip() for item in items if item.inner_text().strip()]