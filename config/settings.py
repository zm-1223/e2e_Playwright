# =============================================================================
# config/settings.py — 项目全局配置中心 （项目：config/settings.py）
# 作用：集中管理 Tigshop 站点 URL、测试账号、超时/重试、Allure 路径等常量 （项目：config/settings.py）
# 说明：启动时从 .env 加载环境变量覆盖默认值；被 conftest、Page Object、API Client 等广泛引用 （项目：config/settings.py）
# =============================================================================

# 导入 os：读取环境变量 os.getenv，供账号等敏感配置从 .env 覆盖 （标准库：os）
import os
# 导入 Path：以面向对象方式拼接项目根路径、报告目录等 （标准库：pathlib.Path）
from pathlib import Path
# 导入 load_dotenv：将 .env 文件中的键值对注入 os.environ （第三方：python-dotenv → load_dotenv）
from dotenv import load_dotenv

# 计算项目根目录：当前文件 config/settings.py 的上两级目录即 E2E_demo 根 （标准库：Path.__file__, resolve, parent）
BASE_DIR = Path(__file__).resolve().parent.parent
# 从项目根目录加载 .env，使后续 os.getenv 能读到本地环境变量 （第三方：python-dotenv → load_dotenv）
load_dotenv(BASE_DIR / ".env")

# ---------- 账号（.env 可覆盖） ----------
# 买家登录用户名：优先读环境变量 BUYER_USERNAME，缺省为 "123123" （标准库：os.getenv）
BUYER_USERNAME = os.getenv("BUYER_USERNAME", "123123")
# 买家登录密码：优先读环境变量 BUYER_PASSWORD，缺省为 "123123" （标准库：os.getenv）
BUYER_PASSWORD = os.getenv("BUYER_PASSWORD", "123123")
# 后台管理员用户名：优先读环境变量 ADMIN_USERNAME，缺省为 "demo" （标准库：os.getenv）
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "demo")
# 后台管理员密码：优先读环境变量 ADMIN_PASSWORD，缺省为 "demo123" （标准库：os.getenv）
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "demo123")

# 兼容旧变量名
# 旧名 USER_EMAIL 映射到 BUYER_USERNAME，供历史代码或文档引用 （项目：config/settings.py → BUYER_USERNAME）
USER_EMAIL = BUYER_USERNAME
# 旧名 USER_PASSWORD 映射到 BUYER_PASSWORD，保持向后兼容 （项目：config/settings.py → BUYER_PASSWORD）
USER_PASSWORD = BUYER_PASSWORD

# ---------- Tigshop 站点 ----------
# 前台 UI 根地址，Page Object 与 UI 测试导航使用 （项目：ui/pages/*, tests/conftest.py → UI_BASE_URL）
UI_BASE_URL = "https://demo.tigshop.cn"
# 后台管理 UI 根地址，admin Page Object 登录与操作使用 （项目：ui/pages/admin/*, tests/conftest.py → ADMIN_UI_BASE_URL）
ADMIN_UI_BASE_URL = "https://demo.tigshop.cn/admin"
# 买家端 REST API 根地址，Auth/Product/Cart 等 Client 的 base_url 来源 （项目：tests/conftest.py → api_base_url）
API_BASE_URL = "https://demo.tigshop.cn/api"
# 后台 REST API 根地址，AdminApiClient 的 base_url 来源 （项目：tests/conftest.py → admin_api_base_url）
ADMIN_API_BASE_URL = "https://demo.tigshop.cn/adminapi"

# 默认浏览器类型，DriverManager 创建 WebDriver 时使用 （项目：ui/driver/driver_manager.py → BROWSER）
BROWSER = "chrome"
# 是否无头模式运行浏览器，False 表示有界面便于本地调试 （项目：ui/driver/driver_manager.py → HEADLESS）
HEADLESS = False

# Selenium 隐式等待秒数：find_element 全局默认最长等待时间 （项目：ui/driver/driver_manager.py → IMPLICIT_WAIT）
IMPLICIT_WAIT = 10
# 显式等待默认超时，BasePage 中 WebDriverWait 使用 （项目：ui/pages/base_page.py → EXPLICIT_WAIT）
EXPLICIT_WAIT = 20
# 页面加载超时，driver.set_page_load_timeout 使用 （项目：ui/driver/driver_manager.py → PAGE_LOAD_TIMEOUT）
PAGE_LOAD_TIMEOUT = 45
# 等待 document.readyState 为 complete 的超时 （项目：utils/wait_helper.py → PAGE_READY_TIMEOUT）
PAGE_READY_TIMEOUT = 25
# 关键 UI 操作后的稳定延迟秒数，减轻页面抖动 （项目：utils/wait_helper.py → ACTION_STABLE_DELAY）
ACTION_STABLE_DELAY = 0.5
# UI 操作失败时的默认重试次数 （项目：utils/wait_helper.py → ACTION_RETRY_COUNT）
ACTION_RETRY_COUNT = 3

