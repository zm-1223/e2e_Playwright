# 从 selenium 包导入 webdriver 模块，用于创建浏览器实例（第三方：selenium → webdriver）
from selenium import webdriver
# 导入 Chrome 浏览器的选项类，并重命名为 ChromeOptions 便于使用（第三方：selenium.webdriver.chrome.options → Options）
from selenium.webdriver.chrome.options import Options as ChromeOptions
# 导入 Chrome 驱动服务类，用于指定 chromedriver 可执行文件路径（第三方：selenium.webdriver.chrome.service → Service）
from selenium.webdriver.chrome.service import Service as ChromeService
# 导入 Edge 浏览器的选项类（第三方：selenium.webdriver.edge.options → Options）
from selenium.webdriver.edge.options import Options as EdgeOptions
# 导入 Edge 驱动服务类（第三方：selenium.webdriver.edge.service → Service）
from selenium.webdriver.edge.service import Service as EdgeService
# 导入 webdriver-manager 的 Chrome 驱动管理器，可自动下载匹配版本的驱动（第三方：webdriver_manager.chrome → ChromeDriverManager）
from webdriver_manager.chrome import ChromeDriverManager
# 导入 Edge Chromium 驱动管理器（第三方：webdriver_manager.microsoft → EdgeChromiumDriverManager）
from webdriver_manager.microsoft import EdgeChromiumDriverManager
# 从项目配置导入：浏览器类型、无头模式、隐式等待、页面加载超时（项目：config/settings.py → BROWSER, HEADLESS, IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT）
from config.settings import BROWSER, HEADLESS, IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT


# WebDriver 工厂类：负责创建与销毁浏览器实例（项目：ui/driver/driver_manager.py → WebDriverManager）
class WebDriverManager:
    """WebDriver 工厂类：创建与销毁浏览器实例。"""

    @staticmethod
    def create_driver() -> webdriver.Remote:
        """根据配置创建并返回 WebDriver 实例。"""
        # 若配置指定使用 edge 浏览器，走 Edge 分支（项目：config/settings.py → BROWSER）
        if BROWSER == "edge":
            # 创建 Edge 浏览器选项对象（第三方：selenium.webdriver.edge.options → EdgeOptions）
            options = EdgeOptions()
            # 若开启无头模式，浏览器在后台运行，不显示窗口（项目：config/settings.py → HEADLESS）
            if HEADLESS:
                # 添加无头模式启动参数（第三方：selenium → Options.add_argument）
                options.add_argument("--headless=new")
            # 禁用 GPU 硬件加速，减少部分环境下的渲染问题（第三方：selenium → Options.add_argument）
            options.add_argument("--disable-gpu")
            # 忽略 HTTPS 证书错误，便于测试环境访问（第三方：selenium → Options.add_argument）
            options.add_argument("--ignore-certificate-errors")
            # 启动时尽量最大化窗口（第三方：selenium → Options.add_argument）
            options.add_argument("--start-maximized")
            # 实例化 Edge WebDriver（第三方：selenium → webdriver.Edge）
            driver = webdriver.Edge(
                service=EdgeService(EdgeChromiumDriverManager().install()),  # 自动下载并安装 Edge 驱动（第三方：webdriver_manager.microsoft → EdgeChromiumDriverManager）
                options=options,  # 传入上面配置的浏览器启动参数（第三方：selenium → Options）
            )
        else:
            # 默认分支：使用 Chrome 浏览器（项目：config/settings.py → BROWSER）
            # 创建 Chrome 浏览器选项对象（第三方：selenium.webdriver.chrome.options → ChromeOptions）
            options = ChromeOptions()
            # 无头模式下不弹出可见浏览器窗口（项目：config/settings.py → HEADLESS）
            if HEADLESS:
                # 添加无头模式启动参数（第三方：selenium → Options.add_argument）
                options.add_argument("--headless=new")
            # 禁用 GPU，提高自动化稳定性（第三方：selenium → Options.add_argument）
            options.add_argument("--disable-gpu")
            # 忽略证书错误（第三方：selenium → Options.add_argument）
            options.add_argument("--ignore-certificate-errors")
            # 关闭沙箱，在 CI/Linux 容器中常需要此参数（第三方：selenium → Options.add_argument）
            options.add_argument("--no-sandbox")
            # 启动时最大化窗口（第三方：selenium → Options.add_argument）
            options.add_argument("--start-maximized")
            # 实例化 Chrome WebDriver（第三方：selenium → webdriver.Chrome）
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),  # 自动下载并安装 Chrome 驱动（第三方：webdriver_manager.chrome → ChromeDriverManager）
                options=options,  # 传入 Chrome 启动选项（第三方：selenium → Options）
            )
        # 设置隐式等待：查找元素时若未立即找到，会在 IMPLICIT_WAIT 秒内重试（第三方：selenium → WebDriver.implicitly_wait）
        driver.implicitly_wait(IMPLICIT_WAIT)  # 隐式等待秒数（项目：config/settings.py → IMPLICIT_WAIT）
        # 设置页面加载超时：get() 打开页面超过该秒数则抛出超时异常（第三方：selenium → WebDriver.set_page_load_timeout）
        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)  # 页面加载超时秒数（项目：config/settings.py → PAGE_LOAD_TIMEOUT）
        # 返回配置完成的 driver，供测试用例使用（第三方：selenium → webdriver.Remote）
        return driver

    @staticmethod
    def quit_driver(driver: webdriver.Remote) -> None:
        """安全关闭 WebDriver 并释放资源。"""
        # 仅当 driver 不为 None 时才尝试关闭，避免空引用错误（Python 内置：None）
        if driver is not None:
            try:
                # quit() 会关闭所有窗口并结束浏览器进程（第三方：selenium → WebDriver.quit）
                driver.quit()
            except Exception:
                # 关闭失败时静默忽略，确保测试 teardown 不会因清理失败而中断（Python 内置：Exception）
                pass  # 忽略关闭异常（Python 内置：pass）
