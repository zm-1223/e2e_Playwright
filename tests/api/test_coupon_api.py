# =============================================================================
# 文件：tests/api/test_coupon_api.py
# 作用：Tigshop 买家「我的优惠券」API 自动化用例
# 调用关系：pytest → logged_in_buyer_api + coupon_api → CouponApiClient.my_coupons
# 自定义/框架：自定义测试类 + pytest/allure 框架
# 来源（项目 tests/api 层，覆盖优惠券列表接口）
# =============================================================================
import allure  # 作用：导入 Allure 报告装饰器；调用关系：@allure.epic/feature/title；自定义/框架：框架(allure-pytest)；来源(第三方 allure)
import pytest  # 作用：导入 pytest 测试框架；调用关系：@pytest.mark.api；自定义/框架：框架(pytest)；来源(第三方 pytest)


@allure.epic("Tigshop")  # 作用：Allure 报告 epic 分组；调用关系：TestCouponApi；自定义/框架：框架(allure)；来源(allure)
@allure.feature("API-优惠券")  # 作用：Allure feature 分组「API-优惠券」；调用关系：本模块用例；自定义/框架：框架(allure)；来源(allure)
@pytest.mark.api  # 作用：标记 API 层用例；调用关系：pytest -m api 筛选；自定义/框架：框架(pytest mark)；来源(pytest)
class TestCouponApi:  # 作用：优惠券 API 测试类；调用关系：pytest 收集 test_my_coupons；自定义/框架：自定义；来源(本文件)
    @allure.title("我的优惠券列表接口正常")  # 作用：Allure 用例中文标题；调用关系：test_my_coupons；自定义/框架：框架(allure)；来源(allure)
    def test_my_coupons(self, logged_in_buyer_api, coupon_api):  # 作用：断言 my_coupons 返回分页 records；调用关系：logged_in_buyer_api 登录 + coupon_api；自定义/框架：自定义测试方法；来源(本文件)
        data = coupon_api.my_coupons(page=1, size=5)  # 作用：请求我的优惠券第 1 页；调用关系：CouponApiClient.my_coupons → 远端 API；自定义/框架：自定义；来源(api/client/coupon_client.py)
        assert "records" in data  # 作用：断言响应含 records 分页字段；调用关系：pytest assert；自定义/框架：框架(pytest)；来源(Python assert)