# API 网络请求失败时的最大重试次数 （项目：api/client/base_client.py → API_RETRY_COUNT）
API_RETRY_COUNT = 3
# API 重试间隔秒数，两次请求之间的 sleep 时长 （项目：api/client/base_client.py → API_RETRY_DELAY）
API_RETRY_DELAY = 1.0

# 商品搜索默认关键词，UI/E2E 测试未指定 keyword 时使用 （项目：tests/ui/*, tests/e2e/* → DEFAULT_SEARCH_KEYWORD）
DEFAULT_SEARCH_KEYWORD = "T"
# 默认测试商品 ID，加购/详情等用例的 fallback （项目：tests/conftest.py → DEFAULT_PRODUCT_ID）
DEFAULT_PRODUCT_ID = 338
# 无效商品 ID，异常 UI 用例访问不存在商品页时使用 （项目：tests/ui/test_exception_ui.py → INVALID_PRODUCT_ID）
INVALID_PRODUCT_ID = 999999999
# 默认分类 ID，分类列表 UI 用例使用 （项目：tests/ui/test_front_home_ui.py → DEFAULT_CATEGORY_ID）
DEFAULT_CATEGORY_ID = 1

# 前台 localStorage 中买家 JWT 的键名，session_sync 读写 token 使用 （项目：utils/session_sync.py → AUTH_TOKEN_KEY）
AUTH_TOKEN_KEY = "token"
# 后台 localStorage 中管理员 JWT 的键名 （项目：utils/session_sync.py → ADMIN_AUTH_TOKEN_KEY）
ADMIN_AUTH_TOKEN_KEY = "adminToken"

# 是否在 UI 操作前自动关闭弹窗/遮挡层 （项目：utils/popup_handler.py → AUTO_DISMISS_POPUP）
AUTO_DISMISS_POPUP = True
# 弹窗关闭按钮的 CSS 选择器列表，PopupHandler 依次尝试点击 （项目：utils/popup_handler.py → POPUP_CLOSE_SELECTORS）
POPUP_CLOSE_SELECTORS = [
    ".el-message-box__headerbtn",  # Element Plus 消息框关闭按钮 （项目：config/settings.py → POPUP_CLOSE_SELECTORS）
    ".el-dialog__headerbtn",       # Element Plus 对话框标题栏关闭 （项目：config/settings.py → POPUP_CLOSE_SELECTORS）
    ".el-drawer__close-btn",         # Element Plus 抽屉关闭按钮 （项目：config/settings.py → POPUP_CLOSE_SELECTORS）
    "[aria-label='Close']",          # 通用无障碍关闭标签 （项目：config/settings.py → POPUP_CLOSE_SELECTORS）
    ".el-icon-close",                # Element Plus 关闭图标类 （项目：config/settings.py → POPUP_CLOSE_SELECTORS）
# 作用：执行本行逻辑；调用关系：见上下文；自定义/框架：自定义；来源(config/settings.py)
]

# Allure 原始结果输出目录，pytest --alluredir 与 generate_allure_report 使用 （项目：tests/conftest.py, generate_allure_report.py → ALLURE_RESULTS_DIR）
ALLURE_RESULTS_DIR = BASE_DIR / "reports" / "allure-results"
# Allure HTML 报告生成目录 （项目：generate_allure_report.py → ALLURE_REPORT_DIR）
ALLURE_REPORT_DIR = BASE_DIR / "reports" / "allure-report"
# UI 失败截图保存目录 （项目：tests/conftest.py → SCREENSHOTS_DIR）
SCREENSHOTS_DIR = BASE_DIR / "reports" / "screenshots"

# API 请求头（模拟浏览器，降低反爬拦截）
# HTTP User-Agent 字符串，BaseApiClient 写入 session.headers，模拟 Chrome 浏览器 （项目：api/client/base_client.py → API_USER_AGENT）
API_USER_AGENT = (
# 作用：执行本行逻辑；调用关系：见上下文；自定义/框架：自定义；来源(config/settings.py)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
# 作用：执行本行逻辑；调用关系：见上下文；自定义/框架：自定义；来源(config/settings.py)
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(config/settings.py)
)
