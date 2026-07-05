# =============================================================================
# api/client/cart_client.py — 购物车 API 客户端 （项目：api/client/cart_client.py）
# 作用：封装购物车列表、加购、清空及商品件数统计 （项目：api/client/cart_client.py → CartApiClient）
# 说明：需买家登录后 Session 带 Token；conftest 在 fixture 前后调用 clear_cart 保证隔离 （项目：tests/conftest.py）
# =============================================================================

# 导入 Any/Dict：标注 list_cart/add_to_cart 返回的 data 类型 （标准库：typing）
from typing import Any, Dict

# 导入 BaseApiClient：复用 get/post 与 data_or_raise （项目：api/client/base_client.py → BaseApiClient）
from api.client.base_client import BaseApiClient


# 购物车 API 客户端类 （项目：api/client/cart_client.py → CartApiClient）
class CartApiClient(BaseApiClient):
    """购物车 API。"""

    # 获取当前用户购物车：GET /cart/cart/list （项目：tests/api/test_cart_order_api.py 调用）
    def list_cart(self) -> Dict[str, Any]:
        # 发起 GET，返回按店铺分组的 cartList 结构 （项目：api/client/base_client.py → BaseApiClient.get）
        response = self.get("/cart/cart/list")
        # 解析并返回 data （项目：api/client/base_client.py → BaseApiClient.data_or_raise）
        return self.data_or_raise(response, " /cart/cart/list")

    # 加购：POST /cart/cart/addToCart，需 product_id 与 sku_id （项目：tests/api/test_cart_order_api.py、conftest 调用）
    def add_to_cart(self, product_id: int, sku_id: int, number: int = 1) -> Dict[str, Any]:
        # POST JSON：id 为商品 ID，sku_id 为规格 ID，number 为数量 （项目：api/client/base_client.py → BaseApiClient.post）
        response = self.post(
            "/cart/cart/addToCart",  # Tigshop 加购路径 （项目：api/client/cart_client.py → CartApiClient.add_to_cart）
            json={"id": product_id, "sku_id": sku_id, "number": number},  # 请求体字段与接口约定一致 （项目：api/client/cart_client.py → CartApiClient.add_to_cart）
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(api/client/cart_client.py)
        )
        # 返回加购结果 data （项目：api/client/base_client.py → BaseApiClient.data_or_raise）
        return self.data_or_raise(response, " /cart/cart/addToCart")

    # 清空购物车：POST /cart/cart/clear；失败时静默忽略，避免 teardown 拖垮用例 （项目：tests/conftest.py → fixture 清理）
    def clear_cart(self) -> None:
        # 空 json 体触发服务端清空逻辑 （项目：api/client/base_client.py → BaseApiClient.post）
        response = self.post("/cart/cart/clear", json={})
# 作用：尝试执行可能失败的操作；调用关系：异常处理块；自定义/框架：Python 内置；来源(try)
        try:
            # 正常路径：校验业务 code 并丢弃返回值 （项目：api/client/base_client.py → BaseApiClient.data_or_raise）
            self.data_or_raise(response, " /cart/cart/clear")
# 作用：捕获异常；调用关系：try/except 错误处理；自定义/框架：Python 内置；来源(except)
        except Exception:
            # 清空失败（如已空、网络抖动）不向上抛，保证 fixture 继续执行 （Python 内置：Exception, pass）
            pass

    # 统计购物车商品总件数：遍历 cartList 下各店铺 carts 的 quantity/number （项目：tests/api/test_cart_order_api.py 断言）
    def cart_item_count(self) -> int:
        # 拉取最新购物车快照 （项目：api/client/cart_client.py → CartApiClient.list_cart）
        data = self.list_cart()
        # 累加器，初始为 0 （Python 内置：int）
        total = 0
        # 外层：按店铺分组的 cartList （Python 内置：for, dict.get, or）
        for shop in data.get("cartList") or []:
            # 内层：该店铺下每条 cart 行项 （Python 内置：for）
            for item in shop.get("carts") or []:
                # 兼容 quantity 或 number 字段，缺省按 0 计 （Python 内置：int, dict.get, or, +=）
                total += int(item.get("quantity") or item.get("number") or 0)
        # 返回全站购物车商品件数总和 （Python 内置：return）
        return total
