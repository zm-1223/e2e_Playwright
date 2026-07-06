# =============================================================================
# 文件：tests/conftest.py
# 作用：Pytest 全局 fixture 与钩子定义，为 UI/E2E/异常用例提供会话、登录态、页面对象与失败截图
# 调用关系：被 pytest 自动加载 → 注入各 tests/ui|e2e/**/test_*.py；依赖 config、api.client、ui.pages、utils
# 自定义/框架：自定义 fixture 编排 + pytest 框架钩子
# 来源（项目 tests 层公共配置，pytest 约定 conftest.py 自动发现）
# =============================================================================
import sys  # 作用：导入 Python 标准库 sys；调用关系：供 ROOT_DIR 插入 sys.path；自定义/框架：框架(Python 标准库)；来源(sys)
from pathlib import Path  # 作用：导入路径对象类 Path；调用关系：用于 ROOT_DIR 解析；自定义/框架：框架(Python 标准库)；来源(pathlib)
from typing import Generator  # 作用：导入泛型 Generator 类型注解；调用关系：标注 yield fixture 返回类型；自定义/框架：框架(typing)；来源(typing)

import pytest  # 作用：导入 pytest 测试框架；调用关系：装饰 fixture、hookimpl、session 钩子；自定义/框架：框架(pytest)；来源(第三方 pytest)
import requests  # 作用：导入 HTTP 客户端库；调用关系：api_session 创建 Session；自定义/框架：框架(requests)；来源(第三方 requests)

ROOT_DIR = Path(__file__).resolve().parent.parent  # 作用：计算项目根目录绝对路径；调用关系：供 sys.path 与后续模块导入；自定义/框架：自定义(项目路径常量)；来源(本文件)
sys.path.insert(0, str(ROOT_DIR))  # 作用：将项目根加入 Python 模块搜索路径；调用关系：使 config/api/ui/utils 可被 import；自定义/框架：框架(sys 标准库)；来源(Python import 机制)

