"""倍斯特接口测试框架 - 共享fixtures和配置"""
import os
import json
import pytest
import requests

# Mock API 基础地址（默认 localhost:3001，可通过环境变量覆盖）
API_BASE = os.environ.get("MOCK_API_BASE", "http://localhost:3001")

# 测试超时时间（秒）
TIMEOUT = 10

# 响应时间断言阈值（毫秒）
RESPONSE_TIME_THRESHOLD_MS = 1000

# Schema 目录
SCHEMA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "schemas")


def load_schema(name):
    """加载指定名称的JSON Schema文件"""
    path = os.path.join(SCHEMA_DIR, name)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def assert_response_time(response, threshold_ms=RESPONSE_TIME_THRESHOLD_MS):
    """断言响应时间不超过阈值"""
    elapsed_ms = response.elapsed.total_seconds() * 1000
    assert elapsed_ms < threshold_ms, (
        f"响应时间超限: {elapsed_ms:.0f}ms > {threshold_ms}ms"
    )


def extract_data(response):
    """从API响应信封 {code, message, data, timestamp} 中提取data字段"""
    raw = response.json()
    if "data" in raw:
        return raw["data"]
    return raw


def assert_json_schema(instance, schema_name):
    """使用指定Schema校验JSON响应"""
    import jsonschema
    schema = load_schema(schema_name)
    if schema is None:
        pytest.skip(f"Schema文件不存在: {schema_name}")
    jsonschema.validate(instance, schema)


@pytest.fixture(scope="session")
def api_base():
    return API_BASE


@pytest.fixture(scope="session")
def session():
    """复用连接池的requests Session"""
    s = requests.Session()
    s.headers.update({"Accept": "application/json"})
    yield s
    s.close()


@pytest.fixture(scope="session")
def check_health(session):
    """检查Mock API服务是否就绪"""
    try:
        r = session.get(f"{API_BASE}/health", timeout=5)
        r.raise_for_status()
        return True
    except Exception:
        return False