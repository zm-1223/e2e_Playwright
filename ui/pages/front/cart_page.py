# =============================================================================
# 文件名: cart_page.py
# 模块路径: ui/pages/front/cart_page.py
# 作用: 购物车页 Page Object，封装打开购物车、校验内容、去结算
# 调用关系: 继承 BasePage；被 tests/ui/test_front_shop_ui.py、tests/e2e/* 调用
# 类型: 自定义（项目）
# 来源: E2E_demo 项目
# =============================================================================
# 导入 By，定义元素定位方式（第三方：selenium.webdriver.common.by → By）
from selenium.webdriver.common.by import By

# 导入 Page Object 基类（项目：ui/pages/base_page.py → BasePage）
from ui.pages.base_page import BasePage


# 购物车页类：映射 /cart 页面（项目：ui/pages/front/cart_page.py → FrontCartPage）
class FrontCartPage(BasePage):
    """购物车页 /cart。"""

    # 购物车主容器定位元组，兼容多种布局 class（第三方：selenium → By.CSS_SELECTOR）
    CART_CONTAINER = (By.CSS_SELECTOR, ".cart-list, .cart-box, .cart-main, .container")
    # “去结算”按钮 XPath 定位（第三方：selenium → By.XPATH）
    CHECKOUT_BTN = (By.XPATH, "//button[contains(.,'去结算') or contains(.,'结算')]")
    # 购物车商品行定位元组（第三方：selenium → By.CSS_SELECTOR）
    CART_ITEM = (By.CSS_SELECTOR, ".cart-item, .goods-item, tr")

# 作用：定义函数/方法 open_cart；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/front/cart_page.py)
    def open_cart(self) -> None:
        # 导航到购物车页 /cart（项目：ui/pages/base_page.py → BasePage.open）
        self.open("cart")

# 作用：定义函数/方法 has_cart_content；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/front/cart_page.py)
    def has_cart_content(self) -> bool:
        # 打开购物车页（项目：ui/pages/front/cart_page.py → FrontCartPage.open_cart）
        self.open_cart()
        # 获取 body 元素的全部可见文本（第三方：selenium → WebDriver.find_element, WebElement.text）
        body = self.driver.find_element(By.TAG_NAME, "body").text
        # 页面含“购物车”文案或存在商品行元素则视为有内容（Python 内置：in, len；第三方：selenium → find_elements）
        return "购物车" in body or len(self.driver.find_elements(*self.CART_ITEM)) > 0

# 作用：定义函数/方法 go_checkout；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/front/cart_page.py)
    def go_checkout(self) -> None:
        # 打开购物车页（项目：ui/pages/front/cart_page.py → FrontCartPage.open_cart）
        self.open_cart()
        # 点击“去结算”按钮（项目：ui/pages/base_page.py → BasePage.click）
        self.click(*self.CHECKOUT_BTN)
        # 等待跳转到结算页 order/check（项目：ui/pages/base_page.py → BasePage.wait_url_contains）
        self.wait_url_contains("order/check")
