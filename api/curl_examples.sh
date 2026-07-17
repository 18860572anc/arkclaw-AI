#!/bin/bash
# ============================================================
# 倍斯特 Mock API - CURL 调用示例
# ============================================================
# 使用方式:
#   chmod +x api/curl_examples.sh
#   ./api/curl_examples.sh
#
# 前置条件:
#   1. Mock API 服务运行中: python api/mock_api_server.py
#   2. 默认端口 3001, 可通过 BASE_URL 环境变量修改
#
# 接口版本说明:
#   推荐使用 V1 版本路径: /api/v1/heiyun/*, /api/v1/beiyongxin/*
#   旧路径 /api/heiyun/* 保留兼容, 自动重定向到 /api/v1/heiyun/*
# ============================================================

BASE_URL="${BASE_URL:-http://localhost:3001}"
V1_URL="${BASE_URL}/api/v1"

echo "============================================================"
echo "  倍斯特 Mock API 调用示例"
echo "  服务地址: ${BASE_URL}"
echo "  Swagger:  ${BASE_URL}/docs"
echo "  ReDoc:    ${BASE_URL}/redoc"
echo "============================================================"
echo ""

# ==================== 1. 健康检查 ====================
echo "─── 1. 健康检查 ───"
curl -s "${BASE_URL}/health" | python3 -m json.tool 2>/dev/null || curl -s "${BASE_URL}/health"
echo -e "\n"

# ==================== 2. API 状态概览 ====================
echo "─── 2. API 状态概览 ───"
curl -s "${BASE_URL}/api/status" | python3 -m json.tool 2>/dev/null || curl -s "${BASE_URL}/api/status"
echo -e "\n"

# ==================== 3. 黑云系统 - V1 版本路径 ====================
echo "─── 3. 黑云系统 - BOM查询 (V1) ───"
curl -s "${V1_URL}/heiyun/bom/PROJ001" | python3 -m json.tool 2>/dev/null || curl -s "${V1_URL}/heiyun/bom/PROJ001"
echo -e "\n"

echo "─── 4. 黑云系统 - 订单列表 (V1) ───"
curl -s "${V1_URL}/heiyun/orders" | python3 -m json.tool 2>/dev/null || curl -s "${V1_URL}/heiyun/orders"
echo -e "\n"

echo "─── 5. 黑云系统 - 订单详情 (V1) ───"
curl -s "${V1_URL}/heiyun/orders/ORD1001" | python3 -m json.tool 2>/dev/null || curl -s "${V1_URL}/heiyun/orders/ORD1001"
echo -e "\n"

echo "─── 6. 黑云系统 - 客户列表 (V1) ───"
curl -s "${V1_URL}/heiyun/customers" | python3 -m json.tool 2>/dev/null || curl -s "${V1_URL}/heiyun/customers"
echo -e "\n"

echo "─── 7. 黑云系统 - 客户详情 (V1) ───"
curl -s "${V1_URL}/heiyun/customers/C1001" | python3 -m json.tool 2>/dev/null || curl -s "${V1_URL}/heiyun/customers/C1001"
echo -e "\n"

echo "─── 8. 黑云系统 - 库存数据 (V1) ───"
curl -s "${V1_URL}/heiyun/inventory" | python3 -m json.tool 2>/dev/null || curl -s "${V1_URL}/heiyun/inventory"
echo -e "\n"

# ==================== 4. 倍用心系统 - V1 版本路径 ====================
echo "─── 9. 倍用心系统 - BOM清单查询 (V1) ───"
curl -s "${V1_URL}/beiyongxin/bom/query?product_code=C200" | python3 -m json.tool 2>/dev/null || curl -s "${V1_URL}/beiyongxin/bom/query?product_code=C200"
echo -e "\n"

echo "─── 10. 倍用心系统 - 订单查询 (V1) ───"
curl -s "${V1_URL}/beiyongxin/orders/query?order_no=ORD1001" | python3 -m json.tool 2>/dev/null || curl -s "${V1_URL}/beiyongxin/orders/query?order_no=ORD1001"
echo -e "\n"

echo "─── 11. 倍用心系统 - 订单状态变更 (V1) ───"
curl -s -X POST "${V1_URL}/beiyongxin/orders/status-change" \
  -H "Content-Type: application/json" \
  -d '{
    "order_no": "ORD1001",
    "old_status": "待审核",
    "new_status": "生产中",
    "change_time": "2026-07-16T10:00:00",
    "change_reason": "生产排程完成"
  }' | python3 -m json.tool 2>/dev/null || curl -s -X POST "${V1_URL}/beiyongxin/orders/status-change" \
  -H "Content-Type: application/json" \
  -d '{"order_no":"ORD1001","old_status":"待审核","new_status":"生产中","change_time":"2026-07-16T10:00:00","change_reason":"生产排程完成"}'
