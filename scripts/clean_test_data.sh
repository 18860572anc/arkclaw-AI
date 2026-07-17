#!/bin/bash
# ============================================
# 倍斯特测试数据框架 - 完全清理脚本
# 删除所有生成的数据，但保留目录结构
# ============================================
set -e
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "⚠️ 即将完全清理所有测试数据！"
echo "项目目录: $PROJECT_DIR"
echo "影响范围:"
echo "  - data/mock/business-data/  (所有Mock数据)"
echo "  - data/source/  (所有源数据)"
echo "  - tests/cases/  (所有测试用例)"
echo "  - data/mock/vector-data/  (向量数据库)"
echo "  - results/  (测试结果)"
read -p "确认继续? (y/N): " confirm
if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "已取消"
    exit 0
fi

echo ""
echo "🗑️  正在清理..."
# 清理Mock数据
rm -rf "$PROJECT_DIR/data/mock/business-data/"*
echo "  ✅ Mock数据已清理"
# 清理测试用例
rm -rf "$PROJECT_DIR/tests/cases/normal/"*
rm -rf "$PROJECT_DIR/tests/cases/boundary/"*
rm -rf "$PROJECT_DIR/tests/cases/exception/"*
echo "  ✅ 测试用例已清理"
# 清理源数据
rm -rf "$PROJECT_DIR/data/source/company/"*
rm -rf "$PROJECT_DIR/data/source/faq/"*
rm -rf "$PROJECT_DIR/data/source/templates/"*
rm -rf "$PROJECT_DIR/data/source/policies/"*
echo "  ✅ 源数据已清理"
# 清理向量数据库
rm -rf "$PROJECT_DIR/data/mock/vector-data/"*
echo "  ✅ 向量数据库已清理"
# 清理测试结果
rm -rf "$PROJECT_DIR/results/"*
echo "  ✅ 测试结果已清理"

echo ""
echo "✅ 清理完成！目录结构已保留。"
echo "运行初始化: bash scripts/init_test_data.sh"