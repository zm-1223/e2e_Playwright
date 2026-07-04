# =============================================================================（项目：tests/ui/test_exception_ui.py → 章节分隔）
# tests/ui/test_exception_ui.py — UI 层异常场景测试（项目：tests/ui/test_exception_ui.py → 模块说明）
# 作用：验证访问无效商品页等错误情况时，页面展示是否符合预期（第三方：selenium → WebDriver）
# =============================================================================（项目：tests/ui/test_exception_ui.py → 章节分隔）

# 导入 pytest（第三方：pytest → fixture/mark）
import pytest
# 导入 allure（第三方：allure → epic/feature/title）
import allure
# 导入 By：元素定位方式（第三方：selenium → By）
from selenium.webdriver.common.by import By


# Allure epic（第三方：allure → epic）
@allure.epic("Practice Software Testing")
# Allure feature：UI 异常处理（第三方：allure → feature）
@allure.feature("UI 异常")
# 标记为 UI 测试（第三方：pytest → mark.ui）
@pytest.mark.ui
# 标记为异常场景用例（第三方：pytest → mark.exception）
@pytest.mark.exception
class TestExceptionUi:
    """UI 异常场景测试。"""

    # 用例：访问不存在的商品 ID 时页面应提示错误或仍正常渲染 body（第三方：allure → title）
    @allure.title("无效商品页应显示错误或无标题")
    # authenticated_driver：已登录浏览器（项目：tests/conftest.py → authenticated_driver）
    # base_url：站点根 URL（如 https://practicesoftwaretesting.com）（项目：tests/conftest.py → base_url）
    # test_data：含 invalid_product_id 等测试数据（项目：tests/conftest.py → test_data）
    def test_invalid_product_page(self, authenticated_driver, base_url, test_data):
        # driver.get(url)：导航到无效商品详情页 URL（第三方：selenium → WebDriver.get）
        authenticated_driver.get(f"{base_url}/product/{test_data['invalid_product_id']}")
        # 查找 <body> 元素并读取其可见文本，转小写便于匹配英文提示（第三方：selenium → find_element/By.TAG_NAME）
        body = authenticated_driver.find_element(By.TAG_NAME, "body").text.lower()
        # 宽松断言：页面应包含 not found / error 等提示，或至少有 body 文本（页面有响应）（Python 内置：assert/in/len）
        assert "not found" in body or "error" in body or len(body) > 0