echo -e "\n"

echo "─── 12. 倍用心系统 - 订单交期 (V1) ───"
curl -s "${V1_URL}/beiyongxin/orders/delivery?order_no=ORD1001" | python3 -m json.tool 2>/dev/null || curl -s "${V1_URL}/beiyongxin/orders/delivery?order_no=ORD1001"
echo -e "\n"

echo "─── 13. 倍用心系统 - 实时库存 (V1) ───"
curl -s "${V1_URL}/beiyongxin/inventory/real-time?material_code=MC001" | python3 -m json.tool 2>/dev/null || curl -s "${V1_URL}/beiyongxin/inventory/real-time?material_code=MC001"
echo -e "\n"

echo "─── 14. 倍用心系统 - 欠料明细 (V1) ───"
curl -s "${V1_URL}/beiyongxin/inventory/shortage?order_no=ORD1001" | python3 -m json.tool 2>/dev/null || curl -s "${V1_URL}/beiyongxin/inventory/shortage?order_no=ORD1001"
echo -e "\n"

echo "─── 15. 倍用心系统 - 采购订单 (V1) ───"
curl -s "${V1_URL}/beiyongxin/purchase/orders" | python3 -m json.tool 2>/dev/null || curl -s "${V1_URL}/beiyongxin/purchase/orders"
echo -e "\n"

echo "─── 16. 倍用心系统 - 供应商主数据 (V1) ───"
curl -s "${V1_URL}/beiyongxin/suppliers/master-data" | python3 -m json.tool 2>/dev/null || curl -s "${V1_URL}/beiyongxin/suppliers/master-data"
echo -e "\n"

echo "─── 17. 倍用心系统 - 客户信息 (V1) ───"
curl -s "${V1_URL}/beiyongxin/crm/customer-info" | python3 -m json.tool 2>/dev/null || curl -s "${V1_URL}/beiyongxin/crm/customer-info"
echo -e "\n"

# ==================== 5. 旧路径兼容测试 ====================
echo "─── 18. 旧路径兼容 - 黑云BOM查询 (旧路径) ───"
curl -s "${BASE_URL}/api/heiyun/bom/PROJ001" | python3 -m json.tool 2>/dev/null || curl -s "${BASE_URL}/api/heiyun/bom/PROJ001"
echo -e "\n"

echo "─── 19. 旧路径兼容 - 黑云订单列表 (旧路径) ───"
curl -s "${BASE_URL}/api/heiyun/orders" | python3 -m json.tool 2>/dev/null || curl -s "${BASE_URL}/api/heiyun/orders"
echo -e "\n"

# ==================== 6. 平台流量接口 ====================
echo "─── 20. 平台流量数据 ───"
curl -s "${BASE_URL}/api/platform/aliexpress/metrics" | python3 -m json.tool 2>/dev/null || curl -s "${BASE_URL}/api/platform/aliexpress/metrics"
echo -e "\n"

# ==================== 7. 竞品分析 ====================
echo "─── 21. 竞品分析 ───"
curl -s "${BASE_URL}/api/competitors" | python3 -m json.tool 2>/dev/null || curl -s "${BASE_URL}/api/competitors"
echo -e "\n"

# ==================== 8. 市场行情 ====================
echo "─── 22. 元器件行情 ───"
curl -s "${BASE_URL}/api/market/prices" | python3 -m json.tool 2>/dev/null || curl -s "${BASE_URL}/api/market/prices"
echo -e "\n"

# ==================== 9. 重新加载数据 ====================
echo "─── 23. 重新加载Mock数据 ───"
curl -s -X POST "${BASE_URL}/api/admin/reload" | python3 -m json.tool 2>/dev/null || curl -s -X POST "${BASE_URL}/api/admin/reload"
echo -e "\n"

echo "============================================================"
echo "  全部示例调用完成!"
echo "============================================================"
echo ""
echo "常见问题:"
echo "  1. 确认服务运行: python api/mock_api_server.py"
echo "  2. 查看文档: ${BASE_URL}/docs (Swagger), ${BASE_URL}/redoc (ReDoc)"
echo "  3. 修改端口: 编辑 mock_api_server.py 中的 port 参数"
echo "  4. 自定义 BASE_URL: BASE_URL=http://myhost:3001 ./api/curl_examples.sh"
echo ""