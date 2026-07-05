# =============================================================================
# api/client/product_client.py — 商品与首页 API 客户端 （项目：api/client/product_client.py）
# 作用：封装首页、分类、商品列表/搜索/详情及 SKU 解析等接口 （项目：api/client/product_client.py → ProductApiClient）
# 说明：继承 BaseApiClient；conftest 的 product_api fixture 注入测试；加购前常调用 first_sku_id （项目：tests/conftest.py）
# =============================================================================

# 导入 Any/Dict/List：标注首页、列表、详情等返回类型 （标准库：typing）
from typing import Any, Dict, List

# 导入 BaseApiClient：复用 get/post 与 data_or_raise （项目：api/client/base_client.py → BaseApiClient）
from api.client.base_client import BaseApiClient


# 商品与首页 API 客户端类 （项目：api/client/product_client.py → ProductApiClient）
class ProductApiClient(BaseApiClient):
    """商品与首页 API。"""

    # 获取首页聚合数据：GET /home/home/index （项目：tests/api/test_home_product_api.py 调用）
    def home_index(self) -> Dict[str, Any]:
        # preview_id=0 表示非预览模式的首页数据 （项目：api/client/base_client.py → BaseApiClient.get）
        response = self.get("/home/home/index", params={"preview_id": 0})
        # 返回首页 modules/banners 等 data 结构 （项目：api/client/base_client.py → BaseApiClient.data_or_raise）
        return self.data_or_raise(response, " /home/home/index")

    # 获取热门分类列表：GET /category/category/hot （项目：tests/api/test_home_product_api.py 调用）
    def hot_categories(self) -> List[Dict[str, Any]]:
        # 请求热门分类接口 （项目：api/client/base_client.py → BaseApiClient.get）
        response = self.get("/category/category/hot")
        # 解析 JSON 并得到 data 字段 （项目：api/client/base_client.py → BaseApiClient.data_or_raise）
        data = self.data_or_raise(response, " /category/category/hot")
        # 若 data 已是 list 则直接返回，否则返回空列表保证类型一致 （Python 内置：isinstance）
        return data if isinstance(data, list) else []

    # 分页商品列表，可选 keyword 与 categoryId 筛选 （项目：api/client/product_client.py → search_products 委托）
    def list_products(
# 作用：执行本行逻辑；调用关系：见上下文；自定义/框架：自定义；来源(api/client/product_client.py)
        self,
        page: int = 1,           # 页码，从 1 开始 （项目：api/client/product_client.py → ProductApiClient.list_products）
        size: int = 10,          # 每页条数 （项目：api/client/product_client.py → ProductApiClient.list_products）
        keyword: str = "",       # 搜索关键词，空则不过滤 （项目：api/client/product_client.py → ProductApiClient.list_products）
        category_id: int = None, # 分类 ID，None 表示不按分类过滤 （项目：api/client/product_client.py → ProductApiClient.list_products）
# 作用：执行本行逻辑；调用关系：见上下文；自定义/框架：自定义；来源(api/client/product_client.py)
    ) -> Dict[str, Any]:
        # 构建 query 参数字典，至少含 page 与 size （Python 内置：dict）
        params: Dict[str, Any] = {"page": page, "size": size}
        # 有关键词时追加 keyword 参数 （Python 内置：if, dict 赋值）
        if keyword:
# 作用：赋值/绑定变量；调用关系：供后续步骤使用；自定义/框架：Python 内置；来源(赋值)
            params["keyword"] = keyword
        # 指定分类时追加 categoryId（接口字段驼峰命名） （Python 内置：if is not None）
        if category_id is not None:
# 作用：赋值/绑定变量；调用关系：供后续步骤使用；自定义/框架：Python 内置；来源(赋值)
            params["categoryId"] = category_id
        # GET 商品列表接口 （项目：api/client/base_client.py → BaseApiClient.get）
        response = self.get("/product/product/list", params=params)
        # 返回分页 data（records/total 等） （项目：api/client/base_client.py → BaseApiClient.data_or_raise）
        return self.data_or_raise(response, " /product/product/list")

    # 按关键词搜索商品的便捷封装，内部调用 list_products （项目：tests/api/test_home_product_api.py 调用）
    def search_products(self, keyword: str, page: int = 1, size: int = 10) -> Dict[str, Any]:
        # 将 keyword 传给 list_products，复用同一列表接口 （项目：api/client/product_client.py → ProductApiClient.list_products）
        return self.list_products(page=page, size=size, keyword=keyword)

    # 获取单个商品详情：GET /product/product/detail?id= （项目：tests/api/test_home_product_api.py 调用）
    def product_detail(self, product_id: int) -> Dict[str, Any]:
        # 通过 query 参数 id 指定商品 （项目：api/client/base_client.py → BaseApiClient.get）
        response = self.get("/product/product/detail", params={"id": product_id})
        # 返回含 skuList、price 等字段的 data （项目：api/client/base_client.py → BaseApiClient.data_or_raise）
        return self.data_or_raise(response, " /product/product/detail")

    # 从商品详情取第一个 SKU 的 skuId，供加购接口使用 （项目：tests/conftest.py、tests/api/test_cart_order_api.py 调用）
    def first_sku_id(self, product_id: int) -> int:
        # 拉取完整商品详情 （项目：api/client/product_client.py → ProductApiClient.product_detail）
        detail = self.product_detail(product_id)
        # 取 skuList 数组，缺失时用空列表 （Python 内置：dict.get, or）
        sku_list = detail.get("skuList") or []
        # 无 SKU 时无法加购，抛 ValueError 明确失败原因 （Python 内置：ValueError）
        if not sku_list:
# 作用：抛出异常；调用关系：错误向上传递；自定义/框架：Python 内置；来源(raise)
            raise ValueError(f"商品 {product_id} 无 SKU")
        # 取第一条 SKU 的 skuId 并转为 int （Python 内置：int, dict 索引）
        return int(sku_list[0]["skuId"])
