# =============================================================================
# utils/popup_handler.py — 突发弹窗/遮挡层处理器 （项目：utils/popup_handler.py）
# 作用：在 UI 操作前快速关闭 Cookie 提示、模态框等，避免挡住按钮导致点击失败 （项目：utils/popup_handler.py → PopupHandler）
# 说明：无弹窗时几乎零耗时（不长时间 wait，只 find_elements 扫描） （第三方：selenium → WebDriver.find_elements）
# =============================================================================

# 导入 logging：记录成功关闭弹窗时的信息，便于排查 （标准库：logging）
import logging
# 导入 List、Optional：类型注解，表示字符串列表、可选参数 （标准库：typing）
from typing import List, Optional
# 导入 WebDriver：Selenium 浏览器驱动类型 （第三方：selenium → WebDriver）
from selenium.webdriver.remote.webdriver import WebDriver
# 导入 By：元素定位策略（CSS、XPath 等） （第三方：selenium → By）
from selenium.webdriver.common.by import By
# 导入 Keys：模拟键盘按键，如 ESC 关闭弹窗 （第三方：selenium → Keys）
from selenium.webdriver.common.keys import Keys
# 导入 Selenium 常见异常：点击失败、元素不可交互、元素已过期 （第三方：selenium → exceptions）
from selenium.common.exceptions import (
    ElementClickInterceptedException,   # 被其他元素遮挡无法点击 （第三方：selenium → ElementClickInterceptedException）
    ElementNotInteractableException,    # 元素存在但不可交互 （第三方：selenium → ElementNotInteractableException）
    StaleElementReferenceException,     # DOM 刷新后旧元素引用失效 （第三方：selenium → StaleElementReferenceException）
)
# 从配置读取：是否启用自动关弹窗、默认关闭按钮选择器列表 （项目：config/settings.py → AUTO_DISMISS_POPUP, POPUP_CLOSE_SELECTORS）
from config.settings import AUTO_DISMISS_POPUP, POPUP_CLOSE_SELECTORS

# 创建以当前模块名命名的日志记录器 （标准库：logging.getLogger）
logger = logging.getLogger(__name__)


# 突发弹窗处理器：快速扫描并关闭常见遮挡层 （项目：utils/popup_handler.py → PopupHandler）
class PopupHandler:
    """突发弹窗处理器：快速扫描并关闭常见遮挡层（无弹窗时几乎零耗时）。"""

    def __init__(
        self,
        driver: WebDriver,
        selectors: Optional[List[str]] = None,
    ) -> None:  # 初始化弹窗处理器 （项目：utils/popup_handler.py → __init__）
        """初始化弹窗处理器。"""
        # 保存 WebDriver，后续查找元素、发送按键都通过它 （第三方：selenium → WebDriver）
        self.driver = driver
        # 若调用方未传 selectors，使用 settings 中的 POPUP_CLOSE_SELECTORS （项目：config/settings.py → POPUP_CLOSE_SELECTORS）
        self.selectors = selectors or POPUP_CLOSE_SELECTORS

    def dismiss_all(self) -> int:  # 尝试关闭所有可识别弹窗 （项目：utils/popup_handler.py → dismiss_all）
        """尝试关闭所有可识别的弹窗，返回成功关闭数量。"""
        # 配置关闭自动处理时，直接返回 0，不做任何操作 （项目：config/settings.py → AUTO_DISMISS_POPUP）
        if not AUTO_DISMISS_POPUP:
            return 0
        # 累计本次成功关闭的弹窗/遮挡层数量 （项目：utils/popup_handler.py → dismiss_all）
        closed = 0
        # 先按 ESC 键，许多模态框支持 ESC 关闭 （项目：utils/popup_handler.py → _press_escape）
        closed += self._press_escape()
        # 按配置的选择器列表，逐个尝试点击可见的关闭按钮 （项目：utils/popup_handler.py → _try_click_selector）
        for selector in self.selectors:
            if self._try_click_selector(selector):
                closed += 1
        # 若存在 JavaScript alert/confirm，则 accept 掉 （项目：utils/popup_handler.py → _accept_alert_if_present）
        closed += self._accept_alert_if_present()
        # 返回总共关闭的次数（可能为 0，表示没有弹窗） （Python 内置：return）
        return closed

    def _press_escape(self) -> int:  # 发送 ESC 键尝试关闭弹窗 （项目：utils/popup_handler.py → _press_escape）
        """发送 ESC 键尝试关闭弹窗。"""
        try:
            # 找到页面 body 元素，向它发送键盘事件（Selenium 常见做法） （第三方：selenium → WebDriver.find_element）
            body = self.driver.find_element(By.TAG_NAME, "body")
            # 发送 ESC 键 （第三方：selenium → WebElement.send_keys）
            body.send_keys(Keys.ESCAPE)
            # 认为尝试了一次关闭，返回 1 （Python 内置：return）
            return 1
        except Exception:
            # 任何异常（如无 body）都忽略，返回 0 表示未关闭 （Python 内置：Exception）
            return 0

    def _try_click_selector(self, selector: str) -> bool:  # 快速查找可见关闭按钮并点击 （项目：utils/popup_handler.py → _try_click_selector）
        """快速查找可见关闭按钮并点击（无弹窗时立即返回）。"""
        try:
            # find_elements 不等待：没有匹配元素时立即返回空列表，避免累积超时 （第三方：selenium → WebDriver.find_elements）
            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            # 遍历所有匹配到的元素（页面上可能有多个关闭按钮） （Python 内置：for）
            for element in elements:
                # 只点击「当前可见且可交互」的元素 （第三方：selenium → WebElement.is_displayed, is_enabled）
                if element.is_displayed() and element.is_enabled():
                    element.click()  # 点击关闭按钮 （第三方：selenium → WebElement.click）
                    logger.info("已关闭弹窗: %s", selector)  # 记录日志 （标准库：logging.Logger.info）
                    # 成功点击一个即返回 True，不再继续同选择器的其他元素 （Python 内置：return）
                    return True
            # 没有找到可点击的关闭按钮 （Python 内置：return）
            return False
        except (
            ElementNotInteractableException,
            ElementClickInterceptedException,
            StaleElementReferenceException,
        ):
            # 点击过程中出现已知 Selenium 异常时，视为本次选择器失败 （第三方：selenium → exceptions）
            return False

    def _accept_alert_if_present(self) -> int:  # 若存在 JavaScript alert 则接受 （项目：utils/popup_handler.py → _accept_alert_if_present）
        """若存在 JavaScript alert 则接受。"""
        try:
            # switch_to.alert 切换到浏览器原生 alert；不存在时会抛异常 （第三方：selenium → WebDriver.switch_to.alert）
            alert = self.driver.switch_to.alert
            # accept() 相当于点击 alert 的「确定」 （第三方：selenium → Alert.accept）
            alert.accept()
            return 1  # 成功关闭 alert （Python 内置：return）
        except Exception:
            # 没有 alert 或切换失败时返回 0 （Python 内置：Exception）
            return 0
