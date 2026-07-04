# 从 Selenium 导入 By（本类暂未直接使用，保留以便后续扩展定位器）（第三方：selenium.webdriver.common.by → By）
from selenium.webdriver.common.by import By
# 从基类页面对象导入 BasePage（项目：ui/pages/base_page.py → BasePage）
from ui.pages.base_page import BasePage


# 商品搜索 Page Object（项目：ui/pages/search_page.py → SearchPage）
class SearchPage(BasePage):
    """商品搜索（通过 API 获取商品 ID 后打开详情页）。"""

    def open_product_by_id(self, product_id: str) -> None:
        """打开商品详情页。"""
        # 已知商品 ID 时，直接打开 product/{id} 详情页（项目：ui/pages/base_page.py → BasePage.open）
        self.open(f"product/{product_id}")  # 拼接商品详情路径（Python 内置：f-string）
