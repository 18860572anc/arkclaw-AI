"""
数据表格页面对象模型
封装数据表格的交互操作（分页、排序、搜索、空状态）
"""

from typing import List, Dict, Any, Optional


class DataTablePage:
    """数据表格页面对象"""

    # 表格选择器
    TABLE = (
        "table, .table, .data-table, "
        "[role='table'], .ag-grid, table.table"
    )
    TABLE_HEADER = "thead th, thead td, [role='columnheader']"
    TABLE_ROW = "tbody tr, [role='row']"
    TABLE_CELL = "tbody td, [role='gridcell']"
    TABLE_BODY = "tbody, [role='rowgroup']"

    # 分页
    PAGINATION = (
        ".pagination, nav[aria-label*='pagination'], "
        ".pager, .dataTables_paginate"
    )
    PAGE_BTN = (
        ".pagination a, .pagination button, "
        ".page-item, [aria-label*='page'], "
        "[role='navigation'] button"
    )
    PAGE_NEXT = (
        ".pagination .next, .pagination [aria-label='Next'], "
        ".pagination [aria-label='下一页'], "
        "a.next, button.next, "
        "[aria-label*='next' i]"
    )
    PAGE_PREV = (
        ".pagination .prev, .pagination [aria-label='Previous'], "
        ".pagination [aria-label='上一页'], "
        "a.prev, button.prev, "
        "[aria-label*='previous' i], [aria-label*='prev' i]"
    )
    PAGE_INFO = (
        ".page-info, .dataTables_info, "
        "[aria-live='polite'], .pagination-info"
    )

    # 排序
    SORTABLE_HEADER = (
        "th[aria-sort], th.sortable, th.sort-header, "
        "[aria-sort], .sortable, .sort-header"
    )
    SORT_ASC = "th[aria-sort='ascending'], [aria-sort='ascending']"
    SORT_DESC = "th[aria-sort='descending'], [aria-sort='descending']"

    # 搜索
    SEARCH_INPUT = (
        "input[type='search'], input.search, .search-input, "
        "input[aria-label*='search'], input[aria-label*='Search'], "
        "input[placeholder*='search' i], input[placeholder*='搜索' i], "
        "#search, #table-search"
    )
    SEARCH_BTN = (
        "button[aria-label*='search'], button.search-btn, "
        ".search-button, button[type='submit']"
    )

    # 空状态
    EMPTY_STATE = (
        ".empty-state, .no-data, .empty, "
        "[aria-label*='empty'], .no-records, "
        "td.empty, tr.empty, "
        "text:has-text('暂无数据'), "
        "text:has-text('no data'), "
        "text:has-text('No data')"
    )
    EMPTY_ICON = ".empty-state img, .empty-state .icon, .no-data img"
    EMPTY_TEXT = ".empty-state p, .empty-state h3, .no-data p, .no-data h3"

    # 加载状态
    LOADING = (
        ".loading, .spinner, .table-loading, "
        "[aria-busy='true'], .data-loading"
    )

    def __init__(self, page):
        self.page = page

    # ======== 表格存在性 ========

    def is_table_present(self) -> bool:
        """表格是否存在"""
        return self.page.locator(self.TABLE).first.is_visible()

    def get_column_count(self) -> int:
        """获取表格列数"""
        headers = self.page.query_selector_all(self.TABLE_HEADER)
        return len(headers)

    def get_row_count(self) -> int:
        """获取当前行数（不含表头）"""
        rows = self.page.query_selector_all(self.TABLE_ROW)
        return len(rows)

    def get_table_headers(self) -> List[str]:
        """获取表头文本列表"""
        headers = self.page.query_selector_all(self.TABLE_HEADER)
        return [h.inner_text().strip() for h in headers if h.inner_text().strip()]

    def get_cell_text(self, row: int, col: int) -> str:
        """获取指定单元格文本（0-indexed）"""
        rows = self.page.query_selector_all(self.TABLE_ROW)
        if row < len(rows):
            cells = rows[row].query_selector_all(self.TABLE_CELL)
            if col < len(cells):
                return cells[col].inner_text().strip()
        return ""

    def get_all_row_data(self) -> List[List[str]]:
        """获取所有行数据"""
        rows = self.page.query_selector_all(self.TABLE_ROW)
        data = []
        for row in rows:
            cells = row.query_selector_all(self.TABLE_CELL)
            data.append([c.inner_text().strip() for c in cells])
        return data

    def get_first_row_data(self) -> List[str]:
        """获取第一行数据"""
        rows = self.page.query_selector_all(self.TABLE_ROW)
        if rows:
            cells = rows[0].query_selector_all(self.TABLE_CELL)
            return [c.inner_text().strip() for c in cells]
        return []

    # ======== 分页操作 ========

    def is_pagination_visible(self) -> bool:
        """分页控件是否可见"""
        return self.page.locator(self.PAGINATION).first.is_visible()

    def click_next_page(self):
        """点击下一页"""
        next_btn = self.page.locator(self.PAGE_NEXT).first
        if next_btn.is_visible() and not next_btn.is_disabled():
            next_btn.click()
            self.page.wait_for_load_state("networkidle")

    def click_prev_page(self):
        """点击上一页"""
        prev_btn = self.page.locator(self.PAGE_PREV).first
        if prev_btn.is_visible() and not prev_btn.is_disabled():
            prev_btn.click()
            self.page.wait_for_load_state("networkidle")

    def click_page_number(self, page_num: int):
        """点击指定页码"""
        btn = self.page.locator(self.PAGE_BTN).filter(has_text=str(page_num)).first
        if btn.is_visible():
            btn.click()
            self.page.wait_for_load_state("networkidle")

    def get_page_numbers(self) -> List[int]:
        """获取所有可见页码"""
        btns = self.page.query_selector_all(self.PAGE_BTN)
        numbers = []
        for btn in btns:
            text = btn.inner_text().strip()
            try:
                numbers.append(int(text))
            except ValueError:
                continue
        return sorted(set(numbers))

    def get_page_info_text(self) -> str:
        """获取分页信息文本"""
        info = self.page.locator(self.PAGE_INFO).first
        return info.inner_text().strip() if info.is_visible() else ""

    # ======== 排序操作 ========

    def get_sortable_columns(self) -> List[str]:
        """获取可排序的列"""
        headers = self.page.query_selector_all(self.SORTABLE_HEADER)
        return [h.inner_text().strip() for h in headers]

    def click_column_header(self, col_name: str):
        """点击列头进行排序"""
        header = (
            self.page.locator(self.TABLE_HEADER)
            .filter(has_text=col_name)
            .first
        )
        if header.is_visible():
            header.click()
            self.page.wait_for_load_state("networkidle")

    def is_sorted_ascending(self) -> bool:
        """当前是否升序"""
        return self.page.locator(self.SORT_ASC).first.is_visible()

    def is_sorted_descending(self) -> bool:
        """当前是否降序"""
        return self.page.locator(self.SORT_DESC).first.is_visible()

    # ======== 搜索操作 ========

    def is_search_visible(self) -> bool:
        """搜索框是否可见"""
        return self.page.locator(self.SEARCH_INPUT).first.is_visible()

    def search(self, query: str):
        """输入搜索关键词"""
        input_el = self.page.locator(self.SEARCH_INPUT).first
        if input_el.is_visible():
            input_el.fill(query)
            input_el.press("Enter")
            self.page.wait_for_load_state("networkidle")

    def clear_search(self):
        """清空搜索框"""
        input_el = self.page.locator(self.SEARCH_INPUT).first
        if input_el.is_visible():
            input_el.clear()
            input_el.press("Enter")
            self.page.wait_for_load_state("networkidle")

    # ======== 空状态 ========

    def is_empty_state(self) -> bool:
        """是否处于空状态"""
        return self.page.locator(self.EMPTY_STATE).first.is_visible()

    def get_empty_state_text(self) -> str:
        """获取空状态提示文本"""
        return self.page.locator(self.EMPTY_TEXT).first.inner_text().strip()

    def has_empty_icon(self) -> bool:
        """空状态是否有图标"""
        return self.page.locator(self.EMPTY_ICON).first.is_visible()

    # ======== 加载状态 ========

    def is_loading(self) -> bool:
        """是否正在加载"""
        return self.page.locator(self.LOADING).first.is_visible()

    def wait_for_table_ready(self, timeout: int = 10000):
        """等待表格加载完成"""
        self.page.wait_for_selector(self.TABLE, timeout=timeout)
        self.page.wait_for_load_state("networkidle")

    # ======== 可访问性 ========

    def get_table_role(self) -> str:
        """获取表格 ARIA role"""
        return self.page.locator(self.TABLE).first.get_attribute("role") or ""

    def has_aria_label(self) -> bool:
        """表格是否有 ARIA label"""
        table = self.page.locator(self.TABLE).first
        label = table.get_attribute("aria-label")
        labelledby = table.get_attribute("aria-labelledby")
        return bool(label or labelledby)