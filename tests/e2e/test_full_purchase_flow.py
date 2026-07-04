# =============================================================================（项目：tests/e2e/test_full_purchase_flow.py → 章节分隔）
# tests/e2e/test_full_purchase_flow.py — API + UI 混合端到端购买流程测试（项目：tests/e2e/test_full_purchase_flow.py → 模块说明）
# 作用：串联登录、搜索、UI 加购、API 下单与查单，验证完整业务链路（项目：tests/e2e/ → 混合 E2E）
# =============================================================================（项目：tests/e2e/test_full_purchase_flow.py → 章节分隔）

# 导入 pytest（第三方：pytest → fixture/mark）
import pytest
# 导入 allure（第三方：allure → epic/feature/title）
import allure
# 导入 attach_json：将 JSON 附加到 Allure 报告（项目：utils/allure_helper.py → attach_json）
from utils.allure_helper import attach_json
# 导入 Token 同步工具：让 API 客户端与浏览器共享同一登录态（项目：utils/session_sync.py → sync_api_token_to_browser/sync_token_to_clients）
from utils.session_sync import sync_api_token_to_browser, sync_token_to_clients


# Allure epic（第三方：allure → epic）
@allure.epic("Practice Software Testing")
# Allure feature：混合 E2E（API 与 UI 协作）（第三方：allure → feature）
@allure.feature("混合 E2E")
# pytest 标记：端到端测试（第三方：pytest → mark.e2e）
@pytest.mark.e2e
# 冒烟测试：核心业务流程（第三方：pytest → mark.smoke）
@pytest.mark.smoke
# 失败重试，提高 UI 步骤稳定性（第三方：pytest → mark.flaky）
@pytest.mark.flaky(reruns=2, reruns_delay=2)
class TestFullPurchaseFlow:
    """API + UI 混合购买流程。"""

    # 用例标题概括完整步骤（第三方：allure → title）
    @allure.title("登录→搜索→UI加购→API下单→查单")
    def test_full_purchase_flow_hybrid(
        self,
        driver,          # 未登录或待同步 Token 的 WebDriver（项目：tests/conftest.py → driver）
        base_url,        # UI 站点根地址（项目：tests/conftest.py → base_url）
        auth_api,        # 认证 API 客户端（项目：tests/conftest.py → auth_api）
        product_api,     # 商品/购物车 API 客户端（项目：tests/conftest.py → product_api）
        order_api,       # 订单 API 客户端（项目：tests/conftest.py → order_api）
        product_page,    # 商品页 Page Object（项目：tests/conftest.py → product_page）
        test_data,       # 邮箱、密码、关键词等测试数据（项目：tests/conftest.py → test_data）
    ):
        # ---------- 步骤 1：API 登录并同步 Token 到 API 客户端与浏览器 ----------（项目：tests/e2e/test_full_purchase_flow.py → 步骤注释）
        # 使用测试账号调用登录接口（项目：api/client/auth_client.py → login）
        login = auth_api.login(test_data["email"], test_data["password"])
        # 从登录响应中取出 access_token（JWT 或类似令牌）（Python 内置：dict 索引）
        token = login["access_token"]
        # 把 Token 设置到 product_api、order_api，后续 API 请求带同一身份（项目：utils/session_sync.py → sync_token_to_clients）
        sync_token_to_clients(token, product_api, order_api)
        # 把 Token 写入浏览器（Cookie/LocalStorage），UI 操作视为已登录（项目：utils/session_sync.py → sync_api_token_to_browser）
        sync_api_token_to_browser(driver, token, base_url)

        # ---------- 步骤 2：API 搜索商品 ----------（项目：tests/e2e/test_full_purchase_flow.py → 步骤注释）
        # 按关键词搜索，得到商品列表（项目：api/client/product_client.py → search）
        search = product_api.search(test_data["keyword"])
        # 取搜索结果中第一件商品，作为后续 UI 与下单对象（Python 内置：list 索引）
        product = search["data"][0]

        # ---------- 步骤 3：UI 打开商品页并加购 ----------（项目：tests/e2e/test_full_purchase_flow.py → 步骤注释）
        # Page Object 打开该商品详情页（项目：ui/pages/product_page.py → open_product）
        product_page.open_product(product["id"])
        # 验证页面标题包含商品名关键词，确保 UI 展示正确商品（Python 内置：assert/str.split）
        assert product["name"].split()[0].lower() in product_page.get_product_title().lower()
        # 在 UI 上点击加入购物车（项目：ui/pages/product_page.py → add_to_cart）
        product_page.add_to_cart()

        # ---------- 步骤 4：API 创建购物车、加购并提交订单 ----------（项目：tests/e2e/test_full_purchase_flow.py → 步骤注释）
        # 新建一个空购物车（与 UI 购物车可能独立，此处用 API 路径完成下单）（项目：api/client/product_client.py → create_cart）
        cart = product_api.create_cart()
        # 将同一商品加入 API 购物车（项目：api/client/product_client.py → add_to_cart）
        product_api.add_to_cart(cart["id"], product["id"])
        # 提交订单，返回发票/订单信息（项目：api/client/order_client.py → submit_order）
        invoice = order_api.submit_order(cart["id"])
        # 将下单结果附加到 Allure 报告（项目：utils/allure_helper.py → attach_json）
        attach_json(invoice, name="提交订单结果")

        # ---------- 步骤 5：API 验证订单列表 ----------（项目：tests/e2e/test_full_purchase_flow.py → 步骤注释）
        # 查询当前用户订单列表（项目：api/client/order_client.py → list_orders）
        orders = order_api.list_orders()
        # 从发票中取单号或 id 字符串，用于在列表结果中检索（Python 内置：dict.get/str）
        invoice_number = invoice.get("invoice_number") or str(invoice.get("id", ""))
        # 断言：列表数据中应能匹配到本单号或商品名，证明下单成功且可查（Python 内置：assert/in/str）
        assert invoice_number in str(orders) or product["name"] in str(orders)
