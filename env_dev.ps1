# 将项目 .venv 加入当前 PowerShell 会话 PATH，之后可直接输入 pytest
$venvScripts = Join-Path $PSScriptRoot ".venv\Scripts"
$env:Path = "$venvScripts;$env:Path"
Write-Host "[OK] 已启用项目虚拟环境，可直接运行: pytest"
Write-Host "     默认执行 tests/ 目录下全部 test_*.py 用例"
