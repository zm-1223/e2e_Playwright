# =============================================================================（项目：tests/e2e/test_exception_e2e.py → 章节分隔）
# tests/e2e/test_exception_e2e.py — 混合 E2E 异常场景测试（项目：tests/e2e/test_exception_e2e.py → 模块说明）
# 作用：在接近真实链路的环境下验证非法 Token 等异常 API 行为（项目：api/client/auth_client.py → AuthApiClient）
# =============================================================================（项目：tests/e2e/test_exception_e2e.py → 章节分隔）

# 导入 pytest（第三方：pytest → fixture/mark/raises）
import pytest
# 导入 allure（第三方：allure → epic/feature/title）
import allure
# 导入 requests：用于 HTTPError 与 status_code 断言（第三方：requests → HTTPError）
import requests


# Allure epic（第三方：allure → epic）
@allure.epic("Practice Software Testing")
# Allure feature：E2E 异常场景（第三方：allure → feature）
@allure.feature("E2E 异常")
# 标记为端到端测试（第三方：pytest → mark.e2e）
@pytest.mark.e2e
# 标记为异常用例（第三方：pytest → mark.exception）
@pytest.mark.exception
class TestExceptionE2e:
    """混合 E2E 异常场景。"""

    # 用例：使用伪造 Token 访问用户信息接口应被拒绝（第三方：allure → title）
    @allure.title("无效 Token 无法获取用户信息")
    # auth_api：认证客户端，可手动 set_token（项目：tests/conftest.py → auth_api）
    def test_invalid_token_api(self, auth_api):
        # 故意设置一个无效的 Token 字符串，模拟 Token 过期或被篡改（项目：api/client/auth_client.py → set_token）
        auth_api.set_token("invalid-token-xyz")
        # 期望后续 get_me 请求因认证失败抛出 HTTPError（第三方：pytest → raises）
        with pytest.raises(requests.HTTPError) as exc:
            auth_api.get_me()
        # 401 Unauthorized 或 403 Forbidden 均表示无权访问（标准库：HTTP 状态码语义）
        assert exc.value.response.status_code in (401, 403)
