# 从 Selenium 导入 By，用于 CSS 选择器定位（第三方：selenium.webdriver.common.by → By）
from selenium.webdriver.common.by import By
# 从基类页面对象导入 BasePage（项目：ui/pages/base_page.py → BasePage）
from ui.pages.base_page import BasePage


# 我的订单（Invoices）页 Page Object（项目：ui/pages/order_page.py → OrderPage）
class OrderPage(BasePage):
    """我的订单（Invoices）页。"""

    # 订单列表页的 URL 相对路径（项目：ui/pages/order_page.py → OrderPage.PATH）
    PATH = "account/invoices"
    # 导航栏“我的订单/发票”入口（第三方：selenium.webdriver.common.by → By.CSS_SELECTOR）
    NAV_INVOICES = (By.CSS_SELECTOR, "[data-test='nav-my-invoices']")

    def open_invoices(self) -> None:
        """打开订单列表页。"""
        # 直接通过 URL 打开 account/invoices 页面（项目：ui/pages/base_page.py → BasePage.open）
        self.open(self.PATH)

    def open_via_nav(self) -> None:
        """通过导航进入订单页。"""
        # 模拟用户点击导航栏中的订单入口（项目：ui/pages/base_page.py → BasePage.click）
        self.click(*self.NAV_INVOICES)

    def page_contains_invoice(self, invoice_number: str) -> bool:
        """页面是否包含指定订单号。"""
        # 读取 body 全文，判断指定订单号是否出现在页面文本中（第三方：selenium → WebDriver.find_element, WebElement.text）
        return invoice_number in self.driver.find_element(By.TAG_NAME, "body").text  # 成员检测（Python 内置：in）
