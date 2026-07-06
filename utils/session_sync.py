# =============================================================================
# utils/session_sync.py — 浏览器 localStorage 与 API Session 的 Token 同步工具 （项目：utils/session_sync.py）
# 作用：在 UI 登录与 requests API 客户端之间双向传递 JWT，支撑 E2E「UI 操作 + API 断言」模式 （项目：utils/session_sync.py）
# 调用关系：被 conftest.py、ui_auth.py、E2E 用例调用；依赖 wait_helper、popup_handler、config.settings （项目：utils/session_sync.py）
# =============================================================================

# 导入 Optional：类型注解，表示可能为 None 的返回值或参数 （标准库：typing）
from typing import Optional

# 导入 WebDriver：Selenium 远程浏览器驱动类型，用于 execute_script 读写 localStorage （第三方：selenium → WebDriver）
from selenium.webdriver.remote.webdriver import WebDriver

# 从项目配置读取：买家/后台 token 在 localStorage 中的键名、前台 UI 基础 URL （项目：config/settings.py → AUTH_TOKEN_KEY 等）
from config.settings import AUTH_TOKEN_KEY, ADMIN_AUTH_TOKEN_KEY, UI_BASE_URL
# 导入页面就绪等待：注入 token 后刷新页面前后需等待 SPA 稳定 （项目：utils/wait_helper.py → wait_for_page_ready）
from utils.wait_helper import wait_for_page_ready
# 导入弹窗处理器：token 注入并刷新后关闭可能出现的 Cookie/模态框遮挡 （项目：utils/popup_handler.py → PopupHandler）
from utils.popup_handler import PopupHandler


# 从浏览器 localStorage 提取 Tigshop JWT token （项目：utils/session_sync.py → extract_token_from_browser）
def extract_token_from_browser(driver: WebDriver, keys: Optional[list] = None) -> Optional[str]:
    """从 localStorage 读取 Tigshop JWT。"""
    # 若调用方未指定 keys，使用默认候选键列表（买家 token 键 + 常见别名 + 后台键 + 通用 token） （项目：config/settings.py → AUTH_TOKEN_KEY）
    candidates = keys or [AUTH_TOKEN_KEY, "accessToken", "userToken", ADMIN_AUTH_TOKEN_KEY, "token"]
    # 按顺序遍历每个 localStorage 键名，找到第一个非空值即返回 （Python 内置：for）
    for key in candidates:
        # 通过 Selenium 在页面上下文执行 JS，读取 window.localStorage 指定键 （第三方：selenium → WebDriver.execute_script）
        token = driver.execute_script("return window.localStorage.getItem(arguments[0]);", key)
        # 若该键存在且值非空/非 null，转为字符串并返回 （Python 内置：if, str, return）
        if token:
# 作用：返回结果给调用方；调用关系：函数出口；自定义/框架：Python 内置；来源(return)
            return str(token)
    # 兜底：前端 token 键名不固定（买家/后台不一致，或被 JSON 包裹），遍历所有 localStorage 查找形如 JWT(eyJ 开头) 的值 （第三方：selenium → WebDriver.execute_script）
    token = driver.execute_script(
        r"""
        const isJwt = v => typeof v === 'string' && /^eyJ[\w-]+\.[\w-]+\./.test(v);
        for (let i = 0; i < localStorage.length; i++) {
          const raw = localStorage.getItem(localStorage.key(i));
          if (!raw) continue;
          if (isJwt(raw)) return raw;
          try {
            const stack = [JSON.parse(raw)];
            while (stack.length) {
              const cur = stack.pop();
              if (cur && typeof cur === 'object') {
                for (const val of Object.values(cur)) {
                  if (isJwt(val)) return val;
                  if (val && typeof val === 'object') stack.push(val);
                }
              }
            }
          } catch (e) {}
        }
        return null;
        """
    )
    # localStorage 找到 JWT 直接返回 （Python 内置：if, str, return）
    if token:
        return str(token)
    # 兜底：Tigshop 买家前台把 JWT 存在 cookie(如 accessToken) 而非 localStorage，遍历 cookie 查找候选名或形如 JWT 的值 （第三方：selenium → WebDriver.get_cookies）
    import re  # 延迟导入正则，用于识别 JWT 格式的 cookie 值 （标准库：re）

    jwt_pattern = re.compile(r"^eyJ[\w-]+\.[\w-]+\.")  # JWT 三段式特征：eyJ 开头 + 两个点分隔 （标准库：re）
    cookies = driver.get_cookies()  # 读取当前域下全部 cookie（含 httpOnly） （第三方：selenium → WebDriver.get_cookies）
    # 优先按候选名精确匹配 cookie （Python 内置：for）
    for cookie in cookies:
        if cookie.get("name") in candidates and cookie.get("value"):
            return str(cookie["value"])
    # 再兜底：任意值形如 JWT 的 cookie （Python 内置：for）
    for cookie in cookies:
        if jwt_pattern.match(str(cookie.get("value", ""))):
            return str(cookie["value"])
    # 所有存储均未找到 token 时返回 None，表示确实未登录或未持久化 token （Python 内置：return None）
    return None


