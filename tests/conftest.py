# =============================================================================（项目：tests/conftest.py → 章节分隔）
# tests/conftest.py — pytest 全局配置文件（项目：tests/conftest.py → 模块说明）
# 作用：为 tests/ 下所有用例提供 Fixture（测试夹具）、Hook（钩子）、公共数据（第三方：pytest → fixture/hook）
# pytest 会自动加载此文件，无需在用例中 import（第三方：pytest → conftest 自动加载）
# =============================================================================（项目：tests/conftest.py → 章节分隔）

# 导入 sys：用于修改 Python 模块搜索路径，保证能 import 项目根目录下的包（标准库：sys）
import sys
# 导入 pytest：测试框架核心，提供 fixture / mark / hook 等能力（第三方：pytest → fixture/mark/hook）
import pytest
# 导入 requests：HTTP 库，api_session Fixture 用它创建可复用的 Session（第三方：requests → Session）
import requests
# 导入 Generator：类型注解，表示「生成器型 Fixture」（yield 前后可执行 setup/teardown）（标准库：typing → Generator）
from typing import Generator
# 导入 Path：面向对象的路径处理，比字符串拼接更安全（标准库：pathlib → Path）
from pathlib import Path

# ---------------------------------------------------------------------------（项目：tests/conftest.py → 章节分隔）
# 路径配置：把项目根目录加入 sys.path，使 `from config.xxx import` 能正常工作（标准库：sys.path）
# ---------------------------------------------------------------------------（项目：tests/conftest.py → 章节分隔）
# __file__ 是当前 conftest.py 的路径；.parent 是 tests/；再 .parent 是项目根 E2E_demo/（Python 内置：__file__）
ROOT_DIR = Path(__file__).resolve().parent.parent
# insert(0, ...) 插到搜索路径最前，优先从项目根导入模块（标准库：sys.path.insert）
sys.path.insert(0, str(ROOT_DIR))

# ---------------------------------------------------------------------------（项目：tests/conftest.py → 章节分隔）
# 从 config/settings.py 导入全局配置（非敏感项为常量，账号密码来自 .env）（项目：config/settings.py → 配置常量）
# ---------------------------------------------------------------------------（项目：tests/conftest.py → 章节分隔）
from config.settings import (
    API_BASE_URL,           # API 根地址，如 https://api.practicesoftwaretesting.com（项目：config/settings.py → API_BASE_URL）
    UI_BASE_URL,            # UI 根地址，如 https://practicesoftwaretesting.com（项目：config/settings.py → UI_BASE_URL）
    USER_EMAIL,             # 测试账号邮箱（来自 .env 或默认值）（项目：config/settings.py → USER_EMAIL）
    USER_PASSWORD,          # 测试账号密码（来自 .env 或默认值）（项目：config/settings.py → USER_PASSWORD）
    SCREENSHOTS_DIR,        # 失败截图保存目录 reports/screenshots/（项目：config/settings.py → SCREENSHOTS_DIR）
    DEFAULT_SEARCH_KEYWORD, # 默认搜索关键词，如 pliers（项目：config/settings.py → DEFAULT_SEARCH_KEYWORD）
)
# 三个 API 客户端：分别封装认证、商品/购物车、订单接口（项目：api/client/ → AuthApiClient/ProductApiClient/OrderApiClient）
from api.client.auth_client import AuthApiClient
from api.client.product_client import ProductApiClient
from api.client.order_client import OrderApiClient
# WebDriver 工厂：负责创建/销毁 Chrome/Edge 浏览器实例（项目：ui/driver/driver_manager.py → WebDriverManager）
from ui.driver.driver_manager import WebDriverManager
# Page Object：各页面对象，供 UI/E2E 用例直接调用页面操作（项目：ui/pages/ → Page Object）
from ui.pages.login_page import LoginPage
from ui.pages.home_page import HomePage
from ui.pages.search_page import SearchPage
from ui.pages.product_page import ProductPage
from ui.pages.cart_page import CartPage
from ui.pages.order_page import OrderPage
# Allure 辅助：ensure_dir 创建目录；attach_screenshot 失败时附截图到报告（项目：utils/allure_helper.py → ensure_dir/attach_screenshot）
from utils.allure_helper import ensure_dir, attach_screenshot
# 弹窗处理器：关闭 Cookie 横幅、模态框、alert 等遮挡（项目：utils/popup_handler.py → PopupHandler）
from utils.popup_handler import PopupHandler
# Token 注入：把 API 的 access_token 写入浏览器 localStorage（项目：utils/session_sync.py → inject_auth_token）
from utils.session_sync import inject_auth_token


