# =============================================================================
# run_e2e.py — 一键运行全部测试并生成 Allure 报告 （项目：run_e2e.py）
# 作用：项目简化入口脚本，适合初学者双击或在命令行 `python run_e2e.py` 快速跑完整套测试 （项目：run_e2e.py）
# 调用关系：内部调用 generate_allure_report.run_tests_and_report；不直接被测试代码 import （项目：run_e2e.py）
# =============================================================================

# 导入 subprocess：本文件未直接使用，但 generate_allure_report 通过它调用 pytest/allure （标准库：subprocess）
import subprocess
# 导入 sys：用于 sys.exit / SystemExit 向操作系统传递进程退出码 （标准库：sys）
import sys
# 导入 Path：定位项目根目录，与 generate_allure_report 保持一致 （标准库：pathlib.Path）
from pathlib import Path

# 当前脚本所在目录即为项目根目录 E2E_demo （项目：run_e2e.py → ROOT）
ROOT = Path(__file__).resolve().parent


# 项目 CLI 入口函数：跑全部测试并自动生成、打开 Allure 报告 （项目：run_e2e.py → main）
def main():  # 作用：封装一键跑测与报告生成；调用关系：__main__ 块调用；自定义/框架：自定义；来源(本文件)
    # 方法文档：说明 main 对用户可见的行为（Python 内置：docstring）
    """一键运行全部测试并生成 Allure 可视化报告（自动打开浏览器）。"""
    # 延迟导入：避免在仅 import run_e2e 模块时加载 generate_allure_report 的全部依赖链 （项目：generate_allure_report.py → run_tests_and_report）
    from generate_allure_report import run_tests_and_report

    # 调用共用逻辑：运行 tests 目录、verbose 模式、测试结束后自动打开 Allure HTML 报告 （项目：generate_allure_report.py → run_tests_and_report）
    return run_tests_and_report(pytest_args=["tests", "-v"], open_browser=True)


# 直接执行 `python run_e2e.py` 时进入此分支；被其他模块 import 时不执行 （Python 内置：__name__）
if __name__ == "__main__":  # 作用：脚本直接运行入口；调用关系：python run_e2e.py；自定义/框架：框架(Python)；来源(Python)
    # main() 返回整数退出码（0=成功，非0=失败）；raise SystemExit 等价于 sys.exit （Python 内置：SystemExit）
    raise SystemExit(main())
