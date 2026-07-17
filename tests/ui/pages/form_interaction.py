"""
表单交互页面对象模型
封装表单输入校验、提交、重置、错误提示等交互
"""

from typing import Dict, Optional, List


class FormInteractionPage:
    """表单交互页面对象"""

    # 表单选择器
    FORM = "form, [role='form'], .form, .form-container"
    INPUT = (
        "input:not([type='hidden']):not([type='submit']):not([type='button']), "
        "textarea, select, [role='textbox'], [contenteditable='true']"
    )
    TEXT_INPUT = "input[type='text'], input:not([type])"
    NUMBER_INPUT = "input[type='number']"
    EMAIL_INPUT = "input[type='email']"
    SELECT = "select, [role='listbox']"
    TEXTAREA = "textarea, [role='textbox']"
    CHECKBOX = "input[type='checkbox'], [role='checkbox']"
    RADIO = "input[type='radio'], [role='radio']"

    # 按钮
    SUBMIT_BTN = (
        "button[type='submit'], input[type='submit'], "
        ".submit-btn, .btn-submit, "
        "[aria-label*='submit' i], [aria-label*='提交' i]"
    )
    RESET_BTN = (
        "button[type='reset'], input[type='reset'], "
        ".reset-btn, .btn-reset, "
        "[aria-label*='reset' i], [aria-label*='重置' i]"
    )
    CANCEL_BTN = (
        ".cancel-btn, .btn-cancel, "
        "[aria-label*='cancel' i], [aria-label*='取消' i]"
    )

    # 校验与错误
    ERROR_MSG = (
        ".error, .error-message, .form-error, "
        ".invalid-feedback, .help-block.is-error, "
        "[aria-invalid='true'] + .error, "
        "[role='alert'], .alert.alert-danger, "
        ".field-error, .validation-error, "
        ".text-danger"
    )
    FIELD_ERROR = (
        "[aria-invalid='true'], .is-invalid, "
        ".has-error input, .has-error select, .has-error textarea"
    )
    SUCCESS_MSG = (
        ".success, .success-message, .form-success, "
        ".alert.alert-success, .text-success"
    )
    VALIDATION_SUMMARY = ".validation-summary, .error-summary, [aria-live='polite'].error"

    # Label
    LABEL = "label, [role='label'], .form-label, .field-label"
    REQUIRED_MARK = ".required, [aria-required='true']"

    # 占位符
    PLACEHOLDER = "[placeholder]"

    def __init__(self, page):
        self.page = page

    # ======== 表单存在性 ========

    def is_form_present(self) -> bool:
        """表单是否存在"""
        return self.page.locator(self.FORM).first.is_visible()

    def get_form_action(self) -> str:
        """获取表单 action 属性"""
        form = self.page.locator(self.FORM).first
        return form.get_attribute("action") or ""

    def get_form_method(self) -> str:
        """获取表单 method 属性"""
        form = self.page.locator(self.FORM).first
        return form.get_attribute("method") or ""

    # ======== 输入操作 ========

    def fill_input(self, label_or_placeholder: str, value: str):
        """根据 Label 或 Placeholder 填写输入框"""
        # 尝试通过关联 Label 查找
        label = self.page.locator(self.LABEL).filter(has_text=label_or_placeholder).first
        if label.is_visible():
            for_id = label.get_attribute("for")
            if for_id:
                input_el = self.page.locator(f"#{for_id}")
                if input_el.is_visible():
                    input_el.fill(value)
                    return

        # 尝试通过 placeholder 查找
        input_el = (
            self.page.locator(self.INPUT)
            .filter(has_text=label_or_placeholder)
            .first
        )
        if input_el.is_visible():
            input_el.fill(value)
            return

        # 兜底：按文本匹配最近的 input
        input_el = self.page.get_by_label(label_or_placeholder).first
        if input_el.is_visible():
            input_el.fill(value)

    def get_input_value(self, label_or_placeholder: str) -> str:
        """获取输入框的值"""
        input_el = self.page.get_by_label(label_or_placeholder).first
        if input_el.is_visible():
            return input_el.input_value()
        return ""

    def clear_input(self, label_or_placeholder: str):
        """清空输入框"""
        input_el = self.page.get_by_label(label_or_placeholder).first
        if input_el.is_visible():
            input_el.clear()

    def select_option(self, label_or_placeholder: str, option_text: str):
        """选择下拉选项"""
        select_el = self.page.get_by_label(label_or_placeholder).first
        if select_el.is_visible():
            select_el.select_option(label=option_text)

    def check_checkbox(self, label: str, checked: bool = True):
        """勾选/取消复选框"""
        checkbox = self.page.get_by_label(label).first
        if checkbox.is_visible():
            if checked:
                checkbox.check()
            else:
                checkbox.uncheck()

    def is_checkbox_checked(self, label: str) -> bool:
        """复选框是否已勾选"""
        checkbox = self.page.get_by_label(label).first
        return checkbox.is_checked() if checkbox.is_visible() else False

    def upload_file(self, label: str, file_path: str):
        """上传文件"""
        upload_el = self.page.get_by_label(label).first
        if upload_el.is_visible():
            upload_el.set_input_files(file_path)

    # ======== 按钮操作 ========

    def click_submit(self):
        """点击提交按钮"""
        btn = self.page.locator(self.SUBMIT_BTN).first
        if btn.is_visible():
            btn.click()
            self.page.wait_for_load_state("networkidle")

    def click_reset(self):
        """点击重置按钮"""
        btn = self.page.locator(self.RESET_BTN).first
        if btn.is_visible():
            btn.click()
            self.page.wait_for_load_state("networkidle")

    def click_cancel(self):
        """点击取消按钮"""
        btn = self.page.locator(self.CANCEL_BTN).first
        if btn.is_visible():
            btn.click()
            self.page.wait_for_load_state("networkidle")

    # ======== 校验与错误 ========

    def has_errors(self) -> bool:
        """是否存在错误信息"""
        return self.page.locator(self.ERROR_MSG).first.is_visible()

    def get_error_messages(self) -> List[str]:
        """获取所有错误信息"""
        errors = self.page.query_selector_all(self.ERROR_MSG)
        return [e.inner_text().strip() for e in errors if e.inner_text().strip()]

    def get_field_error_count(self) -> int:
        """获取错误字段数量"""
        fields = self.page.query_selector_all(self.FIELD_ERROR)
        return len(fields)

    def has_success_message(self) -> bool:
        """是否存在成功消息"""
        return self.page.locator(self.SUCCESS_MSG).first.is_visible()

    def get_success_message(self) -> str:
        """获取成功消息文本"""
        msg = self.page.locator(self.SUCCESS_MSG).first
        return msg.inner_text().strip() if msg.is_visible() else ""

    def has_validation_summary(self) -> bool:
        """是否存在校验摘要"""
        return self.page.locator(self.VALIDATION_SUMMARY).first.is_visible()

    # ======== 表单字段元信息 ========

    def get_all_labels(self) -> List[str]:
        """获取所有标签文本"""
        labels = self.page.query_selector_all(self.LABEL)
        return [l.inner_text().strip() for l in labels if l.inner_text().strip()]

    def get_required_fields(self) -> List[str]:
        """获取所有必填字段标签"""
        required = self.page.locator(self.REQUIRED_MARK).all()
        required_labels = []
        for r in required:
            # 向上找最近的 label
            label = r.evaluate("el => el.closest('label')?.innerText?.trim() || ''")
            if label:
                required_labels.append(label)
        return required_labels

    def has_placeholder(self) -> bool:
        """输入框是否有 placeholder"""
        return self.page.locator(self.PLACEHOLDER).first.is_visible()

    def get_all_placeholders(self) -> List[str]:
        """获取所有 placeholder"""
        inputs = self.page.query_selector_all(self.PLACEHOLDER)
        return [
            inp.get_attribute("placeholder") or ""
            for inp in inputs
        ]

    # ======== 表单重置验证 ========

    def are_fields_cleared(self) -> bool:
        """所有字段是否已清空（重置后验证）"""
        inputs = self.page.query_selector_all(self.INPUT)
        for input_el in inputs:
            value = input_el.input_value()
            if value:
                return False
        return True

    # ======== 可访问性 ========

    def has_aria_describedby(self) -> bool:
        """字段是否有 aria-describedby"""
        inputs = self.page.query_selector_all(self.INPUT)
        for inp in inputs:
            if inp.get_attribute("aria-describedby"):
                return True
        return False

    def has_form_aria_label(self) -> bool:
        """表单是否有 aria-label 或 aria-labelledby"""
        form = self.page.locator(self.FORM).first
        return bool(
            form.get_attribute("aria-label")
            or form.get_attribute("aria-labelledby")
        )


