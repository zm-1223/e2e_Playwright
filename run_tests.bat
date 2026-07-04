@echo off
REM 与 pytest.bat 相同：使用 .venv 运行全部 test_*.py
set ROOT=%~dp0
"%ROOT%.venv\Scripts\pytest.exe" %*