from config.settings import (  # 作用：从项目配置模块批量导入环境常量；调用关系：fixture 与登录/截图使用；自定义/框架：自定义(config.settings)；来源(项目 config/settings.py)
    ADMIN_API_BASE_URL,  # 作用：后台 API 基址常量；调用关系：admin_api_base_url、AdminApiClient；自定义/框架：自定义；来源(config.settings)
    ADMIN_PASSWORD,  # 作用：后台演示账号密码；调用关系：logged_in_admin_api、admin_logged_in_driver；自定义/框架：自定义；来源(config.settings)
    ADMIN_UI_BASE_URL,  # 作用：后台 UI 基址；调用关系：admin_base_url、AdminLoginPage；自定义/框架：自定义；来源(config.settings)
    ADMIN_USERNAME,  # 作用：后台演示账号用户名；调用关系：admin 登录 fixture；自定义/框架：自定义；来源(config.settings)
    API_BASE_URL,  # 作用：前台买家 API 基址；调用关系：api_base_url、AuthApiClient 等；自定义/框架：自定义；来源(config.settings)
    BUYER_PASSWORD,  # 作用：买家演示密码；调用关系：test_data；自定义/框架：自定义；来源(config.settings)
    BUYER_USERNAME,  # 作用：买家演示用户名；调用关系：test_data；自定义/框架：自定义；来源(config.settings)
    DEFAULT_PRODUCT_ID,  # 作用：默认测试商品 ID；调用关系：test_data；自定义/框架：自定义；来源(config.settings)
    DEFAULT_SEARCH_KEYWORD,  # 作用：默认搜索关键词；调用关系：test_data；自定义/框架：自定义；来源(config.settings)
    INVALID_PRODUCT_ID,  # 作用：无效商品 ID；调用关系：test_data 异常用例；自定义/框架：自定义；来源(config.settings)
    SCREENSHOTS_DIR,  # 作用：失败截图保存目录；调用关系：front_driver、pytest_runtest_makereport；自定义/框架：自定义；来源(config.settings)
    UI_BASE_URL,  # 作用：前台 UI 基址；调用关系：front_base_url、WebDriver 导航；自定义/框架：自定义；来源(config.settings)
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(tests/conftest.py)
)
from api.client.auth_client import AuthApiClient  # 作用：导入买家认证 API 客户端；调用关系：buyer_auth_api、E2E 异常用例；自定义/框架：自定义；来源(api/client/auth_client.py)
from api.client.cart_client import CartApiClient  # 作用：导入购物车 API 客户端；调用关系：cart_api、E2E 加购清理；自定义/框架：自定义；来源(api/client/cart_client.py)
from api.client.order_client import OrderApiClient  # 作用：导入订单 API 客户端；调用关系：order_api fixture、E2E 结算断言；自定义/框架：自定义；来源(api/client/order_client.py)
from api.client.product_client import ProductApiClient  # 作用：导入商品 API 客户端；调用关系：product_api、E2E SKU 查询；自定义/框架：自定义；来源(api/client/product_client.py)
from ui.driver.driver_manager import WebDriverManager  # 作用：导入 WebDriver 生命周期管理器；调用关系：front_driver、登录回退；自定义/框架：自定义；来源(ui/driver/driver_manager.py)
from ui.pages.admin.coupon_page import AdminCouponPage  # 作用：导入后台优惠券页面对象；调用关系：admin_coupon_page fixture；自定义/框架：自定义；来源(ui/pages/admin/coupon_page.py)
from ui.pages.admin.login_page import AdminLoginPage  # 作用：导入后台登录页面对象；调用关系：admin_login_page、admin_logged_in_driver；自定义/框架：自定义；来源(ui/pages/admin/login_page.py)
from ui.pages.front.cart_page import FrontCartPage  # 作用：导入前台购物车页面对象；调用关系：front_cart_page fixture；自定义/框架：自定义；来源(ui/pages/front/cart_page.py)
from ui.pages.front.checkout_page import FrontCheckoutPage  # 作用：导入前台结算页面对象；调用关系：front_checkout_page fixture；自定义/框架：自定义；来源(ui/pages/front/checkout_page.py)
from ui.pages.front.coupon_page import FrontCouponPage  # 作用：导入前台优惠券页面对象；调用关系：front_coupon_page fixture；自定义/框架：自定义；来源(ui/pages/front/coupon_page.py)
from ui.pages.front.home_page import FrontHomePage  # 作用：导入前台首页页面对象；调用关系：front_home_page fixture；自定义/框架：自定义；来源(ui/pages/front/home_page.py)
from ui.pages.front.login_page import FrontLoginPage  # 作用：导入前台登录页面对象；调用关系：front_login_page fixture；自定义/框架：自定义；来源(ui/pages/front/login_page.py)
from ui.pages.front.member_page import FrontMemberPage  # 作用：导入前台会员中心页面对象；调用关系：front_member_page fixture；自定义/框架：自定义；来源(ui/pages/front/member_page.py)
from ui.pages.front.product_page import FrontProductPage  # 作用：导入前台商品详情页面对象；调用关系：front_product_page fixture；自定义/框架：自定义；来源(ui/pages/front/product_page.py)
from utils.allure_helper import attach_screenshot, ensure_dir  # 作用：导入 Allure 截图附件与目录创建工具；调用关系：session 初始化、失败截图；自定义/框架：自定义；来源(utils/allure_helper.py)
from utils.popup_handler import PopupHandler  # 作用：导入弹窗关闭处理器；调用关系：front_driver、admin_driver 启动后 dismiss；自定义/框架：自定义；来源(utils/popup_handler.py)
from utils.ui_auth import login_buyer_via_ui  # 作用：导入买家 UI 登录辅助；调用关系：buyer_driver fixture；自定义/框架：自定义；来源(utils/ui_auth.py)


