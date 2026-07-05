# =============================================================================
# 文件：tests/ui/test_front_home_ui.py
# 作用：Tigshop 前台首页、分类、搜索 UI 自动化用例（无需登录或使用 front_driver）
# 调用关系：pytest → front_driver/front_base_url/test_data → FrontHomePage → Selenium WebDriver
# 自定义/框架：自定义测试类 + pytest/allure + Selenium + POM
# 来源（项目 tests/ui 层，覆盖首页展示与搜索导航）
# =============================================================================
import allure  # 作用：导入 Allure 装饰器；调用关系：epic/feature/title；自定义/框架：框架(allure)；来源(第三方 allure)
import pytest  # 作用：导入 pytest；调用关系：mark.ui、mark.flaky；自定义/框架：框架(pytest)；来源(第三方 pytest)

from ui.pages.front.home_page import FrontHomePage  # 作用：导入前台首页页面对象；调用关系：各用例实例化 FrontHomePage；自定义/框架：自定义 POM；来源(ui/pages/front/home_page.py)


@allure.epic("Tigshop")  # 作用：Allure epic；调用关系：报告；自定义/框架：框架(allure)；来源(allure)
@allure.feature("UI-前台首页与列表")  # 作用：Allure feature 分组；调用关系：TestFrontHomeUi；自定义/框架：框架(allure)；来源(allure)
@pytest.mark.ui  # 作用：UI 层 pytest 标记；调用关系：-m ui；自定义/框架：框架(pytest)；来源(pytest)
@pytest.mark.flaky(reruns=2, reruns_delay=2)  # 作用：失败重跑 2 次，间隔 2 秒；调用关系：pytest-rerunfailures；自定义/框架：框架(插件)；来源(pytest-rerunfailures)
class TestFrontHomeUi:  # 作用：前台首页 UI 测试类；调用关系：pytest 收集；自定义/框架：自定义；来源(本文件)
    @allure.title("首页展示商品链接")  # 作用：Allure 标题；调用关系：test_home_product_links；自定义/框架：框架(allure)；来源(allure)
    def test_home_product_links(self, front_driver, front_base_url):  # 作用：首页至少有 1 个商品链接；调用关系：front_driver fixture、FrontHomePage；自定义/框架：自定义；来源(本文件)
        page = FrontHomePage(front_driver, front_base_url)  # 作用：构造首页 POM；调用关系：FrontHomePage.__init__；自定义/框架：自定义；来源(ui/pages/front/home_page.py)
        page.open_home()  # 作用：导航并等待首页加载；调用关系：FrontHomePage.open_home；自定义/框架：自定义；来源(ui/pages/front/home_page.py)
        assert page.product_link_count() >= 1  # 作用：断言商品链接数量 ≥1；调用关系：FrontHomePage.product_link_count；自定义/框架：自定义；来源(ui/pages/front/home_page.py)

    @allure.title("首页领券区块可见")  # 作用：Allure 标题；调用关系：test_home_coupon_section；自定义/框架：框架(allure)；来源(allure)
    def test_home_coupon_section(self, front_driver, front_base_url):  # 作用：验证领券区域可见；调用关系：FrontHomePage.has_coupon_section；自定义/框架：自定义；来源(本文件)
        page = FrontHomePage(front_driver, front_base_url)  # 作用：实例化首页 POM（front_driver 已打开基址）；调用关系：conftest front_driver；自定义/框架：自定义；来源(ui/pages/front/home_page.py)
        assert page.has_coupon_section()  # 作用：断言领券区块存在；调用关系：FrontHomePage 方法；自定义/框架：自定义；来源(ui/pages/front/home_page.py)

    @allure.title("分类商品列表页有商品")  # 作用：Allure 标题；调用关系：test_category_list；自定义/框架：框架(allure)；来源(allure)
    def test_category_list(self, front_driver, front_base_url):  # 作用：分类 ID=1 列表页有商品；调用关系：open_category_list；自定义/框架：自定义；来源(本文件)
        page = FrontHomePage(front_driver, front_base_url)  # 作用：构造首页 POM；调用关系：FrontHomePage；自定义/框架：自定义；来源(ui/pages/front/home_page.py)
        page.open_category_list(category_id=1)  # 作用：打开分类 1 商品列表；调用关系：FrontHomePage.open_category_list；自定义/框架：自定义；来源(ui/pages/front/home_page.py)
        assert page.category_has_products()  # 作用：断言分类页有商品；调用关系：FrontHomePage.category_has_products；自定义/框架：自定义；来源(ui/pages/front/home_page.py)

    @allure.title("搜索后进入搜索结果页")  # 作用：Allure 标题；调用关系：test_search_results；自定义/框架：框架(allure)；来源(allure)
    def test_search_results(self, front_driver, front_base_url, test_data):  # 作用：搜索后 URL 含 search；调用关系：page.search、test_data keyword；自定义/框架：自定义；来源(本文件)
        page = FrontHomePage(front_driver, front_base_url)  # 作用：实例化首页 POM；调用关系：FrontHomePage；自定义/框架：自定义；来源(ui/pages/front/home_page.py)
        page.search(test_data["keyword"])  # 作用：输入关键词并提交搜索；调用关系：FrontHomePage.search、test_data；自定义/框架：自定义；来源(ui/pages/front/home_page.py)
        assert "search" in page.current_url  # 作用：断言当前 URL 包含 search；调用关系：BasePage.current_url 属性；自定义/框架：自定义；来源(ui/pages/base_page.py)
