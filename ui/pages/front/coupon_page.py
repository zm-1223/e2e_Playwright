# =============================================================================
# 文件名: coupon_page.py
# 模块路径: ui/pages/front/coupon_page.py
# 作用: 前台优惠券 Page Object，封装集券中心与我的优惠券页面
# 调用关系: 继承 BasePage；被 tests/ui/test_front_shop_ui.py 等测试调用
# 类型: 自定义（项目）
# 来源: E2E_demo 项目
# =============================================================================
# 导入 By，定义元素定位方式（第三方：selenium.webdriver.common.by → By）
from selenium.webdriver.common.by import By

# 导入 Page Object 基类（项目：ui/pages/base_page.py → BasePage）
from ui.pages.base_page import BasePage


# 优惠券页类：映射 /coupon/list 与 /member/coupon/list（项目：ui/pages/front/coupon_page.py → FrontCouponPage）
class FrontCouponPage(BasePage):
    """优惠券：集券中心 /coupon/list 与我的优惠券 /member/coupon/list。"""

    # 优惠券卡片列表容器定位元组（第三方：selenium → By.CSS_SELECTOR）
    COUPON_LIST = (By.CSS_SELECTOR, ".coupon-card-list, .container.coupon-list, .coupon_list")
    # “马上领/再次领取”按钮 XPath 定位（第三方：selenium → By.XPATH）
    CLAIM_BTN = (By.XPATH, "//button[contains(.,'马上领') or contains(.,'再次领取')]")
    # 页面标题/集券中心文案 XPath 定位（第三方：selenium → By.XPATH）
    PAGE_TITLE = (By.XPATH, "//*[contains(text(),'集券中心') or contains(text(),'优惠券')]")

# 作用：定义函数/方法 open_coupon_center；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/front/coupon_page.py)
    def open_coupon_center(self) -> None:
        # 打开集券中心 /coupon/list（项目：ui/pages/base_page.py → BasePage.open）
        self.open("coupon/list")

# 作用：定义函数/方法 open_my_coupons；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/front/coupon_page.py)
    def open_my_coupons(self) -> None:
        # 打开我的优惠券 /member/coupon/list（项目：ui/pages/base_page.py → BasePage.open）
        self.open("member/coupon/list")

# 作用：定义函数/方法 coupon_center_loaded；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/front/coupon_page.py)
    def coupon_center_loaded(self) -> bool:
        # 进入集券中心（项目：ui/pages/front/coupon_page.py → FrontCouponPage.open_coupon_center）
        self.open_coupon_center()
        # 显式等待优惠券列表或页面标题渲染后判断，应对 SPA 异步渲染（项目：ui/pages/base_page.py → BasePage.elements_present）
        return bool(self.elements_present(*self.COUPON_LIST)) or self.wait_body_contains_any(
            ["集券中心", "优惠券"]
        )

# 作用：定义函数/方法 my_coupons_loaded；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/front/coupon_page.py)
    def my_coupons_loaded(self) -> bool:
        # 打开我的优惠券页（项目：ui/pages/front/coupon_page.py → FrontCouponPage.open_my_coupons）
        self.open_my_coupons()
        # 显式等待 body 出现"优惠券"文案，应对 SPA 异步渲染（项目：ui/pages/base_page.py → BasePage.wait_body_contains_any）
        return self.wait_body_contains_any(["优惠券"])

# 作用：定义函数/方法 claim_button_count；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/front/coupon_page.py)
    def claim_button_count(self) -> int:
        # 打开集券中心（项目：ui/pages/front/coupon_page.py → FrontCouponPage.open_coupon_center）
        self.open_coupon_center()
        # 统计可领取按钮数量（第三方：selenium → WebDriver.find_elements；Python 内置：len）
        return len(self.driver.find_elements(*self.CLAIM_BTN))
