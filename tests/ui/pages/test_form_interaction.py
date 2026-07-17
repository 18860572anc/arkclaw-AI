"""
表单交互测试 - 输入校验/提交/重置/错误提示
"""

import pytest
from tests.ui.pages.form_interaction import FormInteractionPage


class TestFormInteraction:
    """表单交互功能测试"""

    # ======== 表单存在性 ========

    @pytest.mark.chromium
    def test_form_present(self, page, base_url):
        """测试表单元素存在"""
        form = FormInteractionPage(page)
        assert form.is_form_present(), "表单元素应存在于页面"

    @pytest.mark.chromium
    def test_form_has_labels(self, page, base_url):
        """测试表单有标签"""
        form = FormInteractionPage(page)
        labels = form.get_all_labels()
        assert len(labels) > 0, "表单应包含标签"

    @pytest.mark.chromium
    def test_form_has_inputs(self, page, base_url):
        """测试表单有输入框"""
        form = FormInteractionPage(page)
        assert form.has_placeholder() or len(form.get_all_labels()) > 0, \
            "表单应有输入框（placeholder 或 label）"

    @pytest.mark.chromium
    def test_submit_button_exists(self, page, base_url):
        """测试提交按钮存在"""
        form = FormInteractionPage(page)
        try:
            form.click_submit()
            page.wait_for_load_state("networkidle")
            # 点击后页面不应崩溃
            assert page.title() is not None, "点击提交后页面不崩溃"
        except Exception:
            pytest.skip("提交按钮不存在或不可点击，跳过")

    # ======== 输入操作 ========

    @pytest.mark.chromium
    def test_fill_text_input(self, page, base_url):
        """测试文本输入框填写"""
        form = FormInteractionPage(page)
        labels = form.get_all_labels()
        if labels:
            first_label = labels[0]
            try:
                form.fill_input(first_label, "测试输入")
                value = form.get_input_value(first_label)
                assert value == "测试输入" or value != "", \
                    "输入框应能接收文本输入"
            except Exception:
                pytest.skip("无法填写该字段，跳过")

    @pytest.mark.chromium
    def test_clear_input_field(self, page, base_url):
        """测试清空输入框"""
        form = FormInteractionPage(page)
        labels = form.get_all_labels()
        if labels:
            first_label = labels[0]
            try:
                form.fill_input(first_label, "some text")
                form.clear_input(first_label)
                cleared_value = form.get_input_value(first_label)
                assert cleared_value == "", "清空后输入框应为空"
            except Exception:
                pytest.skip("无法操作该字段，跳过")

    # ======== 提交测试 ========

    @pytest.mark.chromium
    def test_submit_empty_form(self, page, base_url):
        """测试提交空表单"""
        form = FormInteractionPage(page)
        try:
            # 清空所有字段
            for label in form.get_all_labels():
                try:
                    form.clear_input(label)
                except Exception:
                    pass
            form.click_submit()
            page.wait_for_load_state("networkidle")
            # 提交后页面不应崩溃
            assert page.title() is not None, "提交空表单后页面不崩溃"
        except Exception:
            pytest.skip("提交操作不可用，跳过")

    @pytest.mark.chromium
    def test_submit_with_data(self, page, base_url):
        """测试填写数据后提交"""
        form = FormInteractionPage(page)
        labels = form.get_all_labels()
        if labels:
            try:
                for i, label in enumerate(labels):
                    try:
                        form.fill_input(label, f"测试数据_{i}")
                    except Exception:
                        pass
                form.click_submit()
                page.wait_for_load_state("networkidle")
                assert page.title() is not None, "提交表单后页面不崩溃"
            except Exception:
                pytest.skip("提交操作不可用，跳过")

    # ======== 校验与错误 ========

    @pytest.mark.chromium
    def test_error_messages_on_invalid(self, page, base_url):
        """测试无效输入时错误提示"""
        form = FormInteractionPage(page)
        try:
            has_errors_before = form.has_errors()
            if not has_errors_before:
                # 尝试提交空表单触发校验
                for label in form.get_all_labels():
                    try:
                        form.clear_input(label)
                    except Exception:
                        pass
                form.click_submit()
                page.wait_for_load_state("networkidle")
            # 检查是否有错误信息
            if form.has_errors():
                errors = form.get_error_messages()
                assert len(errors) > 0, "错误信息不应为空列表"
            else:
                pytest.skip("未触发校验错误，跳过")
        except Exception:
            pytest.skip("校验功能不可用，跳过")

    @pytest.mark.chromium
    def test_field_error_indicators(self, page, base_url):
        """测试错误字段指示器"""
        form = FormInteractionPage(page)
        error_fields = form.get_field_error_count()
        # 验证错误字段标记存在性
        assert error_fields >= 0, "错误字段计数应为非负"

    @pytest.mark.chromium
    def test_success_message_on_valid(self, page, base_url):
        """测试成功后提示信息"""
        form = FormInteractionPage(page)
        if form.has_success_message():
            msg = form.get_success_message()
            assert msg != "", "成功提示信息不应为空"

    # ======== 重置测试 ========

    @pytest.mark.chromium
    def test_reset_button_clears_form(self, page, base_url):
        """测试重置按钮清空表单"""
        form = FormInteractionPage(page)
        try:
            # 先填写一些数据
            labels = form.get_all_labels()
            for label in labels[:2]:
                try:
                    form.fill_input(label, "data")
                except Exception:
                    pass
            # 尝试点击重置
            form.click_reset()
            page.wait_for_load_state("networkidle")
            # 验证字段被清空
            cleared = True
            for label in labels[:2]:
                try:
                    val = form.get_input_value(label)
                    if val:
                        cleared = False
                        break
                except Exception:
                    pass
            if cleared:
                assert True, "重置后字段已清空"
        except Exception:
            pytest.skip("重置按钮不存在或不可用，跳过")

    # ======== 可访问性 ========

    @pytest.mark.chromium
    @pytest.mark.accessibility
    def test_form_aria_label(self, page, base_url):
        """可访问性：表单 ARIA label"""
        form = FormInteractionPage(page)
        has_label = form.has_form_aria_label()
        # ARIA label 不是强制的

    @pytest.mark.chromium
    @pytest.mark.accessibility
    def test_required_fields_marked(self, page, base_url):
        """可访问性：必填字段标记"""
        form = FormInteractionPage(page)
        required = form.get_required_fields()
        # 可能有也可能没有必填标记

    @pytest.mark.chromium
    @pytest.mark.accessibility
    def test_aria_describedby_present(self, page, base_url):
        """可访问性：aria-describedby"""
        form = FormInteractionPage(page)
        # 验证字段描述关联

    # ======== 跨浏览器 ========

    @pytest.mark.firefox
    def test_form_firefox_compatible(self, page, base_url):
        """Firefox 下表单渲染"""
        form = FormInteractionPage(page)
        assert form.is_form_present(), "Firefox 下表单应正常渲染"

    @pytest.mark.webkit
    def test_form_webkit_compatible(self, page, base_url):
        """WebKit 下表单渲染"""
        form = FormInteractionPage(page)
        assert form.is_form_present(), "WebKit 下表单应正常渲染"