def pytest_sessionstart(session):  # 作用：pytest 会话开始钩子，初始化 Allure 环境文件；调用关系：pytest 框架调用 → ensure_dir/write_text；自定义/框架：框架(pytest hook)；来源(pytest 钩子约定)
    from config.settings import ALLURE_RESULTS_DIR  # 作用：延迟导入 Allure 结果目录常量；调用关系：避免循环导入、写入 environment.properties；自定义/框架：自定义；来源(config.settings)

    ensure_dir(ALLURE_RESULTS_DIR)  # 作用：确保 Allure 结果目录存在；调用关系：自定义 ensure_dir；自定义/框架：自定义(utils.allure_helper)；来源(utils/allure_helper.py)
    (ALLURE_RESULTS_DIR / "environment.properties").write_text(  # 作用：写入 Allure 环境属性文件路径并写内容；调用关系：Path 拼接 + write_text；自定义/框架：框架(pathlib)；来源(Python pathlib)
        f"UI={UI_BASE_URL}\nADMIN={ADMIN_UI_BASE_URL}\nAPI={API_BASE_URL}\n",  # 作用：格式化环境变量文本供 Allure 报告展示；调用关系：引用 settings 常量；自定义/框架：自定义；来源(config.settings)
        encoding="utf-8",  # 作用：指定文件编码为 UTF-8；调用关系：write_text 参数；自定义/框架：框架(pathlib)；来源(Python)
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(tests/conftest.py)
    )


def pytest_sessionfinish(session, exitstatus):  # 作用：pytest 会话结束钩子，主进程生成 Allure HTML 报告；调用关系：pytest → generate_allure_report；自定义/框架：框架(pytest hook)；来源(pytest 钩子约定)
    if getattr(session.config, "workerinput", None) is not None:  # 作用：检测是否为 pytest-xdist  worker 子进程；调用关系：worker 跳过报告生成避免冲突；自定义/框架：框架(pytest-xdist 约定)；来源(pytest-xdist)
        return  # 作用：worker 进程直接返回不生成报告；调用关系：由 sessionfinish 提前结束；自定义/框架：自定义(分支逻辑)；来源(本文件)
    from generate_allure_report import generate_allure_report  # 作用：延迟导入报告生成脚本函数；调用关系：session 结束时调用；自定义/框架：自定义；来源(generate_allure_report.py)

    generate_allure_report(open_browser=False)  # 作用：生成 Allure HTML 报告且不自动打开浏览器；调用关系：调用项目脚本；自定义/框架：自定义；来源(generate_allure_report.py)


@pytest.fixture(scope="session")  # 作用：声明 session 级 pytest fixture 装饰器；调用关系：pytest 注入 front_base_url；自定义/框架：框架(pytest)；来源(pytest)
def front_base_url() -> str:  # 作用：提供前台 UI 基址字符串；调用关系：front_driver、buyer_driver 等依赖；自定义/框架：自定义 fixture；来源(本文件)
    return UI_BASE_URL  # 作用：返回 config 中的前台 URL；调用关系：读取 settings 常量；自定义/框架：自定义；来源(config.settings)


@pytest.fixture(scope="session")  # 作用：声明 session 级 fixture；调用关系：admin 相关 driver/page 依赖；自定义/框架：框架(pytest)；来源(pytest)
def admin_base_url() -> str:  # 作用：提供后台 UI 基址；调用关系：admin_driver、AdminLoginPage；自定义/框架：自定义 fixture；来源(本文件)
    return ADMIN_UI_BASE_URL  # 作用：返回后台 UI URL 常量；调用关系：settings；自定义/框架：自定义；来源(config.settings)


@pytest.fixture(scope="session")  # 作用：声明 session 级 API 基址 fixture；调用关系：买家 API client 依赖；自定义/框架：框架(pytest)；来源(pytest)
def api_base_url() -> str:  # 作用：提供前台 API 基址；调用关系：AuthApiClient、ProductApiClient 等；自定义/框架：自定义 fixture；来源(本文件)
    return API_BASE_URL  # 作用：返回 API_BASE_URL 常量；调用关系：config.settings；自定义/框架：自定义；来源(config.settings)


