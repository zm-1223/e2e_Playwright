# =============================================================================
# 文件名: login_page.py
# 模块路径: ui/pages/front/login_page.py
# 作用: 前台买家登录页 Page Object，封装 /member/login 的打开与登录流程
# 调用关系: 继承 BasePage；被 utils/ui_auth.py、tests/conftest.py buyer_driver 调用
# 类型: 自定义（项目）
# 来源: E2E_demo 项目
# =============================================================================
# 导入 By，定义 CSS/XPath 等定位方式（第三方：selenium.webdriver.common.by → By）
from selenium.webdriver.common.by import By

# 导入 Page Object 基类，复用 open/find/click 等通用方法（项目：ui/pages/base_page.py → BasePage）
from ui.pages.base_page import BasePage
# 操作后短暂稳定延迟，勾选协议后等待 DOM 稳定（项目：utils/wait_helper.py → stable_delay）
from utils.wait_helper import stable_delay


# 前台登录页类：映射 Tigshop 买家登录界面（项目：ui/pages/front/login_page.py → FrontLoginPage）
class FrontLoginPage(BasePage):
    # 类文档：说明本 POM 对应的路由路径（Python 内置：docstring）
    """前台买家登录页 /member/login。"""

    # 用户名输入框定位元组：(定位方式, 选择器)（第三方：selenium → By.CSS_SELECTOR）
    USERNAME = (By.CSS_SELECTOR, "input.el-input__inner[placeholder='用户名/手机/邮箱']")
    # 密码输入框定位元组（第三方：selenium → By.CSS_SELECTOR）
    PASSWORD = (By.CSS_SELECTOR, "input.el-input__inner[placeholder='密码']")
    # 登录提交按钮定位元组（第三方：selenium → By.CSS_SELECTOR）
    SUBMIT = (By.CSS_SELECTOR, "button.login_btn.submit_btn")
    # 服务协议/隐私协议复选框定位元组，匹配「我已阅读并同意…」文案（第三方：selenium → By.XPATH）
    AGREE_CHECKBOX = (
        By.XPATH,  # 定位方式：XPath（第三方：selenium → By.XPATH）
        "//label[contains(@class,'el-checkbox')][.//*[contains(.,'我已阅读并同意')]]",  # 选择器：Element Plus 协议复选框 label
    )

    # 点击登录前自动勾选服务协议与隐私协议（项目：ui/pages/front/login_page.py → _ensure_agreement_checked）
    def _ensure_agreement_checked(self) -> None:
        # 方法文档：说明勾选目的，避免登录按钮不可用（Python 内置：docstring）
        """点击登录前勾选「我已阅读并同意《服务协议》和《隐私协议》」。"""
        # 关闭 Cookie/广告弹窗，避免遮挡复选框（项目：utils/popup_handler.py → PopupHandler.dismiss_all）
        self.popup.dismiss_all()
        # 查找页面上所有协议复选框元素（第三方：selenium → WebDriver.find_elements）
        for checkbox in self.driver.find_elements(*self.AGREE_CHECKBOX):
            # 跳过不可见元素，避免点击失败（第三方：selenium → WebElement.is_displayed）
            if not checkbox.is_displayed():
                continue  # 继续下一个候选复选框（Python 内置：continue）
            # 若 label 已含 is-checked 类，表示已勾选，无需重复点击（第三方：selenium → get_attribute）
            if "is-checked" in (checkbox.get_attribute("class") or ""):
                return  # 已勾选则直接返回（Python 内置：return）
            # 点击 label 勾选协议（第三方：selenium → WebElement.click）
            checkbox.click()
            # 勾选后短暂等待，让 Element Plus 状态更新（项目：utils/wait_helper.py → stable_delay）
            stable_delay()
            return  # 成功勾选一个即可退出（Python 内置：return）

    # 打开买家登录页并指定登录成功后的跳转地址（项目：ui/pages/front/login_page.py → open_login）
    def open_login(self, return_url: str = "/member/index") -> None:
        # 导航至 /member/login 并携带 returnUrl 查询参数（项目：ui/pages/base_page.py → BasePage.open）
        self.open(f"member/login?returnUrl={return_url}")

    # 完整登录流程：填表 → 勾选协议 → 提交（项目：ui/pages/front/login_page.py → login）
    def login(self, username: str, password: str, return_url: str = "/member/index") -> None:
        # 第一步：导航到登录页（项目：ui/pages/front/login_page.py → FrontLoginPage.open_login）
        self.open_login(return_url)
        # 等待用户名输入框可见，确保页面渲染完成（项目：ui/pages/base_page.py → BasePage.find）
        self.find(*self.USERNAME)
        # 在用户名框输入账号（项目：ui/pages/base_page.py → BasePage.input_text）
        self.input_text(*self.USERNAME, username)
        # 在密码框输入密码（项目：ui/pages/base_page.py → BasePage.input_text）
        self.input_text(*self.PASSWORD, password)
        # 勾选服务协议与隐私协议，否则登录按钮可能不可用（项目：ui/pages/front/login_page.py → _ensure_agreement_checked）
        self._ensure_agreement_checked()
        # 等待提交按钮可点击（项目：ui/pages/base_page.py → BasePage.find_clickable）
        self.find_clickable(*self.SUBMIT)
        # 点击登录按钮提交表单（项目：ui/pages/base_page.py → BasePage.click）
        self.click(*self.SUBMIT)
        # 等待 URL 离开登录页，确认登录跳转成功（项目：ui/pages/base_page.py → BasePage.wait_url_not_contains）
        self.wait_url_not_contains("/member/login")

    # 判断当前是否已离开登录页（项目：ui/pages/front/login_page.py → is_logged_in）
    def is_logged_in(self) -> bool:
        # 当前 URL 不含 /member/login 则视为已登录（项目：ui/pages/base_page.py → BasePage.current_url）
        return "/member/login" not in self.current_url
