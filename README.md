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
cd D:\github-code\E2E_demo
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
copy .env.example .env

.\pytest.bat -m api    # 先跑 API（最快）
.\pytest.bat           # 全部 29 用例
```

跑完后打开报告：

```powershell
start reports\allure-report\index.html
```

---

## 测试分层（29 用例）

| 类型 | 目录 | 数量 | 覆盖 |
|------|------|------|------|
| API | `tests/api/` | 13 | 首页、商品、购物车、订单、优惠券、后台 |
| UI | `tests/ui/` | 15 | 前台 13 + 后台 2 |
| E2E | `tests/e2e/` | 1 | 搜索→加购→结算混合流程 |

**业务场景：** 商品列表、搜索、加购、购物车、结算、订单、优惠券、个人中心（前台 + 后台）

详细用例说明见 **[TESTCASES.md](./TESTCASES.md)**。

---

## 项目结构

```
config/settings.py       # Tigshop URL、账号、stable_delay（逐行中文注释）
api/client/              # 买家/后台 API 客户端（逐行中文注释）
ui/driver/driver_manager.py  # WebDriver 工厂（逐行中文注释）
ui/pages/base_page.py        # Page Object 基类（逐行中文注释）
ui/pages/front/              # 前台 Page Object（逐行中文注释）
ui/pages/admin/              # 后台 Page Object（逐行中文注释）
utils/                   # 等待、弹窗、Allure、UI 登录、Token 同步（逐行中文注释）
generate_allure_report.py / run_e2e.py  # 报告生成与一键跑测入口（逐行中文注释）
tests/conftest.py        # Fixture + 账号隔离 + 购物车清理（逐行中文注释）
tests/api|ui|e2e/        # 测试用例（10 个 test_*.py 逐行中文注释）
TESTCASES.md             # 用例说明文档
COMMANDS.md              # 终端命令速查
node.md                  # 架构与面试题
```

---

## 核心设计

1. **stable_delay**：SPA 操作间 0.5s 稳定延迟（`ACTION_STABLE_DELAY`）
2. **账号隔离**：每条用例独立 Session / WebDriver；买家与后台 API 分离
3. **串号防护**：登录 fixture 前后 `clear_cart()`，E2E 用 API 重建购物车
4. **登录策略**：API 优先；人机验证时回退 UI 登录同步 JWT

---

## 文档导航

| 文档 | 内容 |
|------|------|
| [TESTCASES.md](./TESTCASES.md) | 用例清单、定位器、断言说明 |
| [COMMANDS.md](./COMMANDS.md) | 终端命令与排错 |
| [node.md](./node.md) | 架构、疑难点、面试题 |

---

*Technology: pytest · Selenium · requests · Allure · Element Plus (Nuxt 3)*
