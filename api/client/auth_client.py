# 导入 requests 库，logout 里需要捕获 requests 的异常类型 （第三方：requests）
import requests
# 从 typing 导入类型注解：Any 任意类型，Dict 字典类型 （标准库：typing）
from typing import Any, Dict
# 从基类模块导入 BaseApiClient，AuthApiClient 将继承它的 GET/POST/重试等能力 （项目：api/client/base_client.py → BaseApiClient）
from api.client.base_client import BaseApiClient


# 定义认证相关的 API 客户端类，继承 BaseApiClient （项目：api/client/auth_client.py → AuthApiClient）
class AuthApiClient(BaseApiClient):
    """Practice Software Testing 认证 API。"""

    # 用户登录：用邮箱和密码换取 access_token 等信息 （项目：api/client/auth_client.py → login）
    def login(self, email: str, password: str) -> Dict[str, Any]:
        # 向 /users/login 发送 POST，json= 会把字典自动序列化为 JSON 请求体 （项目：api/client/base_client.py → post）
        response = self.post("/users/login", json={"email": email, "password": password})
        # 检查 HTTP 状态并解析 JSON；若失败会在 Allure 里附加 "/users/login" 上下文 （项目：api/client/base_client.py → json_or_raise）
        data = self.json_or_raise(response, " /users/login")
        # 若响应里包含 access_token，就写入 session 请求头，后续接口自动带 Token （项目：api/client/base_client.py → set_token）
        if data.get("access_token"):
            self.set_token(data["access_token"])
        # 返回完整登录响应（可能含 token、用户信息等） （Python 内置：return）
        return data

    # 获取当前登录用户的信息（需要先 login 或 set_token） （项目：api/client/auth_client.py → get_me）
    def get_me(self) -> Dict[str, Any]:
        # 向 /users/me 发送 GET 请求 （项目：api/client/base_client.py → get）
        response = self.get("/users/me")
        # 解析 JSON 并返回用户信息字典 （项目：api/client/base_client.py → json_or_raise）
        return self.json_or_raise(response, " /users/me")

    # 退出登录：通知服务端注销会话 （项目：api/client/auth_client.py → logout）
    def logout(self) -> None:
        try:
            # 向 /users/logout 发送 POST；失败时可能抛 RequestException （项目：api/client/base_client.py → post）
            self.post("/users/logout")
        except requests.RequestException:
            # logout 失败也不影响测试继续，静默忽略所有 requests 相关异常 （第三方：requests → RequestException）
            pass