@pytest.fixture(scope="function")  # 作用：声明 function 级 fixture，每条用例独立实例；调用关系：E2E API 客户端依赖；自定义/框架：框架(pytest)；来源(pytest)
def api_session() -> Generator[requests.Session, None, None]:  # 作用：创建并 yield HTTP Session，用例结束 close；调用关系：buyer_auth_api 等注入 session；自定义/框架：自定义 fixture；来源(本文件)
    session = requests.Session()  # 作用：实例化 requests 会话对象；调用关系：requests 库；自定义/框架：框架(requests)；来源(requests)
    yield session  # 作用：将 session 交给测试用例使用；调用关系：pytest fixture yield 协议；自定义/框架：框架(pytest)；来源(pytest)
    session.close()  # 作用：用例 teardown 关闭连接释放资源；调用关系：api_session fixture 清理；自定义/框架：框架(requests)；来源(requests.Session.close)


@pytest.fixture(scope="function")  # 作用：function 级买家认证客户端 fixture；调用关系：E2E 异常用例 test_invalid_token_api；自定义/框架：框架(pytest)；来源(pytest)
def buyer_auth_api(api_session, api_base_url) -> AuthApiClient:  # 作用：组装 AuthApiClient；调用关系：依赖 api_session、api_base_url；自定义/框架：自定义 fixture；来源(本文件)
    return AuthApiClient(base_url=api_base_url, session=api_session)  # 作用：返回配置好 base_url 与 session 的客户端；调用关系：AuthApiClient 构造函数；自定义/框架：自定义；来源(api/client/auth_client.py)


@pytest.fixture(scope="function")  # 作用：function 级商品 API 客户端 fixture；调用关系：E2E 购物流程 SKU 查询；自定义/框架：框架(pytest)；来源(pytest)
def product_api(api_session, api_base_url) -> ProductApiClient:  # 作用：组装 ProductApiClient；调用关系：api_session、api_base_url；自定义/框架：自定义 fixture；来源(本文件)
    return ProductApiClient(base_url=api_base_url, session=api_session)  # 作用：返回商品 API 客户端实例；调用关系：ProductApiClient.__init__；自定义/框架：自定义；来源(api/client/product_client.py)


@pytest.fixture(scope="function")  # 作用：function 级购物车 API 客户端 fixture；调用关系：E2E 加购/清理；自定义/框架：框架(pytest)；来源(pytest)
def cart_api(api_session, api_base_url) -> CartApiClient:  # 作用：组装 CartApiClient；调用关系：api_session、api_base_url；自定义/框架：自定义 fixture；来源(本文件)
    return CartApiClient(base_url=api_base_url, session=api_session)  # 作用：返回购物车 API 客户端；调用关系：CartApiClient.__init__；自定义/框架：自定义；来源(api/client/cart_client.py)


@pytest.fixture(scope="function")  # 作用：function 级订单 API 客户端 fixture；调用关系：E2E 结算断言；自定义/框架：框架(pytest)；来源(pytest)
def order_api(api_session, api_base_url) -> OrderApiClient:  # 作用：组装 OrderApiClient；调用关系：api_session、api_base_url；自定义/框架：自定义 fixture；来源(本文件)
    return OrderApiClient(base_url=api_base_url, session=api_session)  # 作用：返回订单 API 客户端；调用关系：OrderApiClient.__init__；自定义/框架：自定义；来源(api/client/order_client.py)


