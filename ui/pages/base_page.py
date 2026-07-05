# =============================================================================
# 文件名: base_page.py
# 模块路径: ui/pages/base_page.py
# 作用: Page Object 基类，封装通用 Selenium 页面操作（导航、定位、点击、输入、URL 等待）
# 调用关系: 被 ui/pages/front/*、ui/pages/admin/* 继承；依赖 config/settings、utils/*
# 类型: 自定义（项目）
# 来源: E2E_demo 项目
# =============================================================================
# 从 typing 模块导入 Optional，用于标注“可以是某类型或 None”的可选参数（标准库：typing → Optional）
from typing import Optional
# 从 Selenium 导入 WebDriver 类型，代表浏览器驱动对象（第三方：selenium.webdriver.remote.webdriver → WebDriver）
from selenium.webdriver.remote.webdriver import WebDriver
# 导入 expected_conditions 并简写为 EC，提供各种“等待条件”（如元素可见、可点击）（第三方：selenium.webdriver.support → expected_conditions）
from selenium.webdriver.support import expected_conditions as EC
# 导入 WebDriverWait，用于在指定时间内轮询等待某个条件成立（第三方：selenium.webdriver.support.ui → WebDriverWait）
from selenium.webdriver.support.ui import WebDriverWait
# 导入 By，定义元素定位方式（如 ID、CSS 选择器、XPath 等）（第三方：selenium.webdriver.common.by → By）
from selenium.webdriver.common.by import By
# 从 Selenium 异常模块导入两种常见异常，用于点击重试（第三方：selenium.common.exceptions → ElementClickInterceptedException, StaleElementReferenceException）
from selenium.common.exceptions import (
    ElementClickInterceptedException,  # 元素被遮挡导致点击失败（第三方：selenium.common.exceptions → ElementClickInterceptedException）
    StaleElementReferenceException,    # 元素已过期（页面刷新后旧引用失效）（第三方：selenium.common.exceptions → StaleElementReferenceException）
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(ui/pages/base_page.py)
)
# 从项目配置中导入显式等待的默认超时秒数（项目：config/settings.py → EXPLICIT_WAIT）
from config.settings import EXPLICIT_WAIT
# 从工具模块导入：等待页面就绪、稳定延迟、失败重试（项目：utils/wait_helper.py → wait_for_page_ready, stable_delay, retry_action）
from utils.wait_helper import wait_for_page_ready, stable_delay, retry_action
# 从工具模块导入弹窗处理器，用于关闭 Cookie 提示等遮挡层（项目：utils/popup_handler.py → PopupHandler）
from utils.popup_handler import PopupHandler


# Page Object 基类：封装通用页面操作（含等待与弹窗处理）（项目：ui/pages/base_page.py → BasePage）
class BasePage:
    """Page Object 基类，封装通用页面操作（含等待与弹窗处理）。"""

# 作用：定义函数/方法 __init__；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/base_page.py)
    def __init__(self, driver: WebDriver, base_url: str, timeout: int = None) -> None:
        # 保存浏览器驱动实例，后续所有操作都通过它执行（第三方：selenium → WebDriver）
        self.driver = driver
        # 保存站点根 URL，并去掉末尾多余的斜杠，便于拼接路径（Python 内置：str.rstrip）
        self.base_url = base_url.rstrip("/")
        # 若调用方未传 timeout，则使用配置文件中的 EXPLICIT_WAIT 作为默认超时（项目：config/settings.py → EXPLICIT_WAIT）
        self.timeout = timeout or EXPLICIT_WAIT
        # 创建弹窗处理器，绑定当前 driver（项目：utils/popup_handler.py → PopupHandler）
        self.popup = PopupHandler(driver)

# 作用：定义函数/方法 open；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/base_page.py)
    def open(self, path: str = "") -> None:
        # 若 path 非空，拼接成完整 URL；否则只打开 base_url（Python 内置：str.lstrip, f-string）
        url = f"{self.base_url}/{path.lstrip('/')}" if path else self.base_url
        # 让浏览器导航到目标 URL（第三方：selenium → WebDriver.get）
        self.driver.get(url)
        # 等待页面加载完成（如 document.readyState 为 complete）（项目：utils/wait_helper.py → wait_for_page_ready）
        wait_for_page_ready(self.driver, timeout=self.timeout)
        # 关闭可能出现的弹窗，避免遮挡后续操作（项目：utils/popup_handler.py → PopupHandler.dismiss_all）
        self.popup.dismiss_all()

# 作用：定义函数/方法 find；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/base_page.py)
    def find(self, by: By, locator: str):
        # 短暂延迟，降低页面抖动导致的定位失败（项目：utils/wait_helper.py → stable_delay）
        stable_delay()
        # 在 timeout 内轮询，直到元素出现在 DOM 中且可见（第三方：selenium → WebDriverWait, EC.visibility_of_element_located）
        return WebDriverWait(self.driver, self.timeout).until(
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(ui/pages/base_page.py)
            EC.visibility_of_element_located((by, locator))
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(ui/pages/base_page.py)
        )

