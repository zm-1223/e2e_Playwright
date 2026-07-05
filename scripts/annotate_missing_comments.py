# =============================================================================
# scripts/annotate_missing_comments.py — 为缺少注释的代码行补全中文注释
# 作用：扫描项目 .py 文件，按既有风格为无注释行添加上方说明行
# 调用关系：由维护者手动执行 python scripts/annotate_missing_comments.py
# =============================================================================
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"__pycache__", ".venv", "scripts"}


def is_documented(lines: list[str], idx: int) -> bool:
    line = lines[idx]
    s = line.strip()
    if not s or s.startswith("#"):
        return True
    if s.startswith('"""') or s.startswith("'''"):
        return True
    if re.search(r"\s#", line):
        return True
    if idx > 0:
        prev = lines[idx - 1].strip()
        if prev.startswith("#"):
            return True
    return False


def guess_comment(line: str, filepath: Path) -> str:
    s = line.strip()
    rel = filepath.as_posix()
    if s.startswith("from ") or s.startswith("import "):
        mod = s.split()[1].split(".")[0]
        kind = "标准库" if mod in {"sys", "os", "re", "time", "json", "pathlib", "typing", "datetime", "shutil", "subprocess", "webbrowser"} else (
            "第三方" if mod in {"pytest", "allure", "requests", "selenium", "dotenv"} else "自定义"
        )
        return f"# 作用：导入依赖模块；调用关系：本文件后续代码使用；自定义/框架：{kind}；来源({s})"
    if s.startswith("class "):
        name = s.split()[1].split("(")[0].rstrip(":")
        return f"# 作用：定义类 {name}；调用关系：被测试或模块内实例化；自定义/框架：自定义；来源({rel})"
    if s.startswith("def "):
        name = s.split()[1].split("(")[0]
        return f"# 作用：定义函数/方法 {name}；调用关系：见函数体调用链；自定义/框架：自定义；来源({rel})"
    if s.startswith("@"):
        return f"# 作用：装饰器 {s}；调用关系：修饰紧随其后的类/函数；自定义/框架：框架；来源({s.split('(')[0]})"
    if s.startswith("return "):
        return f"# 作用：返回结果给调用方；调用关系：函数出口；自定义/框架：Python 内置；来源(return)"
    if s.startswith("if ") or s.startswith("elif "):
        return f"# 作用：条件分支判断；调用关系：控制流程；自定义/框架：Python 内置；来源(if)"
    if s.startswith("except ") or s == "except Exception:":
        return f"# 作用：捕获异常；调用关系：try/except 错误处理；自定义/框架：Python 内置；来源(except)"
    if s.startswith("try:") or s == "try:":
        return f"# 作用：尝试执行可能失败的操作；调用关系：异常处理块；自定义/框架：Python 内置；来源(try)"
    if s.startswith("finally:") or s == "finally:":
        return f"# 作用：无论成败都执行的清理逻辑；调用关系：try/finally；自定义/框架：Python 内置；来源(finally)"
    if s.startswith("for ") or s.startswith("while "):
        return f"# 作用：循环遍历；调用关系：迭代处理；自定义/框架：Python 内置；来源(循环)"
    if s == "continue":
        return f"# 作用：跳过本次循环剩余代码；调用关系：for/while 内部；自定义/框架：Python 内置；来源(continue)"
    if s == "raise" or s.startswith("raise "):
        return f"# 作用：抛出异常；调用关系：错误向上传递；自定义/框架：Python 内置；来源(raise)"
    if s == "pass":
        return f"# 作用：占位空操作；调用关系：语法需要无实际逻辑；自定义/框架：Python 内置；来源(pass)"
    if s.startswith("assert "):
        return f"# 作用：断言条件为真；调用关系：pytest 用例校验；自定义/框架：框架(pytest)；来源(assert)"
    if ".click()" in s:
        return f"# 作用：点击页面元素；调用关系：Selenium WebElement.click；自定义/框架：框架(Selenium)；来源(selenium)"
    if ".send_keys(" in s:
        return f"# 作用：向输入框发送文本/按键；调用关系：Selenium WebElement.send_keys；自定义/框架：框架(Selenium)；来源(selenium)"
    if ".find_element" in s or ".find_elements" in s:
        return f"# 作用：定位 DOM 元素；调用关系：Selenium WebDriver；自定义/框架：框架(Selenium)；来源(selenium)"
    if ".get(" in s and "driver" in s:
        return f"# 作用：浏览器导航到 URL；调用关系：Selenium WebDriver.get；自定义/框架：框架(Selenium)；来源(selenium)"
    if s.endswith(")"):
        return f"# 作用：调用方法/函数；调用关系：见左侧调用表达式；自定义/框架：自定义或框架；来源({rel})"
    if "=" in s and not s.startswith("("):
        return f"# 作用：赋值/绑定变量；调用关系：供后续步骤使用；自定义/框架：Python 内置；来源(赋值)"
    return f"# 作用：执行本行逻辑；调用关系：见上下文；自定义/框架：自定义；来源({rel})"


def annotate_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    out: list[str] = []
    added = 0
    for i, line in enumerate(lines):
        if not is_documented(lines, i) and line.strip():
            out.append(guess_comment(line, path.relative_to(ROOT)))
            added += 1
        out.append(line)
    if added:
        path.write_text("\n".join(out) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")
    return added


def main() -> None:
    total = 0
    for p in sorted(ROOT.rglob("*.py")):
        if p.name.startswith("_check") or "annotate_missing" in p.name:
            continue
        if any(s in p.parts for s in SKIP):
            continue
        n = annotate_file(p)
        if n:
            print(f"{p.relative_to(ROOT)}: +{n}")
            total += n
    print(f"done, added {total} comment lines")


if __name__ == "__main__":
    main()
