#!/bin/bash
# ============================================================
# 倍斯特 Web 自动化测试一键运行脚本
# 使用方式:
#   ./scripts/run_web_tests.sh                    # 运行所有 WEB 测试（无头模式）
#   ./scripts/run_web_tests.sh --headed           # 有头模式（可见浏览器）
#   ./scripts/run_web_tests.sh --screenshot       # 失败时自动截图
#   ./scripts/run_web_tests.sh --report           # 生成 HTML 测试报告
#   ./scripts/run_web_tests.sh --all              # 全部功能（有头+截图+报告）
#   ./scripts/run_web_tests.sh --help             # 查看帮助
#   ./scripts/run_web_tests.sh --docker           # 通过 Docker Compose 运行
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 默认参数
HEADLESS=true
SCREENSHOT=false
GEN_REPORT=false
USE_DOCKER=false
WEB_TEST_BASE_URL="${WEB_TEST_BASE_URL:-http://localhost:80}"
BROWSERLESS_WS="${BROWSERLESS_WS:-ws://localhost:3000}"

# ── 参数解析 ──────────────────────────────────────────────────────────────────

for arg in "$@"; do
  case "$arg" in
    --headed)
      HEADLESS=false
      ;;
    --screenshot)
      SCREENSHOT=true
      ;;
    --report)
      GEN_REPORT=true
      ;;
    --all)
      HEADLESS=false
      SCREENSHOT=true
      GEN_REPORT=true
      ;;
    --docker)
      USE_DOCKER=true
      ;;
    --help)
      echo "用法: $0 [选项]"
      echo ""
      echo "选项:"
      echo "  --headed      有头模式（可见浏览器窗口）"
      echo "  --screenshot  测试失败时自动截图"
      echo "  --report      生成 HTML 测试报告"
      echo "  --all         全部功能（有头+截图+报告）"
      echo "  --docker      通过 Docker Compose 运行"
      echo "  --help        查看帮助"
      exit 0
      ;;
    *)
      echo -e "${RED}未知参数: $arg${NC}"
      echo "用法: $0 [--headed | --screenshot | --report | --all | --docker | --help]"
      exit 1
      ;;
  esac
done

# ── Docker 模式 ───────────────────────────────────────────────────────────────

if [ "$USE_DOCKER" = true ]; then
  echo -e "${CYAN}========================================${NC}"
  echo -e "${CYAN}  倍斯特 Web 测试 - Docker 模式${NC}"
  echo -e "${CYAN}========================================${NC}"
  echo ""
  echo -e "${YELLOW}启动 Docker Compose web-test 服务...${NC}"
  docker compose --profile web-test up --build --abort-on-container-exit
  EXIT_CODE=$?
  echo ""
  if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}所有 WEB 测试通过 ✅${NC}"
  else
    echo -e "${RED}部分 WEB 测试失败 ❌ (退出码: $EXIT_CODE)${NC}"
  fi
  echo -e "${GREEN}测试报告: ${PROJECT_DIR}/results/web-report.html${NC}"
  echo -e "${GREEN}截图目录: ${PROJECT_DIR}/results/screenshots/${NC}"
  exit $EXIT_CODE
fi

