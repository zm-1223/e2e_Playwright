# =============================================================================
# api/client/base_client.py — Tigshop API 客户端基类 （项目：api/client/base_client.py）
# 作用：封装 HTTP 重试、JSON 解析、业务 code 校验、Bearer Token 与 Allure 附件 （项目：api/client/base_client.py → BaseApiClient）
# 说明：各业务 Client（auth/product/cart 等）继承本类；tests/conftest 创建 Session 并注入子类实例 （项目：tests/conftest.py）
# =============================================================================

# 导入 time：API 重试间隔时调用 sleep （标准库：time）
import time
# 导入 logging：记录每次 API 请求的方法、路径与尝试次数 （标准库：logging）
import logging
# 导入 Any/Dict/Optional：类型注解，表示任意类型、字典、可选参数 （标准库：typing）
from typing import Any, Dict, Optional

# 导入 requests：发起 HTTP 请求并维护 Session/Cookie （第三方：requests）
import requests

# 导入 attach_text：HTTP/业务错误时将响应摘要附加到 Allure 报告 （项目：utils/allure_helper.py → attach_text）
from utils.allure_helper import attach_text

# 为本模块创建 logger，日志名称为 api.client.base_client （标准库：logging.getLogger）
logger = logging.getLogger(__name__)


# 自定义业务异常：HTTP 200 但响应体 code != 0 时抛出 （项目：api/client/base_client.py → TigshopApiError）
class TigshopApiError(Exception):
    """Tigshop 业务层错误：HTTP 200 但 code != 0。"""

    # 构造异常：保存服务端 message 与完整 payload，供测试断言或日志使用 （项目：api/client/base_client.py → TigshopApiError.__init__）
    def __init__(self, message: str, payload: Dict[str, Any]):
        # 调用 Exception 基类，设置异常展示文案 （Python 内置：super, Exception）
        super().__init__(message)
        # 挂载完整 JSON 响应体，便于调试业务错误字段 （项目：api/client/base_client.py → TigshopApiError.payload）
        self.payload = payload


