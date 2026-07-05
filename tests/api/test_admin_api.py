# =============================================================================
# 文件：tests/api/test_admin_api.py
# 作用：Tigshop 后台管理 API 自动化用例（登录、优惠券列表）
# 调用关系：pytest → admin_api/logged_in_admin_api/test_data → AdminApiClient
# 自定义/框架：自定义测试类 + pytest/allure + TigshopApiError 业务异常处理
# 来源（项目 tests/api 层，覆盖后台 token 登录与优惠券列表）
# =============================================================================
import allure  # 作用：导入 Allure 装饰器；调用关系：epic/feature/title；自定义/框架：框架(allure)；来源(第三方 allure)
import pytest  # 作用：导入 pytest；调用关系：mark.api、pytest.skip；自定义/框架：框架(pytest)；来源(第三方 pytest)

from api.client.base_client import TigshopApiError  # 作用：导入 API 业务异常类；调用关系：test_admin_login 捕获验证码；自定义/框架：自定义；来源(api/client/base_client.py)


@allure.epic("Tigshop")  # 作用：Allure epic 分组；调用关系：报告；自定义/框架：框架(allure)；来源(allure)
@allure.feature("API-后台")  # 作用：Allure feature「API-后台」；调用关系：TestAdminApi；自定义/框架：框架(allure)；来源(allure)
@pytest.mark.api  # 作用：API 层 pytest 标记；调用关系：-m api；自定义/框架：框架(pytest)；来源(pytest)
class TestAdminApi:  # 作用：后台 API 测试类；调用关系：pytest 收集；自定义/框架：自定义；来源(本文件)
    @allure.title("后台 API 登录返回 token（若触发验证码则跳过）")  # 作用：Allure 标题说明验证码 skip 策略；调用关系：test_admin_login；自定义/框架：框架(allure)；来源(allure)
    def test_admin_login(self, admin_api, test_data):  # 作用：验证后台 login 返回 token 或 skip；调用关系：admin_api.login、TigshopApiError；自定义/框架：自定义；来源(本文件)
        try:  # 作用：尝试 API 登录；调用关系：admin_api.login；自定义/框架：自定义；来源(本文件)
            data = admin_api.login(test_data["admin_username"], test_data["admin_password"])  # 作用：调用后台登录；调用关系：AdminApiClient.login、test_data；自定义/框架：自定义；来源(api/client/admin_client.py)
            assert data.get("token")  # 作用：断言响应含 token；调用关系：pytest assert；自定义/框架：框架(pytest)；来源(Python)
        except TigshopApiError as exc:  # 作用：捕获 Tigshop API 业务错误；调用关系：login 失败；自定义/框架：自定义；来源(api/client/base_client.py)
            if "验证" in str(exc):  # 作用：判断是否人机验证错误；调用关系：错误消息字符串；自定义/框架：自定义；来源(本文件)
                pytest.skip("后台 API 登录触发人机验证，请依赖 UI 登录同步 token 的用例")  # 作用：验证码场景跳过而非失败；调用关系：pytest.skip；自定义/框架：框架(pytest)；来源(pytest)
            raise  # 作用：其他错误重新抛出；调用关系：pytest 失败；自定义/框架：框架(Python)；来源(Python)

    @allure.title("后台优惠券列表有数据")  # 作用：Allure 标题；调用关系：test_admin_coupon_list；自定义/框架：框架(allure)；来源(allure)
    def test_admin_coupon_list(self, logged_in_admin_api):  # 作用：验证后台优惠券名称列表非空；调用关系：logged_in_admin_api.coupon_names；自定义/框架：自定义；来源(本文件)
        names = logged_in_admin_api.coupon_names(size=5)  # 作用：获取最多 5 条优惠券名称；调用关系：AdminApiClient.coupon_names；自定义/框架：自定义；来源(api/client/admin_client.py)
        assert len(names) >= 1  # 作用：断言至少一条优惠券；调用关系：pytest assert；自定义/框架：框架(pytest)；来源(Python)
