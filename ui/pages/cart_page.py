# 从 Selenium 导入 By，用于按标签名等方式定位元素（第三方：selenium.webdriver.common.by → By）
from selenium.webdriver.common.by import By
# 从基类页面对象导入 BasePage（项目：ui/pages/base_page.py → BasePage）
from ui.pages.base_page import BasePage


# 购物车页 Page Object（项目：ui/pages/cart_page.py → CartPage）
class CartPage(BasePage):
    """购物车页。"""

    # 购物车页面的 URL 路径（相对路径）（项目：ui/pages/cart_page.py → CartPage.PATH）
    PATH = "checkout/cart"

    def open_cart(self) -> None:
        """打开购物车。"""
        # 打开 checkout/cart 对应的购物车页面（项目：ui/pages/base_page.py → BasePage.open）
        self.open(self.PATH)

    def has_items(self) -> bool:
        """购物车是否有商品（简单判断页面文本）。"""
        # 获取整个 body 的可见文本，并转为小写便于比较（第三方：selenium → WebDriver.find_element, WebElement.text）
        body = self.driver.find_element(By.TAG_NAME, "body").text.lower()  # 转小写（Python 内置：str.lower）
        # 若页面不含 "empty" 且含 "cart"，认为购物车非空（Python 内置：in, and）
        return "empty" not in body and "cart" in body
