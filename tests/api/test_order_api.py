# =============================================================================（项目：tests/api/test_order_api.py → 章节分隔）
# tests/api/test_order_api.py — 订单相关 API 接口测试（项目：tests/api/test_order_api.py → 模块说明）
# 作用：验证提交订单、查询订单列表及未授权下单等场景（项目：api/client/order_client.py → OrderApiClient）
# =============================================================================（项目：tests/api/test_order_api.py → 章节分隔）

# 导入 pytest：测试运行与断言框架（第三方：pytest → fixture/mark/raises）
import pytest
# 导入 allure：测试报告装饰器（第三方：allure → epic/feature/title）
import allure
# 导入 requests：用于断言 HTTP 异常及状态码（第三方：requests → HTTPError）
import requests
# 从项目工具模块导入 attach_json：把 JSON 数据附加到 Allure 报告便于查看（项目：utils/allure_helper.py → attach_json）
from utils.allure_helper import attach_json


# Allure epic：报告顶层分组（第三方：allure → epic）
@allure.epic("Practice Software Testing")
# Allure feature：订单功能模块（第三方：allure → feature）
@allure.feature("订单")
# pytest 标记：API 测试（第三方：pytest → mark.api）
@pytest.mark.api
class TestOrderApi:
    """订单 API 测试。"""

    # 用例标题：完整走通「提交订单 + 查询列表」（第三方：allure → title）
    @allure.title("提交订单并查询列表")
    # cart_with_product：已含商品的购物车，可直接用于下单（项目：tests/conftest.py → cart_with_product）
    def test_submit_and_list_orders(self, logged_in_api, order_api, cart_with_product):
        # 传入购物车 ID 提交订单，返回发票/订单信息（项目：api/client/order_client.py → submit_order）
        invoice = order_api.submit_order(cart_with_product["id"])
        # 将订单详情 JSON 附加到 Allure 报告，name 为附件显示名称（项目：utils/allure_helper.py → attach_json）
        attach_json(invoice, name="订单详情")
        # 成功下单后响应中应有 invoice_number 或 id 之一（Python 内置：assert）
        assert invoice.get("invoice_number") or invoice.get("id")

        # 调用列表接口查询当前用户的所有订单（项目：api/client/order_client.py → list_orders）
        orders = order_api.list_orders()
        # data 字段应存在（可能为空列表，但不能缺失该键）（Python 内置：assert）
        assert orders.get("data") is not None

    # 用例标题：未登录用户不能提交订单（第三方：allure → title）
    @allure.title("未登录无法提交订单")
    @pytest.mark.exception
    # guest_cart_with_product：未登录状态下创建的购物车（仍可能有 cart id）（项目：tests/conftest.py → guest_cart_with_product）
    def test_submit_order_unauthorized(self, order_api, guest_cart_with_product):
        # 未携带 Token 提交订单应失败（第三方：pytest → raises）
        with pytest.raises(requests.HTTPError) as exc:
            order_api.submit_order(guest_cart_with_product["id"])
        # 401 表示需要认证（标准库：HTTP 状态码语义）
        assert exc.value.response.status_code == 401
