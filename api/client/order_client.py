# =============================================================================
# api/client/order_client.py — 订单 API 客户端 （项目：api/client/order_client.py）
# 作用：封装结算页数据、订单列表、订单数量与状态名提取 （项目：api/client/order_client.py → OrderApiClient）
# 说明：继承 BaseApiClient；需买家登录；tests/api/test_cart_order_api.py 等使用 （项目：tests/conftest.py → order_api）
# =============================================================================

# 导入 Any/Dict/List：标注结算/列表返回与 status_names 列表 （标准库：typing）
from typing import Any, Dict, List

# 导入 BaseApiClient：复用 post/get 与 data_or_raise （项目：api/client/base_client.py → BaseApiClient）
from api.client.base_client import BaseApiClient


# 订单 API 客户端类 （项目：api/client/order_client.py → OrderApiClient）
class OrderApiClient(BaseApiClient):
    """订单 API。"""

    # 进入结算页/获取结算信息：POST /order/check/index （项目：tests/api/test_cart_order_api.py 调用）
    def checkout_index(self, flow_type: int = 1) -> Dict[str, Any]:
        # flow_type=1 通常表示普通购买流程 （项目：api/client/base_client.py → BaseApiClient.post）
        response = self.post("/order/check/index", json={"flow_type": flow_type})
        # 返回地址、商品、金额等结算 data （项目：api/client/base_client.py → BaseApiClient.data_or_raise）
        return self.data_or_raise(response, " /order/check/index")

    # 分页查询用户订单列表：GET /user/order/list （项目：tests/api/test_cart_order_api.py 调用）
    def list_orders(self, page: int = 1, size: int = 10) -> Dict[str, Any]:
        # 带 page/size 查询参数 （项目：api/client/base_client.py → BaseApiClient.get）
        response = self.get("/user/order/list", params={"page": page, "size": size})
        # 返回含 records、total 的分页 data （项目：api/client/base_client.py → BaseApiClient.data_or_raise）
        return self.data_or_raise(response, " /user/order/list")

    # 获取订单总数：优先读 total 字段，否则用 records 长度 （项目：tests/api/test_cart_order_api.py 断言订单数）
    def order_count(self) -> int:
        # 只取第 1 页 1 条即可拿到 total 元数据 （项目：api/client/order_client.py → OrderApiClient.list_orders）
        data = self.list_orders(page=1, size=1)
        # total 存在则转 int，否则 fallback 到 records 列表长度 （Python 内置：int, dict.get, len, or）
        return int(data.get("total") or len(data.get("records") or []))

    # 提取最近若干订单的状态中文名列表，便于 UI/API 对照断言 （项目：tests/api/test_cart_order_api.py 调用）
    def order_status_names(self) -> List[str]:
        # 取前 5 条订单记录 （项目：api/client/order_client.py → OrderApiClient.list_orders）
        data = self.list_orders(page=1, size=5)
        # 订单记录列表，无则空列表 （Python 内置：dict.get, or）
        records = data.get("records") or []
        # 收集非空的 orderStatusName 字段 （Python 内置：list comprehension）
        return [r.get("orderStatusName", "") for r in records if r.get("orderStatusName")]
