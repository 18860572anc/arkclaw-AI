#!/bin/bash
# ============================================
# 倍斯特测试数据框架 - 一键初始化脚本
# 用法: bash init_test_data.sh
# ============================================
set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
echo "=========================================="
echo "倍斯特测试数据框架 - 一键初始化"
echo "项目目录: $PROJECT_DIR"
echo "=========================================="

# 步骤1: 生成源数据
echo ""
echo "[1/6] 生成源数据..."
python3 "$PROJECT_DIR/scripts/generate_source_data.py"

# 步骤2: 生成Mock数据
echo ""
echo "[2/6] 生成Mock模拟数据..."
python3 "$PROJECT_DIR/scripts/generate_mock_data.py"

# 步骤3: 生成测试用例
echo ""
echo "[3/6] 生成测试用例..."
python3 "$PROJECT_DIR/scripts/generate_test_cases.py"

# 步骤4: 创建校验Schema（如无则复制）
echo ""
echo "[4/6] 校验数据Schema..."
for schema in "$PROJECT_DIR/tests/schemas/"*.schema.json; do
    if [ -f "$schema" ]; then
        echo "  ✅ Schema: $(basename $schema)"
    fi
done

# 步骤5: 启动Docker服务
echo ""
echo "[5/6] 启动Docker服务..."
cd "$PROJECT_DIR"
if command -v docker &> /dev/null; then
    docker compose up -d 2>/dev/null || docker-compose up -d 2>/dev/null || echo "  ⚠️ Docker Compose不可用，请手动启动"
    echo "  ✅ Docker服务已启动"
else
    echo "  ⚠️ Docker未安装，跳过Docker启动"
fi

# 步骤6: 验证数据完整性
echo ""
echo "[6/6] 验证数据完整性..."
python3 -c "
import json, os
checks = [
    ('源数据-公司', 'data/source/company/company_info.json', ['name', 'products']),
    ('源数据-FAQ', 'data/source/faq/faq_data.json', ['faq']),
    ('源数据-模板', 'data/source/templates/templates_data.json', ['communication', 'sales_tips']),
    ('源数据-制度', 'data/source/policies/policies_data.json', ['policies']),
    ('Mock-流量', 'data/mock/business-data/traffic_data.json', ['traffic']),
    ('Mock-客户', 'data/mock/business-data/customer_data.json', ['customers']),
    ('Mock-订单', 'data/mock/business-data/order_data.json', ['orders']),
    ('Mock-竞品', 'data/mock/business-data/competitor_data.json', ['competitors']),
    ('Mock-BOM', 'data/mock/business-data/bom_data.json', ['boms']),
    ('Mock-库存', 'data/mock/business-data/inventory_data.json', ['items']),
    ('Mock-行情', 'data/mock/business-data/material_prices.json', ['materials']),
    ('测试用例-正常', 'tests/cases/normal/normal_cases.json', ['cases']),
    ('测试用例-边界', 'tests/cases/boundary/boundary_cases.json', ['cases']),
    ('测试用例-异常', 'tests/cases/exception/exception_cases.json', ['cases']),
]
all_ok = True
for name, rel_path, keys in checks:
    path = os.path.join('$PROJECT_DIR', rel_path)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        ok = all(k in data for k in keys)
        status = '✅' if ok else '❌'
        count = len(data.get(keys[0], [])) if keys else 0
        print(f'  {status} {name}: {os.path.basename(rel_path)} ({count}条)')
        if not ok:
            all_ok = False
    else:
        print(f'  ❌ {name}: 文件不存在')
        all_ok = False
print()
if all_ok:
    echo_text = '🎯 所有数据校验通过！'
    print(f'  {echo_text}')
else:
    print('  ⚠️ 部分数据校验失败，请检查')
"

echo ""
echo "=========================================="
echo "✅ 初始化完成！"
echo "=========================================="
echo ""
echo "Mock API:    http://localhost:3001"
echo "API状态:     http://localhost:3001/api/status"
echo "健康检查:    http://localhost:3001/health"
echo "数据目录:    $PROJECT_DIR/data/"
echo "测试用例:    $PROJECT_DIR/tests/cases/"
echo "脚本目录:    $PROJECT_DIR/scripts/"
echo ""
echo "运行重置:  bash scripts/reset_test_data.sh"
echo "运行清理:  bash scripts/clean_test_data.sh"