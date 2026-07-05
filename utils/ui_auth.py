# =============================================================================
# utils/ui_auth.py — 通过 UI 页面完成登录并引导获取 JWT Token （项目：utils/ui_auth.py）
# 作用：封装买家/后台 UI 登录流程，供 fixture 在 API 登录失败时降级为 UI 登录获取 token （项目：utils/ui_auth.py）
# 调用关系：被 conftest.py 调用；依赖 Page Object、WebDriverManager、session_sync.extract_token_from_browser （项目：utils/ui_auth.py）
# =============================================================================

# 导入 WebDriver：Selenium 浏览器驱动类型，传递给 Page Object 执行 UI 操作 （第三方：selenium → WebDriver）
from selenium.webdriver.remote.webdriver import WebDriver

# 从项目配置读取：后台 token 键名、前后台账号密码、前后台 UI 基础 URL （项目：config/settings.py）
from config.settings import (
    ADMIN_AUTH_TOKEN_KEY,   # 后台 JWT 在 localStorage 中的键名 （项目：config/settings.py → ADMIN_AUTH_TOKEN_KEY）
    ADMIN_PASSWORD,         # 后台默认登录密码 （项目：config/settings.py → ADMIN_PASSWORD）
    ADMIN_UI_BASE_URL,      # 后台管理界面基础 URL （项目：config/settings.py → ADMIN_UI_BASE_URL）
    ADMIN_USERNAME,         # 后台默认登录用户名 （项目：config/settings.py → ADMIN_USERNAME）
    BUYER_PASSWORD,         # 买家默认登录密码 （项目：config/settings.py → BUYER_PASSWORD）
    BUYER_USERNAME,         # 买家默认登录用户名 （项目：config/settings.py → BUYER_USERNAME）
    UI_BASE_URL,            # 前台商城基础 URL （项目：config/settings.py → UI_BASE_URL）
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(utils/ui_auth.py)
)
# 导入 WebDriver 生命周期管理：创建/销毁浏览器实例 （项目：ui/driver/driver_manager.py → WebDriverManager）
from ui.driver.driver_manager import WebDriverManager
# 导入后台登录页 Page Object：封装 Element Plus 后台登录表单操作 （项目：ui/pages/admin/login_page.py → AdminLoginPage）
from ui.pages.admin.login_page import AdminLoginPage
# 导入前台登录页 Page Object：封装 Tigshop 买家登录表单操作 （项目：ui/pages/front/login_page.py → FrontLoginPage）
from ui.pages.front.login_page import FrontLoginPage
# 导入 token 提取：UI 登录成功后从 localStorage 读取 JWT （项目：utils/session_sync.py → extract_token_from_browser）
from utils.session_sync import extract_token_from_browser


# 通过前台 UI 页面登录买家账号 （项目：utils/ui_auth.py → login_buyer_via_ui）
def login_buyer_via_ui(driver: WebDriver, username: str = None, password: str = None) -> None:
    # 实例化前台登录页，传入 driver 与前台基础 URL （项目：ui/pages/front/login_page.py → FrontLoginPage.__init__）
    page = FrontLoginPage(driver, UI_BASE_URL)
    # 调用 Page Object 的 login 方法：username/password 未传时使用 settings 默认买家账号 （项目：ui/pages/front/login_page.py → FrontLoginPage.login）
    page.login(username or BUYER_USERNAME, password or BUYER_PASSWORD)


# 通过后台 UI 页面登录管理员账号 （项目：utils/ui_auth.py → login_admin_via_ui）
def login_admin_via_ui(driver: WebDriver, username: str = None, password: str = None) -> None:
    # 实例化后台登录页，传入 driver 与后台基础 URL （项目：ui/pages/admin/login_page.py → AdminLoginPage.__init__）
    page = AdminLoginPage(driver, ADMIN_UI_BASE_URL)
    # 调用 Page Object 的 login 方法：username/password 未传时使用 settings 默认后台账号 （项目：ui/pages/admin/login_page.py → AdminLoginPage.login）
    page.login(username or ADMIN_USERNAME, password or ADMIN_PASSWORD)


# 独立启动浏览器、UI 登录买家、提取 token 后关闭浏览器 （项目：utils/ui_auth.py → bootstrap_buyer_token_via_ui）
def bootstrap_buyer_token_via_ui() -> str:
    # 通过 WebDriverManager 创建新的 Chrome WebDriver 实例（headless 与否由 settings 控制） （项目：ui/driver/driver_manager.py → WebDriverManager.create_driver）
    driver = WebDriverManager.create_driver()
# 作用：尝试执行可能失败的操作；调用关系：异常处理块；自定义/框架：Python 内置；来源(try)
    try:
        # 在当前 driver 上执行买家 UI 登录流程 （项目：utils/ui_auth.py → login_buyer_via_ui）
        login_buyer_via_ui(driver)
        # 登录成功后从浏览器 localStorage 读取买家 JWT （项目：utils/session_sync.py → extract_token_from_browser）
        token = extract_token_from_browser(driver)
        # 未获取到 token 时抛出错误，说明 UI 登录可能失败或 localStorage 键名不匹配 （Python 内置：RuntimeError）
        if not token:
# 作用：抛出异常；调用关系：错误向上传递；自定义/框架：Python 内置；来源(raise)
            raise RuntimeError("UI 登录后未获取到买家 token")
        # 返回 token 字符串，供 conftest 写入 API Session （Python 内置：return）
        return token
# 作用：无论成败都执行的清理逻辑；调用关系：try/finally；自定义/框架：Python 内置；来源(finally)
    finally:
        # 无论成功或异常，都关闭浏览器释放资源 （项目：ui/driver/driver_manager.py → WebDriverManager.quit_driver）
        WebDriverManager.quit_driver(driver)


# 独立启动浏览器、UI 登录后台、提取 token 后关闭浏览器 （项目：utils/ui_auth.py → bootstrap_admin_token_via_ui）
def bootstrap_admin_token_via_ui() -> str:
    # 创建新的 WebDriver 实例用于后台登录 （项目：ui/driver/driver_manager.py → WebDriverManager.create_driver）
    driver = WebDriverManager.create_driver()
# 作用：尝试执行可能失败的操作；调用关系：异常处理块；自定义/框架：Python 内置；来源(try)
    try:
        # 在当前 driver 上执行后台 UI 登录流程 （项目：utils/ui_auth.py → login_admin_via_ui）
        login_admin_via_ui(driver)
        # 后台 token 键名可能与买家不同，传入后台专用候选键列表 （项目：config/settings.py → ADMIN_AUTH_TOKEN_KEY）
        token = extract_token_from_browser(driver, keys=[ADMIN_AUTH_TOKEN_KEY, "token", "adminToken"])
        # 未获取到 token 时抛出错误 （Python 内置：RuntimeError）
        if not token:
# 作用：抛出异常；调用关系：错误向上传递；自定义/框架：Python 内置；来源(raise)
            raise RuntimeError("UI 登录后未获取到后台 token")
        # 返回后台 JWT 供 admin_api fixture 使用 （Python 内置：return）
        return token
# 作用：无论成败都执行的清理逻辑；调用关系：try/finally；自定义/框架：Python 内置；来源(finally)
    finally:
        # 确保浏览器进程被关闭，避免僵尸 Chrome 占用资源 （项目：ui/driver/driver_manager.py → WebDriverManager.quit_driver）
        WebDriverManager.quit_driver(driver)
