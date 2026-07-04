# =============================================================================（项目：tests/api/test_auth_api.py → 章节分隔）
# tests/api/test_auth_api.py — 认证相关 API 接口测试（项目：tests/api/test_auth_api.py → 模块说明）
# 作用：验证登录、获取用户信息等认证接口在正常与异常场景下的行为（项目：api/client/auth_client.py → AuthApiClient）
# =============================================================================（项目：tests/api/test_auth_api.py → 章节分隔）

# 导入 pytest：Python 测试框架，提供测试运行、断言、Fixture 注入、异常捕获等能力（第三方：pytest → fixture/mark/raises）
import pytest
# 导入 allure：测试报告装饰器库，用于在 Allure 报告中展示分层标题与用例说明（第三方：allure → epic/feature/title）
import allure
# 导入 requests：HTTP 请求库；本文件用其 HTTPError 异常类型判断接口返回的错误状态码（第三方：requests → HTTPError）
import requests


# @allure.epic：在 Allure 报告最顶层分组，表示整个项目/产品的大模块名称（第三方：allure → epic）
@allure.epic("Practice Software Testing")
# @allure.feature：epic 下的功能模块，这里表示「认证」相关测试（第三方：allure → feature）
@allure.feature("认证")
# @pytest.mark.api：自定义标记，可通过 pytest -m api 只运行 API 层测试（第三方：pytest → mark.api）
@pytest.mark.api
# 定义测试类：pytest 会把类中以 test_ 开头的方法当作测试用例执行（第三方：pytest → 测试类发现）
class TestAuthApi:
    """认证 API 测试。"""

    # @allure.title：在 Allure 报告中显示本条用例的可读标题（第三方：allure → title）
    @allure.title("登录成功返回 access_token")
    # test_ 前缀的方法会被 pytest 识别为测试用例（第三方：pytest → 用例发现）
    # auth_api、test_data 来自 conftest.py 中的 Fixture，pytest 会自动注入（项目：tests/conftest.py → auth_api/test_data）
    def test_login_success(self, auth_api, test_data):
        # 调用认证客户端的 login 方法，传入测试数据中的邮箱和密码（项目：api/client/auth_client.py → login）
        result = auth_api.login(test_data["email"], test_data["password"])
        # assert 断言：登录响应中必须包含 access_token 字段且值不为空（Python 内置：assert）
        assert result.get("access_token")
        # 登录成功后，调用 get_me 获取当前登录用户信息（项目：api/client/auth_client.py → get_me）
        me = auth_api.get_me()
        # 断言返回的用户邮箱与测试账号邮箱一致，证明 Token 有效且身份正确（Python 内置：assert）
        assert me["email"] == test_data["email"]

    # Allure 报告标题：描述「错误密码应登录失败」这一场景（第三方：allure → title）
    @allure.title("错误密码登录失败")
    def test_login_wrong_password(self, auth_api, test_data):
        # with pytest.raises(...)：期望 with 代码块内会抛出指定类型的异常（第三方：pytest → raises）
        # as exc：把捕获到的异常对象保存到变量 exc，便于后续检查（Python 内置：with/as）
        with pytest.raises(requests.HTTPError) as exc:
            # 使用错误密码尝试登录，接口应返回 HTTP 错误而非成功（项目：api/client/auth_client.py → login）
            auth_api.login(test_data["email"], test_data["wrong_password"])
        # exc.value 是实际的 HTTPError 实例；response.status_code 是 HTTP 状态码（第三方：requests → HTTPError.response.status_code）
        # 401 表示未授权/认证失败，符合错误密码的预期（标准库：HTTP 状态码语义）
        assert exc.value.response.status_code == 401

    # Allure 报告标题：未登录时不能获取用户信息（第三方：allure → title）
    @allure.title("未登录无法获取用户信息")
    # @pytest.mark.exception：标记为异常场景用例，便于单独筛选运行（第三方：pytest → mark.exception）
    @pytest.mark.exception
    def test_get_me_unauthorized(self, auth_api):
        # 期望在未携带有效 Token 时调用 get_me 会抛出 HTTPError（第三方：pytest → raises）
        with pytest.raises(requests.HTTPError) as exc:
            # auth_api Fixture 默认未登录，直接请求用户信息应失败（项目：tests/conftest.py → auth_api）
            auth_api.get_me()
        # 未登录访问受保护接口，通常返回 401 Unauthorized（标准库：HTTP 状态码语义）
        assert exc.value.response.status_code == 401
