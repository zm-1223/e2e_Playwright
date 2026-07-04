# 导入 time 模块，用于 sleep 暂停执行（重试间隔、稳定延迟等） （标准库：time）
import time
# 从 typing 导入 Callable（可调用对象类型）和 TypeVar（泛型变量） （标准库：typing）
from typing import Callable, TypeVar
# 导入 Selenium 的 WebDriver 类型，用于函数参数类型标注 （第三方：selenium → WebDriver）
from selenium.webdriver.remote.webdriver import WebDriver
# 导入 WebDriverWait，用于在指定超时内轮询等待某个条件成立 （第三方：selenium → WebDriverWait）
from selenium.webdriver.support.ui import WebDriverWait
# 从项目配置中导入：页面就绪超时、操作后稳定延迟、默认重试次数 （项目：config/settings.py → PAGE_READY_TIMEOUT, ACTION_STABLE_DELAY, ACTION_RETRY_COUNT）
from config.settings import PAGE_READY_TIMEOUT, ACTION_STABLE_DELAY, ACTION_RETRY_COUNT

# 定义泛型变量 T，表示 retry_action 成功时返回值的类型（由传入的 func 决定） （标准库：typing.TypeVar）
T = TypeVar("T")


# 定义函数：等待浏览器页面加载完成（document.readyState 为 complete） （项目：utils/wait_helper.py → wait_for_page_ready）
def wait_for_page_ready(driver: WebDriver, timeout: int = None) -> None:
    """等待 document.readyState == complete（超时则继续，不阻塞测试）。"""
    # 若调用者没传 timeout，就用配置文件里的 PAGE_READY_TIMEOUT （项目：config/settings.py → PAGE_READY_TIMEOUT）
    wait_seconds = timeout or PAGE_READY_TIMEOUT
    # 用 try/except 包住等待逻辑，超时时不让测试失败 （Python 内置：try/except）
    try:
        # 创建 WebDriverWait，最多等 wait_seconds 秒 （第三方：selenium → WebDriverWait）
        WebDriverWait(driver, wait_seconds).until(
            # 每隔一小段时间执行 lambda：用 JS 读 readyState，等于 "complete" 则条件满足 （第三方：selenium → WebDriver.execute_script）
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
    except Exception:
        # 超时或任何异常都忽略，避免偶发慢加载导致整个用例挂掉 （Python 内置：Exception）
        pass


# 定义函数：简单休眠指定秒数 （项目：utils/wait_helper.py → wait_seconds）
def wait_seconds(seconds: float) -> None:
    # 调用 time.sleep 暂停当前线程 seconds 秒 （标准库：time.sleep）
    time.sleep(seconds)


# 定义函数：在关键操作后等待一小段时间，让页面/API 状态稳定 （项目：utils/wait_helper.py → stable_delay）
def stable_delay() -> None:
    # 只有配置了大于 0 的延迟时才 sleep，0 表示不等待 （项目：config/settings.py → ACTION_STABLE_DELAY）
    if ACTION_STABLE_DELAY > 0:
        time.sleep(ACTION_STABLE_DELAY)  # 暂停 ACTION_STABLE_DELAY 秒 （标准库：time.sleep）


# 定义函数：对可能失败的操作进行多次重试 （项目：utils/wait_helper.py → retry_action）
def retry_action(
    func: Callable[..., T],  # 要执行的可调用对象（通常是无参 lambda 或函数） （标准库：typing.Callable）
    retries: int = None,  # 最大尝试次数；None 则用配置里的 ACTION_RETRY_COUNT （项目：config/settings.py → ACTION_RETRY_COUNT）
    delay: float = 1.0,  # 每次失败后等待多少秒再重试 （项目：utils/wait_helper.py → retry_action）
    exceptions: tuple = (Exception,),  # 只捕获这些异常类型时才重试 （Python 内置：Exception）
) -> T:  # 成功时返回 func() 的返回值 （标准库：typing.TypeVar）
    """对单次操作重试（供 API 或关键步骤手动调用）。"""
    # 确定实际重试次数：显式传入优先，否则用默认值 （项目：config/settings.py → ACTION_RETRY_COUNT）
    max_retries = retries if retries is not None else ACTION_RETRY_COUNT
    # 记录最后一次失败的异常，全部重试仍失败时抛出 （Python 内置：Exception）
    last_error = None
    # 从第 1 次尝试循环到第 max_retries 次（含） （标准库：range）
    for attempt in range(1, max_retries + 1):
        try:
            # 执行 func；成功则直接返回结果，不再重试 （Python 内置：return）
            return func()
        except exceptions as exc:
            # 捕获到指定类型的异常，记下错误信息 （Python 内置：Exception）
            last_error = exc
            # 若已是最后一次尝试，把异常继续向上抛出 （Python 内置：raise）
            if attempt >= max_retries:
                raise
            # 还没用完次数，先等待 delay 秒再进入下一轮 （标准库：time.sleep）
            time.sleep(delay)
    # 理论上走不到这里；若走到则抛出最后一次错误（类型检查用 ignore） （Python 内置：raise）
    raise last_error  # type: ignore[misc]
