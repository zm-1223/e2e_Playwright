@echo off
REM 运行全部测试 + 生成 Allure HTML 报告 + 用浏览器打开
set ROOT=%~dp0
setlocal

echo [1/2] 运行测试...
"%ROOT%.venv\Scripts\pytest.exe" "%ROOT%tests" -v
set TEST_EXIT=%ERRORLEVEL%

echo.
echo [2/2] 生成 Allure 可视化报告...
allure generate "%ROOT%reports\allure-results" -o "%ROOT%reports\allure-report" --clean
if errorlevel 1 (
    echo 生成报告失败，请确认已安装 Allure CLI 并已加入 PATH
    exit /b 1
)

echo.
echo 报告路径: %ROOT%reports\allure-report\index.html
start "" "%ROOT%reports\allure-report\index.html"

exit /b %TEST_EXIT%