# API 客户端基类：网络重试 + Tigshop {code,message,data} 解析 （项目：api/client/base_client.py → BaseApiClient）
class BaseApiClient:
    """API 客户端基类：网络重试 + Tigshop {code,message,data} 解析。"""

    # 初始化：绑定 base_url、创建或复用 requests.Session、设置通用请求头 （项目：tests/conftest.py → buyer_auth_api 等 fixture 调用）
    def __init__(self, base_url: str, session: Optional[requests.Session] = None) -> None:
        # 延迟导入 API_USER_AGENT，避免与 config.settings 循环依赖 （项目：config/settings.py → API_USER_AGENT）
        from config.settings import API_USER_AGENT

        # 去掉 base_url 末尾斜杠，便于与 path 拼接 （Python 内置：str.rstrip）
        self.base_url = base_url.rstrip("/")
        # 使用传入 Session（conftest 共享）或新建 Session 保持 Cookie/Token （第三方：requests → Session）
        self.session = session or requests.Session()
        # 设置 JSON API 常用头与浏览器 User-Agent，降低被 WAF 拦截概率 （第三方：requests → Session.headers.update）
        self.session.headers.update(
# 作用：执行本行逻辑；调用关系：见上下文；自定义/框架：自定义；来源(api/client/base_client.py)
            {
                "Accept": "application/json",           # 声明期望 JSON 响应 （项目：api/client/base_client.py → BaseApiClient.__init__）
                "Content-Type": "application/json",     # POST/PUT 默认 JSON 请求体 （项目：api/client/base_client.py → BaseApiClient.__init__）
                "User-Agent": API_USER_AGENT,           # 模拟 Chrome 浏览器标识 （项目：config/settings.py → API_USER_AGENT）
# 作用：执行本行逻辑；调用关系：见上下文；自定义/框架：自定义；来源(api/client/base_client.py)
            }
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(api/client/base_client.py)
        )

    # 内部方法：将相对 path 拼成完整 URL （项目：api/client/base_client.py → BaseApiClient._url）
    def _url(self, path: str) -> str:
        # 拼接 base_url 与去掉前导斜杠的 path （Python 内置：f-string, str.lstrip）
        return f"{self.base_url}/{path.lstrip('/')}"

    # 内部方法：带重试的 HTTP 请求，仅对连接错误/超时重试 （项目：api/client/base_client.py → BaseApiClient._request_with_retry）
    def _request_with_retry(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        # 延迟导入重试配置，与 settings 解耦 （项目：config/settings.py → API_RETRY_COUNT, API_RETRY_DELAY）
        from config.settings import API_RETRY_COUNT, API_RETRY_DELAY

        # 记录最后一次网络异常，全部重试失败后抛出 （Python 内置：Exception）
        last_error = None
        # 从第 1 次到 API_RETRY_COUNT 次循环尝试 （标准库：range）
        for attempt in range(1, API_RETRY_COUNT + 1):
# 作用：尝试执行可能失败的操作；调用关系：异常处理块；自定义/框架：Python 内置；来源(try)
            try:
                # 记录 INFO 日志：方法、路径、当前是第几次尝试 （标准库：logging.Logger.info）
                logger.info("API %s %s (attempt %s)", method, path, attempt)
                # GET 请求：调用 session.get 并传入 _url 与额外参数 （第三方：requests → Session.get）
                if method == "GET":
# 作用：返回结果给调用方；调用关系：函数出口；自定义/框架：Python 内置；来源(return)
                    return self.session.get(self._url(path), **kwargs)
                # POST 请求：调用 session.post （第三方：requests → Session.post）
                if method == "POST":
# 作用：返回结果给调用方；调用关系：函数出口；自定义/框架：Python 内置；来源(return)
                    return self.session.post(self._url(path), **kwargs)
                # DELETE 请求：调用 session.delete （第三方：requests → Session.delete）
                if method == "DELETE":
# 作用：返回结果给调用方；调用关系：函数出口；自定义/框架：Python 内置；来源(return)
                    return self.session.delete(self._url(path), **kwargs)
                # 非 GET/POST/DELETE 则抛出，由调用方感知不支持的方法 （Python 内置：ValueError）
                raise ValueError(f"不支持的方法: {method}")
            # 仅捕获连接失败与超时，其他异常直接向上抛 （第三方：requests → ConnectionError, Timeout）
            except (requests.ConnectionError, requests.Timeout) as exc:
                # 保存本次异常供最后一轮失败后 re-raise （Python 内置：Exception）
                last_error = exc
                # 已达最大重试次数则不再 sleep，直接抛出 （Python 内置：raise）
                if attempt >= API_RETRY_COUNT:
# 作用：抛出异常；调用关系：错误向上传递；自定义/框架：Python 内置；来源(raise)
                    raise
                # 等待 API_RETRY_DELAY 秒后进入下一轮重试 （标准库：time.sleep）
                time.sleep(API_RETRY_DELAY)
        # 理论上不可达；满足类型检查并抛出最后错误 （Python 内置：raise）
        raise last_error  # type: ignore[misc]

    # 公开方法：GET 请求的入口，委托 _request_with_retry （项目：api/client/* → self.get 调用）
    def get(self, path: str, **kwargs: Any) -> requests.Response:
        # 固定 method 为 GET 并转发 path 与 kwargs （项目：api/client/base_client.py → BaseApiClient.get）
        return self._request_with_retry("GET", path, **kwargs)

    # 公开方法：POST 请求的入口 （项目：api/client/* → self.post 调用）
    def post(self, path: str, **kwargs: Any) -> requests.Response:
        # 固定 method 为 POST 并转发 （项目：api/client/base_client.py → BaseApiClient.post）
        return self._request_with_retry("POST", path, **kwargs)

    # 公开方法：DELETE 请求的入口 （项目：api/client/* → self.delete 调用）
    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        # 固定 method 为 DELETE 并转发 （项目：api/client/base_client.py → BaseApiClient.delete）
        return self._request_with_retry("DELETE", path, **kwargs)

    # 校验 HTTP 状态码：非 2xx 时附加 Allure 文本并 re-raise （项目：api/client/base_client.py → BaseApiClient.raise_or_attach）
    def raise_or_attach(self, response: requests.Response, context: str = "") -> None:
# 作用：尝试执行可能失败的操作；调用关系：异常处理块；自定义/框架：Python 内置；来源(try)
        try:
            # 若 status_code 表示错误则抛出 HTTPError （第三方：requests → Response.raise_for_status）
            response.raise_for_status()
# 作用：捕获异常；调用关系：try/except 错误处理；自定义/框架：Python 内置；来源(except)
        except requests.HTTPError:
            # 将 URL、状态码、响应体前 2000 字符写入 Allure 附件 （项目：utils/allure_helper.py → attach_text）
            attach_text(
# 作用：执行本行逻辑；调用关系：见上下文；自定义/框架：自定义；来源(api/client/base_client.py)
                f"URL: {response.url}\nStatus: {response.status_code}\nBody: {response.text[:2000]}",
# 作用：赋值/绑定变量；调用关系：供后续步骤使用；自定义/框架：Python 内置；来源(赋值)
                name=f"API HTTP 错误{context}",
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(api/client/base_client.py)
            )
            # 继续向上抛出 HTTPError，让测试失败 （Python 内置：raise）
            raise

    # 解析 JSON 响应：先校验 HTTP，再返回 dict （项目：api/client/base_client.py → BaseApiClient.parse_json）
    def parse_json(self, response: requests.Response, context: str = "") -> Dict[str, Any]:
        # 确保 HTTP 层成功 （项目：api/client/base_client.py → BaseApiClient.raise_or_attach）
        self.raise_or_attach(response, context)
        # 将响应体反序列化为 Python 字典 （第三方：requests → Response.json）
        return response.json()

    # Tigshop 业务层解析：code==0 返回 data，否则抛 TigshopApiError 并附 Allure （项目：api/client/base_client.py → BaseApiClient.data_or_raise）
    def data_or_raise(self, response: requests.Response, context: str = "") -> Any:
        # 先走 HTTP 校验并拿到完整 JSON payload （项目：api/client/base_client.py → BaseApiClient.parse_json）
        payload = self.parse_json(response, context)
        # Tigshop 约定：code 非 0 表示业务失败 （Python 内置：dict.get）
        if payload.get("code") != 0:
            # 将 code/message/data 摘要附加到 Allure 便于排查 （项目：utils/allure_helper.py → attach_text）
            attach_text(
# 作用：执行本行逻辑；调用关系：见上下文；自定义/框架：自定义；来源(api/client/base_client.py)
                f"URL: {response.url}\nCode: {payload.get('code')}\nMessage: {payload.get('message')}\n"
# 作用：执行本行逻辑；调用关系：见上下文；自定义/框架：自定义；来源(api/client/base_client.py)
                f"Data: {str(payload.get('data'))[:2000]}",
# 作用：赋值/绑定变量；调用关系：供后续步骤使用；自定义/框架：Python 内置；来源(赋值)
                name=f"API 业务错误{context}",
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(api/client/base_client.py)
            )
            # 抛出自定义异常，tests 可 catch TigshopApiError （项目：api/client/base_client.py → TigshopApiError）
            raise TigshopApiError(str(payload.get("message")), payload)
        # 业务成功，返回 data 字段（可能为 dict/list/None） （Python 内置：dict.get）
        return payload.get("data")

    # 将 Bearer Token 写入 Session 请求头，后续请求自动带 Authorization （项目：api/client/auth_client.py → login 成功后调用）
    def set_token(self, token: str) -> None:
        # 设置 Authorization 头为 Bearer 格式 （第三方：requests → Session.headers 赋值）
        self.session.headers["Authorization"] = f"Bearer {token}"

    # 清除 Authorization 头，用于登出或切换账号场景 （项目：tests/conftest.py → fixture teardown 可能间接使用）
    def clear_token(self) -> None:
        # pop 键不存在时不报错，第二个参数 None 为默认值 （Python 内置：dict.pop）
        self.session.headers.pop("Authorization", None)
