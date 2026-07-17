# 倍斯特测试框架 — 测试维度覆盖评估报告

> 评估时间：2026-07-17 13:52
> 项目路径：`/opt/beste-arkclaw/`
> 仓库：`git@github.com:18860572anc/arkclaw-AI.git`（main分支）

---

## 评估结论总览

| 评估维度 | 覆盖状态 | 优先级 |
|:---------|:--------:|:------:|
| ① UI层面测试 | ❌ **未覆盖** | 🔴 高 |
| ② 接口测试点 | ⚠️ **部分覆盖** | 🟡 中 |
| ③ WEB端口测试 | ⚠️ **部分覆盖** | 🟡 中 |
| ④ 性能测试 | ❌ **未覆盖** | 🟢 低 |

---

## 维度一：UI层面测试

### 覆盖状态：❌ 未覆盖

### 当前现状

当前框架**没有任何UI测试能力**。分析如下：

1. **测试用例内容**：现有的131条测试用例（正常68+边界50+异常13）全部是针对AI Agent场景的**功能/业务逻辑测试用例**，例如"小红书海报生成"、"订单进度查询"等，而非UI层面的元素定位、交互操作、页面渲染测试。

2. **测试用例格式**：测试用例以 JSON 文件形式存在（`tests/cases/normal/`、`tests/cases/boundary/`、`tests/cases/exception/`），定义了 `input` 和 `expected` 字段，属于**数据驱动测试用例定义**，而非可执行的 UI 自动化脚本。

3. **基础设施**：`docker-compose.yml` 中虽然定义了 `browser` 服务（browserless/chrome），但该服务是用于**AI Agent的浏览器自动化交互**（如访问网页获取信息），而非用于 UI 测试。

4. **无UI测试框架依赖**：`api/requirements.txt` 中只有 FastAPI 和 Uvicorn 依赖，没有任何 UI 测试框架（如 Selenium、Playwright、Cypress）。

### 补充方案

| 方案 | 推荐工具 | 实施难度 | 说明 |
|:----|:---------|:--------:|:-----|
| **方案A（推荐）** | **Playwright** | ⭐⭐ 中等 | 现代浏览器自动化，支持Python/JS/Java，速度最快，社区活跃，支持Chromium/Firefox/WebKit |
| **方案B** | **Selenium** | ⭐⭐⭐ 较易 | 最成熟，资料最多，但速度较慢，维护成本高 |
| **方案C** | **Cypress** | ⭐⭐⭐⭐ 较难 | 前端开发友好，但仅支持Chrome，需Node.js环境 |

**推荐方案A（Playwright）的具体实施步骤：**

```bash
# 1. 安装 Playwright
pip install playwright
playwright install chromium

# 2. 创建 UI 测试目录
mkdir -p tests/ui

# 3. 示例 UI 测试脚本 tests/ui/test_login.py
```

**示例测试用例：**

```python
# tests/ui/test_login.py
import pytest
from playwright.sync_api import Page, expect

def test_login_page_elements(page: Page):
    page.goto("http://localhost:80")
    expect(page.locator("h1")).to_contain_text("倍斯特")
    expect(page.locator("#username")).to_be_visible()
    expect(page.locator("#password")).to_be_visible()

def test_invalid_login(page: Page):
    page.goto("http://localhost:80/login")
    page.fill("#username", "admin")
    page.fill("#password", "wrong_password")
    page.click("#login-btn")
    expect(page.locator(".error-message")).to_be_visible()
```

**需要覆盖的UI测试场景建议：**
- 登录页面元素渲染与交互
- 导航菜单响应
- 数据表格展示与分页
- 表单提交与校验反馈
- 移动端适配（响应式布局）
- AI Agent 交互界面可用性

---

## 维度二：接口测试点

### 覆盖状态：⚠️ 部分覆盖

### 当前现状

#### ✅ 已覆盖部分

1. **Mock API 服务完整**：基于 FastAPI 构建，共 **68个API端点**，覆盖6大数据域：
   - 黑云系统接口（10+个）- 订单、客户、BOM、库存等
   - 倍用心系统接口（21个）- 订单与BOM(4) / 库存与物料(3) / 采购与供应商(4) / 生产与进度(3) / 财务与收款(4) / CRM与客户(3)
   - 其他业务接口（37+个）- OEM、海外、定价、供应商品质、HR、物流等

2. **测试用例类型完整**：131条用例分三类覆盖：
   - **正常用例**（68条）：标准输入预期输出
   - **边界用例**（50条）：空输入、超长输入、不存在的数据等
   - **异常用例**（13条）：服务超时、API不可用、生成失败等

