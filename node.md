# Tigshop E2E 项目知识梳理（node.md）

> 站点：[Tigshop PC 前台](https://demo.tigshop.cn/) · [后台](https://demo.tigshop.cn/admin/)  
> 技术栈：pytest + Selenium + requests + Allure + Nuxt 3 / Element Plus

---

## 文档导航

| 文档 | 定位 |
|------|------|
| [README.md](./README.md) | 快速入门 |
| [TESTCASES.md](./TESTCASES.md) | 27 条用例明细 |
| [COMMANDS.md](./COMMANDS.md) | 终端命令 |
| **node.md（本文）** | 架构、设计、面试 |

---

## 1. 目录结构

```
E2E_demo/
├── config/settings.py          # URL、账号、stable_delay（逐行中文注释）
├── api/client/                 # 买家/后台 API 客户端（逐行中文注释）
│   ├── base_client.py          # Tigshop {code,message,data} 解析
│   ├── auth_client.py          # 买家登录/用户详情
│   ├── admin_client.py         # 后台登录/优惠券
│   ├── product_client.py       # 首页/列表/详情/搜索
│   ├── cart_client.py          # 加购/列表/清空
│   ├── order_client.py         # 结算/订单
│   └── coupon_client.py        # 我的优惠券
├── ui/
│   ├── driver/driver_manager.py # WebDriver 工厂（Chrome/Edge，逐行中文注释）
│   └── pages/
│       ├── base_page.py         # 通用操作 + stable_delay + URL 等待（逐行中文注释）
│       ├── front/               # 前台 Page Object（7 文件，逐行中文注释）
│       └── admin/               # 后台 Page Object（2 文件，逐行中文注释）
├── utils/
│   ├── wait_helper.py          # stable_delay / retry_action（逐行中文注释）
│   ├── popup_handler.py        # 弹窗/遮挡层关闭（逐行中文注释）
│   ├── allure_helper.py        # Allure 步骤/附件封装（逐行中文注释）
│   ├── ui_auth.py              # UI 登录 + token 引导（逐行中文注释）
│   └── session_sync.py         # localStorage ↔ API Session（逐行中文注释）
├── generate_allure_report.py   # Allure 报告生成 CLI（逐行中文注释）
├── run_e2e.py                  # 一键跑测 + 开报告（逐行中文注释）
├── tests/
│   ├── conftest.py             # 隔离 Fixture + 购物车清理（逐行中文注释）
│   ├── api/   (4 文件, 13 用例，逐行中文注释)
│   ├── ui/    (4 文件, 15 用例，逐行中文注释)
│   └── e2e/   (1 文件,  1 用例，逐行中文注释)
└── TESTCASES.md
```

---

## 2. 核心设计

### 2.1 三层测试

| 层 | 职责 | Tigshop 特点 |
|----|------|--------------|
| API | 快速验证 JSON 数据 | 响应 `{code:0, data:{}}`；部分接口需 JWT |
| UI | 验证 Element Plus 页面展示 | 无 data-test，用 CSS/XPath + 中文文案 |
| E2E | UI 交互 + API 断言 | Token 从浏览器同步到 requests |

### 2.2 代码注释规范

`config/settings.py` 与 `api/client/*.py` 采用与 `utils/wait_helper.py`、`ui/pages/base_page.py` 一致的逐行中文注释：

- 文件头 `# =============================================================================` 块说明模块职责与调用方
- 每行代码标注：作用、调用关系、自定义/框架/标准库、来源括号（如 `（项目：…）`、`（第三方：requests → Session.get）`）
- 仅注释，不改动业务逻辑

### 2.3 stable_delay 实践

Tigshop 为 Nuxt SPA，`document.readyState=complete` 后 DOM 仍可能变化。

- `ACTION_STABLE_DELAY=0.5` 在 `find/click` 前后执行
- 配合 `WebDriverWait` 显式等待，降低 flaky
- 详见 `utils/wait_helper.py` → `stable_delay()`

### 2.4 账号上下文隔离

| Fixture | scope | 隔离方式 |
|---------|-------|----------|
| `api_session` | function | 独立 requests.Session |
| `front_driver` / `admin_driver` | function | 独立 WebDriver |
| `buyer_auth_api` / `admin_api` | function | 不同 base_url，不共享 token |
| `logged_in_buyer_api` | function | 登录 + clear_cart，teardown 再清理 |

### 2.5 串号（状态污染）防护

| 问题 | 方案 |
|------|------|
| 购物车残留 | `cart_api.clear_cart()` setup/teardown |
| UI/API 购物车 ID 不一致 | E2E 中 UI 验证点击，API 独立加购断言 |
| 登录 token 串用 | 每用例新 Session；`sync_browser_token_to_clients` 仅当前用例 |

### 2.6 登录与人机验证

- 买家 API：`POST /api/user/login/signin`
- 频繁调用可能返回 `code=1002` 人机验证
- **策略**：API 优先 → 失败则 UI 登录 → 读 localStorage `token` → 写入 Session Header

---

## 3. 关键 API

| 方法 | 路径 |
|------|------|
| GET | `/api/home/home/index` |
| GET | `/api/product/product/list?keyword=` |
| GET | `/api/product/product/detail?id=` |
| POST | `/api/cart/cart/addToCart` body: `{id, sku_id, number}` |
| POST | `/api/order/check/index` body: `{flow_type:1}` |
| GET | `/api/user/order/list` |
| POST | `/adminapi/login/signin` |

---

## 4. 关键 UI 定位

| 页面 | 选择器 |
|------|--------|
| 搜索 | `input.search-input[name='keywords']` |
| 买家登录 | `input[placeholder='用户名/手机/邮箱']` |
| 加购 | `//button[contains(.,'加入购物车')]` |
| 去结算 | `//button[contains(.,'去结算')]` |
| 后台登录 | `input[placeholder='请输入用户名']` |
| 后台优惠券 | `/admin/promotion/coupon/list` |

---

## 5. 疑难点

1. **无 data-test**：依赖 Element Plus class + 中文 XPath
2. **SKU 商品**：加购前需选规格（`select_first_sku_if_needed`）
3. **登录 URL**：前台为 `/member/login`，非 `/login`
4. **后台账号**：买家 `123123` 不能登后台，需 `demo/demo123`
5. **反爬 Reptiles**：API 需 User-Agent；纯脚本易被拦，UI 登录更稳

---

## 6. 面试题精选

**Q：如何防止 E2E 测试串号？**  
独立 Session/Driver；购物车 setup/teardown 清理；E2E 不假设 UI 与 API 共用 cart_id。

**Q：stable_delay 和显式等待区别？**  
显式等待等条件成立；stable_delay 是条件满足后的固定缓冲，应对 SPA 动画/渲染延迟。

**Q：API 登录被验证码拦截怎么办？**  
UI 登录获取 JWT → `localStorage` → 同步到 requests Session，见 `logged_in_buyer_api`。

**Q：Page Object 基类价值？**  
统一 wait、弹窗、dismiss、retry；子类只写 Tigshop 业务定位与方法。

---

## 7. 常用命令

见 [COMMANDS.md](./COMMANDS.md) 与 [TESTCASES.md](./TESTCASES.md)。

---

*最后更新：2026-07-05*
