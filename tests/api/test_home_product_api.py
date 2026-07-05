# =============================================================================
# 文件：tests/api/test_home_product_api.py
# 作用：Tigshop 前台商品与首页相关 API 接口自动化用例（无需登录）
# 调用关系：pytest 收集 → conftest product_api/test_data fixture → ProductApiClient → 远端 API
# 自定义/框架：自定义测试类 + pytest/allure 框架装饰
# 来源（项目 tests/api 层，覆盖首页/分类/搜索/详情接口）
# =============================================================================
import allure  # 作用：导入 Allure 报告装饰器；调用关系：@allure.epic/feature/title；自定义/框架：框架(allure-pytest)；来源(第三方 allure)
import pytest  # 作用：导入 pytest 框架；调用关系：@pytest.mark.api、用例收集；自定义/框架：框架(pytest)；来源(第三方 pytest)


@allure.epic("Tigshop")  # 作用：Allure 报告一级分组 epic；调用关系：报告层级 TestHomeProductApi；自定义/框架：框架(allure)；来源(allure)
@allure.feature("API-首页与商品")  # 作用：Allure 二级 feature 分组；调用关系：本模块所有用例；自定义/框架：框架(allure)；来源(allure)
@pytest.mark.api  # 作用：标记为 API 层用例，可按 -m api 筛选；调用关系：pytest 标记；自定义/框架：框架(pytest mark)；来源(pytest)
class TestHomeProductApi:  # 作用：首页与商品 API 测试类容器；调用关系：pytest 按类收集 test_* 方法；自定义/框架：自定义；来源(本文件)
    @allure.title("首页模块数据返回成功")  # 作用：Allure 用例中文标题；调用关系：test_home_index；自定义/框架：框架(allure)；来源(allure)
    def test_home_index(self, product_api):  # 作用：断言首页 index 接口返回 moduleList；调用关系：product_api fixture → home_index；自定义/框架：自定义测试方法；来源(本文件)
        data = product_api.home_index()  # 作用：调用首页聚合数据 API；调用关系：ProductApiClient.home_index → GET 接口；自定义/框架：自定义；来源(api/client/product_client.py)
        assert data.get("moduleList")  # 作用：断言响应含 moduleList 且非空；调用关系：pytest assert；自定义/框架：框架(pytest)；来源(Python assert)

    @allure.title("热门分类列表不为空")  # 作用：Allure 用例标题；调用关系：test_hot_categories；自定义/框架：框架(allure)；来源(allure)
    def test_hot_categories(self, product_api):  # 作用：验证热门分类接口有数据；调用关系：product_api.hot_categories；自定义/框架：自定义；来源(本文件)
        categories = product_api.hot_categories()  # 作用：请求热门分类列表；调用关系：ProductApiClient.hot_categories；自定义/框架：自定义；来源(api/client/product_client.py)
        assert len(categories) >= 1  # 作用：断言至少一条分类；调用关系：len + assert；自定义/框架：框架(pytest)；来源(Python)
        assert categories[0].get("categoryName")  # 作用：断言首条含 categoryName 字段；调用关系：dict.get；自定义/框架：自定义；来源(本文件)

    @allure.title("商品列表分页返回 records")  # 作用：Allure 标题；调用关系：test_product_list；自定义/框架：框架(allure)；来源(allure)
    def test_product_list(self, product_api):  # 作用：验证商品分页列表；调用关系：product_api.list_products；自定义/框架：自定义；来源(本文件)
        data = product_api.list_products(page=1, size=5)  # 作用：请求第 1 页 5 条商品；调用关系：ProductApiClient.list_products；自定义/框架：自定义；来源(api/client/product_client.py)
        records = data.get("records") or []  # 作用：提取 records 列表，缺省为空列表；调用关系：dict.get；自定义/框架：自定义；来源(本文件)
        assert len(records) >= 1  # 作用：断言有至少一条商品记录；调用关系：pytest assert；自定义/框架：框架(pytest)；来源(Python)

    @allure.title("关键词搜索商品有结果")  # 作用：Allure 标题；调用关系：test_search_products；自定义/框架：框架(allure)；来源(allure)
    def test_search_products(self, product_api, test_data):  # 作用：关键词搜索有结果；调用关系：product_api + test_data fixture；自定义/框架：自定义；来源(本文件)
        data = product_api.search_products(test_data["keyword"], size=5)  # 作用：按配置关键词搜索；调用关系：ProductApiClient.search_products、test_data["keyword"]；自定义/框架：自定义；来源(api/client/product_client.py + conftest)
        records = data.get("records") or []  # 作用：取搜索结果 records；调用关系：API 响应解析；自定义/框架：自定义；来源(本文件)
        assert len(records) >= 1  # 作用：断言搜索至少一条；调用关系：pytest assert；自定义/框架：框架(pytest)；来源(Python)

    @allure.title("商品详情含名称与 SKU")  # 作用：Allure 标题；调用关系：test_product_detail；自定义/框架：框架(allure)；来源(allure)
    def test_product_detail(self, product_api, test_data):  # 作用：验证商品详情含名称与 skuList；调用关系：product_api.product_detail；自定义/框架：自定义；来源(本文件)
        detail = product_api.product_detail(test_data["product_id"])  # 作用：请求默认商品详情；调用关系：ProductApiClient.product_detail、test_data；自定义/框架：自定义；来源(api/client/product_client.py)
        item = detail.get("item") or detail  # 作用：兼容 item 嵌套或扁平 JSON；调用关系：dict.get；自定义/框架：自定义；来源(本文件)
        assert item.get("productName")  # 作用：断言商品名称存在；调用关系：pytest assert；自定义/框架：框架(pytest)；来源(Python)
        assert detail.get("skuList")  # 作用：断言 SKU 列表存在；调用关系：detail 顶层字段；自定义/框架：自定义；来源(本文件)
