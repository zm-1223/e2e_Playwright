@echo off
REM 将项目 .venv 加入当前 CMD 窗口 PATH，之后可直接输入 pytest
set "PATH=%~dp0.venv\Scripts;%PATH%"
echo [OK] 已启用项目虚拟环境，可直接运行: pytest
echo      默认执行 tests/ 目录下全部 test_*.py 用例
