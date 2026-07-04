# 导入类型注解，说明方法返回的是字典结构 （标准库：typing）
from typing import Any, Dict
# 导入基类，订单客户端同样继承统一的请求与重试逻辑 （项目：api/client/base_client.py → BaseApiClient）
from api.client.base_client import BaseApiClient
# 从配置文件导入默认邮编和国家，lookup_address 未传参时使用 （项目：config/settings.py → DEFAULT_POSTCODE, DEFAULT_COUNTRY）
from config.settings import DEFAULT_COUNTRY, DEFAULT_POSTCODE


# 定义订单（发票 Invoice）相关的 API 客户端 （项目：api/client/order_client.py → OrderApiClient）
class OrderApiClient(BaseApiClient):
    """订单（Invoice）API。"""

    # 根据邮编和国家查询地址信息（用于填写账单地址）
    # postcode、country 可不传，会使用配置文件里的默认值
    def lookup_address(self, postcode: str = None, country: str = None) -> Dict[str, Any]:  # 邮编地址查询 （项目：api/client/order_client.py → lookup_address）
        # 组装查询参数字典；若参数为 None 则用 or 后面的默认值 （项目：config/settings.py → DEFAULT_POSTCODE, DEFAULT_COUNTRY）
        params = {
            "postcode": postcode or DEFAULT_POSTCODE,
            "country": country or DEFAULT_COUNTRY,
        }
        # GET /postcode-lookup?postcode=...&country=... （项目：api/client/base_client.py → get）
        response = self.get("/postcode-lookup", params=params)
        return self.json_or_raise(response, " /postcode-lookup")  # 解析响应 JSON （项目：api/client/base_client.py → json_or_raise）

    # 提交订单：用购物车 ID 创建发票/订单
    # payment_method: 支付方式，默认货到付款 "cash-on-delivery"
    def submit_order(self, cart_id: str, payment_method: str = "cash-on-delivery") -> Dict[str, Any]:  # 提交订单 （项目：api/client/order_client.py → submit_order）
        # 先查默认地址，得到街道、城市、州、国家、邮编等字段 （项目：api/client/order_client.py → lookup_address）
        addr = self.lookup_address()
        # 构造 POST /invoices 的请求体 （项目：api/client/order_client.py → submit_order）
        payload = {
            "cart_id": cart_id,  # 要结算的购物车 ID （项目：api/client/order_client.py → submit_order）
            "payment_method": payment_method,  # 支付方式 （项目：api/client/order_client.py → submit_order）
            # 账单街道：把 street 和 house_number 拼成一行地址 （Python 内置：str 格式化）
            "billing_street": f"{addr['street']} {addr['house_number']}",
            "billing_city": addr["city"],  # 账单城市 （项目：api/client/order_client.py → submit_order）
            "billing_state": addr["state"],  # 账单省/州 （项目：api/client/order_client.py → submit_order）
            "billing_country": addr["country"],  # 账单国家 （项目：api/client/order_client.py → submit_order）
            "billing_postal_code": addr["postcode"],  # 账单邮编 （项目：api/client/order_client.py → submit_order）
            "payment_details": {},  # 货到付款时支付详情为空对象 （项目：api/client/order_client.py → submit_order）
        }
        # 提交订单 （项目：api/client/base_client.py → post）
        response = self.post("/invoices", json=payload)
        return self.json_or_raise(response, " POST /invoices")  # 解析响应 JSON （项目：api/client/base_client.py → json_or_raise）

    # 列出当前用户的所有订单 （项目：api/client/order_client.py → list_orders）
    def list_orders(self) -> Dict[str, Any]:
        response = self.get("/invoices")  # GET /invoices （项目：api/client/base_client.py → get）
        return self.json_or_raise(response, " GET /invoices")  # 解析响应 JSON （项目：api/client/base_client.py → json_or_raise）

    # 根据发票/订单 ID 查询单个订单详情 （项目：api/client/order_client.py → get_order）
    def get_order(self, invoice_id: str) -> Dict[str, Any]:
        response = self.get(f"/invoices/{invoice_id}")  # GET /invoices/{id} （项目：api/client/base_client.py → get）
        return self.json_or_raise(response, f" GET /invoices/{invoice_id}")  # 解析响应 JSON （项目：api/client/base_client.py → json_or_raise）
