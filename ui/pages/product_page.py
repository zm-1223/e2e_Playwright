# 从 Selenium 导入 By，用于指定 CSS 选择器等定位方式（第三方：selenium.webdriver.common.by → By）
from selenium.webdriver.common.by import By
# 从本项目的基类页面对象导入 BasePage，复用通用操作方法（项目：ui/pages/base_page.py → BasePage）
from ui.pages.base_page import BasePage


# 商品详情页 Page Object（项目：ui/pages/product_page.py → ProductPage）
class ProductPage(BasePage):
    """商品详情页。"""

    # 商品标题元素：优先匹配 data-test 属性，否则匹配 h1 标签（第三方：selenium.webdriver.common.by → By.CSS_SELECTOR）
    PRODUCT_TITLE = (By.CSS_SELECTOR, "[data-test='product-name'], h1")
    # “加入购物车”按钮（第三方：selenium.webdriver.common.by → By.CSS_SELECTOR）
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, "[data-test='add-to-cart']")
    # 导航栏中的“购物车”入口（第三方：selenium.webdriver.common.by → By.CSS_SELECTOR）
    NAV_CART = (By.CSS_SELECTOR, "[data-test='nav-cart']")

    def open_product(self, product_id: str) -> None:
        # 根据商品 ID 打开对应详情页，例如 product/123（项目：ui/pages/base_page.py → BasePage.open）
        self.open(f"product/{product_id}")  # 拼接商品详情路径（Python 内置：f-string）

    def get_product_title(self) -> str:
        # 读取并返回页面上显示的商品名称文本（项目：ui/pages/base_page.py → BasePage.get_text）
        return self.get_text(*self.PRODUCT_TITLE)

    def add_to_cart(self) -> None:
        # 点击“加入购物车”按钮（项目：ui/pages/base_page.py → BasePage.click）
        self.click(*self.ADD_TO_CART_BTN)

    def go_to_cart(self) -> None:
        # 通过导航栏进入购物车页面（项目：ui/pages/base_page.py → BasePage.click）
        self.click(*self.NAV_CART)