3. **JSON Schema 校验**：`tests/schemas/` 下定义了多个数据校验 Schema（客户、CRM、财务、HR、库存等），支持响应数据格式校验。

4. **状态码覆盖**：Mock API 实现了多种响应码：
   - `200 OK` - 正常返回
   - `400 Bad Request` - 参数错误（如空订单号、数量为负）
   - `404 Not Found` - 资源不存在（如项目不存在、客户不存在）
   - `500 Internal Server Error` - 服务不可用

#### ❌ 未覆盖部分

1. **无自动化接口测试执行框架**：测试用例是 JSON 静态文件，**没有集成 pytest / unittest / Postman 等自动化测试执行器**。用例无法自动运行、自动断言。

2. **无 CI/CD 集成**：没有配置 GitHub Actions / Jenkins 等持续集成流水线，接口测试无法在每次提交时自动执行。

3. **无响应时间断言**：用例中未定义接口响应时间阈值（如 `response_time < 500ms`）。

4. **无安全性测试**：缺少 SQL 注入、XSS、权限越权等安全测试用例。

5. **无接口文档化**：虽然 FastAPI 会自动生成 Swagger 文档，但未集成到测试流程中，无 OpenAPI/Swagger 规范文件。

### 补充方案

| 需求 | 推荐方案 | 实施难度 | 说明 |
|:----|:---------|:--------:|:-----|
| **自动化测试执行** | **pytest + requests** | ⭐ 简单 | 将 JSON 用例转为可执行 pytest 脚本，自动断言状态码和响应体 |
| **接口测试框架** | **Postman + Newman** | ⭐ 简单 | 导出 Postman 集合，CI中用 Newman 命令行执行 |
| **Schema校验集成** | **pytest + jsonschema** | ⭐ 简单 | 用现有 JSON Schema 对 API 响应做自动校验 |
| **CI/CD流水线** | **GitHub Actions** | ⭐⭐ 中等 | 配置 push/PR 触发自动运行接口测试 |

**具体实施建议：**

```bash
# 1. 安装依赖
pip install pytest requests pytest-html

# 2. 创建自动化接口测试目录
mkdir -p tests/api

# 3. 示例接口测试脚本
```

```python
# tests/api/test_mock_heiyun.py
import pytest
import requests
import json
from jsonschema import validate

BASE_URL = "http://localhost:3001"

def test_health_check():
    resp = requests.get(f"{BASE_URL}/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_get_customers():
    resp = requests.get(f"{BASE_URL}/api/heiyun/customers")
    assert resp.status_code == 200
    data = resp.json()
    assert "customers" in data
    assert data["total"] > 0
    # 响应时间校验
    assert resp.elapsed.total_seconds() < 1.0

def test_get_customer_not_found():
    resp = requests.get(f"{BASE_URL}/api/heiyun/customers/NONEXIST")
    assert resp.status_code == 404
    assert resp.json()["detail"]["code"] == "CUSTOMER_NOT_FOUND"

def test_schema_validation():
    """使用现有的 JSON Schema 进行响应校验"""
    with open("tests/schemas/customer.schema.json") as f:
        schema = json.load(f)
    resp = requests.get(f"{BASE_URL}/api/heiyun/customers")
    validate(instance=resp.json(), schema=schema)

def test_boundary_qty_zero():
    """边界测试：数量为0"""
    resp = requests.get(f"{BASE_URL}/api/pricing/quote",
                        params={"product_id": "C200", "qty": 0, "customer_level": "B"})
    assert resp.status_code == 400

def test_response_time():
    """响应时间测试：批量请求验证性能基线"""
    import time
    times = []
    for _ in range(20):
        start = time.time()
        requests.get(f"{BASE_URL}/api/heiyun/orders")
        times.append(time.time() - start)
    avg_time = sum(times) / len(times)
    assert avg_time < 0.5, f"平均响应时间 {avg_time:.3f}s 超过阈值"
```

---

## 维度三：WEB端口测试

### 覆盖状态：⚠️ 部分覆盖

### 当前现状

#### ✅ 已覆盖部分

1. **Nginx 反向代理配置完整**：`nginx/default.conf` 已配置：
   - `/api/` 路由转发到 Mock API 服务（端口3001）
   - `/health` 健康检查端点
   - `/results/` 静态测试报告服务
   - 根路径重定向到 `/api/status`

2. **Docker 网络配置**：`docker-compose.yml` 定义了 `beste-network` 桥接网络，4个服务（mock-api、lancedb、browser、nginx）互联互通。

3. **Browser 服务可用**：`browserless/chrome` 服务（端口3000）已配置，可用于 AI Agent 的浏览器自动化操作。

