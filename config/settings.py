# =============================================================================
# config/settings.py — 项目全局配置文件 （项目：config/settings.py）
# 作用：集中存放 URL、浏览器、超时、路径等常量；账号密码从 .env 读取 （项目：config/settings.py）
# 说明：修改非敏感配置时直接改本文件即可，无需改测试代码 （项目：config/settings.py）
#
# 【注释括号说明】全项目 # 注释末尾的（）标记符号来源，格式如下：
#   （标准库：模块）          — Python 自带，如 os、pathlib
#   （第三方：包 → 符号）     — pip 安装，如 pytest、selenium、requests、dotenv
#   （项目：路径 → 符号）    — 本项目自定义，如 config/settings.py → USER_EMAIL
#   （Python 内置：符号）     — 语言内置，如 __file__、assert、None
# =============================================================================

# 导入 os 模块：用于读取操作系统环境变量（如 USER_EMAIL） （标准库：os）
import os
# 导入 Path：面向对象的路径类，比字符串拼接更安全、跨平台 （标准库：pathlib.Path）
from pathlib import Path
# 导入 load_dotenv：从 .env 文件加载键值对到环境变量，供 os.getenv 使用 （第三方：dotenv → load_dotenv）
from dotenv import load_dotenv

# __file__ 是当前 settings.py 的路径；resolve() 转为绝对路径；parent 是 config/；再 parent 是项目根 （Python 内置：__file__）
BASE_DIR = Path(__file__).resolve().parent.parent  # 项目根目录路径 （标准库：pathlib.Path）
# 从项目根目录加载 .env 文件（若不存在则静默跳过，使用默认值） （第三方：dotenv → load_dotenv）
load_dotenv(BASE_DIR / ".env")

# ---------- 敏感信息：从 .env 读取（勿提交真实密码到 Git） ----------
# os.getenv("键名", "默认值")：优先读环境变量，没有则用默认值 （标准库：os.getenv）
USER_EMAIL = os.getenv("USER_EMAIL", "customer@practicesoftwaretesting.com")  # 登录邮箱 （项目：config/settings.py → USER_EMAIL）
USER_PASSWORD = os.getenv("USER_PASSWORD", "welcome01")  # 登录密码 （项目：config/settings.py → USER_PASSWORD）

# ---------- 以下均为固定配置，直接修改本文件即可 ----------

# 被测网站的前端地址（Selenium 打开的页面） （项目：config/settings.py → UI_BASE_URL）
UI_BASE_URL = "https://practicesoftwaretesting.com"
# 被测网站的后端 API 根地址（requests 请求的目标） （项目：config/settings.py → API_BASE_URL）
API_BASE_URL = "https://api.practicesoftwaretesting.com"

# 浏览器类型：目前 driver_manager 支持 chrome / edge （项目：config/settings.py → BROWSER）
BROWSER = "chrome"
# 是否无头模式（不显示浏览器窗口）；False 便于调试，且可避免 Cloudflare 拦截 （项目：config/settings.py → HEADLESS）
HEADLESS = False  # Headless 可能触发 Cloudflare （项目：config/settings.py → HEADLESS）

# Selenium 隐式等待（秒）：find_element 找不到元素时最多等这么久 （项目：config/settings.py → IMPLICIT_WAIT）
IMPLICIT_WAIT = 10
# 显式等待（秒）：WebDriverWait 等待某条件成立的最大时间 （项目：config/settings.py → EXPLICIT_WAIT）
EXPLICIT_WAIT = 15
# 页面加载超时（秒）：driver.get(url) 等待页面加载完成的上限 （项目：config/settings.py → PAGE_LOAD_TIMEOUT）
PAGE_LOAD_TIMEOUT = 30
# 等待 document.readyState 为 complete 的超时（秒） （项目：config/settings.py → PAGE_READY_TIMEOUT）
PAGE_READY_TIMEOUT = 20
# 每次 UI 操作后的短暂停顿（秒），让动画/渲染稳定后再继续 （项目：config/settings.py → ACTION_STABLE_DELAY）
ACTION_STABLE_DELAY = 0.3
# UI 操作失败时的重试次数（如点击被遮挡） （项目：config/settings.py → ACTION_RETRY_COUNT）
ACTION_RETRY_COUNT = 3

# API 请求失败（网络错误、5xx）时的重试次数 （项目：config/settings.py → API_RETRY_COUNT）
API_RETRY_COUNT = 3
# 每次 API 重试前的等待间隔（秒） （项目：config/settings.py → API_RETRY_DELAY）
API_RETRY_DELAY = 1.0

# 默认搜索关键词，UI/E2E 测试搜索商品时使用 （项目：config/settings.py → DEFAULT_SEARCH_KEYWORD）
DEFAULT_SEARCH_KEYWORD = "pliers"
# 登录后 Token 写入 localStorage 的键名，用于 UI 与 API 会话同步 （项目：config/settings.py → AUTH_TOKEN_KEY）
AUTH_TOKEN_KEY = "auth-token"
# 下单时默认邮编（Practice Software Testing 示例站点） （项目：config/settings.py → DEFAULT_POSTCODE）
DEFAULT_POSTCODE = "2314 ST"
# 下单时默认国家 （项目：config/settings.py → DEFAULT_COUNTRY）
DEFAULT_COUNTRY = "The Netherlands"

# 是否在页面操作前自动尝试关闭弹窗/Cookie 提示 （项目：config/settings.py → AUTO_DISMISS_POPUP）
AUTO_DISMISS_POPUP = True
# 弹窗关闭按钮的 CSS 选择器列表，按顺序尝试点击 （项目：config/settings.py → POPUP_CLOSE_SELECTORS）
POPUP_CLOSE_SELECTORS = [
    "[data-test='close']",   # 站点 data-test 关闭按钮 （项目：config/settings.py → POPUP_CLOSE_SELECTORS）
    "button.close",          # Bootstrap 等常见 class （项目：config/settings.py → POPUP_CLOSE_SELECTORS）
    ".modal-close",          # 模态框关闭 （项目：config/settings.py → POPUP_CLOSE_SELECTORS）
    "[aria-label='Close']",  # 无障碍标签为 Close 的按钮 （项目：config/settings.py → POPUP_CLOSE_SELECTORS）
]

# pytest-allure 插件写入的原始结果目录（JSON/XML） （项目：config/settings.py → ALLURE_RESULTS_DIR）
ALLURE_RESULTS_DIR = BASE_DIR / "reports" / "allure-results"
# Allure CLI 生成的 HTML 报告输出目录 （项目：config/settings.py → ALLURE_REPORT_DIR）
ALLURE_REPORT_DIR = BASE_DIR / "reports" / "allure-report"
# 测试失败时 Selenium 截图保存目录 （项目：config/settings.py → SCREENSHOTS_DIR）
SCREENSHOTS_DIR = BASE_DIR / "reports" / "screenshots"