@pytest.fixture(scope="function")  # 作用：function 级未登录前台 WebDriver；调用关系：UI 用例、front_login_page；自定义/框架：框架(pytest)；来源(pytest)
def front_driver(front_base_url) -> Generator:  # 作用：创建前台浏览器、打开首页、关闭弹窗后 yield；调用关系：WebDriverManager、PopupHandler；自定义/框架：自定义 fixture；来源(本文件)
    ensure_dir(SCREENSHOTS_DIR)  # 作用：确保截图目录存在；调用关系：失败截图保存；自定义/框架：自定义；来源(utils/allure_helper.py)
    driver = WebDriverManager.create_driver()  # 作用：实例化 Selenium WebDriver；调用关系：driver_manager；自定义/框架：自定义；来源(ui/driver/driver_manager.py)
    driver.get(front_base_url)  # 作用：导航至前台首页；调用关系：Selenium WebDriver.get；自定义/框架：框架(Selenium)；来源(selenium)
    PopupHandler(driver).dismiss_all()  # 作用：关闭广告/ cookie 等弹窗；调用关系：PopupHandler；自定义/框架：自定义；来源(utils/popup_handler.py)
    yield driver  # 作用：将 driver 注入用例；调用关系：pytest；自定义/框架：框架(pytest)；来源(pytest)
    WebDriverManager.quit_driver(driver)  # 作用：用例结束关闭浏览器；调用关系：teardown；自定义/框架：自定义；来源(ui/driver/driver_manager.py)


@pytest.fixture(scope="function")  # 作用：function 级未登录后台 WebDriver；调用关系：admin_login_page；自定义/框架：框架(pytest)；来源(pytest)
def admin_driver(admin_base_url) -> Generator:  # 作用：创建后台浏览器并打开登录页；调用关系：WebDriverManager、PopupHandler；自定义/框架：自定义 fixture；来源(本文件)
    ensure_dir(SCREENSHOTS_DIR)  # 作用：确保截图目录；调用关系：allure_helper；自定义/框架：自定义；来源(utils/allure_helper.py)
    driver = WebDriverManager.create_driver()  # 作用：创建 WebDriver；调用关系：driver_manager；自定义/框架：自定义；来源(ui/driver/driver_manager.py)
    driver.get(admin_base_url)  # 作用：打开后台 UI 基址；调用关系：Selenium get；自定义/框架：框架(Selenium)；来源(selenium)
    PopupHandler(driver).dismiss_all()  # 作用：关闭弹窗；调用关系：PopupHandler；自定义/框架：自定义；来源(utils/popup_handler.py)
    yield driver  # 作用：yield driver 给用例；调用关系：pytest；自定义/框架：框架(pytest)；来源(pytest)
    WebDriverManager.quit_driver(driver)  # 作用：teardown 关闭浏览器；调用关系：driver_manager；自定义/框架：自定义；来源(ui/driver/driver_manager.py)


@pytest.fixture(scope="session")  # 作用：session 级已登录买家 WebDriver，全套件只创建/登录一次；调用关系：前台购物/会员/优惠券 UI 用例共享；自定义/框架：框架(pytest)；来源(pytest)
def buyer_driver(front_base_url) -> Generator:  # 作用：独立创建浏览器并只登录一次，供所有登录依赖用例复用，避免高频登录触发站点行为验证风控；调用关系：login_buyer_via_ui；自定义/框架：自定义 fixture；来源(本文件)
    ensure_dir(SCREENSHOTS_DIR)  # 作用：确保截图目录存在；调用关系：失败截图；自定义/框架：自定义；来源(utils/allure_helper.py)
    driver = WebDriverManager.create_driver()  # 作用：实例化 Selenium WebDriver；调用关系：driver_manager；自定义/框架：自定义；来源(ui/driver/driver_manager.py)
    driver.get(front_base_url)  # 作用：导航至前台首页；调用关系：Selenium WebDriver.get；自定义/框架：框架(Selenium)；来源(selenium)
    PopupHandler(driver).dismiss_all()  # 作用：关闭弹窗；调用关系：PopupHandler；自定义/框架：自定义；来源(utils/popup_handler.py)
    login_buyer_via_ui(driver)  # 作用：通过 UI 登录买家账号（整套件仅此一次）；调用关系：utils.ui_auth；自定义/框架：自定义；来源(utils/ui_auth.py)
    yield driver  # 作用：返回已登录 driver，供所有登录依赖用例复用；调用关系：pytest；自定义/框架：框架(pytest)；来源(pytest)
    WebDriverManager.quit_driver(driver)  # 作用：session 结束关闭浏览器；调用关系：teardown；自定义/框架：自定义；来源(ui/driver/driver_manager.py)


