# =============================================================================
# 文件名: checkout_page.py
# 模块路径: ui/pages/front/checkout_page.py
# 作用: 结算页 Page Object，封装 /order/check 页面加载校验与元素探测
# 调用关系: 继承 BasePage；被 tests/ui/test_front_shop_ui.py、tests/e2e/* 调用
# 类型: 自定义（项目）
# 来源: E2E_demo 项目
# =============================================================================
# 导入 By，定义元素定位方式（第三方：selenium.webdriver.common.by → By）
from selenium.webdriver.common.by import By

# 导入 Page Object 基类（项目：ui/pages/base_page.py → BasePage）
from ui.pages.base_page import BasePage


# 结算页类：映射 /order/check 下单确认页（项目：ui/pages/front/checkout_page.py → FrontCheckoutPage）
class FrontCheckoutPage(BasePage):
    """结算页 /order/check。"""

    # 收货地址区域 XPath 定位（第三方：selenium → By.XPATH）
    ADDRESS_SECTION = (By.XPATH, "//*[contains(text(),'收货地址') or contains(text(),'地址')]")
    # “提交订单”按钮 XPath 定位（第三方：selenium → By.XPATH）
    SUBMIT_ORDER = (By.XPATH, "//button[contains(.,'提交订单')]")
    # 优惠券区域 XPath 定位（第三方：selenium → By.XPATH）
    COUPON_SECTION = (By.XPATH, "//*[contains(text(),'优惠券')]")

# 作用：定义函数/方法 open_checkout；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/front/checkout_page.py)
    def open_checkout(self) -> None:
        # 直接打开结算页（项目：ui/pages/base_page.py → BasePage.open）
        self.open("order/check")

# 作用：定义函数/方法 page_loaded；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/front/checkout_page.py)
    def page_loaded(self) -> bool:
        # 显式等待结算页渲染出关键文案，应对 SPA 异步渲染 + implicit_wait=0（项目：ui/pages/base_page.py → BasePage.wait_body_contains_any）
        return self.wait_body_contains_any(["结算", "提交订单", "收货"])

# 作用：定义函数/方法 has_coupon_section；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/front/checkout_page.py)
    def has_coupon_section(self) -> bool:
        # 查找优惠券相关元素，存在则返回 True（第三方：selenium → WebDriver.find_elements；Python 内置：bool）
        return bool(self.driver.find_elements(*self.COUPON_SECTION))

# 作用：定义函数/方法 submit_button_visible；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/front/checkout_page.py)
    def submit_button_visible(self) -> bool:
        # 查找提交订单按钮元素，存在则返回 True（第三方：selenium → WebDriver.find_elements；Python 内置：bool）
        return bool(self.driver.find_elements(*self.SUBMIT_ORDER))
