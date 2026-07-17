# 倍斯特 × ArkClaw 测试数据框架

> 版本：v1.0.0 | 构建日期：2026-07-17

## 项目结构

```
beste-arkclaw/
├── api/                    # Mock API 服务
│   ├── Dockerfile          # Docker 构建文件
│   ├── mock_api_server.py  # FastAPI Mock API 服务
│   └── requirements.txt    # Python 依赖
├── data/                   # 测试数据
│   ├── source/             # 源数据（人工准备）
│   │   ├── company/        # 公司基础资料
│   │   ├── faq/            # FAQ文档
│   │   ├── templates/      # 模板文件
│   │   └── policies/       # 制度文档
│   ├── mock/               # 模拟数据（自动生成）
│   │   ├── business-data/  # 合成业务数据
│   │   ├── vector-data/    # LanceDB 向量数据
│   │   └── api-responses/  # Mock API 响应缓存
│   └── configs/            # 场景配置
├── tests/                  # 测试用例
│   ├── cases/              # 测试用例文件
│   │   ├── normal/         # 正常场景用例
│   │   ├── boundary/       # 边界场景用例
│   │   └── exception/      # 异常场景用例
│   └── schemas/            # JSON Schema 校验定义
├── scripts/                # 自动化脚本
│   ├── init_test_data.sh   # 一键初始化
│   ├── reset_test_data.sh  # 重置数据
│   ├── clean_test_data.sh  # 清理数据
│   ├── snapshot_lancedb.sh # 快照管理
│   ├── generate_source_data.py    # 源数据生成器
│   ├── generate_mock_data.py      # Mock数据生成器
│   └── generate_test_cases.py     # 测试用例生成器
├── nginx/                  # Nginx 反向代理配置
├── results/                # 测试结果输出
├── docker-compose.yml      # Docker 编排配置
├── data/VERSION            # 版本文件
└── README.md               # 本文件
```

## 快速开始

### 一键初始化

```bash
bash scripts/init_test_data.sh
```

### 手动步骤

```bash
# 1. 生成源数据
python3 scripts/generate_source_data.py

# 2. 生成Mock数据
python3 scripts/generate_mock_data.py

# 3. 生成测试用例
python3 scripts/generate_test_cases.py

# 4. 启动Mock API
docker compose up -d

# 5. 验证服务
curl http://localhost:3001/health
curl http://localhost:3001/api/status
```

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/heiyun/bom/{project_id}` | GET | 获取BOM物料清单 |
| `/api/heiyun/orders` | GET | 获取订单列表 |
| `/api/heiyun/orders/{order_id}` | GET | 获取订单详情 |
| `/api/heiyun/customers` | GET | 获取客户列表 |
| `/api/heiyun/customers/{customer_id}` | GET | 获取客户详情 |
| `/api/heiyun/inventory` | GET | 获取库存数据 |
| `/api/platform/{platform}/metrics` | GET | 获取平台流量 |
| `/api/competitors` | GET | 获取竞品列表 |
| `/api/market/prices` | GET | 获取元器件行情 |
| `/health` | GET | 健康检查 |
| `/api/status` | GET | 数据源状态 |

## 测试用例

共生成 3 类测试用例（正常/边界/异常），覆盖14个场景。

## 数据管理

```bash
# 重置数据（保留目录结构）
bash scripts/reset_test_data.sh

# 完全清理
bash scripts/clean_test_data.sh

# 快照管理
bash scripts/snapshot_lancedb.sh save    # 保存快照
bash scripts/snapshot_lancedb.sh list    # 列出快照
bash scripts/snapshot_lancedb.sh restore <name>  # 恢复快照
```