#### ❌ 未覆盖部分

1. **无端到端（E2E）测试**：没有编写任何 E2E 测试用例，无法验证从 Nginx 入口 → API 网关 → 后端服务的完整请求链路。

2. **无 WEB 自动化测试脚本**：`browserless/chrome` 服务仅用于 AI Agent 的网页内容获取，未集成到 WEB 自动化测试流程中。

3. **无跨域/安全头测试**：未测试 CORS 配置、Content-Security-Policy、XSS 防护等 WEB 安全头。

4. **无页面加载性能测试**：未测试页面加载时间、资源加载顺序、首屏渲染时间等。

### 补充方案

| 需求 | 推荐方案 | 实施难度 | 说明 |
|:----|:---------|:--------:|:-----|
| **E2E测试** | **Playwright + pytest** | ⭐⭐ 中等 | 利用现有 browserless/chrome 服务，编写端到端测试 |
| **WEB安全测试** | **OWASP ZAP** | ⭐⭐⭐ 较难 | 自动化 WEB 安全扫描 |
| **页面性能测试** | **Lighthouse** | ⭐⭐ 中等 | 集成到 CI 流水线中 |

**具体实施建议：**

```python
# tests/e2e/test_full_flow.py
"""端到端测试：模拟完整业务流程"""
import pytest
import requests

BASE_URL = "http://localhost:80"  # 通过Nginx入口

def test_e2e_customer_to_order():
    """E2E：查询客户 → 查看订单 → 检查进度"""
    # 1. 查询客户列表
    resp = requests.get(f"{BASE_URL}/api/heiyun/customers")
    assert resp.status_code == 200
    customers = resp.json()["customers"]
    assert len(customers) > 0

    # 2. 查看客户详情
    customer_id = customers[0]["id"]
    resp = requests.get(f"{BASE_URL}/api/heiyun/customers/{customer_id}")
    assert resp.status_code == 200

    # 3. 查询订单列表
    resp = requests.get(f"{BASE_URL}/api/heiyun/orders")
    assert resp.status_code == 200
    orders = resp.json()["orders"]
    assert len(orders) > 0

    # 4. 查看订单详情
    order_id = orders[0]["id"]
    resp = requests.get(f"{BASE_URL}/api/heiyun/orders/{order_id}")
    assert resp.status_code == 200

    # 5. 查看订单进度
    resp = requests.get(f"{BASE_URL}/api/orders/{order_id}/progress")
    assert resp.status_code == 200
    assert "current_stage" in resp.json()

def test_e2e_nginx_health_check():
    """通过Nginx代理访问健康检查"""
    resp = requests.get(f"{BASE_URL}/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_e2e_nginx_api_routing():
    """验证Nginx API路由正确转发"""
    resp = requests.get(f"{BASE_URL}/api/status")
    assert resp.status_code == 200
    assert "heiyun" in resp.json()

def test_web_security_headers():
    """验证WEB安全头"""
    resp = requests.get(f"{BASE_URL}/api/status")
    # CORS 头检查
    assert "access-control-allow-origin" in resp.headers
    # 内容类型检查
    assert "application/json" in resp.headers.get("content-type", "")
```

**docker-compose 补充配置（用于E2E测试）：**

```yaml
# 在 docker-compose.yml 中增加 E2E 测试服务
services:
  # ... 现有服务 ...

  # E2E测试服务
  e2e-test:
    image: mcr.microsoft.com/playwright:v1.48.0
    container_name: beste-e2e
    working_dir: /tests
    volumes:
      - ./tests/e2e:/tests/e2e
      - ./tests/reports:/tests/reports
    command: ["sh", "-c", "pip install pytest && pytest e2e/ -v --html=reports/e2e-report.html"]
    networks:
      - beste-network
    depends_on:
      - nginx
      - mock-api
    profiles:
      - test  # 仅测试时启动
```

---

## 维度四：性能测试

### 覆盖状态：❌ 未覆盖

### 当前现状

当前框架**没有任何性能测试能力**：
- 无性能测试脚本或工具集成
- 无负载测试、压力测试、稳定性测试方案
- 无性能基准（baseline）数据
- 无性能指标监控（TPS、响应时间、错误率、资源使用率）
- `docker-compose.yml` 中未定义性能测试服务

### 补充方案

#### 推荐工具对比

