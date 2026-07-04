# =============================================================================（项目：generate_allure_report.py）
# generate_allure_report.py — 生成 Allure HTML 测试报告（项目：generate_allure_report.py）
# 作用：读取 pytest 产生的 allure-results，调用 Allure CLI 生成可视化报告并可自动打开浏览器（项目：generate_allure_report.py）
# =============================================================================（项目：generate_allure_report.py）

# 导入 shutil：查找系统 PATH 中的可执行文件（如 allure 命令）（标准库：shutil）
import shutil
# 导入 subprocess：在子进程中执行外部命令（allure generate、pytest）（标准库：subprocess）
import subprocess
# 导入 sys：访问命令行参数 argv、当前 Python 解释器路径 executable（标准库：sys）
import sys
# 导入 webbrowser：用系统默认浏览器打开本地 HTML 文件（标准库：webbrowser）
import webbrowser
# 导入 Path：跨平台路径对象，便于拼接与解析绝对路径（标准库：pathlib.Path）
from pathlib import Path

# __file__ 是当前脚本路径；resolve() 转为绝对路径；parent 是脚本所在目录（项目根 E2E_demo）（项目：ROOT）
ROOT = Path(__file__).resolve().parent
# pytest-allure 插件写入的原始结果目录（项目：RESULTS_DIR）
RESULTS_DIR = ROOT / "reports" / "allure-results"
# Allure CLI 生成的 HTML 报告输出目录（项目：REPORT_DIR）
REPORT_DIR = ROOT / "reports" / "allure-report"


# 从 allure-results 生成 HTML 报告（项目：generate_allure_report.py → generate_allure_report）
def generate_allure_report(open_browser: bool = True) -> int:
    """从 allure-results 生成 HTML 报告，并用默认浏览器打开 index.html。"""
    # 若结果目录不存在，或目录为空（没有任何结果文件），则无法生成报告（项目：RESULTS_DIR）
    if not RESULTS_DIR.exists() or not any(RESULTS_DIR.iterdir()):
        # 提示用户先运行测试以产生 allure-results（第三方：pytest）
        print("未找到测试结果，请先运行测试：")
        print("  .venv\\Scripts\\pytest.exe tests -v")
        # 返回非 0 表示失败，供命令行或调用方判断（Python 内置：int）
        return 1

    # shutil.which 在系统 PATH 中查找名为 allure 的可执行文件，找不到返回 None（标准库：shutil.which）
    allure_cmd = shutil.which("allure")  # Allure CLI 可执行文件路径（第三方：allure）
    if not allure_cmd:
        # 未安装 Allure 命令行工具时给出安装指引（第三方：allure）
        print("未找到 allure 命令，请先安装 Allure CLI 并加入 PATH：")
        print("  https://github.com/allure-framework/allure2/releases")
        return 1

    # 确保 reports/ 等父目录存在，exist_ok=True 表示已存在也不报错（标准库：pathlib.Path.mkdir）
    REPORT_DIR.parent.mkdir(parents=True, exist_ok=True)
    # 运行子进程：allure generate <结果目录> -o <输出目录> --clean（清空旧报告）（标准库：subprocess.run）
    result = subprocess.run(  # Allure 命令执行结果（标准库：subprocess.CompletedProcess）
        [allure_cmd, "generate", str(RESULTS_DIR), "-o", str(REPORT_DIR), "--clean"],
        cwd=str(ROOT),  # 子进程工作目录设为项目根（项目：ROOT）
    )
    # Allure 命令执行失败时直接返回其退出码（标准库：subprocess.CompletedProcess.returncode）
    if result.returncode != 0:
        return result.returncode

    # 报告入口 HTML 文件路径（项目：index_html）
    index_html = REPORT_DIR / "index.html"  # Allure 报告 index.html 路径（项目：index_html）
    # 打印分隔线与报告路径，方便用户手动打开（Python 内置：print）
    print("\n" + "=" * 60)
    print(f"Allure 报告已生成: {index_html}")
    print("也可手动用浏览器打开上述 index.html")
    print("=" * 60)

    # open_browser 为 True 且 index.html 已生成时，用默认浏览器打开 file:// URI（标准库：webbrowser.open）
    if open_browser and index_html.exists():
        webbrowser.open(index_html.resolve().as_uri())

    # 0 表示成功（Python 内置：int）
    return 0


# 运行 pytest 并生成 Allure 报告（项目：generate_allure_report.py → run_tests_and_report）
def run_tests_and_report(pytest_args: list = None, open_browser: bool = True) -> int:
    """运行 pytest 并生成可视化 Allure 报告。"""
    # 若未传入 pytest 参数，默认运行 tests 目录且 verbose 输出（项目：pytest_args）
    args = pytest_args or ["tests", "-v"]  # 实际传给 pytest 的参数列表（项目：args）
    # 优先使用项目虚拟环境中的 pytest.exe（Windows 路径）（第三方：pytest）
    pytest_exe = ROOT / ".venv" / "Scripts" / "pytest.exe"  # pytest 可执行文件路径（第三方：pytest）
    if not pytest_exe.exists():
        # 虚拟环境不存在时，尝试与当前 python 同目录的 pytest.exe（标准库：sys.executable）
        pytest_exe = Path(sys.executable).with_name("pytest.exe")
        if not pytest_exe.exists():
            # 再不行则直接用当前 Python 解释器（需已安装 pytest 模块）（标准库：sys.executable）
            pytest_exe = Path(sys.executable)

    # 组装完整命令行：pytest 可执行文件 + 参数列表（项目：test_cmd）
    test_cmd = [str(pytest_exe), *args]  # pytest 完整命令行（项目：test_cmd）
    print("运行测试:", " ".join(test_cmd))
    # 运行 pytest，cwd 为项目根（标准库：subprocess.run）
    test_result = subprocess.run(test_cmd, cwd=str(ROOT))  # pytest 执行结果（标准库：subprocess.CompletedProcess）
    # 测试结束后无论成败都尝试生成报告（便于查看失败详情）（项目：generate_allure_report）
    report_result = generate_allure_report(open_browser=open_browser)  # 报告生成退出码（项目：generate_allure_report）
    # 若 pytest 失败则返回 pytest 退出码；否则返回报告生成退出码（标准库：subprocess.CompletedProcess.returncode）
    return test_result.returncode or report_result


# 仅当直接运行本脚本时执行（python generate_allure_report.py），被 import 时不执行（Python 内置：__name__）
if __name__ == "__main__":
    # 命令行含 --no-open 时不自动打开浏览器（标准库：sys.argv）
    open_in_browser = "--no-open" not in sys.argv  # 是否自动打开浏览器（项目：open_in_browser）
    # --report-only：只根据已有 allure-results 生成报告，不跑测试（标准库：sys.argv）
    if "--report-only" in sys.argv:
        raise SystemExit(generate_allure_report(open_browser=open_in_browser))

    # 过滤掉本脚本识别的特殊参数，其余传给 pytest（标准库：sys.argv）
    extra = [a for a in sys.argv[1:] if a not in ("--no-open", "--report-only")]  # 传给 pytest 的额外参数（项目：extra）
    # 无额外参数时默认 tests -v；SystemExit 将退出码传给操作系统（Python 内置：SystemExit）
    raise SystemExit(run_tests_and_report(pytest_args=extra or ["tests", "-v"], open_browser=open_in_browser))
