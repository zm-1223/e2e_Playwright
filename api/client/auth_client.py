# =============================================================================
# api/client/auth_client.py — 买家认证与用户 API 客户端 （项目：api/client/auth_client.py）
# 作用：封装前台用户登录、获取用户详情等 /user/* 接口 （项目：api/client/auth_client.py → AuthApiClient）
# 说明：继承 BaseApiClient；由 tests/conftest.py 的 buyer_auth_api / logged_in_buyer_api 创建并注入测试 （项目：tests/conftest.py）
# =============================================================================

# 导入 Any/Dict：标注 login/get_user_detail 的返回值类型为字典 （标准库：typing）
from typing import Any, Dict

# 导入 BaseApiClient：复用 HTTP 重试、data_or_raise、set_token 等基类能力 （项目：api/client/base_client.py → BaseApiClient）
from api.client.base_client import BaseApiClient


# 买家认证与用户 API 客户端类 （项目：api/client/auth_client.py → AuthApiClient）
class AuthApiClient(BaseApiClient):
    """买家认证与用户 API。"""

    # 密码登录：POST /user/login/signin，成功后将 token 写入 Session （项目：tests/conftest.py → logged_in_buyer_api 调用）
    def login(self, username: str, password: str) -> Dict[str, Any]:
        # 发起 POST 登录请求，json 体符合 Tigshop 密码登录接口约定 （项目：api/client/base_client.py → BaseApiClient.post）
        response = self.post(
            "/user/login/signin",  # Tigshop 买家登录路径 （项目：api/client/auth_client.py → AuthApiClient.login）
# 作用：赋值/绑定变量；调用关系：供后续步骤使用；自定义/框架：Python 内置；来源(赋值)
            json={
                "login_type": "password",   # 登录方式：密码登录 （项目：api/client/auth_client.py → AuthApiClient.login）
                "username": username,         # 用户名，来自 settings 或测试参数 （项目：api/client/auth_client.py → AuthApiClient.login）
                "password": password,         # 密码 （项目：api/client/auth_client.py → AuthApiClient.login）
                "mobile": "",                 # 手机号登录字段，密码模式留空 （项目：api/client/auth_client.py → AuthApiClient.login）
                "mobile_code": "",            # 短信验证码，密码模式留空 （项目：api/client/auth_client.py → AuthApiClient.login）
                "verify_token": "",           # 图形/滑块验证 token，测试环境通常留空 （项目：api/client/auth_client.py → AuthApiClient.login）
# 作用：执行本行逻辑；调用关系：见上下文；自定义/框架：自定义；来源(api/client/auth_client.py)
            },
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(api/client/auth_client.py)
        )
        # 解析响应：HTTP 与 code 校验，失败抛 TigshopApiError （项目：api/client/base_client.py → BaseApiClient.data_or_raise）
        data = self.data_or_raise(response, " /user/login/signin")
        # 从 data 中取出 JWT token 字符串 （Python 内置：dict.get）
        token = data.get("token")
        # 若服务端返回 token，写入 Session Authorization 供后续 API 使用 （项目：api/client/base_client.py → BaseApiClient.set_token）
        if token:
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(api/client/auth_client.py)
            self.set_token(token)
        # 返回完整登录 data（含 token、用户信息等），供测试断言 （Python 内置：return）
        return data

    # 获取当前登录用户详情：GET /user/user/detail，需已 set_token （项目：tests/api/test_home_product_api.py 等调用）
    def get_user_detail(self) -> Dict[str, Any]:
        # 发起 GET 请求，Session 自动携带 Bearer Token （项目：api/client/base_client.py → BaseApiClient.get）
        response = self.get("/user/user/detail")
        # 解析并返回 data 字段中的用户详情 dict （项目：api/client/base_client.py → BaseApiClient.data_or_raise）
        return self.data_or_raise(response, " /user/user/detail")