| 工具 | 语言 | 适用场景 | 优点 | 实施难度 |
|:----|:----|:---------|:----|:--------:|
| **JMeter** | Java | 接口/协议级性能测试 | 最成熟，GUI配置，插件丰富，支持复杂场景 | ⭐⭐ 中等 |
| **k6** | JavaScript | 接口级负载测试 | 轻量，CLI友好，CI集成简单，代码即脚本 | ⭐ 简单 |
| **Locust** | Python | 接口级负载测试 | Python原生，分布式，代码即脚本 | ⭐ 简单 |
| **wrk** | C | HTTP基准测试 | 极高并发，适合简单场景 | ⭐⭐ 中等 |

**推荐方案：k6（轻量级，CI友好） + Locust（Python原生，与现有框架一致）**

#### 性能测试方案

```python
# tests/performance/locustfile.py - Locust 性能测试脚本
"""倍斯特 Mock API 性能测试脚本
运行方式：
    pip install locust
    locust -f tests/performance/locustfile.py --host=http://localhost:3001
"""
from locust import HttpUser, task, between

class APIPerformanceTest(HttpUser):
    wait_time = between(1, 3)  # 用户操作间隔

    @task(3)
    def get_customers(self):
        """客户列表接口 - 高频访问"""
        self.client.get("/api/heiyun/customers")

    @task(2)
    def get_orders(self):
        """订单列表接口 - 高频访问"""
        self.client.get("/api/heiyun/orders")

    @task(1)
    def get_inventory(self):
        """库存查询接口"""
        self.client.get("/api/heiyun/inventory")

    @task(1)
    def get_competitors(self):
        """竞品数据接口"""
        self.client.get("/api/competitors")

    @task(1)
    def get_bom(self):
        """BOM查询接口 - 周期性访问"""
        self.client.get("/api/heiyun/bom/P001")

    @task(1)
    def get_market_prices(self):
        """市场行情接口"""
        self.client.get("/api/market/prices")

    @task(1)
    def health_check(self):
        """健康检查"""
        self.client.get("/health")
```

```javascript
// tests/performance/k6-script.js - k6 性能测试脚本
/* 运行方式：
    k6 run tests/performance/k6-script.js
*/
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

const errorRate = new Rate('errors');

export const options = {
    stages: [
        { duration: '2m', target: 50 },   // 逐渐增加到50并发
        { duration: '5m', target: 50 },   // 保持50并发5分钟
        { duration: '2m', target: 100 },  // 增加到100并发
        { duration: '5m', target: 100 },  // 保持100并发
        { duration: '2m', target: 0 },    // 逐渐减少
    ],
    thresholds: {
        http_req_duration: ['p(95)<500'],   // 95%的请求应在500ms内
        errors: ['rate<0.05'],              // 错误率低于5%
    },
};

const BASE_URL = 'http://localhost:3001';

export default function () {
    // 随机选择接口
    const endpoints = [
        '/api/heiyun/customers',
        '/api/heiyun/orders',
        '/api/heiyun/inventory',
        '/api/competitors',
        '/api/market/prices',
        '/health',
    ];
    const url = `${BASE_URL}${endpoints[Math.floor(Math.random() * endpoints.length)]}`;

    const res = http.get(url);
    check(res, {
        'status is 200': (r) => r.status === 200,
        'response time < 500ms': (r) => r.timings.duration < 500,
    });
    errorRate.add(res.status !== 200);
    sleep(1);
}
```

#### 性能测试指标建议

| 指标 | 建议阈值 | 说明 |
|:----|:--------:|:-----|
| **并发用户数** | 50-100 | 模拟日常使用峰值 |
| **TPS（每秒事务数）** | ≥ 200 | 接口吞吐量基准 |
| **P95响应时间** | < 500ms | 95%的请求在500ms内 |
| **P99响应时间** | < 1000ms | 99%的请求在1秒内 |
| **错误率** | < 5% | 失败请求比例 |
| **CPU使用率** | < 70% | Mock API 服务 |
| **内存使用** | < 500MB | Mock API 服务 |

#### Docker Compose 集成（性能测试）

```yaml
# 在 docker-compose.yml 中增加性能测试服务
services:
  # ... 现有服务 ...

  # 性能测试服务
  k6-test:
    image: grafana/k6:latest
    container_name: beste-k6
    volumes:
      - ./tests/performance/k6-script.js:/scripts/k6-script.js
    command: run /scripts/k6-script.js
    networks:
      - beste-network
    profiles:
      - performance  # 仅性能测试时启动
```

---

## 综合评估与改进路线图

### 当前框架定位

倍斯特测试框架目前是一个**以数据生成和Mock API为核心的测试数据基础设施**，主要服务于 AI Agent 场景的功能验证。它**不是**一个完整的测试框架，而是一个**测试数据/环境支撑层**。

### 各维度成熟度评估