# =============================================================================（项目：tests/conftest.py → 章节分隔）
# pytest Hook：测试会话开始时执行（整个 pytest 进程只跑一次）（第三方：pytest → pytest_sessionstart）
# =============================================================================（项目：tests/conftest.py → 章节分隔）
def pytest_sessionstart(session):
    """
    写入 Allure 环境信息。
    session 参数为 pytest 内置的 Session 对象，此处未直接使用但 Hook 签名要求保留。
    """
    # 延迟导入，避免 settings 与 conftest 循环依赖（此处其实无循环，属习惯写法）（项目：config/settings.py → ALLURE_RESULTS_DIR）
    from config.settings import ALLURE_RESULTS_DIR

    # 确保 Allure 结果目录存在（项目：utils/allure_helper.py → ensure_dir）
    ensure_dir(ALLURE_RESULTS_DIR)
    # 写入 environment.properties，Allure 报告「Environment」页会展示 UI/API 地址（第三方：allure → environment.properties）
    (ALLURE_RESULTS_DIR / "environment.properties").write_text(
        f"UI={UI_BASE_URL}\nAPI={API_BASE_URL}\n",
        encoding="utf-8",
    )


# =============================================================================（项目：tests/conftest.py → 章节分隔）
# Session 级 Fixture：整个测试会话只创建一次，所有用例共享（第三方：pytest → scope=session）
# =============================================================================（项目：tests/conftest.py → 章节分隔）

@pytest.fixture(scope="session")
def base_url() -> str:
    """UI 站点地址。供 driver、Page Object 等拼接页面 URL。"""
    return UI_BASE_URL


@pytest.fixture(scope="session")
def api_base_url() -> str:
    """API 站点地址。供 auth_api / product_api / order_api 拼接接口 URL。"""
    return API_BASE_URL


# =============================================================================（项目：tests/conftest.py → 章节分隔）
# Function 级 Fixture：每条测试用例独立创建/销毁，避免用例间状态污染（第三方：pytest → scope=function）
# =============================================================================（项目：tests/conftest.py → 章节分隔）

@pytest.fixture(scope="function")
def api_session() -> Generator[requests.Session, None, None]:
    """
    创建 requests.Session（HTTP 会话）。
    - yield 之前：setup，创建 Session
    - yield 之后：teardown，关闭 Session 释放连接
    同一用例内 auth_api / product_api / order_api 共用此 Session，Token 自动共享。
    """
    session = requests.Session()
    yield session          # 将 Session 注入到依赖此 Fixture 的测试/other fixture（第三方：pytest → yield fixture）
    session.close()        # 用例结束后关闭，防止连接泄漏（第三方：requests → Session.close）


@pytest.fixture(scope="function")
def auth_api(api_session, api_base_url) -> AuthApiClient:
    """
    认证 API 客户端。
    依赖：api_session（共享 Session）、api_base_url（API 根地址）
    """
    return AuthApiClient(base_url=api_base_url, session=api_session)


@pytest.fixture(scope="function")
def product_api(api_session, api_base_url) -> ProductApiClient:
    """商品/购物车 API 客户端。与 auth_api 共用 api_session。"""
    return ProductApiClient(base_url=api_base_url, session=api_session)


