@echo off
REM 项目内 pytest 入口：使用 .venv，默认运行 tests/ 下全部 test_*.py
set ROOT=%~dp0
"%ROOT%.venv\Scripts\pytest.exe" %*
