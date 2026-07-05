# =============================================================================
# 文件：tests/e2e/test_front_purchase_e2e.py
# 作用：Tigshop 前台完整购物流程 E2E（搜索→详情→加购→购物车→结算，UI+API 混合断言）
# 调用关系：pytest → buyer_driver + API clients + POM → sync_browser_token_to_clients 桥接
# 自定义/框架：自定义 E2E 类 + pytest/allure/smoke/flaky + 自定义 session 同步
# 来源（项目 tests/e2e 层，冒烟级混合自动化流程）
# =============================================================================
import allure  # 作用：导入 Allure 装饰器；调用关系：epic/feature/title、attach_json；自定义/框架：框架(allure)；来源(第三方 allure)
import pytest  # 作用：导入 pytest；调用关系：mark.e2e/smoke/flaky；自定义/框架：框架(pytest)；来源(第三方 pytest)
from utils.allure_helper import attach_json  # 作用：导入 Allure JSON 附件工具；调用关系：attach_json 记录加购与结算数据；自定义/框架：自定义；来源(utils/allure_helper.py)


@allure.epic("Tigshop")  # 作用：Allure epic；调用关系：E2E 报告分组；自定义/框架：框架(allure)；来源(allure)
@allure.feature("E2E-前台完整购物流程")  # 作用：Allure feature；调用关系：TestFrontPurchaseE2e；自定义/框架：框架(allure)；来源(allure)
@pytest.mark.e2e  # 作用：E2E 层 pytest 标记；调用关系：-m e2e；自定义/框架：框架(pytest)；来源(pytest)
@pytest.mark.smoke  # 作用：冒烟测试标记；调用关系：-m smoke 快速回归；自定义/框架：框架(pytest)；来源(pytest)
@pytest.mark.flaky(reruns=2, reruns_delay=2)  # 作用：E2E 失败重跑 2 次；调用关系：pytest-rerunfailures；自定义/框架：框架(插件)；来源(pytest-rerunfailures)
class TestFrontPurchaseE2e:  # 作用：前台购物流程 E2E 测试类；调用关系：pytest 收集；自定义/框架：自定义；来源(本文件)
    @allure.title("搜索→详情→加购→购物车→结算页")  # 作用：Allure 用例标题描述完整链路；调用关系：test_search_to_checkout；自定义/框架：框架(allure)；来源(allure)
    def test_search_to_checkout(  # 作用：端到端验证搜索到结算全流程；调用关系：多 POM + API + session_sync；自定义/框架：自定义；来源(本文件)
        self,  # 作用：测试类实例（pytest 约定）；调用关系：类方法第一个参数；自定义/框架：框架(Python/pytest)；来源(Python)
        buyer_driver,  # 作用：已登录买家 WebDriver；调用关系：conftest buyer_driver 链；自定义/框架：自定义 fixture；来源(tests/conftest.py)
        front_base_url,  # 作用：前台 UI 基址；调用关系：POM 构造函数；自定义/框架：自定义 fixture；来源(tests/conftest.py)
        product_api,  # 作用：商品 API 客户端；调用关系：first_sku_id、E2E API 断言；自定义/框架：自定义 fixture；来源(tests/conftest.py)
        cart_api,  # 作用：购物车 API 客户端；调用关系：clear_cart、add_to_cart；自定义/框架：自定义 fixture；来源(tests/conftest.py)
        order_api,  # 作用：订单 API 客户端；调用关系：checkout_index 断言；自定义/框架：自定义 fixture；来源(tests/conftest.py)
        test_data,  # 作用：测试数据（keyword、product_id）；调用关系：搜索与商品 ID；自定义/框架：自定义 fixture；来源(tests/conftest.py)
# 作用：执行本行逻辑；调用关系：见上下文；自定义/框架：自定义；来源(tests/e2e/test_front_purchase_e2e.py)
    ):
        from ui.pages.front.home_page import FrontHomePage  # 作用：延迟导入首页 POM；调用关系：home.search；自定义/框架：自定义；来源(ui/pages/front/home_page.py)
        from ui.pages.front.product_page import FrontProductPage  # 作用：延迟导入商品页 POM；调用关系：open_product、add_to_cart；自定义/框架：自定义；来源(ui/pages/front/product_page.py)
        from ui.pages.front.cart_page import FrontCartPage  # 作用：延迟导入购物车 POM；调用关系：open_cart；自定义/框架：自定义；来源(ui/pages/front/cart_page.py)
        from ui.pages.front.checkout_page import FrontCheckoutPage  # 作用：延迟导入结算页 POM；调用关系：open_checkout；自定义/框架：自定义；来源(ui/pages/front/checkout_page.py)
        from utils.session_sync import sync_browser_token_to_clients  # 作用：延迟导入 token 同步；调用关系：UI 登录态写入 API Session；自定义/框架：自定义；来源(utils/session_sync.py)

        home = FrontHomePage(buyer_driver, front_base_url)  # 作用：实例化首页 POM；调用关系：FrontHomePage.__init__；自定义/框架：自定义；来源(ui/pages/front/home_page.py)
        home.search(test_data["keyword"])  # 作用：UI 执行关键词搜索；调用关系：FrontHomePage.search、test_data；自定义/框架：自定义；来源(ui/pages/front/home_page.py)
        assert "search" in home.current_url  # 作用：断言进入搜索结果页；调用关系：BasePage.current_url；自定义/框架：自定义；来源(ui/pages/base_page.py)

        product_id = test_data["product_id"]  # 作用：取出默认商品 ID；调用关系：test_data fixture；自定义/框架：自定义；来源(conftest test_data)
        product_page = FrontProductPage(buyer_driver, front_base_url)  # 作用：构造商品详情 POM；调用关系：FrontProductPage；自定义/框架：自定义；来源(ui/pages/front/product_page.py)
        product_page.open_product(product_id)  # 作用：UI 打开指定商品详情；调用关系：FrontProductPage.open_product；自定义/框架：自定义；来源(ui/pages/front/product_page.py)
        title = product_page.get_product_title()  # 作用：读取商品标题文本；调用关系：FrontProductPage.get_product_title；自定义/框架：自定义；来源(ui/pages/front/product_page.py)
        assert title  # 作用：断言标题非空；调用关系：pytest assert；自定义/框架：框架(pytest)；来源(Python)

        product_page.add_to_cart()  # 作用：UI 点击加入购物车；调用关系：FrontProductPage.add_to_cart；自定义/框架：自定义；来源(ui/pages/front/product_page.py)

        sync_browser_token_to_clients(buyer_driver, product_api, cart_api, order_api)  # 作用：将浏览器 cookie/token 同步至 API Session；调用关系：utils.session_sync；自定义/框架：自定义；来源(utils/session_sync.py)
        cart_api.clear_cart()  # 作用：API 清空购物车保证后续加购可控；调用关系：CartApiClient.clear_cart；自定义/框架：自定义；来源(api/client/cart_client.py)
        sku_id = product_api.first_sku_id(product_id)  # 作用：API 获取首个 SKU；调用关系：ProductApiClient.first_sku_id；自定义/框架：自定义；来源(api/client/product_client.py)
        cart_api.add_to_cart(product_id, sku_id, 1)  # 作用：API 加购 1 件（与 UI 步骤互补验证）；调用关系：CartApiClient.add_to_cart；自定义/框架：自定义；来源(api/client/cart_client.py)
        attach_json({"product_id": product_id, "sku_id": sku_id, "title": title}, "加购商品")  # 作用：Allure 附加加购 JSON；调用关系：utils.allure_helper.attach_json；自定义/框架：自定义；来源(utils/allure_helper.py)

        cart_page = FrontCartPage(buyer_driver, front_base_url)  # 作用：构造购物车 POM；调用关系：FrontCartPage；自定义/框架：自定义；来源(ui/pages/front/cart_page.py)
        cart_page.open_cart()  # 作用：UI 导航至购物车页；调用关系：FrontCartPage.open_cart；自定义/框架：自定义；来源(ui/pages/front/cart_page.py)
        assert cart_page.has_cart_content()  # 作用：断言购物车页有内容；调用关系：FrontCartPage.has_cart_content；自定义/框架：自定义；来源(ui/pages/front/cart_page.py)

        checkout = FrontCheckoutPage(buyer_driver, front_base_url)  # 作用：构造结算页 POM；调用关系：FrontCheckoutPage；自定义/框架：自定义；来源(ui/pages/front/checkout_page.py)
        checkout.open_checkout()  # 作用：UI 打开结算页；调用关系：FrontCheckoutPage.open_checkout；自定义/框架：自定义；来源(ui/pages/front/checkout_page.py)
        assert checkout.page_loaded()  # 作用：断言结算页 UI 已加载；调用关系：FrontCheckoutPage.page_loaded；自定义/框架：自定义；来源(ui/pages/front/checkout_page.py)

        checkout_data = order_api.checkout_index(flow_type=1)  # 作用：API 拉取结算 index 数据；调用关系：OrderApiClient.checkout_index；自定义/框架：自定义；来源(api/client/order_client.py)
        attach_json(checkout_data, "结算页 API 数据")  # 作用：Allure 附加结算 API JSON；调用关系：attach_json；自定义/框架：自定义；来源(utils/allure_helper.py)
        assert checkout_data.get("addressList") is not None  # 作用：断言 API 结算数据含 addressList；调用关系：pytest assert；自定义/框架：框架(pytest)；来源(Python)
