# =============================================================================
# 文件名: driver_manager.py
# 模块路径: ui/driver/driver_manager.py
# 作用: WebDriver 工厂类，按配置创建 Chrome/Edge 浏览器驱动并设置超时
# 调用关系: 被 tests/conftest.py 的 front_driver/admin_driver fixture 调用
# 类型: 自定义（项目）
# 来源: E2E_demo 项目
# =============================================================================
# 导入 Selenium webdriver 主模块，用于实例化浏览器驱动（第三方：selenium → webdriver）
from selenium import webdriver
# 导入 Chrome 浏览器选项类（第三方：selenium.webdriver.chrome.options → Options）
from selenium.webdriver.chrome.options import Options as ChromeOptions
# 导入 Chrome 驱动服务类，配合 webdriver-manager 指定驱动路径（第三方：selenium.webdriver.chrome.service → Service）
from selenium.webdriver.chrome.service import Service as ChromeService
# 导入 Edge 浏览器选项类（第三方：selenium.webdriver.edge.options → Options）
from selenium.webdriver.edge.options import Options as EdgeOptions
# 导入 Edge 驱动服务类（第三方：selenium.webdriver.edge.service → Service）
from selenium.webdriver.edge.service import Service as EdgeService

# 从项目配置导入浏览器类型、无头模式、隐式等待与页面加载超时（项目：config/settings.py → BROWSER, HEADLESS, IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT）
from config.settings import BROWSER, HEADLESS, IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT


# WebDriver 工厂类：优先 Selenium Manager 自动管理驱动，失败时回退 webdriver-manager（项目：ui/driver/driver_manager.py → WebDriverManager）
class WebDriverManager:
    """WebDriver 工厂：优先 Selenium Manager，webdriver-manager 作备选。"""

# 作用：装饰器 @staticmethod；调用关系：修饰紧随其后的类/函数；自定义/框架：框架；来源(@staticmethod)
    @staticmethod
# 作用：定义函数/方法 _create_chrome；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/driver/driver_manager.py)
    def _create_chrome(options: ChromeOptions) -> webdriver.Chrome:
        # 优先尝试 Selenium 4 内置 Selenium Manager 自动下载/匹配 ChromeDriver（第三方：selenium → webdriver.Chrome）
        try:
# 作用：返回结果给调用方；调用关系：函数出口；自定义/框架：Python 内置；来源(return)
            return webdriver.Chrome(options=options)
# 作用：捕获异常；调用关系：try/except 错误处理；自定义/框架：Python 内置；来源(except)
        except Exception:
            # Selenium Manager 失败时，延迟导入 webdriver-manager 作为备选（第三方：webdriver_manager.chrome → ChromeDriverManager）
            from webdriver_manager.chrome import ChromeDriverManager

            # 使用 webdriver-manager 安装驱动并通过 ChromeService 指定路径（第三方：webdriver_manager, selenium → ChromeService）
            return webdriver.Chrome(
# 作用：赋值/绑定变量；调用关系：供后续步骤使用；自定义/框架：Python 内置；来源(赋值)
                service=ChromeService(ChromeDriverManager().install()),
# 作用：赋值/绑定变量；调用关系：供后续步骤使用；自定义/框架：Python 内置；来源(赋值)
                options=options,
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(ui/driver/driver_manager.py)
            )

# 作用：装饰器 @staticmethod；调用关系：修饰紧随其后的类/函数；自定义/框架：框架；来源(@staticmethod)
    @staticmethod
# 作用：定义函数/方法 _create_edge；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/driver/driver_manager.py)
    def _create_edge(options: EdgeOptions) -> webdriver.Edge:
        # 优先尝试 Selenium Manager 创建 Edge 驱动（第三方：selenium → webdriver.Edge）
        try:
# 作用：返回结果给调用方；调用关系：函数出口；自定义/框架：Python 内置；来源(return)
            return webdriver.Edge(options=options)
# 作用：捕获异常；调用关系：try/except 错误处理；自定义/框架：Python 内置；来源(except)
        except Exception:
            # 失败时延迟导入 Edge Chromium 驱动管理器（第三方：webdriver_manager.microsoft → EdgeChromiumDriverManager）
            from webdriver_manager.microsoft import EdgeChromiumDriverManager

            # 通过 EdgeService 指定 webdriver-manager 安装的驱动路径（第三方：webdriver_manager, selenium → EdgeService）
            return webdriver.Edge(
# 作用：赋值/绑定变量；调用关系：供后续步骤使用；自定义/框架：Python 内置；来源(赋值)
                service=EdgeService(EdgeChromiumDriverManager().install()),
# 作用：赋值/绑定变量；调用关系：供后续步骤使用；自定义/框架：Python 内置；来源(赋值)
                options=options,
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(ui/driver/driver_manager.py)
            )