# 作用：定义函数/方法 find_clickable；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/base_page.py)
    def find_clickable(self, by: By, locator: str):
        # 短暂延迟，等待 DOM 稳定（项目：utils/wait_helper.py → stable_delay）
        stable_delay()
        # 在 timeout 内轮询，直到元素可见且可被点击（第三方：selenium → WebDriverWait, EC.element_to_be_clickable）
        return WebDriverWait(self.driver, self.timeout).until(
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(ui/pages/base_page.py)
            EC.element_to_be_clickable((by, locator))
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(ui/pages/base_page.py)
        )

# 作用：定义函数/方法 click；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/base_page.py)
    def click(self, by: By, locator: str) -> None:
        # 定义内部函数，封装一次完整的点击流程（Python 内置：def 嵌套函数）
        def _do_click():
            # 点击前先尝试关闭弹窗（项目：utils/popup_handler.py → PopupHandler.dismiss_all）
            self.popup.dismiss_all()
            # 找到可点击元素并执行 click()（第三方：selenium → WebElement.click）
            self.find_clickable(by, locator).click()
            # 点击后短暂等待，给页面响应时间（项目：utils/wait_helper.py → stable_delay）
            stable_delay()

        # 若点击被遮挡或元素过期，自动重试 _do_click（项目：utils/wait_helper.py → retry_action）
        retry_action(
# 作用：执行本行逻辑；调用关系：见上下文；自定义/框架：自定义；来源(ui/pages/base_page.py)
            _do_click,
# 作用：赋值/绑定变量；调用关系：供后续步骤使用；自定义/框架：Python 内置；来源(赋值)
            exceptions=(ElementClickInterceptedException, StaleElementReferenceException),
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(ui/pages/base_page.py)
        )

# 作用：定义函数/方法 input_text；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/base_page.py)
    def input_text(self, by: By, locator: str, text: str) -> None:
        # 输入前先关闭弹窗（项目：utils/popup_handler.py → PopupHandler.dismiss_all）
        self.popup.dismiss_all()
        # 定位到输入框元素（等待可见）（项目：ui/pages/base_page.py → BasePage.find）
        element = self.find(by, locator)
        # 清空输入框原有内容（第三方：selenium → WebElement.clear）
        element.clear()
        # 模拟键盘输入指定文本（第三方：selenium → WebElement.send_keys）
        element.send_keys(text)

# 作用：定义函数/方法 get_text；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/base_page.py)
    def get_text(self, by: By, locator: str) -> str:
        # 读取文本前先关闭弹窗（项目：utils/popup_handler.py → PopupHandler.dismiss_all）
        self.popup.dismiss_all()
        # 定位元素并返回其 .text 属性（可见文本）（第三方：selenium → WebElement.text）
        return self.find(by, locator).text

# 作用：定义函数/方法 wait_url_contains；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/base_page.py)
    def wait_url_contains(self, fragment: str) -> None:
        # 在 timeout 内轮询，直到当前 URL 包含指定片段 fragment（第三方：selenium → WebDriverWait, EC.url_contains）
        WebDriverWait(self.driver, self.timeout).until(EC.url_contains(fragment))
        # URL 变化后等待页面加载完成，避免 SPA 路由切换未完成（项目：utils/wait_helper.py → wait_for_page_ready）
        wait_for_page_ready(self.driver, timeout=self.timeout)
        # 页面就绪后关闭可能出现的弹窗（项目：utils/popup_handler.py → PopupHandler.dismiss_all）
        self.popup.dismiss_all()

# 作用：定义函数/方法 wait_url_not_contains；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/base_page.py)
    def wait_url_not_contains(self, fragment: str) -> None:
        # 在 timeout 内轮询，直到当前 URL 不再包含 fragment（第三方：selenium → WebDriverWait + lambda 自定义条件）
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: fragment not in d.current_url  # lambda 接收 WebDriver 实例 d，检查 d.current_url（第三方：selenium → WebDriver.current_url）
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(ui/pages/base_page.py)
        )
        # URL 变化后等待页面加载完成（项目：utils/wait_helper.py → wait_for_page_ready）
        wait_for_page_ready(self.driver, timeout=self.timeout)
        # 页面就绪后关闭弹窗（项目：utils/popup_handler.py → PopupHandler.dismiss_all）
        self.popup.dismiss_all()

# 作用：定义函数/方法 wait_text_present；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/base_page.py)
    def wait_text_present(self, by: By, locator: str, expected: str) -> None:
        # 等待指定元素的文本内容包含 expected 字符串（第三方：selenium → WebDriverWait, EC.text_to_be_present_in_element）
        WebDriverWait(self.driver, self.timeout).until(
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(ui/pages/base_page.py)
            EC.text_to_be_present_in_element((by, locator), expected)
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(ui/pages/base_page.py)
        )

# 作用：装饰器 @property；调用关系：修饰紧随其后的类/函数；自定义/框架：框架；来源(@property)
    @property
# 作用：定义函数/方法 current_url；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/base_page.py)
    def current_url(self) -> str:
        # 只读属性：返回浏览器当前地址栏 URL（第三方：selenium → WebDriver.current_url）
        return self.driver.current_url

# 作用：装饰器 @property；调用关系：修饰紧随其后的类/函数；自定义/框架：框架；来源(@property)
    @property
# 作用：定义函数/方法 title；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/base_page.py)
    def title(self) -> str:
        # 只读属性：返回当前页面标题（<title> 标签内容）（第三方：selenium → WebDriver.title）
        return self.driver.title
