#!/bin/bash
# ============================================================
# 倍斯特前端 UI 组件测试一键运行脚本
# 支持 Chromium / Firefox / WebKit 多浏览器测试
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_DIR"

# 默认值
BROWSER="chromium"
HEADLESS="--headed=false"
SCREENSHOT=""
EXTRA_ARGS=""
PARALLEL=false
REPORT_DIR="${PROJECT_DIR}/results"
SCREENSHOT_DIR="${PROJECT_DIR}/tests/ui/screenshots"
TEST_PATH="tests/ui/"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_usage() {
    echo -e "${BLUE}倍斯特前端 UI 组件测试运行脚本${NC}"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  --chrome         仅运行 Chromium 测试 (默认)"
    echo "  --firefox        仅运行 Firefox 测试"
    echo "  --webkit         仅运行 WebKit 测试"
    echo "  --all-browsers   运行所有浏览器测试"
    echo "  --headed         有头模式（可见浏览器窗口）"
    echo "  --screenshot     失败时自动截图"
    echo "  --parallel       并行运行多浏览器测试"
    echo "  --viewport SIZE  视口尺寸: desktop|tablet|mobile (默认 desktop)"
    echo "  --path PATH      指定测试路径 (默认 tests/ui/)"
    echo "  -m MARKER        按标记过滤 (如 'chromium', 'accessibility')"
    echo "  -k EXPR          按关键字表达式过滤"
    echo "  -h, --help       显示此帮助"
    echo ""
    echo "示例:"
    echo "  $0 --chrome                          # 运行 Chromium 测试"
    echo "  $0 --all-browsers --headed            # 有头模式所有浏览器"
    echo "  $0 --firefox --screenshot            # Firefox + 失败截图"
    echo "  $0 --chrome -m accessibility         # 只运行可访问性测试"
    echo "  $0 --chrome -k test_navigation       # 只运行导航测试"
    echo "  $0 --viewport mobile                 # 移动端视口"
    echo "  $0 --path tests/ui/pages/test_navigation.py  # 指定单文件"
    echo ""
    echo "Docker 模式:"
    echo "  docker compose --profile ui-test up  # Docker 一键运行"
}

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --chrome)
            BROWSER="chromium"
            shift
            ;;
        --firefox)
            BROWSER="firefox"
            shift
            ;;
        --webkit)
            BROWSER="webkit"
            shift
            ;;
        --all-browsers)
            BROWSER="all"
            shift
            ;;
        --headed)
            HEADLESS="--headed"
            shift
            ;;
        --screenshot)
            SCREENSHOT="--screenshot"
            shift
            ;;
        --parallel)
            PARALLEL=true
            shift
            ;;
        --viewport)
            EXTRA_ARGS="$EXTRA_ARGS --viewport $2"
            shift 2
            ;;
        --path)
            TEST_PATH="$2"
            shift 2
            ;;
        -m)
            EXTRA_ARGS="$EXTRA_ARGS -m $2"
            shift 2
            ;;
        -k)
            EXTRA_ARGS="$EXTRA_ARGS -k $2"
            shift 2
            ;;
        -h|--help)
            print_usage
            exit 0
            ;;
        *)
            echo -e "${RED}未知参数: $1${NC}"
            print_usage
            exit 1
            ;;
    esac
done

# 检查依赖
check_deps() {
    echo -e "${BLUE}[检查依赖]${NC}"
    
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}错误: 未找到 python3${NC}"
        exit 1
    fi
    
    # 检查 playwright
    if python3 -c "import playwright" 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} Playwright 已安装"
    else
        echo -e "  ${YELLOW}⚠ Playwright 未安装，正在安装...${NC}"
        pip install playwright pytest pytest-html
        python3 -m playwright install --with-deps chromium firefox webkit
    fi

    # 检查 pytest
    if python3 -c "import pytest" 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} pytest 已安装"
    else
        echo -e "  ${YELLOW}⚠ 正在安装 pytest...${NC}"
        pip install pytest pytest-html
    fi

    # 检查 pytest-playwright
    if python3 -c "import pytest_playwright" 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} pytest-playwright 已安装"
    else
        echo -e "  ${YELLOW}⚠ 正在安装 pytest-playwright...${NC}"
        pip install pytest-playwright
    fi
}