@pytest.fixture(scope="function")
def order_api(api_session, api_base_url) -> OrderApiClient:
    """订单 API 客户端。与 auth_api 共用 api_session。"""
    return OrderApiClient(base_url=api_base_url, session=api_session)


@pytest.fixture(scope="function")
def logged_in_api(auth_api, product_api) -> dict:
    """
    已登录的 API 状态（yield 型 Fixture）。
    - 前置：调用 login，断言返回 access_token；login 会把 Token 写入 Session Header
    - 后置：调用 logout 尝试清理（失败也不影响测试结果）
    依赖 product_api 是为确保 Session 已建立；实际登录只用 auth_api。
    """
    result = auth_api.login(USER_EMAIL, USER_PASSWORD)
    assert "access_token" in result   # 登录失败则当前用例 setup 阶段直接失败（Python 内置：assert）
    yield result                      # 把完整登录响应（含 token）交给测试用例（第三方：pytest → yield fixture）
    auth_api.logout()                 # teardown：用例结束后尝试登出（项目：api/client/auth_client.py → logout）


# =============================================================================（项目：tests/conftest.py → 章节分隔）
# 浏览器 Fixture：UI / E2E 测试专用（项目：tests/conftest.py → WebDriver Fixture）
# =============================================================================（项目：tests/conftest.py → 章节分隔）

@pytest.fixture(scope="function")
def driver(base_url) -> Generator:
    """
    裸 WebDriver：未登录，仅打开首页并关弹窗。
    - 每条用例独立浏览器，测完 quit
    """
    ensure_dir(SCREENSHOTS_DIR)                    # 确保截图目录存在（项目：utils/allure_helper.py → ensure_dir）
    web_driver = WebDriverManager.create_driver()  # 按 settings 创建 Chrome/Edge（项目：ui/driver/driver_manager.py → create_driver）
    web_driver.get(base_url)                       # 导航到 UI 首页（第三方：selenium → WebDriver.get）
    PopupHandler(web_driver).dismiss_all()         # 关闭可能出现的弹窗（项目：utils/popup_handler.py → dismiss_all）
    yield web_driver                               # 交给用例使用（第三方：pytest → yield fixture）
    WebDriverManager.quit_driver(web_driver)       # teardown：关闭浏览器（项目：ui/driver/driver_manager.py → quit_driver）


@pytest.fixture(scope="function")
def authenticated_driver(driver, auth_api, base_url) -> Generator:
    """
    已登录 WebDriver：API 登录后把 Token 注入 localStorage，UI 显示已登录态。
    依赖 driver → 复用同一浏览器实例，在其上注入 Token，而不是新开浏览器。
    """
    login = auth_api.login(USER_EMAIL, USER_PASSWORD)
    inject_auth_token(driver, login["access_token"], base_url)  # 写 localStorage + refresh（项目：utils/session_sync.py → inject_auth_token）
    yield driver   # 与 driver 是同一个 WebDriver 对象（第三方：pytest → yield fixture）


# =============================================================================（项目：tests/conftest.py → 章节分隔）
# Page Object Fixture：把 Page 类实例注入用例，用例无需自己 new Page（项目：ui/pages/ → Page Object）
# 全部依赖 authenticated_driver，即默认 UI 用例处于已登录状态（项目：tests/conftest.py → authenticated_driver）
# =============================================================================（项目：tests/conftest.py → 章节分隔）

@pytest.fixture(scope="function")
def login_page(authenticated_driver, base_url) -> LoginPage:
    """登录页 Page Object。"""
    return LoginPage(authenticated_driver, base_url)


@pytest.fixture(scope="function")
def home_page(authenticated_driver, base_url) -> HomePage:
    """首页 Page Object。"""
    return HomePage(authenticated_driver, base_url)


@pytest.fixture(scope="function")
def search_page(authenticated_driver, base_url) -> SearchPage:
    """搜索页 Page Object。"""
    return SearchPage(authenticated_driver, base_url)


