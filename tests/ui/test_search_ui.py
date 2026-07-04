# =============================================================================（项目：tests/ui/test_search_ui.py → 章节分隔）
# tests/ui/test_search_ui.py — UI 层搜索与商品页测试（项目：tests/ui/test_search_ui.py → 模块说明）
# 作用：通过 Selenium 驱动浏览器，验证登录导航、商品页展示与加购等界面行为（第三方：selenium → WebDriver）
# =============================================================================（项目：tests/ui/test_search_ui.py → 章节分隔）

# 导入 pytest：测试框架（第三方：pytest → fixture/mark）
import pytest
# 导入 allure：Allure 报告装饰（第三方：allure → epic/feature/title）
import allure
# 导入 By：Selenium 定位策略枚举（ID、CSS、XPath 等）（第三方：selenium → By）
from selenium.webdriver.common.by import By
# 导入 WebDriverWait：显式等待，在超时前轮询直到条件满足（第三方：selenium → WebDriverWait）
from selenium.webdriver.support.ui import WebDriverWait
# 导入 expected_conditions 并简写为 EC：预置的等待条件（如元素出现、可点击）（第三方：selenium → expected_conditions）
from selenium.webdriver.support import expected_conditions as EC


# Allure epic（第三方：allure → epic）
@allure.epic("Practice Software Testing")
# Allure feature：UI 搜索与商品相关（第三方：allure → feature）
@allure.feature("UI 搜索与商品")
# pytest 标记：UI 层测试（可用 pytest -m ui 筛选）（第三方：pytest → mark.ui）
@pytest.mark.ui
# flaky：失败时自动重跑，reruns=2 最多重试 2 次，reruns_delay=2 每次间隔 2 秒（第三方：pytest → mark.flaky）
# UI 测试易受网络/渲染影响，重试可提高稳定性（项目：tests/ui/ → UI 稳定性策略）
@pytest.mark.flaky(reruns=2, reruns_delay=2)
class TestSearchUi:
    """UI 搜索与商品页测试。"""

    # 冒烟测试：快速验证核心路径（登录后导航可见）（第三方：pytest → mark.smoke）
    @allure.title("已登录用户可见账户导航")
    @pytest.mark.smoke
    # authenticated_driver：已登录的 WebDriver 实例（conftest 中完成登录）（项目：tests/conftest.py → authenticated_driver）
    def test_logged_in_nav_visible(self, authenticated_driver):
        # WebDriverWait(driver, 15)：最多等待 15 秒（第三方：selenium → WebDriverWait）
        # until(EC.presence_of_element_located(...))：直到 DOM 中出现指定元素（第三方：selenium → expected_conditions）
        WebDriverWait(authenticated_driver, 15).until(
            # CSS 选择器定位 data-test='nav-my-account' 的导航元素（第三方：selenium → By.CSS_SELECTOR）
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='nav-my-account']"))
        )
        # 若超时未找到元素，WebDriverWait 会抛异常，测试失败（第三方：selenium → TimeoutException）

    # 用例：打开商品详情页并加入购物车（第三方：allure → title）
    @allure.title("打开商品页并加购")
    # product_page：商品页 Page Object，封装页面操作（项目：tests/conftest.py → product_page）
    # first_product：API 或 Fixture 提供的商品数据（项目：tests/conftest.py → first_product）
    def test_product_page_add_to_cart(self, product_page, first_product):
        # 通过 Page Object 打开指定 id 的商品页（项目：ui/pages/product_page.py → open_product）
        product_page.open_product(first_product["id"])
        # 读取页面上显示的商品标题文本（项目：ui/pages/product_page.py → get_product_title）
        title = product_page.get_product_title()
        # 取商品名第一个单词（忽略大小写）应出现在页面标题中，验证打开的是正确商品（Python 内置：str.split/lower）
        assert first_product["name"].split()[0].lower() in title.lower()
        # 点击加购按钮（或等价操作）（项目：ui/pages/product_page.py → add_to_cart）
        product_page.add_to_cart()
