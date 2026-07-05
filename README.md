# Tigshop E2E 自动化

基于 **pytest + Selenium + requests + Allure** 的 Tigshop 演示站自动化框架。

| 环境 | 地址 |
|------|------|
| PC 前台 | https://demo.tigshop.cn/ |
| 后台管理 | https://demo.tigshop.cn/admin/ |
| 买家 API | https://demo.tigshop.cn/api/ |
| 后台 API | https://demo.tigshop.cn/adminapi/ |

**买家账号：** `123123` / `123123`  
**后台账号：** `demo` / `demo123`

---

## 快速开始

```powershell
cd D:\github-code\e2e_function
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
copy .env.example .env

.\pytest.bat -m ui         # 先跑 UI 功能测试
.\pytest.bat               # 全部 18 用例
```

跑完后打开报告：

```powershell
start reports\allure-report\index.html
```

---

## 测试分层（18 用例）

| 类型 | 目录 | 数量 | 覆盖 |
|------|------|------|------|
| UI 功能 | `tests/ui/` | 15 | 前台 13 + 后台 2 |
| UI 异常 | `tests/ui/test_exception_ui.py` | 1 | 无效商品页 |
| E2E | `tests/e2e/` | 2 | 购物流程 + 无效 Token |

**已移除：** `tests/api/` 纯接口测试（API 客户端仍供 E2E 混合断言使用）

**业务场景：** 商品列表、搜索、加购、购物车、结算、订单、优惠券、个人中心（前台 + 后台）+ 异常场景

详细用例说明见 **[TESTCASES.md](./TESTCASES.md)**。

---

## 项目结构

```
config/settings.py       # Tigshop URL、账号、stable_delay（逐行中文注释）
api/client/              # 买家/后台 API 客户端（E2E 混合断言，逐行中文注释）
ui/driver/driver_manager.py  # WebDriver 工厂（逐行中文注释）
ui/pages/base_page.py        # Page Object 基类（逐行中文注释）
ui/pages/front/              # 前台 Page Object（逐行中文注释）
ui/pages/admin/              # 后台 Page Object（逐行中文注释）
utils/                   # 等待、弹窗、Allure、UI 登录、Token 同步（逐行中文注释）
generate_allure_report.py / run_e2e.py  # 报告生成与一键跑测入口（逐行中文注释）
tests/conftest.py        # Fixture + 账号隔离（逐行中文注释）
tests/ui|e2e/            # UI 功能 + 异常 + E2E 用例（逐行中文注释）
TESTCASES.md             # 用例说明文档
COMMANDS.md              # 终端命令速查
node.md                  # 架构与面试题
```

---

## 核心设计

1. **stable_delay**：SPA 操作间 0.5s 稳定延迟（`ACTION_STABLE_DELAY`）
2. **账号隔离**：每条用例独立 WebDriver；E2E 用例独立 API Session
3. **串号防护**：E2E 用 API 重建购物车，避免 UI/API 状态不一致
4. **登录策略**：UI 登录获取 JWT；E2E 通过 `sync_browser_token_to_clients` 同步至 API

---

## 文档导航

| 文档 | 内容 |
|------|------|
| [TESTCASES.md](./TESTCASES.md) | 用例清单、定位器、断言说明 |
| [COMMANDS.md](./COMMANDS.md) | 终端命令与排错 |
| [node.md](./node.md) | 架构、疑难点、面试题 |

---

*Technology: pytest · Selenium · requests · Allure · Element Plus (Nuxt 3)*