@pytest.fixture(scope="function")  # 作用：function 级已登录后台 WebDriver；调用关系：admin_coupon_page；自定义/框架：框架(pytest)；来源(pytest)
def admin_logged_in_driver(admin_driver, admin_base_url) -> Generator:  # 作用：后台 POM 登录后 yield driver；调用关系：AdminLoginPage.login；自定义/框架：自定义 fixture；来源(本文件)
    AdminLoginPage(admin_driver, admin_base_url).login(ADMIN_USERNAME, ADMIN_PASSWORD)  # 作用：页面对象模式登录后台；调用关系：AdminLoginPage；自定义/框架：自定义；来源(ui/pages/admin/login_page.py)
    yield admin_driver  # 作用：向用例提供已登录后台 driver；调用关系：pytest；自定义/框架：框架(pytest)；来源(pytest)


@pytest.fixture(scope="function")  # 作用：前台首页 Page Object fixture；调用关系：可选直接注入（当前多用例内自建）；自定义/框架：框架(pytest)；来源(pytest)
def front_home_page(buyer_driver, front_base_url) -> FrontHomePage:  # 作用：返回已登录状态下的 FrontHomePage；调用关系：buyer_driver；自定义/框架：自定义 fixture；来源(本文件)
    return FrontHomePage(buyer_driver, front_base_url)  # 作用：实例化首页 POM；调用关系：FrontHomePage.__init__；自定义/框架：自定义；来源(ui/pages/front/home_page.py)


@pytest.fixture(scope="function")  # 作用：前台商品页 POM fixture；调用关系：购物流程 UI；自定义/框架：框架(pytest)；来源(pytest)
def front_product_page(buyer_driver, front_base_url) -> FrontProductPage:  # 作用：返回 FrontProductPage 实例；调用关系：buyer_driver；自定义/框架：自定义 fixture；来源(本文件)
    return FrontProductPage(buyer_driver, front_base_url)  # 作用：构造商品页面对象；调用关系：FrontProductPage；自定义/框架：自定义；来源(ui/pages/front/product_page.py)


@pytest.fixture(scope="function")  # 作用：前台购物车页 POM fixture；调用关系：test_cart_page_display；自定义/框架：框架(pytest)；来源(pytest)
def front_cart_page(buyer_driver, front_base_url) -> FrontCartPage:  # 作用：返回 FrontCartPage；调用关系：buyer_driver；自定义/框架：自定义 fixture；来源(本文件)
    return FrontCartPage(buyer_driver, front_base_url)  # 作用：实例化购物车 POM；调用关系：FrontCartPage；自定义/框架：自定义；来源(ui/pages/front/cart_page.py)


@pytest.fixture(scope="function")  # 作用：前台结算页 POM fixture；调用关系：test_checkout_page_display；自定义/框架：框架(pytest)；来源(pytest)
def front_checkout_page(buyer_driver, front_base_url) -> FrontCheckoutPage:  # 作用：返回 FrontCheckoutPage；调用关系：buyer_driver；自定义/框架：自定义 fixture；来源(本文件)
    return FrontCheckoutPage(buyer_driver, front_base_url)  # 作用：实例化结算页 POM；调用关系：FrontCheckoutPage；自定义/框架：自定义；来源(ui/pages/front/checkout_page.py)


@pytest.fixture(scope="function")  # 作用：前台会员中心 POM fixture；调用关系：TestFrontMemberUi；自定义/框架：框架(pytest)；来源(pytest)
def front_member_page(buyer_driver, front_base_url) -> FrontMemberPage:  # 作用：返回 FrontMemberPage；调用关系：buyer_driver；自定义/框架：自定义 fixture；来源(本文件)
    return FrontMemberPage(buyer_driver, front_base_url)  # 作用：实例化会员页 POM；调用关系：FrontMemberPage；自定义/框架：自定义；来源(ui/pages/front/member_page.py)


