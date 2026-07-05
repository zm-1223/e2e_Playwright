# =============================================================================
# 文件：tests/e2e/test_exception_e2e.py
# 作用：Tigshop 混合 E2E 异常场景测试（无效 Token 等 API 负面路径）
# 调用关系：pytest → buyer_auth_api → AuthApiClient.set_token/get_user_detail → TigshopApiError
# 自定义/框架：自定义 E2E 异常类 + pytest/allure + 自定义 API 客户端
# 来源（项目 tests/e2e 层，验证认证失败等业务异常）
# =============================================================================
import allure  # 作用：导入 Allure 装饰器；调用关系：epic/feature/title；自定义/框架：框架(allure)；来源(第三方 allure)
import pytest  # 作用：导入 pytest；调用关系：mark.e2e/exception、pytest.raises；自定义/框架：框架(pytest)；来源(第三方 pytest)

from api.client.base_client import TigshopApiError  # 作用：导入 Tigshop 业务异常类；调用关系：无效 Token 断言；自定义/框架：自定义；来源(api/client/base_client.py)


@allure.epic("Tigshop")  # 作用：Allure epic 分组；调用关系：异常 E2E 报告；自定义/框架：框架(allure)；来源(allure)
@allure.feature("E2E-异常场景")  # 作用：Allure feature 分组；调用关系：TestExceptionE2e；自定义/框架：框架(allure)；来源(allure)
@pytest.mark.e2e  # 作用：E2E 层 pytest 标记；调用关系：pytest -m e2e 筛选；自定义/框架：框架(pytest)；来源(pytest)
@pytest.mark.exception  # 作用：异常场景 pytest 标记；调用关系：pytest -m exception 筛选；自定义/框架：框架(pytest)；来源(pytest)
@pytest.mark.flaky(reruns=1, reruns_delay=2)  # 作用：失败重跑 1 次；调用关系：pytest-rerunfailures；自定义/框架：框架(插件)；来源(pytest-rerunfailures)
class TestExceptionE2e:  # 作用：混合 E2E 异常测试类；调用关系：pytest 收集；自定义/框架：自定义；来源(本文件)
    @allure.title("无效 Token 无法获取用户信息")  # 作用：Allure 用例标题；调用关系：test_invalid_token_api；自定义/框架：框架(allure)；来源(allure)
    def test_invalid_token_api(self, buyer_auth_api):  # 作用：伪造 Token 访问用户详情应被拒绝；调用关系：buyer_auth_api fixture、AuthApiClient；自定义/框架：自定义；来源(本文件)
        buyer_auth_api.set_token("invalid-token-xyz")  # 作用：故意设置无效 JWT；调用关系：BaseApiClient.set_token；自定义/框架：自定义；来源(api/client/base_client.py)
        with pytest.raises(TigshopApiError) as exc:  # 作用：期望 get_user_detail 抛出业务异常；调用关系：pytest.raises；自定义/框架：框架(pytest)；来源(pytest)
            buyer_auth_api.get_user_detail()  # 作用：调用需认证的用户详情接口；调用关系：AuthApiClient.get_user_detail；自定义/框架：自定义；来源(api/client/auth_client.py)
        assert exc.value.payload.get("code") != 0  # 作用：断言响应 code 非 0 表示认证失败；调用关系：TigshopApiError.payload；自定义/框架：自定义；来源(api/client/base_client.py)
