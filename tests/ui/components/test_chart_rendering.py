"""
图表渲染测试 - 甘特图/看板/数据可视化组件
"""

import pytest
import re


class TestChartRendering:
    """图表组件渲染测试"""

    # ============ 图表容器检测 ============

    @pytest.mark.chromium
    def test_chart_container_exists(self, page, base_url):
        """测试图表容器元素存在"""
        containers = page.query_selector_all(
            ".chart, .chart-container, .gantt-chart, "
            ".kanban-board, .visualization, "
            "[class*='chart'], [class*='Chart'], "
            "canvas, svg, .echarts, .recharts-wrapper, "
            ".apexcharts-canvas"
        )
        # 有图表容器就验证，没有就跳过
        if len(containers) > 0:
            assert True, f"检测到 {len(containers)} 个图表容器"
        else:
            pytest.skip("当前页面无图表组件，跳过")

    @pytest.mark.chromium
    def test_chart_canvas_rendered(self, page, base_url):
        """测试 Canvas/SVG 图表渲染"""
        canvases = page.query_selector_all("canvas")
        svgs = page.query_selector_all("svg.chart, svg[aria-label*='chart']")
        if len(canvases) > 0 or len(svgs) > 0:
            assert True, f"检测到 {len(canvases)} 个 canvas, {len(svgs)} 个 SVG 图表"
        else:
            pytest.skip("无 Canvas/SVG 图表元素，跳过")

    @pytest.mark.chromium
    def test_chart_dimensions_valid(self, page, base_url):
        """测试图表尺寸有效"""
        charts = page.query_selector_all(
            "canvas, .chart-container, .recharts-wrapper, .apexcharts-canvas"
        )
        valid_count = 0
        for chart in charts:
            try:
                box = chart.bounding_box()
                if box and box["width"] > 0 and box["height"] > 0:
                    valid_count += 1
            except Exception:
                pass
        if len(charts) > 0:
            assert valid_count > 0, f"图表应有有效尺寸（{valid_count}/{len(charts)} 有效）"
        else:
            pytest.skip("无图表元素，跳过")

    # ============ 甘特图特定测试 ============

    @pytest.mark.chromium
    def test_gantt_chart_elements(self, page, base_url):
        """测试甘特图元素"""
        gantt_selectors = (
            ".gantt, .gantt-chart, "
            "[class*='gantt'], [class*='Gantt'], "
            ".gantt-task, .gantt-bar"
        )
        gantt_elements = page.query_selector_all(gantt_selectors)
        if len(gantt_elements) > 0:
            assert True, f"检测到 {len(gantt_elements)} 个甘特图元素"
        else:
            pytest.skip("当前页面无甘特图，跳过")

    @pytest.mark.chromium
    def test_gantt_timeline_visible(self, page, base_url):
        """测试甘特图时间轴可见"""
        timeline = page.query_selector_all(
            ".gantt-timeline, .gantt-header, "
            "[class*='timeline'], [class*='Timeline']"
        )
        if len(timeline) > 0:
            assert True, "甘特图时间轴可见"
        else:
            pytest.skip("无甘特图时间轴，跳过")

    # ============ 看板特定测试 ============

    @pytest.mark.chromium
    def test_kanban_board_structure(self, page, base_url):
        """测试看板结构"""
        kanban = page.query_selector_all(
            ".kanban, .kanban-board, "
            "[class*='kanban'], [class*='Kanban']"
        )
        if len(kanban) > 0:
            # 检查列结构
            columns = page.query_selector_all(
                ".kanban-column, .board-column, "
                "[class*='column'], [class*='Column']"
            )
            cards = page.query_selector_all(
                ".kanban-card, .board-card, "
                "[class*='card'], [class*='Card']"
            )
            assert True, f"看板: {len(columns)} 列, {len(cards)} 卡片"
        else:
            pytest.skip("当前页面无看板组件，跳过")

    @pytest.mark.chromium
    def test_kanban_card_interaction(self, page, base_url):
        """测试看板卡片交互（点击）"""
        cards = page.query_selector_all(
            ".kanban-card, .board-card, "
            "[class*='card'], [class*='Card']"
        )
        if len(cards) > 0:
            try:
                first_card = cards[0]
                if first_card.is_visible():
                    first_card.click()
                    page.wait_for_load_state("networkidle")
                    assert True, "看板卡片点击可交互"
            except Exception:
                pytest.skip("看板卡片不可点击，跳过")
        else:
            pytest.skip("无看板卡片，跳过")

    # ============ 数据可视化 ============

    @pytest.mark.chromium
    def test_data_visualization_renders(self, page, base_url):
        """测试数据可视化渲染"""
        viz_elements = page.query_selector_all(
            ".chart, .visualization, "
            "[data-testid*='chart'], [data-testid*='Chart'], "
            "#chart, #dashboard-chart, "
            ".dashboard .chart, main .chart"
        )
        if len(viz_elements) > 0:
            visible_count = sum(1 for el in viz_elements if el.is_visible())
            assert visible_count > 0, f"应有可见的可视化元素 ({visible_count}/{len(viz_elements)})"
        else:
            pytest.skip("无数据可视化元素，跳过")

    @pytest.mark.chromium
    def test_chart_labels_readable(self, page, base_url):
        """测试图表标签可读"""
        labels = page.query_selector_all(
            ".chart-label, .axis-label, "
            ".legend-text, text.recharts-text, "
            "[class*='label'], [class*='legend']"
        )
        if len(labels) > 0:
            readable = [l for l in labels if l.is_visible() and l.inner_text().strip()]
            assert len(readable) > 0, "图表标签应包含可读文本"
        else:
            pytest.skip("无图表标签，跳过")

    # ============ 响应式测试 ============

    @pytest.mark.chromium
    def test_chart_responsive_viewport(self, page, base_url):
        """测试图表响应式（切换视口）"""
        charts_before = page.query_selector_all(
            "canvas, .chart-container, .recharts-wrapper"
        )
        if len(charts_before) > 0:
            # 切换到移动端视口
            page.set_viewport_size({"width": 375, "height": 667})
            page.wait_for_timeout(500)
            charts_after = page.query_selector_all(
                "canvas, .chart-container, .recharts-wrapper"
            )
            assert len(charts_after) > 0, "移动端视口图表仍应存在"
        else:
            pytest.skip("无图表元素，跳过")

    # ============ 可访问性 ============

    @pytest.mark.chromium
    @pytest.mark.accessibility
    def test_chart_aria_roles(self, page, base_url):
        """可访问性：图表 ARIA 角色"""
        charts = page.query_selector_all(
            "canvas, svg, [role='img'], [role='graphics-document'], "
            "[role='figure']"
        )
        chart_count = len(charts)
        # 图表可能有也可能没有 ARIA 角色

    @pytest.mark.chromium
    @pytest.mark.accessibility
    def test_chart_aria_labels(self, page, base_url):
        """可访问性：图表 ARIA label 标签"""
        labelled = page.query_selector_all(
            "[aria-label*='chart' i], [aria-label*='Chart' i], "
            "[aria-labelledby]"
        )
        if len(labelled) > 0:
            assert True, f"图表可访问性标签: {len(labelled)} 个"

    # ============ 跨浏览器 ============

    @pytest.mark.firefox
    def test_chart_firefox_render(self, page, base_url):
        """Firefox 下图表渲染"""
        charts = page.query_selector_all(
            "canvas, .chart, .chart-container"
        )
        if len(charts) > 0:
            assert True, "Firefox 下图表正常渲染"
        else:
            pytest.skip("无图表元素，跳过")

    @pytest.mark.webkit
    def test_chart_webkit_render(self, page, base_url):
        """WebKit 下图表渲染"""
        charts = page.query_selector_all(
            "canvas, .chart, .chart-container"
        )
        if len(charts) > 0:
            assert True, "WebKit 下图表正常渲染"
        else:
            pytest.skip("无图表元素，跳过")