# =============================================================================（项目：tests/api/test_product_api.py → 章节分隔）
# tests/api/test_product_api.py — 商品与购物车相关 API 接口测试（项目：tests/api/test_product_api.py → 模块说明）
# 作用：验证商品搜索、详情、加购、购物车等接口行为（项目：api/client/product_client.py → ProductApiClient）
# =============================================================================（项目：tests/api/test_product_api.py → 章节分隔）

# 导入 pytest：测试框架，负责发现用例、注入 Fixture、执行断言（第三方：pytest → fixture/mark/raises）
import pytest
# 导入 allure：为测试用例添加报告层级与可读标题（第三方：allure → epic/feature/title）
import allure
# 导入 requests：用于捕获 HTTP 错误并检查状态码（如 404）（第三方：requests → HTTPError）
import requests


# Allure 报告 epic：被测系统/项目名称（第三方：allure → epic）
@allure.epic("Practice Software Testing")
# Allure 报告 feature：本文件聚焦「商品与购物车」功能（第三方：allure → feature）
@allure.feature("商品与购物车")
# pytest 标记：标识为 API 层测试（第三方：pytest → mark.api）
@pytest.mark.api
class TestProductApi:
    """商品与购物车 API 测试。"""

    # 用例标题：验证按关键词搜索商品（第三方：allure → title）
    @allure.title("搜索商品")
    # logged_in_api：确保已登录（副作用 Fixture，可能只用于建立登录态）（项目：tests/conftest.py → logged_in_api）
    # product_api：商品 API 客户端实例（项目：tests/conftest.py → product_api）
    # test_data：公共测试数据字典（含 keyword 等）（项目：tests/conftest.py → test_data）
    def test_search_products(self, logged_in_api, product_api, test_data):
        # 调用 search 接口，传入配置中的搜索关键词（项目：api/client/product_client.py → search）
        result = product_api.search(test_data["keyword"])
        # 断言返回的 data 列表至少有一条商品，说明搜索有效（Python 内置：assert）
        assert len(result["data"]) >= 1

    # 用例标题：根据商品 ID 获取详情（第三方：allure → title）
    @allure.title("获取商品详情")
    # first_product：Fixture 提供的第一个可用商品（含 id、name 等字段）（项目：tests/conftest.py → first_product）
    def test_product_detail(self, logged_in_api, product_api, first_product):
        # 用商品 ID 请求详情接口（项目：api/client/product_client.py → get_detail）
        detail = product_api.get_detail(first_product["id"])
        # 详情中的 id 应与搜索到的商品 id 一致（Python 内置：assert）
        assert detail["id"] == first_product["id"]

    # 用例标题：创建购物车并向其中添加商品（第三方：allure → title）
    @allure.title("创建购物车并加购")
    # cart_with_product：Fixture 已创建购物车并加入一件商品（项目：tests/conftest.py → cart_with_product）
    def test_add_to_cart(self, logged_in_api, product_api, cart_with_product):
        # 根据购物车 ID 查询购物车详情（项目：api/client/product_client.py → get_cart）
        cart_detail = product_api.get_cart(cart_with_product["id"])
        # cart_items 非空表示购物车中确实有商品（Python 内置：assert）
        assert cart_detail["cart_items"]
        # 测试结束后清理：清空购物车，避免影响其他用例（项目：api/client/product_client.py → clear_cart）
        product_api.clear_cart(cart_with_product["id"])

    # 用例标题：无效商品 ID 应返回 404（第三方：allure → title）
    @allure.title("无效商品 ID 返回 404")
    # 标记为异常场景测试（第三方：pytest → mark.exception）
    @pytest.mark.exception
    def test_invalid_product(self, logged_in_api, product_api, test_data):
        # 期望请求不存在的商品 ID 时会抛出 HTTPError（第三方：pytest → raises）
        with pytest.raises(requests.HTTPError) as exc:
            # test_data 中配置了 deliberately 无效的 product id（项目：tests/conftest.py → test_data）
            product_api.get_detail(test_data["invalid_product_id"])
        # 404 Not Found 表示资源不存在（标准库：HTTP 状态码语义）
        assert exc.value.response.status_code == 404
