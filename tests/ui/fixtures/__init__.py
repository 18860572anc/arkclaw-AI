"""
倍斯特 UI 测试 - 共享 Fixtures
提供页面级 fixture 供测试脚本复用
"""

import pytest
from typing import Dict, Any, Generator
from . import test_data


@pytest.fixture
def page_routes() -> Dict[str, str]:
    """页面路由映射"""
    return test_data.PAGE_ROUTES


@pytest.fixture
def valid_form_data() -> Dict[str, str]:
    """有效表单数据"""
    return dict(test_data.FORM_DATA_VALID)


@pytest.fixture
def invalid_form_data() -> Dict[str, str]:
    """无效表单数据"""
    return dict(test_data.FORM_DATA_INVALID)


@pytest.fixture
def empty_form_data() -> Dict[str, str]:
    """空表单数据"""
    return dict(test_data.FORM_DATA_EMPTY)


@pytest.fixture
def search_keywords() -> Dict[str, Any]:
    """搜索关键词"""
    return dict(test_data.SEARCH_KEYWORDS)


@pytest.fixture
def expected_table_columns() -> list:
    """预期的表格列名"""
    return list(test_data.EXPECTED_TABLE_COLUMNS)


@pytest.fixture
def mock_page_content() -> str:
    """
    模拟页面 HTML 内容，用于无浏览器时的结构化断言测试。
    实际测试时会被真实页面内容替换。
    """
    return (
        '<!DOCTYPE html><html><head><title>倍斯特业务数据平台</title></head>'
        '<body>'
        '<nav aria-label="主导航"><a href="/">首页</a><a href="/business">业务数据</a></nav>'
        '<main><h1>Dashboard</h1><table><thead><tr><th>ID</th><th>名称</th></tr></thead>'
        '<tbody><tr><td>1</td><td>测试</td></tr></tbody></table></main>'
        '</body></html>'
    )