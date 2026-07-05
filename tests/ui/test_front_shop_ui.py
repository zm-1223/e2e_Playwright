# =============================================================================
# 文件：tests/ui/test_front_shop_ui.py
# 作用：Tigshop 前台购物流程 UI 用例（商品详情、加购、购物车、结算）
# 调用关系：pytest → buyer_driver/front_*_page/test_data → FrontProductPage 等 POM → Selenium
# 自定义/框架：自定义测试类 + pytest/allure/Selenium By + POM fixture
# 来源（项目 tests/ui 层，覆盖买家登录后购物流程页面）
# =============================================================================
import allure  # 作用：导入 Allure 装饰器；调用关系：epic/feature/title；自定义/框架：框架(allure)；来源(第三方 allure)
import pytest  # 作用：导入 pytest；调用关系：mark.ui、mark.flaky；自定义/框架：框架(pytest)；来源(第三方 pytest)
from selenium.webdriver.common.by import By  # 作用：导入 Selenium 定位枚举 By；调用关系：find_element(By.TAG_NAME)；自定义/框架：框架(Selenium)；来源(第三方 selenium)

from ui.pages.front.product_page import FrontProductPage  # 作用：导入商品详情页 POM；调用关系：test_product_* 用例；自定义/框架：自定义；来源(ui/pages/front/product_page.py)


@allure.epic("Tigshop")  # 作用：Allure epic；调用关系：报告；自定义/框架：框架(allure)；来源(allure)
@allure.feature("UI-前台购物流程")  # 作用：Allure feature；调用关系：TestFrontShopUi；自定义/框架：框架(allure)；来源(allure)
@pytest.mark.ui  # 作用：UI 层标记；调用关系：pytest -m ui；自定义/框架：框架(pytest)；来源(pytest)
@pytest.mark.flaky(reruns=2, reruns_delay=2)  # 作用：UI  flaky 重跑 2 次；调用关系：pytest-rerunfailures；自定义/框架：框架(插件)；来源(pytest-rerunfailures)
class TestFrontShopUi:  # 作用：前台购物流程 UI 测试类；调用关系：pytest 收集；自定义/框架：自定义；来源(本文件)
    @allure.title("商品详情页标题可见")  # 作用：Allure 标题；调用关系：test_product_detail_display；自定义/框架：框架(allure)；来源(allure)
    def test_product_detail_display(self, buyer_driver, front_base_url, test_data):  # 作用：打开默认商品详情页标题可见；调用关系：buyer_driver、FrontProductPage；自定义/框架：自定义；来源(本文件)
        page = FrontProductPage(buyer_driver, front_base_url)  # 作用：构造商品页 POM（已登录 driver）；调用关系：FrontProductPage.__init__；自定义/框架：自定义；来源(ui/pages/front/product_page.py)
        page.open_product(test_data["product_id"])  # 作用：导航至指定商品 ID 详情；调用关系：FrontProductPage.open_product、test_data；自定义/框架：自定义；来源(ui/pages/front/product_page.py)
        assert page.title_visible()  # 作用：断言商品标题元素可见；调用关系：FrontProductPage.title_visible；自定义/框架：自定义；来源(ui/pages/front/product_page.py)

    @allure.title("商品页点击加入购物车")  # 作用：Allure 标题；调用关系：test_add_to_cart_button；自定义/框架：框架(allure)；来源(allure)
    def test_add_to_cart_button(self, buyer_driver, front_base_url, test_data):  # 作用：点击加购后页面有成功反馈；调用关系：add_to_cart、body 文本断言；自定义/框架：自定义；来源(本文件)
        page = FrontProductPage(buyer_driver, front_base_url)  # 作用：实例化商品页 POM；调用关系：FrontProductPage；自定义/框架：自定义；来源(ui/pages/front/product_page.py)
        page.open_product(test_data["product_id"])  # 作用：打开测试商品；调用关系：open_product；自定义/框架：自定义；来源(ui/pages/front/product_page.py)
        page.add_to_cart()  # 作用：点击加入购物车按钮；调用关系：FrontProductPage.add_to_cart；自定义/框架：自定义；来源(ui/pages/front/product_page.py)
        body = buyer_driver.find_element(By.TAG_NAME, "body").text  # 作用：读取页面 body 全文用于断言；调用关系：Selenium find_element、By.TAG_NAME；自定义/框架：框架(Selenium)；来源(selenium)
        assert "购物车" in body or "成功" in body or "cart" in buyer_driver.current_url.lower()  # 作用：断言加购成功提示或跳转购物车；调用关系：driver.current_url；自定义/框架：自定义；来源(本文件)

    @allure.title("购物车页面可打开")  # 作用：Allure 标题；调用关系：test_cart_page_display；自定义/框架：框架(allure)；来源(allure)
    def test_cart_page_display(self, front_cart_page):  # 作用：验证购物车页有内容；调用关系：conftest front_cart_page fixture；自定义/框架：自定义；来源(本文件)
        assert front_cart_page.has_cart_content()  # 作用：断言购物车页加载且有内容区域；调用关系：FrontCartPage.has_cart_content；自定义/框架：自定义；来源(ui/pages/front/cart_page.py)

    @allure.title("结算页展示提交订单区域")  # 作用：Allure 标题；调用关系：test_checkout_page_display；自定义/框架：框架(allure)；来源(allure)
    def test_checkout_page_display(self, front_checkout_page):  # 作用：结算页加载且提交按钮可见；调用关系：front_checkout_page fixture；自定义/框架：自定义；来源(本文件)
        front_checkout_page.open_checkout()  # 作用：导航至结算页；调用关系：FrontCheckoutPage.open_checkout；自定义/框架：自定义；来源(ui/pages/front/checkout_page.py)
        assert front_checkout_page.page_loaded()  # 作用：断言结算页主区域已加载；调用关系：FrontCheckoutPage.page_loaded；自定义/框架：自定义；来源(ui/pages/front/checkout_page.py)
        assert front_checkout_page.submit_button_visible()  # 作用：断言提交订单按钮可见；调用关系：FrontCheckoutPage.submit_button_visible；自定义/框架：自定义；来源(ui/pages/front/checkout_page.py)
