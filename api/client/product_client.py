# 从 typing 导入类型注解，用于标明方法返回值是字典 （标准库：typing）
from typing import Any, Dict
# 导入 API 基类，商品客户端复用其 HTTP 请求与错误处理逻辑 （项目：api/client/base_client.py → BaseApiClient）
from api.client.base_client import BaseApiClient


# 定义商品与购物车相关的 API 客户端 （项目：api/client/product_client.py → ProductApiClient）
class ProductApiClient(BaseApiClient):
    """商品与购物车 API。"""

    # 按关键词搜索商品 （项目：api/client/product_client.py → search）
    def search(self, keyword: str) -> Dict[str, Any]:
        # GET /products/search，params 会变成 URL 查询参数 ?q=关键词 （项目：api/client/base_client.py → get）
        response = self.get("/products/search", params={"q": keyword})
        # 校验状态并返回 JSON 搜索结果 （项目：api/client/base_client.py → json_or_raise）
        return self.json_or_raise(response, " /products/search")

    # 根据商品 ID 获取商品详情 （项目：api/client/product_client.py → get_detail）
    def get_detail(self, product_id: str) -> Dict[str, Any]:
        # f-string 把 product_id 拼进路径，例如 /products/abc123 （Python 内置：f-string）
        response = self.get(f"/products/{product_id}")  # GET /products/{id} （项目：api/client/base_client.py → get）
        return self.json_or_raise(response, f" /products/{product_id}")  # 解析响应 JSON （项目：api/client/base_client.py → json_or_raise）

    # 创建一个新的空购物车，返回的数据里通常包含 cart_id （项目：api/client/product_client.py → create_cart）
    def create_cart(self) -> Dict[str, Any]:
        # POST /carts，无请求体时只创建购物车 （项目：api/client/base_client.py → post）
        response = self.post("/carts")
        return self.json_or_raise(response, " POST /carts")  # 解析响应 JSON （项目：api/client/base_client.py → json_or_raise）

    # 把指定商品加入购物车
    # cart_id: 购物车 ID；product_id: 商品 ID；quantity: 数量，默认 1
    def add_to_cart(self, cart_id: str, product_id: str, quantity: int = 1) -> Dict[str, Any]:  # 加入购物车 （项目：api/client/product_client.py → add_to_cart）
        # POST /carts/{cart_id}，json 里传商品 ID 和数量 （项目：api/client/base_client.py → post）
        response = self.post(
            f"/carts/{cart_id}",
            json={"product_id": product_id, "quantity": quantity},
        )
        return self.json_or_raise(response, f" POST /carts/{cart_id}")  # 解析响应 JSON （项目：api/client/base_client.py → json_or_raise）

    # 查询购物车内容（商品列表、总价等） （项目：api/client/product_client.py → get_cart）
    def get_cart(self, cart_id: str) -> Dict[str, Any]:
        response = self.get(f"/carts/{cart_id}")  # GET /carts/{id} （项目：api/client/base_client.py → get）
        return self.json_or_raise(response, f" GET /carts/{cart_id}")  # 解析响应 JSON （项目：api/client/base_client.py → json_or_raise）

    # 清空或删除整个购物车（无 JSON 响应体，只校验 HTTP 状态） （项目：api/client/product_client.py → clear_cart）
    def clear_cart(self, cart_id: str) -> None:
        # DELETE /carts/{cart_id} （项目：api/client/base_client.py → delete）
        response = self.delete(f"/carts/{cart_id}")
        # 不调用 json()，只检查是否 2xx，失败则附加错误到 Allure （项目：api/client/base_client.py → raise_or_attach）
        self.raise_or_attach(response, f" DELETE /carts/{cart_id}")
