# =============================================================================
# 文件：tests/api/test_cart_order_api.py
# 作用：Tigshop 买家购物车、结算、订单与用户详情 API 自动化用例（需登录）
# 调用关系：pytest → logged_in_buyer_api/cart_api/order_api/product_with_sku → API 客户端
# 自定义/框架：自定义测试类 + pytest/allure + pytest-rerunfailures flaky 标记
# 来源（项目 tests/api 层，覆盖加购/购物车/结算/订单/用户接口）
# =============================================================================
import allure  # 作用：导入 Allure 装饰器；调用关系：epic/feature/title；自定义/框架：框架(allure)；来源(第三方 allure)
import pytest  # 作用：导入 pytest；调用关系：mark.api、mark.flaky；自定义/框架：框架(pytest)；来源(第三方 pytest)


@allure.epic("Tigshop")  # 作用：Allure epic 分组；调用关系：报告树；自定义/框架：框架(allure)；来源(allure)
@allure.feature("API-购物车与订单")  # 作用：Allure feature 分组；调用关系：本类用例；自定义/框架：框架(allure)；来源(allure)
@pytest.mark.api  # 作用：API 层标记；调用关系：pytest -m api；自定义/框架：框架(pytest)；来源(pytest)
@pytest.mark.flaky(reruns=1, reruns_delay=3)  # 作用：失败自动重跑 1 次，间隔 3 秒；调用关系：pytest-rerunfailures 插件；自定义/框架：框架(插件)；来源(pytest-rerunfailures)
class TestCartOrderApi:  # 作用：购物车与订单 API 测试类；调用关系：pytest 收集；自定义/框架：自定义；来源(本文件)
    @allure.title("加购后购物车数量增加")  # 作用：Allure 用例标题；调用关系：test_add_to_cart；自定义/框架：框架(allure)；来源(allure)
    def test_add_to_cart(self, logged_in_buyer_api, cart_api, product_api, product_with_sku):  # 作用：加购前后对比 cart 数量；调用关系：logged_in_buyer_api 登录清理 + cart_api.add_to_cart；自定义/框架：自定义；来源(本文件)
        before = cart_api.cart_item_count()  # 作用：加购前读取购物车条目数；调用关系：CartApiClient.cart_item_count；自定义/框架：自定义；来源(api/client/cart_client.py)
        cart_api.add_to_cart(  # 作用：调用加购 API；调用关系：CartApiClient.add_to_cart；自定义/框架：自定义；来源(api/client/cart_client.py)
            product_with_sku["product_id"],  # 作用：传入商品 ID；调用关系：product_with_sku fixture；自定义/框架：自定义；来源(conftest product_with_sku)
            product_with_sku["sku_id"],  # 作用：传入 SKU ID；调用关系：product_with_sku；自定义/框架：自定义；来源(conftest)
            number=1,  # 作用：加购数量为 1；调用关系：add_to_cart 参数；自定义/框架：自定义；来源(本文件)
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(tests/api/test_cart_order_api.py)
        )
        after = cart_api.cart_item_count()  # 作用：加购后再次读取数量；调用关系：CartApiClient.cart_item_count；自定义/框架：自定义；来源(api/client/cart_client.py)
        assert after >= before + 1  # 作用：断言数量至少增加 1；调用关系：pytest assert；自定义/框架：框架(pytest)；来源(Python)

    @allure.title("购物车列表接口返回 cartList")  # 作用：Allure 标题；调用关系：test_cart_list；自定义/框架：框架(allure)；来源(allure)
    def test_cart_list(self, logged_in_buyer_api, cart_api, product_with_sku):  # 作用：验证 list_cart 含 cartList；调用关系：加购后 list_cart；自定义/框架：自定义；来源(本文件)
        cart_api.add_to_cart(product_with_sku["product_id"], product_with_sku["sku_id"], 1)  # 作用：先加购一件保证列表非空；调用关系：CartApiClient.add_to_cart；自定义/框架：自定义；来源(api/client/cart_client.py)
        data = cart_api.list_cart()  # 作用：获取购物车列表 JSON；调用关系：CartApiClient.list_cart；自定义/框架：自定义；来源(api/client/cart_client.py)
        assert "cartList" in data  # 作用：断言响应含 cartList 键；调用关系：pytest assert in；自定义/框架：框架(pytest)；来源(Python)

    @allure.title("结算页 index 返回地址列表")  # 作用：Allure 标题；调用关系：test_checkout_index；自定义/框架：框架(allure)；来源(allure)
    def test_checkout_index(self, logged_in_buyer_api, cart_api, order_api, product_with_sku):  # 作用：结算 index 含 addressList；调用关系：clear/add + checkout_index；自定义/框架：自定义；来源(本文件)
        cart_api.clear_cart()  # 作用：清空购物车保证干净状态；调用关系：CartApiClient.clear_cart；自定义/框架：自定义；来源(api/client/cart_client.py)
        cart_api.add_to_cart(product_with_sku["product_id"], product_with_sku["sku_id"], 1)  # 作用：加购一件可结算商品；调用关系：CartApiClient；自定义/框架：自定义；来源(api/client/cart_client.py)
        data = order_api.checkout_index(flow_type=1)  # 作用：请求结算页 index 数据 flow_type=1；调用关系：OrderApiClient.checkout_index；自定义/框架：自定义；来源(api/client/order_client.py)
        assert data.get("addressList") is not None  # 作用：断言 addressList 字段存在（可为空列表）；调用关系：pytest assert；自定义/框架：框架(pytest)；来源(Python)

    @allure.title("买家订单列表可查询")  # 作用：Allure 标题；调用关系：test_order_list；自定义/框架：框架(allure)；来源(allure)
    def test_order_list(self, logged_in_buyer_api, order_api):  # 作用：验证订单分页列表；调用关系：order_api.list_orders；自定义/框架：自定义；来源(本文件)
        data = order_api.list_orders(page=1, size=5)  # 作用：查询第 1 页订单；调用关系：OrderApiClient.list_orders；自定义/框架：自定义；来源(api/client/order_client.py)
        assert "records" in data  # 作用：断言分页结构含 records；调用关系：pytest assert；自定义/框架：框架(pytest)；来源(Python)

    @allure.title("登录后用户详情用户名正确")  # 作用：Allure 标题；调用关系：test_user_detail；自定义/框架：框架(allure)；来源(allure)
    def test_user_detail(self, logged_in_buyer_api, buyer_auth_api, test_data):  # 作用：验证 get_user_detail 用户名；调用关系：buyer_auth_api + test_data；自定义/框架：自定义；来源(本文件)
        detail = buyer_auth_api.get_user_detail()  # 作用：调用用户详情 API；调用关系：AuthApiClient.get_user_detail；自定义/框架：自定义；来源(api/client/auth_client.py)
        assert detail.get("username") == test_data["username"]  # 作用：断言 username 与配置一致；调用关系：test_data fixture；自定义/框架：自定义；来源(conftest test_data)
