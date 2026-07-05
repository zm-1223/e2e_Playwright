# =============================================================================
# api/client/admin_client.py — 后台管理 API 客户端 （项目：api/client/admin_client.py）
# 作用：封装管理员登录、优惠券列表等 /adminapi/* 接口 （项目：api/client/admin_client.py → AdminApiClient）
# 说明：base_url 为 ADMIN_API_BASE_URL；由 conftest 的 admin_api / logged_in_admin_api 实例化 （项目：tests/conftest.py）
# =============================================================================

# 导入 Any/Dict/List：标注 API 返回结构与 coupon_names 列表类型 （标准库：typing）
from typing import Any, Dict, List

# 导入 BaseApiClient：复用 POST/GET、data_or_raise、set_token （项目：api/client/base_client.py → BaseApiClient）
from api.client.base_client import BaseApiClient


# 后台管理 API 客户端类 （项目：api/client/admin_client.py → AdminApiClient）
class AdminApiClient(BaseApiClient):
    """后台管理 API。"""

    # 管理员密码登录：POST /login/signin（相对 adminapi 根路径） （项目：tests/conftest.py → logged_in_admin_api 调用）
    def login(self, username: str, password: str) -> Dict[str, Any]:
        # 发起 POST 登录，json 体符合后台登录接口字段 （项目：api/client/base_client.py → BaseApiClient.post）
        response = self.post(
            "/login/signin",  # 后台登录路径（拼接在 ADMIN_API_BASE_URL 后） （项目：api/client/admin_client.py → AdminApiClient.login）
# 作用：赋值/绑定变量；调用关系：供后续步骤使用；自定义/框架：Python 内置；来源(赋值)
            json={
                "login_type": "password",   # 登录类型：密码 （项目：api/client/admin_client.py → AdminApiClient.login）
                "username": username,         # 管理员账号，通常来自 ADMIN_USERNAME （项目：api/client/admin_client.py → AdminApiClient.login）
                "password": password,         # 管理员密码 （项目：api/client/admin_client.py → AdminApiClient.login）
                "remember": False,            # 是否记住登录，测试固定 False （项目：api/client/admin_client.py → AdminApiClient.login）
                "verify_token": None,         # 验证码 token，测试环境为 None （项目：api/client/admin_client.py → AdminApiClient.login）
# 作用：执行本行逻辑；调用关系：见上下文；自定义/框架：自定义；来源(api/client/admin_client.py)
            },
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(api/client/admin_client.py)
        )
        # 校验响应并提取 data；context 便于 Allure 区分接口 （项目：api/client/base_client.py → BaseApiClient.data_or_raise）
        data = self.data_or_raise(response, " /adminapi/login/signin")
        # 读取返回的 admin token （Python 内置：dict.get）
        token = data.get("token")
        # 写入 Session，后续 promotion 等接口需管理员身份 （项目：api/client/base_client.py → BaseApiClient.set_token）
        if token:
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(api/client/admin_client.py)
            self.set_token(token)
        # 返回登录 data 供 fixture 或测试使用 （Python 内置：return）
        return data

    # 分页查询优惠券列表：GET /promotion/coupon/list （项目：tests/api/test_admin_api.py 调用）
    def list_coupons(self, page: int = 1, size: int = 10, keyword: str = "") -> Dict[str, Any]:
        # GET 带 query 参数 page/size/keyword （项目：api/client/base_client.py → BaseApiClient.get）
        response = self.get(
            "/promotion/coupon/list",  # 后台优惠券列表 API 路径 （项目：api/client/admin_client.py → AdminApiClient.list_coupons）
            params={"page": page, "size": size, "keyword": keyword},  # 分页与搜索关键词 （项目：api/client/admin_client.py → AdminApiClient.list_coupons）
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(api/client/admin_client.py)
        )
        # 返回分页 data（通常含 records、total 等） （项目：api/client/base_client.py → BaseApiClient.data_or_raise）
        return self.data_or_raise(response, " /promotion/coupon/list")

    # 便捷方法：从 list_coupons 结果提取非空 couponName 字符串列表 （项目：tests/api/test_admin_api.py → 断言优惠券名称）
    def coupon_names(self, page: int = 1, size: int = 10) -> List[str]:
        # 调用本类 list_coupons 获取分页数据 （项目：api/client/admin_client.py → AdminApiClient.list_coupons）
        data = self.list_coupons(page=page, size=size)
        # 取 records 列表，缺失时用空列表避免 None 迭代 （Python 内置：dict.get, or）
        records = data.get("records") or []
        # 列表推导：每条记录的 couponName 非空则收集 （Python 内置：list comprehension）
        return [item.get("couponName", "") for item in records if item.get("couponName")]
