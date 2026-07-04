# tests/__init__.py — tests 包的初始化文件（项目：tests/__init__.py → 包初始化）
# 作用：把 tests 目录标记为 Python 包，便于 pytest 发现用例；通常无需写测试逻辑（第三方：pytest → 用例发现）
# 说明：即使文件几乎为空，存在 __init__.py 后 import tests.xxx 才符合包结构约定（标准库：import 机制 → 包结构）

# 模块级文档字符串：描述本包用途，help(tests) 或 IDE 悬停时可看到（Python 内置：__doc__ → 模块文档）
"""pytest 测试用例根目录。"""