# ── 本地模式 ──────────────────────────────────────────────────────────────────

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  倍斯特 Web 自动化测试${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# ── 步骤 1: 检查依赖 ──────────────────────────────────────────────────────────

echo -e "${YELLOW}[1/6] 检查测试依赖...${NC}"

# 检查 Python 依赖
python3 -c "import pytest; import playwright" 2>/dev/null || {
  echo -e "${YELLOW}安装测试依赖...${NC}"
  pip install -q pytest playwright pytest-html allure-pytest
}

# 检查 Playwright 浏览器
python3 -c "from playwright.sync_api import sync_playwright; pw = sync_playwright().start(); pw.chromium.launch(headless=True).close(); pw.stop()" 2>/dev/null || {
  echo -e "${YELLOW}安装 Playwright 浏览器...${NC}"
  playwright install chromium
}

echo -e "${GREEN}依赖检查通过 ✅${NC}"

# ── 步骤 2: 检查服务 ──────────────────────────────────────────────────────────

echo -e "${YELLOW}[2/6] 检查服务可用性...${NC}"

SERVICES_OK=true

# 检查 Nginx
if curl -sf "$WEB_TEST_BASE_URL" > /dev/null 2>&1; then
  echo -e "${GREEN}  Nginx/Web 服务运行中 ✅${NC}"
else
  echo -e "${RED}  ❌ Web 服务不可用 ($WEB_TEST_BASE_URL)${NC}"
  echo -e "${YELLOW}  请确保服务已启动: docker compose up -d nginx${NC}"
  SERVICES_OK=false
fi

# 检查 browserless
if curl -sf "$BROWSERLESS_WS" > /dev/null 2>&1; then
  echo -e "${GREEN}  browserless 服务运行中 ✅${NC}"
else
  echo -e "${YELLOW}  ⚠️  browserless 不可用，将使用本地浏览器${NC}"
fi

# 检查 Mock API
if curl -sf "http://localhost:3001/health" > /dev/null 2>&1; then
  echo -e "${GREEN}  Mock API 服务运行中 ✅${NC}"
else
  echo -e "${YELLOW}  ⚠️  Mock API 不可用，部分测试可能受限${NC}"
fi

echo ""

if [ "$SERVICES_OK" = false ]; then
  echo -e "${RED}请先启动必要服务:${NC}"
  echo -e "  docker compose up -d nginx mock-api browser"
  echo ""
  echo -e "${YELLOW}是否继续运行测试？(y/N)${NC}"
  read -r CONTINUE
  if [ "$CONTINUE" != "y" ] && [ "$CONTINUE" != "Y" ]; then
    echo -e "${RED}测试已取消${NC}"
    exit 1
  fi
fi

# ── 步骤 3: 准备截图目录 ──────────────────────────────────────────────────────

echo -e "${YELLOW}[3/6] 准备截图目录...${NC}"
SCREENSHOT_DIR="$PROJECT_DIR/results/screenshots"
mkdir -p "$SCREENSHOT_DIR"
echo -e "${GREEN}截图目录: $SCREENSHOT_DIR ✅${NC}"

# ── 步骤 4: 准备测试报告目录 ──────────────────────────────────────────────────

echo -e "${YELLOW}[4/6] 准备报告目录...${NC}"
REPORT_DIR="$PROJECT_DIR/results"
mkdir -p "$REPORT_DIR"
echo -e "${GREEN}报告目录: $REPORT_DIR ✅${NC}"

# ── 步骤 5: 运行测试 ──────────────────────────────────────────────────────────

echo -e "${YELLOW}[5/6] 运行 Web 测试...${NC}"
echo ""

# 设置环境变量
export WEB_TEST_BASE_URL="$WEB_TEST_BASE_URL"
export BROWSERLESS_WS="$BROWSERLESS_WS"
export PLAYWRIGHT_HEADLESS="$HEADLESS"
export SCREENSHOT_DIR="$SCREENSHOT_DIR"
export PLAYWRIGHT_TIMEOUT="30000"

# 构建 pytest 参数
PYTEST_OPTS="-v"

if [ "$SCREENSHOT" = true ]; then
  PYTEST_OPTS="$PYTEST_OPTS --screenshot=only-on-failure"
fi

if [ "$GEN_REPORT" = true ]; then
  PYTEST_OPTS="$PYTEST_OPTS --html=$REPORT_DIR/web-report.html --self-contained-html"
fi

# 显示配置
echo -e "${CYAN}测试配置:${NC}"
echo -e "  目标 URL:   $WEB_TEST_BASE_URL"
echo -e "  Browserless: $BROWSERLESS_WS"
echo -e "  有头模式:   $([ "$HEADLESS" = false ] && echo '是' || echo '否')"
echo -e "  失败截图:   $([ "$SCREENSHOT" = true ] && echo '是' || echo '否')"
echo -e "  HTML报告:   $([ "$GEN_REPORT" = true ] && echo '是' || echo '否')"
echo ""

# 运行
echo -e "${YELLOW}开始执行测试...${NC}"
cd "$PROJECT_DIR/tests"
python -m pytest web/ $PYTEST_OPTS
TEST_EXIT=$?
cd "$PROJECT_DIR"

# ── 步骤 6: 结果汇总 ──────────────────────────────────────────────────────────

echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  测试结果${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

if [ $TEST_EXIT -eq 0 ]; then
  echo -e "${GREEN}[6/6] 所有 Web 测试通过 ✅${NC}"
else
  echo -e "${RED}[6/6] 部分 Web 测试失败 ❌ (退出码: $TEST_EXIT)${NC}"
fi

if [ "$GEN_REPORT" = true ]; then
  echo -e "${GREEN}测试报告: $REPORT_DIR/web-report.html${NC}"
fi

echo -e "${GREEN}截图目录: $SCREENSHOT_DIR${NC}"
echo ""

exit $TEST_EXIT