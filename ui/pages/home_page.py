# 从 Selenium 导入 By，用于 CSS 选择器等定位方式（第三方：selenium.webdriver.common.by → By）
from selenium.webdriver.common.by import By
# 从基类页面对象导入 BasePage（项目：ui/pages/base_page.py → BasePage）
from ui.pages.base_page import BasePage


# 首页 Page Object（项目：ui/pages/home_page.py → HomePage）
class HomePage(BasePage):
    """首页。"""

    # 导航栏“首页”链接（第三方：selenium.webdriver.common.by → By.CSS_SELECTOR）
    NAV_HOME = (By.CSS_SELECTOR, "[data-test='nav-home']")
    # 导航栏“我的账户”链接（登录后可见）（第三方：selenium.webdriver.common.by → By.CSS_SELECTOR）
    NAV_MY_ACCOUNT = (By.CSS_SELECTOR, "[data-test='nav-my-account']")

    def open_home(self) -> None:
        """打开首页。"""
        # 传入空路径，open() 会只打开 base_url（站点根地址）（项目：ui/pages/base_page.py → BasePage.open）
        self.open("")

    def is_logged_in(self) -> bool:
        """是否已登录。"""
        # 若页面上存在“我的账户”导航元素，则认为已登录（第三方：selenium → WebDriver.find_elements）
        return bool(self.driver.find_elements(*self.NAV_MY_ACCOUNT))  # 转为布尔值（Python 内置：bool）