```
成熟度： 1★(起点) ~ 5★(成熟)
                     当前水平    目标水平
    UI测试能力         ☆☆☆☆☆    ★★★☆☆
    接口测试能力       ★★☆☆☆    ★★★★☆
    WEB端口测试能力    ★☆☆☆☆    ★★★☆☆
    性能测试能力       ☆☆☆☆☆    ★★★☆☆
    自动化程度         ★★☆☆☆    ★★★★☆
    CI/CD集成          ★☆☆☆☆    ★★★★☆
```

### 分阶段改进路线图

| 阶段 | 时间 | 目标 | 具体任务 |
|:----|:----|:-----|:---------|
| **Phase 1** | 1-2周 | 接口测试自动化 | ① pytest + requests 集成；② 将131条用例转为可执行脚本；③ 集成 JSON Schema 校验；④ 配置 GitHub Actions 流水线 |
| **Phase 2** | 2-3周 | WEB端口+E2E测试 | ① Playwright 集成；② 核心业务流程E2E测试；③ Nginx 路由验证；④ WEB安全头检查 |
| **Phase 3** | 2-3周 | 性能测试基础设施 | ① k6 或 Locust 集成；② 性能基准测试；③ 性能指标阈值定义；④ 性能回归测试流水线 |
| **Phase 4** | 3-4周 | UI自动化测试 | ① Playwright 核心UI测试；② 登录/导航/表单交互测试；③ 报告生成；④ 截图对比 |

### 基础设施依赖补充

```bash
# 测试框架依赖安装（完整）
pip install pytest pytest-html requests jsonschema  # 接口测试
pip install playwright && playwright install chromium  # UI/E2E测试
pip install locust  # 性能测试（或 k6 二进制安装）
```

---

## 详细变更清单（按文件）

| 文件路径 | 变更类型 | 说明 |
|:---------|:--------:|:-----|
| `tests/api/` | **新增目录** | 自动化接口测试脚本 |
| `tests/ui/` | **新增目录** | UI自动化测试脚本 |
| `tests/e2e/` | **新增目录** | 端到端测试脚本 |
| `tests/performance/` | **新增目录** | 性能测试脚本 |
| `tests/reports/` | **新增目录** | 测试报告输出 |
| `tests/api/test_mock_heiyun.py` | **新增文件** | 黑云系统接口测试 |
| `tests/api/test_mock_beiyongxin.py` | **新增文件** | 倍用心系统接口测试 |
| `tests/api/test_mock_business.py` | **新增文件** | 其他业务接口测试 |
| `tests/e2e/test_full_flow.py` | **新增文件** | E2E业务流程测试 |
| `tests/performance/locustfile.py` | **新增文件** | Locust性能测试 |
| `tests/performance/k6-script.js` | **新增文件** | k6性能测试 |
| `docker-compose.yml` | **修改** | 新增e2e-test/k6-test服务（profiles） |
| `requirements-test.txt` | **新增文件** | 测试依赖清单 |
| `.github/workflows/test.yml` | **新增文件** | GitHub Actions CI流水线 |
| `README.md` | **修改** | 补充测试指南章节 |

---

## 附录：当前框架上下文回顾

### 已有能力清单

| 能力 | 详情 |
|:----|:------|
| Mock API 端点 | 68个，覆盖6大数据域（黑云+倍用心+其他业务） |
| 测试用例 | 131条（正常68/边界50/异常13），覆盖52个场景 |
| 数据源 | 8个源数据文件，17个Mock数据文件 |
| JSON Schema | 15个数据校验Schema |
| 数据生成脚本 | 4个（source/mock/cases/all） |
| 运维脚本 | 4个（init/reset/clean/snapshot） |
| Docker 服务 | 4个（mock-api/lancedb/browser/nginx） |
| 网络配置 | Nginx反向代理，桥接网络 |

### 缺失能力清单

| 缺失能力 | 严重程度 | 推荐工具 |
|:---------|:--------:|:---------|
| 自动化接口测试执行 | 🔴 高 | pytest + requests |
| CI/CD持续集成 | 🔴 高 | GitHub Actions |
| E2E测试 | 🟡 中 | Playwright |
| WEB安全测试 | 🟡 中 | OWASP ZAP |
| UI自动化测试 | 🟡 中 | Playwright |
| 性能/负载测试 | 🟢 低 | k6 / Locust |
| 代码覆盖率报告 | 🟢 低 | pytest-cov |
| API文档化测试 | 🟢 低 | OpenAPI/Swagger |

---

*报告生成时间：2026-07-17 13:52 CST*
*评估版本：beste-arkclaw v1.0.0*