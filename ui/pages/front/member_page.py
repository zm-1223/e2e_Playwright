# =============================================================================
# 文件名: member_page.py
# 模块路径: ui/pages/front/member_page.py
# 作用: 个人中心 Page Object，封装会员首页、订单列表等页面操作
# 调用关系: 继承 BasePage；被 tests/ui/test_front_member_ui.py 调用
# 类型: 自定义（项目）
# 来源: E2E_demo 项目
# =============================================================================
# 导入 By，定义元素定位方式（第三方：selenium.webdriver.common.by → By）
from selenium.webdriver.common.by import By

# 导入 Page Object 基类（项目：ui/pages/base_page.py → BasePage）
from ui.pages.base_page import BasePage


# 个人中心页类：映射 /member/* 会员模块（项目：ui/pages/front/member_page.py → FrontMemberPage）
class FrontMemberPage(BasePage):
    """个人中心 /member/*。"""

    # 会员中心导航链接定位元组（第三方：selenium → By.CSS_SELECTOR）
    MEMBER_NAV = (By.CSS_SELECTOR, "a[href*='/member/']")
    # 用户名或典型会员页文案 XPath 定位（第三方：selenium → By.XPATH）
    USERNAME_TEXT = (By.XPATH, "//*[contains(text(),'123123') or contains(text(),'个人中心') or contains(text(),'我的订单')]")

# 作用：定义函数/方法 open_member_center；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/front/member_page.py)
    def open_member_center(self) -> None:
        # 打开会员中心首页 /member/index（项目：ui/pages/base_page.py → BasePage.open）
        self.open("member/index")

# 作用：定义函数/方法 open_orders；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/front/member_page.py)
    def open_orders(self) -> None:
        # 打开我的订单列表页（项目：ui/pages/base_page.py → BasePage.open）
        self.open("member/order/list")

# 作用：定义函数/方法 member_page_loaded；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/front/member_page.py)
    def member_page_loaded(self) -> bool:
        # 先进入会员中心（项目：ui/pages/front/member_page.py → FrontMemberPage.open_member_center）
        self.open_member_center()
        # 获取 body 文本（第三方：selenium → WebDriver.find_element, WebElement.text）
        body = self.driver.find_element(By.TAG_NAME, "body").text
        # 含“个人”“会员”或“订单”则视为会员页加载成功（Python 内置：in）
        return "个人" in body or "会员" in body or "订单" in body

# 作用：定义函数/方法 orders_page_loaded；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/front/member_page.py)
    def orders_page_loaded(self) -> bool:
        # 打开订单列表页（项目：ui/pages/front/member_page.py → FrontMemberPage.open_orders）
        self.open_orders()
        # 获取 body 文本（第三方：selenium → WebDriver.find_element, WebElement.text）
        body = self.driver.find_element(By.TAG_NAME, "body").text
        # 含“订单”则视为订单页加载成功（Python 内置：in）
        return "订单" in body

# 作用：定义函数/方法 nav_link_count；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/front/member_page.py)
    def nav_link_count(self) -> int:
        # 打开会员中心（项目：ui/pages/front/member_page.py → FrontMemberPage.open_member_center）
        self.open_member_center()
        # 统计会员导航链接数量（第三方：selenium → WebDriver.find_elements；Python 内置：len）
        return len(self.driver.find_elements(*self.MEMBER_NAV))