# 将浏览器中的 token 同步到多个 API 客户端 Session Header （项目：utils/session_sync.py → sync_browser_token_to_clients）
def sync_browser_token_to_clients(driver: WebDriver, *clients) -> str:
    # 调用本模块 extract_token_from_browser 从当前 driver 的 localStorage 读取 JWT （项目：utils/session_sync.py → extract_token_from_browser）
    token = extract_token_from_browser(driver)
    # 未读到 token 时抛出运行时错误，提示检查 UI 登录是否成功 （Python 内置：RuntimeError）
    if not token:
# 作用：抛出异常；调用关系：错误向上传递；自定义/框架：Python 内置；来源(raise)
        raise RuntimeError("浏览器 localStorage 中未找到 token，请确认 UI 登录成功")
    # 遍历传入的所有 API 客户端（如 AuthClient、CartClient），逐个写入 Authorization Header （Python 内置：for）
    for client in clients:
        # 调用各客户端自定义 set_token 方法，将 JWT 写入 requests Session （项目：api/client/base_client.py → set_token）
        client.set_token(token)
    # 返回同步成功的 token 字符串，供用例或 fixture 后续断言/日志使用 （Python 内置：return）
    return token


# 将已有 token 注入浏览器 localStorage 并刷新，使 UI 处于已登录状态 （项目：utils/session_sync.py → inject_auth_token）
def inject_auth_token(driver: WebDriver, token: str, base_url: str = None) -> None:
    # 确定前台基础 URL：优先使用传入 base_url，否则用 settings 中的 UI_BASE_URL，并去掉末尾斜杠 （项目：config/settings.py → UI_BASE_URL）
    url = (base_url or UI_BASE_URL).rstrip("/")
    # 导航到前台首页，以便在同源上下文中操作 localStorage （第三方：selenium → WebDriver.get）
    driver.get(url)
    # 等待页面 document.readyState 就绪及 SPA 稳定，避免 JS 尚未加载时写 localStorage 失败 （项目：utils/wait_helper.py → wait_for_page_ready）
    wait_for_page_ready(driver)
    # 执行 JS 将 token 写入 localStorage，键名使用项目配置的 AUTH_TOKEN_KEY （第三方：selenium → WebDriver.execute_script）
    driver.execute_script(
# 作用：执行本行逻辑；调用关系：见上下文；自定义/框架：自定义；来源(utils/session_sync.py)
        "window.localStorage.setItem(arguments[0], arguments[1]);",
# 作用：执行本行逻辑；调用关系：见上下文；自定义/框架：自定义；来源(utils/session_sync.py)
        AUTH_TOKEN_KEY,
# 作用：执行本行逻辑；调用关系：见上下文；自定义/框架：自定义；来源(utils/session_sync.py)
        token,
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(utils/session_sync.py)
    )
    # 刷新页面使 Nuxt 应用读取新 token 并更新登录态 （第三方：selenium → WebDriver.refresh）
    driver.refresh()
    # 刷新后再次等待页面稳定，确保后续 UI 操作不因渲染未完成而 flaky （项目：utils/wait_helper.py → wait_for_page_ready）
    wait_for_page_ready(driver)
    # 实例化弹窗处理器并关闭刷新后可能出现的 Cookie/遮挡层，避免挡住后续点击 （项目：utils/popup_handler.py → PopupHandler.dismiss_all）
    PopupHandler(driver).dismiss_all()
