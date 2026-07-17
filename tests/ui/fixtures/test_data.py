"""
倍斯特 UI 测试 - 测试夹具和数据
提供测试所需的页面 URL、表单数据、表格数据等
"""

from typing import Dict, List, Any

# ============ 页面路由 ============

PAGE_ROUTES: Dict[str, str] = {
    "首页": "/",
    "状态": "/api/status",
    "健康检查": "/health",
}

# ============ 导航菜单 ============

NAVIGATION_MENUS: List[str] = [
    "首页",
    "Dashboard",
    "概览",
]

SIDEBAR_MENUS: List[str] = [
    "业务数据",
    "Business",
    "首页",
    "Dashboard",
]

# ============ 表单测试数据 ============

FORM_DATA_VALID: Dict[str, str] = {
    "username": "test_user_arkclaw",
    "email": "test@beste-arkclaw.com",
    "phone": "13800138000",
}

FORM_DATA_EMPTY: Dict[str, str] = {
    "username": "",
    "email": "",
}

FORM_DATA_INVALID: Dict[str, str] = {
    "email": "not-an-email",
    "phone": "abc",
}

# ============ 表格列名 ============

EXPECTED_TABLE_COLUMNS: List[str] = [
    "ID",
    "名称",
    "状态",
    "创建时间",
]

# ============ 搜索关键词 ============

SEARCH_KEYWORDS: Dict[str, Any] = {
    "valid": "test",
    "no_result": "zzzzz_nonexistent_xxxxx",
    "partial": "ark",
}

# ============ 可访问性配置 ============

ACCESSIBILITY_CONFIG: Dict[str, Any] = {
    "required_aria_roles": [
        "navigation",
        "main",
        "banner",
        "button",
        "link",
    ],
    "required_labels": [
        "导航",
        "主要",
    ],
}