@pytest.fixture(scope="function")  # 作用：前台优惠券页 POM fixture；调用关系：TestFrontMemberUi 优惠券用例；自定义/框架：框架(pytest)；来源(pytest)
def front_coupon_page(buyer_driver, front_base_url) -> FrontCouponPage:  # 作用：返回 FrontCouponPage；调用关系：buyer_driver；自定义/框架：自定义 fixture；来源(本文件)
    return FrontCouponPage(buyer_driver, front_base_url)  # 作用：实例化优惠券页 POM；调用关系：FrontCouponPage；自定义/框架：自定义；来源(ui/pages/front/coupon_page.py)


@pytest.fixture(scope="function")  # 作用：未登录前台登录页 POM；调用关系：需测试登录页本身的用例；自定义/框架：框架(pytest)；来源(pytest)
def front_login_page(front_driver, front_base_url) -> FrontLoginPage:  # 作用：基于未登录 driver 返回登录页 POM；调用关系：front_driver；自定义/框架：自定义 fixture；来源(本文件)
    return FrontLoginPage(front_driver, front_base_url)  # 作用：实例化 FrontLoginPage；调用关系：FrontLoginPage；自定义/框架：自定义；来源(ui/pages/front/login_page.py)


@pytest.fixture(scope="function")  # 作用：未登录后台登录页 POM；调用关系：test_admin_login_page；自定义/框架：框架(pytest)；来源(pytest)
def admin_login_page(admin_driver, admin_base_url) -> AdminLoginPage:  # 作用：返回 AdminLoginPage；调用关系：admin_driver；自定义/框架：自定义 fixture；来源(本文件)
    return AdminLoginPage(admin_driver, admin_base_url)  # 作用：实例化后台登录页 POM；调用关系：AdminLoginPage；自定义/框架：自定义；来源(ui/pages/admin/login_page.py)


@pytest.fixture(scope="function")  # 作用：已登录后台优惠券页 POM；调用关系：test_admin_coupon_list；自定义/框架：框架(pytest)；来源(pytest)
def admin_coupon_page(admin_logged_in_driver, admin_base_url) -> AdminCouponPage:  # 作用：返回 AdminCouponPage；调用关系：admin_logged_in_driver；自定义/框架：自定义 fixture；来源(本文件)
    return AdminCouponPage(admin_logged_in_driver, admin_base_url)  # 作用：实例化后台优惠券 POM；调用关系：AdminCouponPage；自定义/框架：自定义；来源(ui/pages/admin/coupon_page.py)


@pytest.fixture(scope="function")  # 作用：通用测试数据字典 fixture；调用关系：UI/E2E/异常用例；自定义/框架：框架(pytest)；来源(pytest)
def test_data() -> dict:  # 作用：聚合账号、关键词、商品 ID；调用关系：从 settings 读取；自定义/框架：自定义 fixture；来源(本文件)
    return {  # 作用：返回不可变语义上的配置快照 dict；调用关系：settings 常量；自定义/框架：自定义；来源(本文件)
        "username": BUYER_USERNAME,  # 作用：买家用户名键值；调用关系：登录相关用例；自定义/框架：自定义；来源(config.settings)
        "password": BUYER_PASSWORD,  # 作用：买家密码键值；调用关系：潜在登录用例；自定义/框架：自定义；来源(config.settings)
        "admin_username": ADMIN_USERNAME,  # 作用：后台用户名；调用关系：test_admin_login；自定义/框架：自定义；来源(config.settings)
        "admin_password": ADMIN_PASSWORD,  # 作用：后台密码；调用关系：admin 登录；自定义/框架：自定义；来源(config.settings)
        "keyword": DEFAULT_SEARCH_KEYWORD,  # 作用：搜索关键词；调用关系：搜索类用例；自定义/框架：自定义；来源(config.settings)
        "product_id": DEFAULT_PRODUCT_ID,  # 作用：默认商品 ID；调用关系：商品/加购用例；自定义/框架：自定义；来源(config.settings)
        "invalid_product_id": INVALID_PRODUCT_ID,  # 作用：无效商品 ID；调用关系：test_invalid_product_page；自定义/框架：自定义；来源(config.settings)
# 作用：执行本行逻辑；调用关系：见上下文；自定义/框架：自定义；来源(tests/conftest.py)
    }