@pytest.fixture(scope="function")
def product_page(authenticated_driver, base_url) -> ProductPage:
    """商品详情页 Page Object。"""
    return ProductPage(authenticated_driver, base_url)


@pytest.fixture(scope="function")
def cart_page(authenticated_driver, base_url) -> CartPage:
    """购物车页 Page Object。"""
    return CartPage(authenticated_driver, base_url)


@pytest.fixture(scope="function")
def order_page(authenticated_driver, base_url) -> OrderPage:
    """订单列表页 Page Object。"""
    return OrderPage(authenticated_driver, base_url)


# =============================================================================（项目：tests/conftest.py → 章节分隔）
# 测试数据 Fixture（项目：tests/conftest.py → test_data）
# =============================================================================（项目：tests/conftest.py → 章节分隔）

@pytest.fixture(scope="function")
def test_data() -> dict:
    """
    用例常用测试数据字典。
    敏感账号来自 settings；invalid / wrong 为写死的异常场景数据。
    """
    return {
        "email": USER_EMAIL,
        "password": USER_PASSWORD,
        "keyword": DEFAULT_SEARCH_KEYWORD,
        "invalid_product_id": "invalid-product-id-000",  # 用于 404 异常测试（项目：tests/conftest.py → test_data）
        "wrong_password": "wrong-password-xyz",            # 用于 401 登录失败测试（项目：tests/conftest.py → test_data）
    }


# =============================================================================（项目：tests/conftest.py → 章节分隔）
# 业务流程 Fixture：封装重复的「搜索 → 加购」准备步骤（项目：tests/conftest.py → 业务流程 Fixture）
# =============================================================================（项目：tests/conftest.py → 章节分隔）

@pytest.fixture(scope="function")
def first_product(logged_in_api, product_api, test_data) -> dict:
    """
    已登录状态下，按关键词搜索并返回第一个商品 dict（含 id、name 等）。
    依赖 logged_in_api 保证 API Session 带 Token。
    """
    result = product_api.search(test_data["keyword"])
    assert result.get("data"), f"关键词 '{test_data['keyword']}' 无搜索结果"
    return result["data"][0]


@pytest.fixture(scope="function")
def cart_with_product(logged_in_api, product_api, first_product) -> dict:
    """
    已登录且已加购的购物车 dict（含 cart id）。
    用于正常下单流程测试。
    """
    cart = product_api.create_cart()
    product_api.add_to_cart(cart["id"], first_product["id"])
    return cart


@pytest.fixture(scope="function")
def guest_cart_with_product(product_api, test_data) -> dict:
    """
    未登录状态下创建的购物车（不依赖 logged_in_api，Session 无 Token）。
    专门用于「未登录提交订单应 401」等权限异常测试。
    注意：若误用 cart_with_product，Session 已有 Token，401 断言会失败。
    """
    result = product_api.search(test_data["keyword"])
    assert result.get("data"), f"关键词 '{test_data['keyword']}' 无搜索结果"
    product = result["data"][0]
    cart = product_api.create_cart()
    product_api.add_to_cart(cart["id"], product["id"])
    return cart


# =============================================================================（项目：tests/conftest.py → 章节分隔）
# pytest Hook：每条用例执行后生成测试报告时触发（第三方：pytest → pytest_runtest_makereport）
# =============================================================================（项目：tests/conftest.py → 章节分隔）

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    用例失败时自动截图并附加到 Allure 报告。
    同时将截图保存到 reports/screenshots/，便于本地查看。
    """
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    if report.failed and report.when in ("call", "setup"):
        drv = item.funcargs.get("driver") or item.funcargs.get("authenticated_driver")
        if drv is not None:
            try:
                from datetime import datetime

                stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_stem = f"{item.name}_{report.when}_{stamp}"
                attach_screenshot(
                    drv,
                    name=f"失败截图_{item.name}",
                    save_dir=SCREENSHOTS_DIR,
                    filename=file_stem,
                )
            except Exception:
                pass
