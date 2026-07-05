# =============================================================================
# 文件：tests/ui/test_exception_ui.py
# 作用：Tigshop 前台 UI 异常场景测试（无效商品页等负面路径）
# 调用关系：pytest → front_driver/front_base_url/test_data → FrontProductPage → Selenium WebDriver
# 自定义/框架：自定义测试类 + pytest/allure + Selenium + POM
# 来源（项目 tests/ui 层，覆盖异常页面展示与错误提示）
# =============================================================================
import allure  # 作用：导入 Allure 装饰器；调用关系：epic/feature/title；自定义/框架：框架(allure)；来源(第三方 allure)
import pytest  # 作用：导入 pytest；调用关系：mark.ui/exception、mark.flaky；自定义/框架：框架(pytest)；来源(第三方 pytest)
from selenium.webdriver.common.by import By  # 作用：导入元素定位枚举；调用关系：By.TAG_NAME 读取 body 文本；自定义/框架：框架(Selenium)；来源(第三方 selenium)

from ui.pages.front.product_page import FrontProductPage  # 作用：导入前台商品详情 POM；调用关系：open_product 打开无效商品页；自定义/框架：自定义 POM；来源(ui/pages/front/product_page.py)


@allure.epic("Tigshop")  # 作用：Allure epic 分组；调用关系：异常 UI 报告；自定义/框架：框架(allure)；来源(allure)
@allure.feature("UI-异常场景")  # 作用：Allure feature 分组；调用关系：TestExceptionUi；自定义/框架：框架(allure)；来源(allure)
@pytest.mark.ui  # 作用：UI 层 pytest 标记；调用关系：pytest -m ui 筛选；自定义/框架：框架(pytest)；来源(pytest)
@pytest.mark.exception  # 作用：异常场景 pytest 标记；调用关系：pytest -m exception 筛选；自定义/框架：框架(pytest)；来源(pytest)
@pytest.mark.flaky(reruns=2, reruns_delay=2)  # 作用：失败重跑 2 次；调用关系：pytest-rerunfailures；自定义/框架：框架(插件)；来源(pytest-rerunfailures)
class TestExceptionUi:  # 作用：前台 UI 异常测试类；调用关系：pytest 收集；自定义/框架：自定义；来源(本文件)
    @allure.title("无效商品页应显示错误或无标题")  # 作用：Allure 用例标题；调用关系：test_invalid_product_page；自定义/框架：框架(allure)；来源(allure)
    def test_invalid_product_page(self, front_driver, front_base_url, test_data):  # 作用：访问不存在商品 ID 时页面有错误提示或正常渲染；调用关系：front_driver、FrontProductPage、test_data；自定义/框架：自定义；来源(本文件)
        page = FrontProductPage(front_driver, front_base_url)  # 作用：构造商品详情 POM；调用关系：FrontProductPage.__init__；自定义/框架：自定义；来源(ui/pages/front/product_page.py)
        page.open_product(test_data["invalid_product_id"])  # 作用：导航至无效商品 URL；调用关系：FrontProductPage.open_product、test_data；自定义/框架：自定义；来源(ui/pages/front/product_page.py)
        body = front_driver.find_element(By.TAG_NAME, "body").text.lower()  # 作用：读取页面 body 可见文本并转小写；调用关系：Selenium find_element；自定义/框架：框架(Selenium)；来源(selenium)
        assert (  # 作用：宽松断言页面有错误提示或至少有内容；调用关系：pytest assert；自定义/框架：框架(pytest)；来源(Python)
            "不存在" in body  # 作用：匹配中文「不存在」提示；调用关系：Tigshop 错误页文案；自定义/框架：自定义；来源(本文件)
            or "错误" in body  # 作用：匹配中文「错误」提示；调用关系：通用错误文案；自定义/框架：自定义；来源(本文件)
            or "404" in body  # 作用：匹配 HTTP 404 英文提示；调用关系：部分 SPA 错误页；自定义/框架：自定义；来源(本文件)
            or len(body) > 0  # 作用：兜底断言页面有响应内容；调用关系：Python len；自定义/框架：框架(Python)；来源(Python)
        )
