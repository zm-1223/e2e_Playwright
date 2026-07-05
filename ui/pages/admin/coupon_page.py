# =============================================================================
# 文件名: coupon_page.py
# 模块路径: ui/pages/admin/coupon_page.py
# 作用: 后台优惠券管理 Page Object，封装 /admin/promotion/coupon/list 页面
# 调用关系: 继承 BasePage；被 tests/ui/test_admin_ui.py 调用
# 类型: 自定义（项目）
# 来源: E2E_demo 项目
# =============================================================================
# 导入 By，定义元素定位方式（第三方：selenium.webdriver.common.by → By）
from selenium.webdriver.common.by import By

# 导入 Page Object 基类（项目：ui/pages/base_page.py → BasePage）
from ui.pages.base_page import BasePage


# 后台优惠券管理页类：映射 promotion/coupon/list（项目：ui/pages/admin/coupon_page.py → AdminCouponPage）
class AdminCouponPage(BasePage):
    """后台优惠券管理 /admin/promotion/coupon/list。"""

    # 优惠券数据表格定位元组，兼容 Element Plus 表格与普通 table（第三方：selenium → By.CSS_SELECTOR）
    TABLE = (By.CSS_SELECTOR, ".el-table, table")
    # 表格数据行定位元组（第三方：selenium → By.CSS_SELECTOR）
    TABLE_ROW = (By.CSS_SELECTOR, ".el-table__row, tbody tr")
    # 页面标题/“优惠券”文案 XPath 定位（第三方：selenium → By.XPATH）
    PAGE_HEADER = (By.XPATH, "//*[contains(text(),'优惠券')]")

# 作用：定义函数/方法 open_coupon_list；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/admin/coupon_page.py)
    def open_coupon_list(self) -> None:
        # 打开后台优惠券列表页（项目：ui/pages/base_page.py → BasePage.open）
        self.open("promotion/coupon/list")

# 作用：定义函数/方法 coupon_page_loaded；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/admin/coupon_page.py)
    def coupon_page_loaded(self) -> bool:
        # 导航到优惠券列表（项目：ui/pages/admin/coupon_page.py → AdminCouponPage.open_coupon_list）
        self.open_coupon_list()
        # 存在页面标题或表格元素则视为加载成功（第三方：selenium → find_elements；Python 内置：bool, or）
        return bool(self.driver.find_elements(*self.PAGE_HEADER)) or bool(
# 作用：定位 DOM 元素；调用关系：Selenium WebDriver；自定义/框架：框架(Selenium)；来源(selenium)
            self.driver.find_elements(*self.TABLE)
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(ui/pages/admin/coupon_page.py)
        )

# 作用：定义函数/方法 table_row_count；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/admin/coupon_page.py)
    def table_row_count(self) -> int:
        # 打开优惠券列表页（项目：ui/pages/admin/coupon_page.py → AdminCouponPage.open_coupon_list）
        self.open_coupon_list()
        # 统计表格行数并返回（第三方：selenium → WebDriver.find_elements；Python 内置：len）
        return len(self.driver.find_elements(*self.TABLE_ROW))
