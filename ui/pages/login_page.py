# 从 Selenium 导入 By，用于元素定位（第三方：selenium.webdriver.common.by → By）
from selenium.webdriver.common.by import By
# 从基类页面对象导入 BasePage（项目：ui/pages/base_page.py → BasePage）
from ui.pages.base_page import BasePage


# 登录页 Page Object（项目：ui/pages/login_page.py → LoginPage）
class LoginPage(BasePage):
    """登录相关（本站点 UI 登录常遇 Cloudflare，测试以 Token 注入为主）。"""

    # 导航栏“我的账户”链接，登录成功后通常会出现（第三方：selenium.webdriver.common.by → By.CSS_SELECTOR）
    NAV_MY_ACCOUNT = (By.CSS_SELECTOR, "[data-test='nav-my-account']")
    # 导航栏“登录”链接（第三方：selenium.webdriver.common.by → By.CSS_SELECTOR）
    NAV_SIGN_IN = (By.CSS_SELECTOR, "[data-test='nav-sign-in']")

    def is_logged_in(self) -> bool:
        """检查导航栏是否显示 My Account。"""
        # find_elements 找不到时返回空列表；bool([]) 为 False，bool([元素]) 为 True（第三方：selenium → WebDriver.find_elements）
        return bool(self.driver.find_elements(*self.NAV_MY_ACCOUNT))  # 转为布尔值（Python 内置：bool）

    def open_login_page(self) -> None:
        """打开登录页。"""
        # 打开 auth/login 路径对应的登录页面（项目：ui/pages/base_page.py → BasePage.open）
        self.open("auth/login")