@pytest.hookimpl(tryfirst=True, hookwrapper=True)  # 作用：注册 pytest 报告钩子，优先执行且包装原钩子；调用关系：每条用例 setup/call/teardown；自定义/框架：框架(pytest hookimpl)；来源(pytest)
def pytest_runtest_makereport(item, call):  # 作用：生成用例阶段报告并在失败时截图；调用关系：pytest 内部 → attach_screenshot；自定义/框架：自定义 hook；来源(本文件)
    outcome = yield  # 作用：委托 pytest 生成 report 对象；调用关系：hookwrapper 协议；自定义/框架：框架(pytest)；来源(pytest)
    report = outcome.get_result()  # 作用：取得 TestReport 实例；调用关系：outcome.get_result；自定义/框架：框架(pytest)；来源(pytest)
    setattr(item, f"rep_{report.when}", report)  # 作用：将 report 挂到 item 供其他 fixture 读取；调用关系：item 动态属性；自定义/框架：自定义；来源(本文件)

    if report.failed and report.when in ("call", "setup"):  # 作用：仅在 setup/call 失败时截图；调用关系：report.failed/when；自定义/框架：自定义；来源(本文件)
        drv = item.funcargs.get("front_driver") or item.funcargs.get("buyer_driver")  # 作用：从前台 fixture 取 driver；调用关系：item.funcargs；自定义/框架：自定义；来源(本文件)
        drv = drv or item.funcargs.get("admin_driver") or item.funcargs.get("admin_logged_in_driver")  # 作用：若无前台 driver 则尝试后台；调用关系：funcargs 链式 or；自定义/框架：自定义；来源(本文件)
        if drv is not None:  # 作用：存在 WebDriver 才截图；调用关系：UI 用例；自定义/框架：自定义；来源(本文件)
            try:  # 作用：截图失败不影响 pytest 报告；调用关系：attach_screenshot；自定义/框架：自定义；来源(本文件)
                from datetime import datetime  # 作用：延迟导入时间模块；调用关系：生成文件名时间戳；自定义/框架：框架(Python 标准库)；来源(datetime)

                stamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # 作用：格式化当前时间为文件名；调用关系：datetime.now/strftime；自定义/框架：框架(Python)；来源(datetime)
                attach_screenshot(  # 作用：保存截图并附加到 Allure；调用关系：utils.allure_helper.attach_screenshot；自定义/框架：自定义；来源(utils/allure_helper.py)
                    drv,  # 作用：传入 WebDriver 截屏；调用关系：Selenium；自定义/框架：框架(Selenium)；来源(selenium)
                    name=f"失败截图_{item.name}",  # 作用：Allure 附件显示名；调用关系：item.name；自定义/框架：自定义；来源(本文件)
                    save_dir=SCREENSHOTS_DIR,  # 作用：本地保存目录；调用关系：settings；自定义/框架：自定义；来源(config.settings)
                    filename=f"{item.name}_{report.when}_{stamp}",  # 作用：本地文件名（含阶段与时间）；调用关系：item/report/stamp；自定义/框架：自定义；来源(本文件)
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(tests/conftest.py)
                )
            except Exception:  # 作用：吞掉截图异常；调用关系：保证 hook 不崩溃；自定义/框架：自定义；来源(本文件)
                pass  # 作用：忽略截图错误；调用关系：except 分支；自定义/框架：自定义；来源(本文件)
