# =============================================================================
# generate_allure_report.py — 生成 Allure HTML 测试报告 （项目：generate_allure_report.py）
# 作用：读取 pytest 产生的 allure-results，调用 Allure CLI 生成可视化报告并可自动打开浏览器 （项目：generate_allure_report.py）
# 调用关系：被 run_e2e.py 调用；也可直接 `python generate_allure_report.py` 作为 CLI 入口 （项目：generate_allure_report.py）
# =============================================================================

# 导入 shutil：在系统 PATH 中查找 allure 可执行文件路径 （标准库：shutil）
import shutil
# 导入 subprocess：在子进程中执行外部命令（allure generate、pytest） （标准库：subprocess）
import subprocess
# 导入 sys：访问命令行参数 argv、当前 Python 解释器路径 executable （标准库：sys）
import sys
# 导入 webbrowser：用系统默认浏览器打开本地 HTML 报告文件 （标准库：webbrowser）
import webbrowser
# 导入 Path：跨平台路径对象，便于拼接与解析绝对路径 （标准库：pathlib.Path）
from pathlib import Path

# __file__ 是当前脚本路径；resolve() 转为绝对路径；parent 即项目根目录 E2E_demo （项目：generate_allure_report.py → ROOT）
ROOT = Path(__file__).resolve().parent
# pytest-allure 插件运行测试后写入的原始 JSON 结果目录 （项目：generate_allure_report.py → RESULTS_DIR）
RESULTS_DIR = ROOT / "reports" / "allure-results"
# Allure CLI 生成的 HTML 可视化报告输出目录 （项目：generate_allure_report.py → REPORT_DIR）
REPORT_DIR = ROOT / "reports" / "allure-report"


# 从 allure-results 目录生成 HTML 报告，可选自动打开浏览器 （项目：generate_allure_report.py → generate_allure_report）
def generate_allure_report(open_browser: bool = True) -> int:
    """从 allure-results 生成 HTML 报告，并用默认浏览器打开 index.html。"""
    # 检查结果目录是否存在且非空；空目录表示尚未运行过带 Allure 的 pytest （项目：generate_allure_report.py → RESULTS_DIR）
    if not RESULTS_DIR.exists() or not any(RESULTS_DIR.iterdir()):
        # 向控制台输出提示，引导用户先运行测试 （Python 内置：print）
        print("未找到测试结果，请先运行测试：")
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(generate_allure_report.py)
        print("  .venv\\Scripts\\pytest.exe tests -v")
        # 返回退出码 1 表示失败，供 CLI 或调用方判断 （Python 内置：int）
        return 1

    # shutil.which 在系统 PATH 中查找名为 allure 的可执行文件，未安装则返回 None （标准库：shutil.which）
    allure_cmd = shutil.which("allure")
    # 未找到 Allure CLI 时打印安装指引并返回失败码 （第三方：allure CLI）
    if not allure_cmd:
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(generate_allure_report.py)
        print("未找到 allure 命令，请先安装 Allure CLI 并加入 PATH：")
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(generate_allure_report.py)
        print("  https://github.com/allure-framework/allure2/releases")
# 作用：返回结果给调用方；调用关系：函数出口；自定义/框架：Python 内置；来源(return)
        return 1

    # 确保 reports/ 等父目录存在，exist_ok=True 表示目录已存在时不报错 （标准库：pathlib.Path.mkdir）
    REPORT_DIR.parent.mkdir(parents=True, exist_ok=True)
    # 启动子进程执行 allure generate：读取 RESULTS_DIR，输出到 REPORT_DIR，--clean 清空旧报告 （标准库：subprocess.run）
    result = subprocess.run(
# 作用：执行本行逻辑；调用关系：见上下文；自定义/框架：自定义；来源(generate_allure_report.py)
        [allure_cmd, "generate", str(RESULTS_DIR), "-o", str(REPORT_DIR), "--clean"],
        cwd=str(ROOT),  # 子进程工作目录设为项目根，保证相对路径一致 （项目：generate_allure_report.py → ROOT）
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(generate_allure_report.py)
    )
    # Allure 命令执行失败时直接返回其退出码，不继续打开浏览器 （标准库：subprocess.CompletedProcess.returncode）
    if result.returncode != 0:
