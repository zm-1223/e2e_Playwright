# 终端命令行指南（COMMANDS.md）

> 项目：Tigshop demo E2E 自动化  
> 前台：https://demo.tigshop.cn/ · 后台：https://demo.tigshop.cn/admin/

---

## 文档导航

| 文档 | 定位 |
|------|------|
| [README.md](./README.md) | 快速入门 |
| [TESTCASES.md](./TESTCASES.md) | 29 条用例说明 |
| **COMMANDS.md（本文）** | 终端命令速查 |
| [node.md](./node.md) | 架构与面试 |

---

## 1. 环境准备

```powershell
cd D:\github-code\E2E_demo
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
copy .env.example .env
```

需要：**Chrome 浏览器**、**Allure CLI**（HTML 报告，可选）

`.env` 账号：

```
BUYER_USERNAME=123123
BUYER_PASSWORD=123123
ADMIN_USERNAME=demo
ADMIN_PASSWORD=demo123
```

---

## 2. 运行测试

```powershell
.\pytest.bat                    # 全部 29 用例
.\pytest.bat -m api             # API 13 条（无浏览器，最快）
.\pytest.bat -m ui              # UI 15 条
.\pytest.bat -m e2e             # E2E 1 条
.\pytest.bat -m smoke           # 冒烟（E2E 购买流程）
```

按文件：

```powershell
.\pytest.bat tests/api/test_home_product_api.py -v
.\pytest.bat tests/ui/test_front_shop_ui.py -v
.\pytest.bat tests/e2e/test_front_purchase_e2e.py -v
```

---

## 3. Allure 报告

`pytest` 结束后自动更新 `reports/allure-report/`（`tests/conftest.py` → `pytest_sessionfinish`，该文件含逐行中文注释说明钩子逻辑）。

```powershell
start reports\allure-report\index.html
.venv\Scripts\python.exe run_e2e.py              # 跑测 + 打开浏览器
.venv\Scripts\python.exe generate_allure_report.py --report-only
```

---

## 4. 脚本速查

| 脚本 | 作用 |
|------|------|
| `pytest.bat` | venv pytest 入口 |
| `run_e2e.py` | 跑测 + 报告 + 开浏览器 |
| `generate_allure_report.py` | 单独生成 HTML |
| `env_dev.ps1` | PowerShell 载入 venv PATH |

---

## 5. 常见问题

| 现象 | 处理 |
|------|------|
| `No module named 'allure'` | 用 `.\pytest.bat` |
| API 登录「需要行为验证」 | 正常；fixture 会自动 UI 登录同步 token |
| UI 元素找不到 | 加大 `EXPLICIT_WAIT`；检查 Nuxt 是否加载完成 |
| 购物车/结算断言失败 | 上一条用例残留；确认 `clear_cart` teardown 生效 |
| webdriver 下载失败 | 已改用 Selenium Manager；确保 Chrome 已安装 |
| 后台登录失败 | 买家账号不能登后台，用 `demo` / `demo123` |

---

## 6. 推荐工作流

```powershell
# 日常：API 快速反馈
.\pytest.bat -m api -v

# 提交前：全量
.\pytest.bat -v

# 演示
.venv\Scripts\python.exe run_e2e.py
```

---

*最后更新：2026-07-05*
