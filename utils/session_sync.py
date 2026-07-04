# 导入 Selenium WebDriver 类型，表示浏览器驱动实例 （第三方：selenium → WebDriver）
from selenium.webdriver.remote.webdriver import WebDriver
# 导入 WebDriverWait，用于显式等待页面元素出现 （第三方：selenium → WebDriverWait）
from selenium.webdriver.support.ui import WebDriverWait
# 导入 expected_conditions 并简写为 EC，提供“元素可见/存在”等等待条件 （第三方：selenium → expected_conditions）
from selenium.webdriver.support import expected_conditions as EC
# 从配置读取：localStorage 里存 token 的键名、UI 站点基础地址 （项目：config/settings.py → AUTH_TOKEN_KEY, UI_BASE_URL）
from config.settings import AUTH_TOKEN_KEY, UI_BASE_URL
# 导入等待页面加载完成的工具函数 （项目：utils/wait_helper.py → wait_for_page_ready）
from utils.wait_helper import wait_for_page_ready
# 导入弹窗处理类，用于关闭页面上的遮挡弹窗 （项目：utils/popup_handler.py → PopupHandler）
from utils.popup_handler import PopupHandler


# 定义函数：把同一个 token 同步设置到多个 API 客户端 （项目：utils/session_sync.py → sync_token_to_clients）
def sync_token_to_clients(token: str, *clients) -> None:
    """将 Token 同步到多个 API 客户端。"""
    # *clients 表示可变数量的客户端对象，逐个设置 token （Python 内置：*args）
    for client in clients:
        # 调用每个客户端的 set_token 方法写入认证令牌 （项目：api/client/base_client.py → set_token）
        client.set_token(token)


# 定义函数：把 API 拿到的 access_token 注入浏览器 localStorage （项目：utils/session_sync.py → inject_auth_token）
def inject_auth_token(driver: WebDriver, token: str, base_url: str = None) -> None:
    """将 API access_token 写入浏览器 localStorage。"""
    # 使用传入的 base_url，否则用配置里的 UI_BASE_URL；rstrip("/") 去掉末尾斜杠 （项目：config/settings.py → UI_BASE_URL）
    url = (base_url or UI_BASE_URL).rstrip("/")
    # 先打开站点首页（或指定地址），以便在同源下操作 localStorage （第三方：selenium → WebDriver.get）
    driver.get(url)
    # 等待页面 DOM/资源加载到 readyState complete （项目：utils/wait_helper.py → wait_for_page_ready）
    wait_for_page_ready(driver)
    # 用 JavaScript 在浏览器里写入 localStorage：键 AUTH_TOKEN_KEY，值为 token （第三方：selenium → WebDriver.execute_script）
    driver.execute_script(
        "window.localStorage.setItem(arguments[0], arguments[1]);",
        AUTH_TOKEN_KEY,
        token,
    )
    # 刷新页面，让前端应用读取刚写入的 token 并完成登录态 （第三方：selenium → WebDriver.refresh）
    driver.refresh()
    # 刷新后再次等待页面就绪 （项目：utils/wait_helper.py → wait_for_page_ready）
    wait_for_page_ready(driver)
    # 创建弹窗处理器并关闭可能出现的广告/提示框 （项目：utils/popup_handler.py → PopupHandler.dismiss_all）
    PopupHandler(driver).dismiss_all()


# 定义函数：混合 E2E 场景——API 登录后的 token 同步到 UI 并验证已登录 （项目：utils/session_sync.py → sync_api_token_to_browser）
def sync_api_token_to_browser(
    driver: WebDriver,  # 浏览器驱动 （第三方：selenium → WebDriver）
    token: str,  # API 登录返回的 access_token （项目：utils/session_sync.py → sync_api_token_to_browser）
    base_url: str = None,  # 可选 UI 地址，默认用配置 （项目：config/settings.py → UI_BASE_URL）
) -> None:
    """混合 E2E：API Token 同步到 UI。"""
    # 先注入 token 并刷新、关弹窗 （项目：utils/session_sync.py → inject_auth_token）
    inject_auth_token(driver, token, base_url)
    # 最多等 15 秒，直到“我的账户”导航元素出现在 DOM 中（说明 UI 已识别登录态） （第三方：selenium → WebDriverWait, expected_conditions）
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(("css selector", "[data-test='nav-my-account']"))
    )
