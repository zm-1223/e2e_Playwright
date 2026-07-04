# 导入 json 模块，用于把 Python 字典/列表转成 JSON 字符串 （标准库：json）
import json
# 从 datetime 模块导入 datetime 类，用于生成带时间戳的文件名 （标准库：datetime.datetime）
from datetime import datetime
# 从 typing 模块导入 Optional，表示“可以是某类型，也可以是 None” （标准库：typing）
from typing import Optional
# 导入 allure 库，用于向 Allure 测试报告添加附件（截图、文本等） （第三方：allure）
import allure
# 从 pathlib 模块导入 Path，用于跨平台地处理文件/目录路径 （标准库：pathlib.Path）
from pathlib import Path


# 定义函数：把浏览器截图附加到 Allure 报告，并可选择保存到本地 （项目：utils/allure_helper.py → attach_screenshot）
def attach_screenshot(
    driver,  # 参数 driver：Selenium 浏览器驱动对象，用来执行截图 （第三方：selenium → WebDriver）
    name: str = "截图",  # 参数 name：在 Allure 报告里显示的附件名称，默认是“截图” （项目：utils/allure_helper.py → attach_screenshot）
    save_dir: Optional[Path] = None,  # 参数 save_dir：本地保存目录；None 表示只附加到报告不存盘 （标准库：pathlib.Path）
    filename: Optional[str] = None,  # 参数 filename：本地文件名（不含 .png）；None 则自动生成 （项目：utils/allure_helper.py → attach_screenshot）
) -> Optional[Path]:  # 返回值：若保存到本地则返回文件路径 Path，否则返回 None （标准库：pathlib.Path）
    """将浏览器截图附加到 Allure 报告，并可选保存到本地目录。"""
    # 调用 driver 的方法，获取当前页面截图的二进制 PNG 数据 （第三方：selenium → WebDriver.get_screenshot_as_png）
    png_bytes = driver.get_screenshot_as_png()
    # 把 PNG 二进制数据作为附件挂到 Allure 报告上 （第三方：allure → attach）
    allure.attach(png_bytes, name=name, attachment_type=allure.attachment_type.PNG)

    # 初始化 saved_path 为 None，表示默认还没有保存到本地 （Python 内置：None）
    saved_path = None
    # 如果调用者传了 save_dir，说明需要把截图写到磁盘 （项目：utils/allure_helper.py → attach_screenshot）
    if save_dir is not None:
        # 确保目标目录存在（不存在就创建，包括父目录） （项目：utils/allure_helper.py → ensure_dir）
        ensure_dir(save_dir)
        # 若没指定 filename，就用“名称_年月日_时分秒”作为文件名 （标准库：datetime.datetime.strftime）
        safe_name = filename or f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        # 拼接完整路径：目录 + 文件名 + .png 后缀 （标准库：pathlib.Path）
        saved_path = save_dir / f"{safe_name}.png"
        # 把 PNG 二进制内容写入该文件 （标准库：pathlib.Path.write_bytes）
        saved_path.write_bytes(png_bytes)
    # 返回本地保存路径（未保存则为 None） （Python 内置：return）
    return saved_path


# 定义函数：把一段文本附加到 Allure 报告 （项目：utils/allure_helper.py → attach_text）
def attach_text(content: str, name: str = "文本信息") -> None:
    """将文本内容附加到 Allure 报告。"""
    # 把字符串 content 作为 TEXT 类型附件添加到 Allure （第三方：allure → attach）
    allure.attach(content, name=name, attachment_type=allure.attachment_type.TEXT)


# 定义函数：把 Python 对象（字典/列表等）以 JSON 形式附加到 Allure 报告 （项目：utils/allure_helper.py → attach_json）
def attach_json(data, name: str = "JSON") -> None:
    """将 JSON 数据附加到 Allure 报告。"""
    # 先把 data 转成格式化的 JSON 字符串，再复用 attach_text 挂到报告上 （标准库：json.dumps）
    attach_text(json.dumps(data, ensure_ascii=False, indent=2), name=name)


# 定义函数：确保某个目录存在，不存在就创建 （项目：utils/allure_helper.py → ensure_dir）
def ensure_dir(path: Path) -> Path:
    """确保目录存在，不存在则创建。"""
    # mkdir：创建目录；parents=True 表示连父目录一起建；exist_ok=True 表示已存在也不报错 （标准库：pathlib.Path.mkdir）
    path.mkdir(parents=True, exist_ok=True)
    # 返回传入的路径对象，方便链式调用 （Python 内置：return）
    return path