# 作用：返回结果给调用方；调用关系：函数出口；自定义/框架：Python 内置；来源(return)
        return result.returncode

    # 拼接 Allure 报告入口 HTML 文件的完整路径 （项目：generate_allure_report.py → index_html）
    index_html = REPORT_DIR / "index.html"
    # 打印分隔线与报告路径，方便用户手动复制打开 （Python 内置：print）
    print("\n" + "=" * 60)
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(generate_allure_report.py)
    print(f"Allure 报告已生成: {index_html}")
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(generate_allure_report.py)
    print("也可手动用浏览器打开上述 index.html")
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(generate_allure_report.py)
    print("=" * 60)

    # open_browser 为 True 且 index.html 已生成时，用默认浏览器打开 file:// URI （标准库：webbrowser.open）
    if open_browser and index_html.exists():
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(generate_allure_report.py)
        webbrowser.open(index_html.resolve().as_uri())

    # 返回 0 表示报告生成成功 （Python 内置：int）
    return 0


# 先运行 pytest 收集结果，再调用 generate_allure_report 生成 HTML 报告 （项目：generate_allure_report.py → run_tests_and_report）
def run_tests_and_report(pytest_args: list = None, open_browser: bool = True) -> int:
    """运行 pytest 并生成可视化 Allure 报告。"""
    # 若调用方未传入 pytest 参数，默认运行 tests 目录且 verbose 输出 （项目：generate_allure_report.py → pytest_args）
    args = pytest_args or ["tests", "-v"]
    # 优先使用项目虚拟环境中的 pytest.exe（Windows 路径约定） （第三方：pytest）
    pytest_exe = ROOT / ".venv" / "Scripts" / "pytest.exe"
    # 虚拟环境 pytest 不存在时，尝试与当前 python 同目录的 pytest.exe （标准库：sys.executable）
    if not pytest_exe.exists():
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(generate_allure_report.py)
        pytest_exe = Path(sys.executable).with_name("pytest.exe")
        # 仍不存在则直接用当前 Python 解释器（需已通过 pip 安装 pytest 模块） （标准库：sys.executable）
        if not pytest_exe.exists():
# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源(generate_allure_report.py)
            pytest_exe = Path(sys.executable)

    # 组装完整命令行：pytest 可执行文件 + 用户/默认参数列表 （项目：generate_allure_report.py → test_cmd）
    test_cmd = [str(pytest_exe), *args]
    # 打印即将执行的命令，便于用户复制调试 （Python 内置：print）
    print("运行测试:", " ".join(test_cmd))
    # 在子进程中运行 pytest，cwd 设为项目根目录 （标准库：subprocess.run）
    test_result = subprocess.run(test_cmd, cwd=str(ROOT))
    # 无论 pytest 成败都尝试生成报告，便于查看失败用例的 Allure 详情 （项目：generate_allure_report.py → generate_allure_report）
    report_result = generate_allure_report(open_browser=open_browser)
    # pytest 失败时优先返回 pytest 退出码；pytest 成功则返回报告生成退出码 （标准库：subprocess.CompletedProcess.returncode）
    return test_result.returncode or report_result


# 仅当直接运行本脚本时执行（python generate_allure_report.py），被 import 时不执行 （Python 内置：__name__）
if __name__ == "__main__":
    # 解析命令行：含 --no-open 时不自动打开浏览器 （标准库：sys.argv）
    open_in_browser = "--no-open" not in sys.argv
    # --report-only 模式：只根据已有 allure-results 生成报告，不跑 pytest （标准库：sys.argv）
    if "--report-only" in sys.argv:
# 作用：抛出异常；调用关系：错误向上传递；自定义/框架：Python 内置；来源(raise)
        raise SystemExit(generate_allure_report(open_browser=open_in_browser))

    # 过滤掉本脚本识别的特殊参数，其余原样传给 pytest （标准库：sys.argv）
    extra = [a for a in sys.argv[1:] if a not in ("--no-open", "--report-only")]
    # 无额外参数时使用默认 tests -v；SystemExit 将整数退出码传给操作系统 （Python 内置：SystemExit）
    raise SystemExit(run_tests_and_report(pytest_args=extra or ["tests", "-v"], open_browser=open_in_browser))
