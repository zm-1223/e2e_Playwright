# =============================================================================
# 文件：tests/ui/test_front_member_ui.py
# 作用：Tigshop 前台会员中心、订单、优惠券相关 UI 自动化用例（需买家登录）
# 调用关系：pytest → front_member_page/front_coupon_page fixture → FrontMemberPage/FrontCouponPage
# 自定义/框架：自定义测试类 + pytest/allure + POM fixture（buyer_driver 链）
# 来源（项目 tests/ui 层，覆盖个人中心与优惠券页面展示）
# =============================================================================
import allure  # 作用：导入 Allure 装饰器；调用关系：epic/feature/title；自定义/框架：框架(allure)；来源(第三方 allure)
import pytest  # 作用：导入 pytest；调用关系：mark.ui、mark.flaky；自定义/框架：框架(pytest)；来源(第三方 pytest)


@allure.epic("Tigshop")  # 作用：Allure epic 分组；调用关系：报告树；自定义/框架：框架(allure)；来源(allure)
@allure.feature("UI-前台会员与优惠券")  # 作用：Allure feature 分组；调用关系：TestFrontMemberUi；自定义/框架：框架(allure)；来源(allure)
@pytest.mark.ui  # 作用：UI 层 pytest 标记；调用关系：-m ui 筛选；自定义/框架：框架(pytest)；来源(pytest)
@pytest.mark.flaky(reruns=2, reruns_delay=2)  # 作用：UI 不稳定时重跑 2 次；调用关系：pytest-rerunfailures；自定义/框架：框架(插件)；来源(pytest-rerunfailures)
class TestFrontMemberUi:  # 作用：前台会员与优惠券 UI 测试类；调用关系：pytest 收集 test_*；自定义/框架：自定义；来源(本文件)
    @allure.title("个人中心页面加载")  # 作用：Allure 用例标题；调用关系：test_member_center；自定义/框架：框架(allure)；来源(allure)
    def test_member_center(self, front_member_page):  # 作用：验证会员中心页加载成功；调用关系：conftest front_member_page → FrontMemberPage；自定义/框架：自定义；来源(本文件)
        assert front_member_page.member_page_loaded()  # 作用：断言个人中心主区域已加载；调用关系：FrontMemberPage.member_page_loaded；自定义/框架：自定义；来源(ui/pages/front/member_page.py)

    @allure.title("个人中心侧栏导航存在")  # 作用：Allure 标题；调用关系：test_member_nav_links；自定义/框架：框架(allure)；来源(allure)
    def test_member_nav_links(self, front_member_page):  # 作用：验证侧栏至少 1 个导航链接；调用关系：FrontMemberPage.nav_link_count；自定义/框架：自定义；来源(本文件)
        assert front_member_page.nav_link_count() >= 1  # 作用：断言导航链接数 ≥1；调用关系：FrontMemberPage 方法；自定义/框架：自定义；来源(ui/pages/front/member_page.py)

    @allure.title("我的订单页展示")  # 作用：Allure 标题；调用关系：test_order_list_page；自定义/框架：框架(allure)；来源(allure)
    def test_order_list_page(self, front_member_page):  # 作用：验证「我的订单」页加载；调用关系：FrontMemberPage.orders_page_loaded；自定义/框架：自定义；来源(本文件)
        assert front_member_page.orders_page_loaded()  # 作用：断言订单列表页已展示；调用关系：FrontMemberPage.orders_page_loaded；自定义/框架：自定义；来源(ui/pages/front/member_page.py)

    @allure.title("集券中心页面展示")  # 作用：Allure 标题；调用关系：test_coupon_center；自定义/框架：框架(allure)；来源(allure)
    def test_coupon_center(self, front_coupon_page):  # 作用：验证集券中心页加载；调用关系：conftest front_coupon_page → FrontCouponPage；自定义/框架：自定义；来源(本文件)
        assert front_coupon_page.coupon_center_loaded()  # 作用：断言集券中心页面已加载；调用关系：FrontCouponPage.coupon_center_loaded；自定义/框架：自定义；来源(ui/pages/front/coupon_page.py)

    @allure.title("我的优惠券页面展示")  # 作用：Allure 标题；调用关系：test_my_coupons_page；自定义/框架：框架(allure)；来源(allure)
    def test_my_coupons_page(self, front_coupon_page):  # 作用：验证「我的优惠券」页加载；调用关系：FrontCouponPage.my_coupons_loaded；自定义/框架：自定义；来源(本文件)
        assert front_coupon_page.my_coupons_loaded()  # 作用：断言我的优惠券页已展示；调用关系：FrontCouponPage.my_coupons_loaded；自定义/框架：自定义；来源(ui/pages/front/coupon_page.py)
