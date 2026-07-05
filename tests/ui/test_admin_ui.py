# =============================================================================
# 文件：tests/ui/test_admin_ui.py
# 作用：Tigshop 后台管理 UI 自动化用例（登录页、优惠券列表）
# 调用关系：pytest → admin_login_page/admin_coupon_page fixture → AdminLoginPage/AdminCouponPage
# 自定义/框架：自定义测试类 + pytest/allure + 后台 POM
# 来源（项目 tests/ui 层，覆盖后台登录页与优惠券管理页）
# =============================================================================
import allure  # 作用：导入 Allure 装饰器；调用关系：epic/feature/title；自定义/框架：框架(allure)；来源(第三方 allure)
import pytest  # 作用：导入 pytest；调用关系：mark.ui、mark.flaky；自定义/框架：框架(pytest)；来源(第三方 pytest)


@allure.epic("Tigshop")  # 作用：Allure epic 分组；调用关系：报告；自定义/框架：框架(allure)；来源(allure)
@allure.feature("UI-后台")  # 作用：Allure feature「UI-后台」；调用关系：TestAdminUi；自定义/框架：框架(allure)；来源(allure)
@pytest.mark.ui  # 作用：UI 层 pytest 标记；调用关系：-m ui；自定义/框架：框架(pytest)；来源(pytest)
@pytest.mark.flaky(reruns=2, reruns_delay=2)  # 作用：后台 UI 失败重跑 2 次；调用关系：pytest-rerunfailures；自定义/框架：框架(插件)；来源(pytest-rerunfailures)
class TestAdminUi:  # 作用：后台 UI 测试类；调用关系：pytest 收集；自定义/框架：自定义；来源(本文件)
    @allure.title("后台登录页标题可见")  # 作用：Allure 标题；调用关系：test_admin_login_page；自定义/框架：框架(allure)；来源(allure)
    def test_admin_login_page(self, admin_login_page):  # 作用：未登录访问后台登录页元素可见；调用关系：conftest admin_login_page → AdminLoginPage；自定义/框架：自定义；来源(本文件)
        assert admin_login_page.login_page_visible()  # 作用：断言登录页标题/表单可见；调用关系：AdminLoginPage.login_page_visible；自定义/框架：自定义；来源(ui/pages/admin/login_page.py)

    @allure.title("后台登录后优惠券列表有表格行")  # 作用：Allure 标题；调用关系：test_admin_coupon_list；自定义/框架：框架(allure)；来源(allure)
    def test_admin_coupon_list(self, admin_coupon_page):  # 作用：登录后优惠券页有表格数据；调用关系：admin_coupon_page fixture（含 admin_logged_in_driver）；自定义/框架：自定义；来源(本文件)
        assert admin_coupon_page.coupon_page_loaded()  # 作用：断言优惠券管理页已加载；调用关系：AdminCouponPage.coupon_page_loaded；自定义/框架：自定义；来源(ui/pages/admin/coupon_page.py)
        assert admin_coupon_page.table_row_count() >= 1  # 作用：断言表格至少一行；调用关系：AdminCouponPage.table_row_count；自定义/框架：自定义；来源(ui/pages/admin/coupon_page.py)
