# =============================================================================
# 文件名: home_page.py
# 模块路径: ui/pages/front/home_page.py
# 作用: 前台首页 Page Object，封装首页打开、搜索、分类列表等操作
# 调用关系: 继承 BasePage；被 tests/ui/test_front_home_ui.py 等测试调用
# 类型: 自定义（项目）
# 来源: E2E_demo 项目
# =============================================================================
# 导入 By，定义元素定位方式（第三方：selenium.webdriver.common.by → By）
from selenium.webdriver.common.by import By
# 导入 Keys，模拟键盘按键（如 Enter）（第三方：selenium.webdriver.common.keys → Keys）
from selenium.webdriver.common.keys import Keys

# 导入 Page Object 基类（项目：ui/pages/base_page.py → BasePage）
from ui.pages.base_page import BasePage


# 前台首页类：映射 Tigshop 商城首页与搜索页（项目：ui/pages/front/home_page.py → FrontHomePage）
class FrontHomePage(BasePage):
    """前台首页与搜索。"""

    # 顶部搜索框定位元组（第三方：selenium → By.CSS_SELECTOR）
    SEARCH_INPUT = (By.CSS_SELECTOR, "input.search-input[name='keywords']")
    # 首页优惠券区块定位元组，兼容多种 DOM 结构（第三方：selenium → By.CSS_SELECTOR）
    COUPON_SECTION = (By.CSS_SELECTOR, ".mod_coupon, .coupon_list, .container.coupon-list")
    # 商品详情链接定位元组（第三方：selenium → By.CSS_SELECTOR）
    PRODUCT_LINK = (By.CSS_SELECTOR, "a[href*='/product/']")

# 作用：定义函数/方法 open_home；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/front/home_page.py)
    def open_home(self) -> None:
        # 打开站点根路径，即首页（项目：ui/pages/base_page.py → BasePage.open）
        self.open("")

# 作用：定义函数/方法 search；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/front/home_page.py)
    def search(self, keyword: str) -> None:
        # 先进入首页（项目：ui/pages/front/home_page.py → FrontHomePage.open_home）
        self.open_home()
        # 定位搜索输入框并等待可见（项目：ui/pages/base_page.py → BasePage.find）
        element = self.find(*self.SEARCH_INPUT)
        # 清空搜索框原有内容（第三方：selenium → WebElement.clear）
        element.clear()
        # 输入搜索关键词（第三方：selenium → WebElement.send_keys）
        element.send_keys(keyword)
        # 模拟按下 Enter 键触发搜索（第三方：selenium → Keys.ENTER）
        element.send_keys(Keys.ENTER)
        # 等待 URL 包含 search，确认进入搜索结果页（项目：ui/pages/base_page.py → BasePage.wait_url_contains）
        self.wait_url_contains("search")

# 作用：定义函数/方法 has_coupon_section；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/front/home_page.py)
    def has_coupon_section(self) -> bool:
        # 打开首页（项目：ui/pages/front/home_page.py → FrontHomePage.open_home）
        self.open_home()
        # 查找优惠券区块元素列表，非空则返回 True（第三方：selenium → WebDriver.find_elements）
        return bool(self.driver.find_elements(*self.COUPON_SECTION))

# 作用：定义函数/方法 product_link_count；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/front/home_page.py)
    def product_link_count(self) -> int:
        # 打开首页（项目：ui/pages/front/home_page.py → FrontHomePage.open_home）
        self.open_home()
        # 统计页面上商品链接数量并返回（第三方：selenium → WebDriver.find_elements；Python 内置：len）
        return len(self.driver.find_elements(*self.PRODUCT_LINK))

# 作用：定义函数/方法 open_category_list；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/front/home_page.py)
    def open_category_list(self, category_id: int = 1) -> None:
        # 打开指定分类的商品列表页（项目：ui/pages/base_page.py → BasePage.open）
        self.open(f"list?cat={category_id}")

# 作用：定义函数/方法 category_has_products；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/front/home_page.py)
    def category_has_products(self) -> bool:
        # 查找分类页中的商品链接，数量大于 0 表示有商品（第三方：selenium → WebDriver.find_elements；Python 内置：len）
        return len(self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/product/']")) > 0

# 作用：定义函数/方法 page_title_contains；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/front/home_page.py)
    def page_title_contains(self, text: str) -> bool:
        # 判断当前页面标题是否包含指定文本（项目：ui/pages/base_page.py → BasePage.title；Python 内置：in）
        return text in self.title
