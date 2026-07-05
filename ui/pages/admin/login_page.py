# =============================================================================
# 文件名: login_page.py
# 模块路径: ui/pages/admin/login_page.py
# 作用: 后台管理员登录页 Page Object，封装 /admin/login/index 登录流程
# 调用关系: 继承 BasePage；被 utils/ui_auth.py、tests/conftest.py admin_logged_in_driver 调用
# 类型: 自定义（项目）
# 来源: E2E_demo 项目
# =============================================================================
# 导入 By，定义元素定位方式（第三方：selenium.webdriver.common.by → By）
from selenium.webdriver.common.by import By

# 导入 Page Object 基类（项目：ui/pages/base_page.py → BasePage）
from ui.pages.base_page import BasePage
# 操作后短暂稳定延迟（项目：utils/wait_helper.py → stable_delay）
from utils.wait_helper import stable_delay


# 后台登录页类：映射 Tigshop 管理后台登录界面（项目：ui/pages/admin/login_page.py → AdminLoginPage）
class AdminLoginPage(BasePage):
    # 类文档：说明本 POM 对应的后台登录路由（Python 内置：docstring）
    """后台登录 /admin/login/index。"""

    # 管理员用户名输入框定位元组（第三方：selenium → By.CSS_SELECTOR）
    USERNAME = (By.CSS_SELECTOR, "input.el-input__inner[placeholder='请输入用户名']")
    # 管理员密码输入框定位元组（第三方：selenium → By.CSS_SELECTOR）
    PASSWORD = (By.CSS_SELECTOR, "input.el-input__inner[placeholder='请输入密码']")
    # 登录提交按钮定位元组（第三方：selenium → By.CSS_SELECTOR）
    SUBMIT = (By.CSS_SELECTOR, "button.login-submit-btn")
    # 登录页欢迎标题 h1 定位，用于断言登录页可见（第三方：selenium → By.XPATH）
    HEADING = (By.XPATH, "//h1[contains(.,'欢迎登录商城后台管理系统')]")
    # 服务协议/隐私协议复选框定位元组（第三方：selenium → By.XPATH）
    AGREE_CHECKBOX = (
        By.XPATH,  # 定位方式：XPath（第三方：selenium → By.XPATH）
        "//label[contains(@class,'el-checkbox')][.//*[contains(.,'我已阅读并同意') or contains(.,'服务协议')]]",  # 选择器：协议复选框
    )

    # 点击登录前自动勾选服务协议与隐私协议（项目：ui/pages/admin/login_page.py → _ensure_agreement_checked）
    def _ensure_agreement_checked(self) -> None:
        # 方法文档：说明勾选目的（Python 内置：docstring）
        """点击登录前勾选「我已阅读并同意《服务协议》和《隐私协议》」。"""
        # 关闭遮挡弹窗（项目：utils/popup_handler.py → PopupHandler.dismiss_all）
        self.popup.dismiss_all()
        # 查找所有协议复选框候选元素（第三方：selenium → WebDriver.find_elements）
        for checkbox in self.driver.find_elements(*self.AGREE_CHECKBOX):
            # 跳过不可见复选框（第三方：selenium → WebElement.is_displayed）
            if not checkbox.is_displayed():
                continue  # 尝试下一个（Python 内置：continue）
            # 已勾选则无需重复操作（第三方：selenium → get_attribute）
            if "is-checked" in (checkbox.get_attribute("class") or ""):
                return  # 直接返回（Python 内置：return）
            # 点击勾选协议（第三方：selenium → WebElement.click）
            checkbox.click()
            # 等待 UI 状态稳定（项目：utils/wait_helper.py → stable_delay）
            stable_delay()
            return  # 勾选完成（Python 内置：return）

    # 打开后台登录页（项目：ui/pages/admin/login_page.py → open_login）
    def open_login(self) -> None:
        # 打开 login/index 并设置登录后 redirect 到后台首页（项目：ui/pages/base_page.py → BasePage.open）
        self.open("login/index?redirect=/")

    # 后台完整登录流程（项目：ui/pages/admin/login_page.py → login）
    def login(self, username: str, password: str) -> None:
        # 导航到登录页（项目：ui/pages/admin/login_page.py → AdminLoginPage.open_login）
        self.open_login()
        # 等待用户名输入框可见（项目：ui/pages/base_page.py → BasePage.find）
        self.find(*self.USERNAME)
        # 输入管理员用户名（项目：ui/pages/base_page.py → BasePage.input_text）
        self.input_text(*self.USERNAME, username)
        # 输入管理员密码（项目：ui/pages/base_page.py → BasePage.input_text）
        self.input_text(*self.PASSWORD, password)
        # 勾选服务协议与隐私协议（项目：ui/pages/admin/login_page.py → _ensure_agreement_checked）
        self._ensure_agreement_checked()
        # 等待提交按钮可点击（项目：ui/pages/base_page.py → BasePage.find_clickable）
        self.find_clickable(*self.SUBMIT)
        # 点击登录按钮（项目：ui/pages/base_page.py → BasePage.click）
        self.click(*self.SUBMIT)
        # 等待 URL 离开 /login，确认登录成功跳转（项目：ui/pages/base_page.py → BasePage.wait_url_not_contains）
        self.wait_url_not_contains("/login")

    # 断言后台登录页标题可见，供 test_admin_login_page 使用（项目：ui/pages/admin/login_page.py → login_page_visible）
    def login_page_visible(self) -> bool:
        # 打开登录页（项目：ui/pages/admin/login_page.py → AdminLoginPage.open_login）
        self.open_login()
        # 查找欢迎标题元素，存在则登录页可见（第三方：selenium → WebDriver.find_elements；Python 内置：bool）
        return bool(self.driver.find_elements(*self.HEADING))