# 作用：装饰器 @staticmethod；调用关系：修饰紧随其后的类/函数；自定义/框架：框架；来源(@staticmethod)
    @staticmethod
# 作用：定义函数/方法 create_driver；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/driver/driver_manager.py)
    def create_driver() -> webdriver.Remote:
        # 根据配置 BROWSER 决定创建 Edge 还是 Chrome（项目：config/settings.py → BROWSER）
        if BROWSER == "edge":
            # 实例化 Edge 浏览器选项对象（第三方：selenium → EdgeOptions）
            options = EdgeOptions()
            # 若配置为无头模式，添加 --headless=new 参数（项目：config/settings.py → HEADLESS；第三方：selenium → Options.add_argument）
            if HEADLESS:
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(ui/driver/driver_manager.py)
                options.add_argument("--headless=new")
            # 禁用 GPU 加速，提高 CI/无头环境稳定性（第三方：selenium → Options.add_argument）
            options.add_argument("--disable-gpu")
            # 忽略 HTTPS 证书错误，便于测试环境访问（第三方：selenium → Options.add_argument）
            options.add_argument("--ignore-certificate-errors")
            # 启动时最大化窗口（第三方：selenium → Options.add_argument）
            options.add_argument("--start-maximized")
            # 调用内部方法创建 Edge 驱动实例（项目：ui/driver/driver_manager.py → WebDriverManager._create_edge）
            driver = WebDriverManager._create_edge(options)
# 作用：执行本行逻辑；调用关系：见上下文；自定义/框架：自定义；来源(ui/driver/driver_manager.py)
        else:
            # 默认分支：实例化 Chrome 浏览器选项（第三方：selenium → ChromeOptions）
            options = ChromeOptions()
            # 无头模式开关（项目：config/settings.py → HEADLESS）
            if HEADLESS:
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(ui/driver/driver_manager.py)
                options.add_argument("--headless=new")
            # 禁用 GPU（第三方：selenium → Options.add_argument）
            options.add_argument("--disable-gpu")
            # 忽略证书错误（第三方：selenium → Options.add_argument）
            options.add_argument("--ignore-certificate-errors")
            # Linux/CI 环境常用参数，避免 sandbox 权限问题（第三方：selenium → Options.add_argument）
            options.add_argument("--no-sandbox")
            # 启动最大化（第三方：selenium → Options.add_argument）
            options.add_argument("--start-maximized")
            # 调用内部方法创建 Chrome 驱动（项目：ui/driver/driver_manager.py → WebDriverManager._create_chrome）
            driver = WebDriverManager._create_chrome(options)
        # 设置隐式等待：查找元素时的默认最长等待秒数（项目：config/settings.py → IMPLICIT_WAIT；第三方：selenium → WebDriver.implicitly_wait）
        driver.implicitly_wait(IMPLICIT_WAIT)
        # 设置页面加载超时：get() 导航的最长等待秒数（项目：config/settings.py → PAGE_LOAD_TIMEOUT；第三方：selenium → WebDriver.set_page_load_timeout）
        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        # 返回配置完成的 WebDriver 实例供测试使用（第三方：selenium → webdriver.Remote）
        return driver

# 作用：装饰器 @staticmethod；调用关系：修饰紧随其后的类/函数；自定义/框架：框架；来源(@staticmethod)
    @staticmethod
# 作用：定义函数/方法 quit_driver；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/driver/driver_manager.py)
    def quit_driver(driver: webdriver.Remote) -> None:
        # 仅当 driver 非 None 时才尝试关闭，避免重复 quit（Python 内置：is not None）
        if driver is not None:
# 作用：尝试执行可能失败的操作；调用关系：异常处理块；自定义/框架：Python 内置；来源(try)
            try:
                # 关闭浏览器并释放驱动进程（第三方：selenium → WebDriver.quit）
                driver.quit()
# 作用：捕获异常；调用关系：try/except 错误处理；自定义/框架：Python 内置；来源(except)
            except Exception:
                # 忽略 quit 过程中的异常，确保 teardown 不中断（Python 内置：try/except pass）
                pass
