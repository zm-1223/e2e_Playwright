# =============================================================================（项目：run_e2e.py）
# run_e2e.py — 一键运行全部测试并生成 Allure 报告（项目：run_e2e.py）
# 作用：项目入口脚本，适合初学者双击或在命令行 python run_e2e.py 快速跑完整套测试（项目：run_e2e.py）
# =============================================================================（项目：run_e2e.py）

# 导入 subprocess：本文件通过 generate_allure_report 间接用它调用 pytest（此处未直接使用）（标准库：subprocess）
import subprocess
# 导入 sys：用于 sys.exit 传递进程退出码（main 的返回值）（标准库：sys）
import sys
# 导入 Path：定位项目根目录（与 generate_allure_report 一致）（标准库：pathlib.Path）
from pathlib import Path

# 当前脚本所在目录 = 项目根目录 E2E_demo（项目：ROOT）
ROOT = Path(__file__).resolve().parent


# 项目入口函数：调用 run_tests_and_report 跑测试并生成报告（项目：run_e2e.py → main）
def main():
    """一键运行全部测试并生成 Allure 可视化报告（自动打开浏览器）。"""
    # 延迟导入：避免在仅查看本模块时加载 generate_allure_report 的全部依赖（项目：generate_allure_report.run_tests_and_report）
    from generate_allure_report import run_tests_and_report

    # 调用共用函数：跑 tests 目录、verbose 模式、测试后打开 Allure 报告（项目：run_tests_and_report）
    return run_tests_and_report(pytest_args=["tests", "-v"], open_browser=True)


# 直接执行 python run_e2e.py 时进入此分支（Python 内置：__name__）
if __name__ == "__main__":
    # main() 返回整数退出码；raise SystemExit 等价于 sys.exit，进程以此码结束（Python 内置：SystemExit）
    raise SystemExit(main())