# 设置环境变量
export PYTHONPATH="${PROJECT_DIR}:${PYTHONPATH}"
export UI_TEST_BASE_URL="${UI_TEST_BASE_URL:-http://localhost:80}"
export UI_TEST_TIMEOUT="${UI_TEST_TIMEOUT:-30000}"
mkdir -p "$SCREENSHOT_DIR" "$REPORT_DIR"

# 单浏览器运行
run_single_browser() {
    local browser=$1
    local report_file="${REPORT_DIR}/ui-report-${browser}.html"
    
    echo ""
    echo -e "${BLUE}================================================================${NC}"
    echo -e "${BLUE}  浏览器: ${browser}${NC}"
    echo -e "${BLUE}  报告: ${report_file}${NC}"
    echo -e "${BLUE}  截图: ${SCREENSHOT_DIR}${NC}"
    echo -e "${BLUE}  参数: ${HEADLESS} ${SCREENSHOT} ${EXTRA_ARGS}${NC}"
    echo -e "${BLUE}================================================================${NC}"
    echo ""
    
    local marker_flag=""
    if [[ "$browser" == "chromium" ]]; then
        marker_flag="-m chromium"
    elif [[ "$browser" == "firefox" ]]; then
        marker_flag="-m firefox"
    elif [[ "$browser" == "webkit" ]]; then
        marker_flag="-m webkit"
    fi

    set +e
    python3 -m pytest "$TEST_PATH" \
        -v \
        $HEADLESS \
        --browser "$browser" \
        --html="$report_file" \
        --self-contained-html \
        $SCREENSHOT \
        $marker_flag \
        $EXTRA_ARGS
    
    local exit_code=$?
    set -e
    
    if [[ $exit_code -eq 0 ]]; then
        echo -e "${GREEN}✓ ${browser} 测试全部通过${NC}"
    else
        echo -e "${YELLOW}⚠ ${browser} 测试部分未通过（exit code: $exit_code）${NC}"
        echo -e "${YELLOW}  查看报告: ${report_file}${NC}"
    fi
    
    return $exit_code
}

# 主逻辑
main() {
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║    倍斯特 - 前端 UI 组件测试框架            ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "  项目路径: ${PROJECT_DIR}"
    echo -e "  测试目标: ${UI_TEST_BASE_URL}"
    echo -e "  测试路径: ${TEST_PATH}"
    echo -e "  时间戳: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""

    check_deps

    if [[ "$BROWSER" == "all" ]]; then
        echo -e "${BLUE}[运行所有浏览器测试]${NC}"
        
        if $PARALLEL; then
            # 并行运行
            run_single_browser "chromium" &
            pid_chromium=$!
            run_single_browser "firefox" &
            pid_firefox=$!
            run_single_browser "webkit" &
            pid_webkit=$!
            
            wait $pid_chromium; rc_c=$?
            wait $pid_firefox; rc_f=$?
            wait $pid_webkit; rc_w=$?
        else
            # 串行运行
            run_single_browser "chromium"; rc_c=$?
            run_single_browser "firefox"; rc_f=$?
            run_single_browser "webkit"; rc_w=$?
        fi
        
        echo ""
        echo -e "${GREEN}============================================${NC}"
        echo -e "${GREEN}  跨浏览器测试汇总${NC}"
        echo -e "${GREEN}============================================${NC}"
        [[ $rc_c -eq 0 ]] && echo -e "  Chromium: ${GREEN}通过${NC}" || echo -e "  Chromium: ${YELLOW}有失败${NC}"
        [[ $rc_f -eq 0 ]] && echo -e "  Firefox:  ${GREEN}通过${NC}" || echo -e "  Firefox:  ${YELLOW}有失败${NC}"
        [[ $rc_w -eq 0 ]] && echo -e "  WebKit:   ${GREEN}通过${NC}" || echo -e "  WebKit:   ${YELLOW}有失败${NC}"
        
    else
        run_single_browser "$BROWSER"
    fi

    # 列出报告文件
    echo ""
    echo -e "${BLUE}[测试报告]${NC}"
    for report in "${REPORT_DIR}"/ui-report*.html; do
        if [[ -f "$report" ]]; then
            echo -e "  ${GREEN}✓${NC} $report"
        fi
    done
    echo ""
    echo -e "${BLUE}完成时间: $(date '+%Y-%m-%d %H:%M:%S')${NC}"
}

main