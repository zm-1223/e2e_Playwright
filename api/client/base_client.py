# 导入 time 模块，用于在请求失败后等待一段时间再重试 （标准库：time）
import time
# 导入 logging 模块，用于记录程序运行时的日志信息（如请求 URL、重试次数等） （标准库：logging）
import logging
# 导入 requests 库，这是 Python 中最常用的 HTTP 请求库，用来发送 GET/POST 等网络请求 （第三方：requests）
import requests
# 从 typing 模块导入类型注解：Any 表示任意类型，Dict 表示字典，Optional 表示“可以是某类型或 None” （标准库：typing）
from typing import Any, Dict, Optional
# 从项目工具模块导入 attach_text，失败时把 API 响应内容附加到 Allure 测试报告里 （项目：utils/allure_helper.py → attach_text）
from utils.allure_helper import attach_text

# 创建一个名为 logger 的日志记录器，__name__ 会自动变成当前模块名（如 api.client.base_client） （标准库：logging.getLogger）
logger = logging.getLogger(__name__)


# 定义 BaseApiClient 类，作为所有 API 客户端的“父类/基类” （项目：api/client/base_client.py → BaseApiClient）
class BaseApiClient:
    """API 客户端基类（含网络重试与失败附件）。"""

    # 构造函数：创建客户端实例时自动执行
    # base_url: API 服务器的基础地址，例如 "https://api.example.com"
    # session: 可选的 requests.Session 对象；不传则自动新建一个
    def __init__(self, base_url: str, session: Optional[requests.Session] = None) -> None:  # 初始化 API 客户端 （项目：api/client/base_client.py → __init__）
        # 去掉 base_url 末尾的 "/"，避免拼接 URL 时出现双斜杠 （标准库：str.rstrip）
        self.base_url = base_url.rstrip("/")
        # 若调用者没传 session，就新建 Session；Session 可以复用连接并保存 Cookie/请求头 （第三方：requests → Session）
        self.session = session or requests.Session()
        # 给 session 设置默认请求头，之后每次请求都会带上这些头 （第三方：requests → Session.headers）
        self.session.headers.update(
            {
                # 告诉服务器：客户端希望收到 JSON 格式的响应 （第三方：requests → Session.headers）
                "Accept": "application/json",
                # 告诉服务器：请求体也是 JSON 格式（POST 时常用） （第三方：requests → Session.headers）
                "Content-Type": "application/json",
            }
        )

    # 内部方法：把相对路径 path 拼成完整 URL （项目：api/client/base_client.py → _url）
    def _url(self, path: str) -> str:
        # lstrip("/") 去掉 path 开头的 "/"，再与 base_url 用 "/" 连接 （标准库：str.lstrip）
        return f"{self.base_url}/{path.lstrip('/')}"

    # 内部方法：带重试机制发送 HTTP 请求
    # method: 请求方法，如 "GET"、"POST"、"DELETE"
    # path: API 路径，如 "/users/login"
    # **kwargs: 其它参数会原样传给 requests（如 json=、params=）
    def _request_with_retry(self, method: str, path: str, **kwargs: Any) -> requests.Response:  # 带重试的 HTTP 请求 （项目：api/client/base_client.py → _request_with_retry）
        # 在函数内部导入配置，避免模块加载时就依赖 config（也可减少循环导入风险） （项目：config/settings.py）
        from config.settings import API_RETRY_COUNT, API_RETRY_DELAY

        # 用来保存最后一次发生的异常，若所有重试都失败则抛出 （Python 内置：Exception）
        last_error = None
        # 从第 1 次尝试到第 API_RETRY_COUNT 次，共尝试 API_RETRY_COUNT 次 （标准库：range）
        for attempt in range(1, API_RETRY_COUNT + 1):
            try:
                # 记录日志：当前方法、路径、第几次尝试 （标准库：logging.Logger.info）
                logger.info("API %s %s (attempt %s)", method, path, attempt)
                # 若是 GET 请求，调用 session.get 并立即返回响应 （第三方：requests → Session.get）
                if method == "GET":
                    return self.session.get(self._url(path), **kwargs)
                # 若是 POST 请求，调用 session.post 并立即返回响应 （第三方：requests → Session.post）
                if method == "POST":
                    return self.session.post(self._url(path), **kwargs)
                # 若是 DELETE 请求，调用 session.delete 并立即返回响应 （第三方：requests → Session.delete）
                if method == "DELETE":
                    return self.session.delete(self._url(path), **kwargs)
                # 若方法不是上面三种，抛出异常说明不支持 （Python 内置：ValueError）
                raise ValueError(f"不支持的方法: {method}")
            # 只捕获连接错误和超时，这两种情况适合重试 （第三方：requests → ConnectionError, Timeout）
            except (requests.ConnectionError, requests.Timeout) as exc:
                # 保存本次异常，以便最后可能再次抛出 （Python 内置：Exception）
                last_error = exc
                # 若已是最后一次尝试，不再等待，直接向上抛出异常 （项目：config/settings.py → API_RETRY_COUNT）
                if attempt >= API_RETRY_COUNT:
                    raise
                # 等待 API_RETRY_DELAY 秒后再进入下一轮循环重试 （标准库：time.sleep）
                time.sleep(API_RETRY_DELAY)
        # 理论上不应走到这里；若走到则抛出最后一次错误（type: ignore 告诉类型检查器忽略此行） （Python 内置：raise）
        raise last_error  # type: ignore[misc]

    # 对外公开的 GET 方法，内部委托给 _request_with_retry （项目：api/client/base_client.py → get）
    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return self._request_with_retry("GET", path, **kwargs)

    # 对外公开的 POST 方法，内部委托给 _request_with_retry （项目：api/client/base_client.py → post）
    def post(self, path: str, **kwargs: Any) -> requests.Response:
        return self._request_with_retry("POST", path, **kwargs)

    # 对外公开的 DELETE 方法，内部委托给 _request_with_retry （项目：api/client/base_client.py → delete）
    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        return self._request_with_retry("DELETE", path, **kwargs)

    # 检查 HTTP 状态码是否正常，并把响应体解析为 JSON 字典返回
    # context: 附加到 Allure 附件名称里的上下文，方便定位是哪个接口出错
    def json_or_raise(self, response: requests.Response, context: str = "") -> Dict[str, Any]:  # 解析 JSON 并校验状态 （项目：api/client/base_client.py → json_or_raise）
        """校验 HTTP 状态并解析 JSON；失败时自动附加响应到 Allure。"""
        # 先调用 raise_or_attach，非 2xx 会抛 HTTPError 并附加响应到报告 （项目：api/client/base_client.py → raise_or_attach）
        self.raise_or_attach(response, context)
        # 状态正常时，把响应正文解析为 Python 字典并返回 （第三方：requests → Response.json）
        return response.json()

    # 只检查 HTTP 状态码，不解析 JSON（例如 DELETE 可能没有 JSON 体） （项目：api/client/base_client.py → raise_or_attach）
    def raise_or_attach(self, response: requests.Response, context: str = "") -> None:
        """仅校验 HTTP 状态（无 JSON 体时使用）。"""
        try:
            # raise_for_status()：状态码为 4xx/5xx 时会抛出 requests.HTTPError （第三方：requests → Response.raise_for_status）
            response.raise_for_status()
        except requests.HTTPError:
            # 请求失败时，把 URL、状态码、响应体前 2000 字符写入 Allure 附件 （项目：utils/allure_helper.py → attach_text）
            attach_text(
                f"URL: {response.url}\n"
                f"Status: {response.status_code}\n"
                f"Body: {response.text[:2000]}",
                name=f"API 错误{context}",
            )
            # 重新抛出 HTTPError，让调用方知道请求失败了 （第三方：requests → HTTPError）
            raise

    # 设置 Bearer Token 到请求头，后续请求会自动带上 Authorization （项目：api/client/base_client.py → set_token）
    def set_token(self, token: str) -> None:
        self.session.headers["Authorization"] = f"Bearer {token}"  # 写入 Authorization 请求头 （第三方：requests → Session.headers）
