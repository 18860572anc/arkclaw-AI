#!/bin/bash
# ============================================
# 倍斯特测试数据框架 - 重置脚本
# 保留目录结构，重新生成所有数据
# ============================================
set -e
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "⚠️ 即将重置所有测试数据（保留目录结构）"
echo "项目目录: $PROJECT_DIR"
read -p "确认继续? (y/N): " confirm
if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "已取消"
    exit 0
fi

echo ""
echo "🔄 正在重置测试数据..."
# 清理Mock数据
rm -f "$PROJECT_DIR/data/mock/business-data/"*.json
echo "  ✅ Mock数据已清理"
# 清理测试用例
rm -f "$PROJECT_DIR/tests/cases/normal/"*.json
rm -f "$PROJECT_DIR/tests/cases/boundary/"*.json
rm -f "$PROJECT_DIR/tests/cases/exception/"*.json
echo "  ✅ 测试用例已清理"
# 清理源数据（保留目录）
rm -f "$PROJECT_DIR/data/source/company/"*.json
rm -f "$PROJECT_DIR/data/source/faq/"*.json
rm -f "$PROJECT_DIR/data/source/templates/"*.json
rm -f "$PROJECT_DIR/data/source/policies/"*.json
echo "  ✅ 源数据已清理"

# 重新生成
echo ""
echo "🔄 重新生成数据..."
bash "$PROJECT_DIR/scripts/init_test_data.sh"