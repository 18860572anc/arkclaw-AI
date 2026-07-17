#!/bin/bash
# ============================================================
# 倍斯特接口测试一键运行脚本
# 使用方式:
#   ./scripts/run_tests.sh           # 运行所有测试
#   ./scripts/run_tests.sh --all     # 运行所有测试
#   ./scripts/run_tests.sh --api     # 仅运行接口测试
#   ./scripts/run_tests.sh --report  # 运行所有测试并生成HTML报告
#   ./scripts/run_tests.sh --help    # 查看帮助
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 默认参数
RUN_ALL=false
RUN_API=false
GEN_REPORT=false
API_BASE="${MOCK_API_BASE:-http://localhost:3001}"

# 解析参数
for arg in "$@"; do
  case "$arg" in
    --all)
      RUN_ALL=true
      ;;
    --api)
      RUN_API=true
      ;;
    --report)
      GEN_REPORT=true
      ;;
    --help)
      echo "用法: $0 [选项]"
      echo ""
      echo "选项:"
      echo "  --all      运行所有测试（默认）"
      echo "  --api      仅运行接口测试"
      echo "  --report   运行测试并生成HTML报告"
      echo "  --help     查看帮助"
      exit 0
      ;;
    *)
      echo "未知参数: $arg"
      echo "用法: $0 [--all | --api | --report | --help]"
      exit 1
      ;;
  esac
done

# 默认行为：无条件运行都运行
if [ "$RUN_ALL" = false ] && [ "$RUN_API" = false ]; then
  RUN_ALL=true
fi

# 检查依赖
echo -e "${YELLOW}[1/5] 检查测试依赖...${NC}"
python3 -c "import pytest; import requests; import jsonschema" 2>/dev/null || {
  echo -e "${YELLOW}安装测试依赖...${NC}"
  pip install -q pytest requests pytest-html jsonschema
}
echo -e "${GREEN}依赖检查通过${NC}"

# 确保数据已生成
echo -e "${YELLOW}[2/5] 准备测试数据...${NC}"
if [ -f scripts/generate_mock_data.py ]; then
  python3 scripts/generate_mock_data.py 2>/dev/null || true
fi
echo -e "${GREEN}测试数据准备完成${NC}"

# 检查 Mock API 服务
echo -e "${YELLOW}[3/5] 检查 Mock API 服务...${NC}"
if curl -sf "$API_BASE/health" > /dev/null 2>&1; then
  echo -e "${GREEN}Mock API 服务运行中 ✅${NC}"
else
  echo -e "${RED}⚠️  Mock API 服务未运行！请先在另一个终端启动:${NC}"
  echo -e "  cd $PROJECT_DIR/api && uvicorn mock_api_server:app --host 0.0.0.0 --port 3001"
  echo ""
  echo -e "${YELLOW}尝试自动启动...${NC}"
  cd "$PROJECT_DIR/api"
  uvicorn mock_api_server:app --host 0.0.0.0 --port 3001 &
  MOCK_PID=$!
  cd "$PROJECT_DIR"
  sleep 2
  if curl -sf "$API_BASE/health" > /dev/null 2>&1; then
    echo -e "${GREEN}Mock API 服务已自动启动 ✅${NC}"
  else
    echo -e "${RED}自动启动失败，请手动启动 Mock API 服务${NC}"
    exit 1
  fi
fi

# 运行测试
echo -e "${YELLOW}[4/5] 运行测试...${NC}"
export MOCK_API_BASE="$API_BASE"
PYTEST_OPTS="-v"

if [ "$GEN_REPORT" = true ]; then
  REPORT_DIR="$PROJECT_DIR/results"
  mkdir -p "$REPORT_DIR"
  PYTEST_OPTS="$PYTEST_OPTS --html=$REPORT_DIR/report.html --self-contained-html"
fi

if [ "$RUN_API" = true ]; then
  echo -e "${YELLOW}运行接口测试...${NC}"
  cd "$PROJECT_DIR/tests"
  python -m pytest api/ $PYTEST_OPTS
elif [ "$RUN_ALL" = true ]; then
  echo -e "${YELLOW}运行所有测试...${NC}"
  cd "$PROJECT_DIR/tests"
  python -m pytest api/ $PYTEST_OPTS
fi

# 结果
TEST_EXIT=$?
echo ""
if [ $TEST_EXIT -eq 0 ]; then
  echo -e "${GREEN}[5/5] 所有测试通过 ✅${NC}"
else
  echo -e "${RED}[5/5] 部分测试失败 ❌ (退出码: $TEST_EXIT)${NC}"
fi

if [ "$GEN_REPORT" = true ]; then
  echo -e "${GREEN}测试报告: $REPORT_DIR/report.html${NC}"
fi

exit $TEST_EXIT