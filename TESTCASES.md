# Tigshop 测试用例说明（TESTCASES.md）

> 被测站点：[Tigshop PC 前台](https://demo.tigshop.cn/) · [后台管理](https://demo.tigshop.cn/admin/)  
> 买家账号：`123123` / `123123`  
> 后台账号：`demo` / `demo123`（官方演示账号，买家账号无法登录后台）

---

## 1. 测试范围总览

| 层级 | 文件 | 用例数 | 说明 |
|------|------|--------|------|
| **UI 功能** | `tests/ui/test_front_*.py`、`test_admin_ui.py` | 15 | 页面元素展示与交互 |
| **UI 异常** | `tests/ui/test_exception_ui.py` | 1 | 无效商品页等负面路径 |
| **E2E** | `tests/e2e/` | 2 | 购物流程 + 无效 Token |
| **合计** | | **18** | 已移除纯 API 接口测试 |

**覆盖业务场景：**

| 场景 | UI 前台 | UI 后台 | E2E | 异常 |
|------|---------|---------|-----|------|
| 商品列表 | ✅ | — | — | — |
| 搜索 | ✅ | — | ✅ | — |
| 加购 | ✅ | — | ✅ | — |
| 购物车 | ✅ | — | ✅ | — |
| 结算 | ✅ | — | ✅ | — |
| 订单 | ✅ | — | — | — |
| 优惠券 | ✅ | ✅ | — | — |
| 个人中心 | ✅ | — | — | — |
| 无效商品页 | — | — | — | ✅ |
| 无效 Token | — | — | — | ✅ |

---

## 2. 设计要点（stable_delay / 账号隔离 / 串号）

### 2.1 stable_delay

- 配置项：`config/settings.py` → `ACTION_STABLE_DELAY = 0.5`
- 在 `BasePage.find()` / `click()` 前后调用，适配 Nuxt + Element Plus SPA 渲染抖动
- Tigshop 无 `data-test` 属性，依赖显式等待 + 固定短延迟组合定位

### 2.2 账号上下文隔离

| 机制 | 实现 |
|------|------|
| **API Session 隔离** | `api_session` fixture 为 `function` 级，E2E 每条用例独立 `requests.Session` |
| **浏览器隔离** | `front_driver` / `admin_driver` / `buyer_driver` 每条用例独立 WebDriver |
| **登录态获取** | UI 登录（`buyer_driver`）；E2E 通过 `sync_browser_token_to_clients` 同步 JWT |

### 2.3 串号（测试间状态污染）防护

| 风险 | 对策 |
|------|------|
| 购物车残留影响加购/结算 | E2E 中 API `clear_cart` + `addToCart` 重建可控数据 |
| UI 与 API 购物车不一致 | E2E 中 UI 验证交互，API 侧独立加购保证断言可控 |

### 2.4 测试代码注释规范

以下测试文件已添加**逐行中文注释**（文件头 + 每行：作用、调用关系、自定义/框架、来源）：

| 文件 | 说明 |
|------|------|
| `tests/conftest.py` | pytest fixture、session 钩子、失败截图 |
| `tests/ui/test_front_home_ui.py` | 前台首页 UI（4 用例） |
| `tests/ui/test_front_shop_ui.py` | 前台购物流程 UI（4 用例） |
| `tests/ui/test_front_member_ui.py` | 会员/优惠券 UI（5 用例） |
| `tests/ui/test_admin_ui.py` | 后台 UI（2 用例） |
| `tests/ui/test_exception_ui.py` | UI 异常（1 用例） |
| `tests/e2e/test_front_purchase_e2e.py` | E2E 完整购物流程（1 用例） |
| `tests/e2e/test_exception_e2e.py` | E2E 异常（1 用例） |

---

## 3. UI 功能用例明细

### 3.1 `test_front_home_ui.py`（4）— 未登录

| 用例 | 页面 | 关键定位 | 断言 |
|------|------|----------|------|
| `test_home_product_links` | `/` | `a[href*='/product/']` | 商品链接 ≥1 |
| `test_home_coupon_section` | `/` | `.mod_coupon` | 领券区块可见 |
| `test_category_list` | `/list?cat=1` | 商品链接 | 分类列表有商品 |
| `test_search_results` | `/search?keyword=` | `input.search-input` | URL 含 `search` |

### 3.2 `test_front_shop_ui.py`（4）— 买家已登录

| 用例 | 页面 | 关键定位 | 断言 |
|------|------|----------|------|
| `test_product_detail_display` | `/product/338` | `h1` / 标题 | 标题非空 |
| `test_add_to_cart_button` | 商品详情 | `//button[contains(.,'加入购物车')]` | 点击后有成功提示或跳转 |
| `test_cart_page_display` | `/cart` | 购物车容器 | 页面含购物车内容 |
| `test_checkout_page_display` | `/order/check` | `//button[contains(.,'提交订单')]` | 结算页加载 |

### 3.3 `test_front_member_ui.py`（5）— 买家已登录

| 用例 | 页面 | 断言 |
|------|------|------|
| `test_member_center` | `/member/index` | 含个人/会员/订单文案 |
| `test_member_nav_links` | 个人中心 | 侧栏 `/member/` 链接 ≥1 |
| `test_order_list_page` | `/member/order/list` | 含「订单」 |
| `test_coupon_center` | `/coupon/list` | 集券中心卡片可见 |
| `test_my_coupons_page` | `/member/coupon/list` | 含「优惠券」 |

### 3.4 `test_admin_ui.py`（2）

| 用例 | 页面 | 断言 |
|------|------|------|
| `test_admin_login_page` | `/admin/login/index` | 欢迎登录标题可见 |
| `test_admin_coupon_list` | `/admin/promotion/coupon/list` | 表格行 ≥1 |

---

## 4. 异常用例明细

### 4.1 `test_exception_ui.py`（1）— UI 异常

| 用例 | 场景 | 断言 |
|------|------|------|
| `test_invalid_product_page` | 访问 `INVALID_PRODUCT_ID=999999999` | 页面含「不存在」「错误」「404」或至少有 body 内容 |

### 4.2 `test_exception_e2e.py`（1）— E2E 异常

| 用例 | 场景 | 断言 |
|------|------|------|
| `test_invalid_token_api` | 设置伪造 Token 后调用 `get_user_detail` | 抛出 `TigshopApiError` 且 `code != 0` |

---

## 5. E2E 用例明细

### `test_front_purchase_e2e.py`（1）

**标题：** 搜索→详情→加购→购物车→结算页

| 步骤 | 动作 | 验证 |
|------|------|------|
| 1 | UI 搜索关键词 | URL 含 `search` |
| 2 | 打开商品详情 | 标题非空 |
| 3 | UI 点击加购 | 交互成功 |
| 4 | API 同步 token，清空并 API 加购 | 数据可控 |
| 5 | 打开购物车页 | 有购物车内容 |
| 6 | 打开结算页 | 页面加载 + 提交按钮可见 |
| 7 | API `checkout_index` | 含收货地址列表 |

---

## 6. 关键 API 端点（E2E 混合断言使用）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/product/product/detail?id=` | 详情 |
| POST | `/api/cart/cart/addToCart` | 加购 |
| POST | `/api/cart/cart/clear` | 清空购物车 |
| POST | `/api/order/check/index` | 结算页数据 |
| GET | `/api/user/user/detail` | 用户信息（异常用例） |

---

## 7. 运行命令

```powershell
.\pytest.bat -m ui           # 仅 UI 功能（15）
.\pytest.bat -m exception     # 仅异常（2）
.\pytest.bat -m e2e           # 仅 E2E（2）
.\pytest.bat -m smoke         # 冒烟（E2E 购买流程）
.\pytest.bat                  # 全部 18
```

报告：`pytest` 结束后自动生成 `reports/allure-report/index.html`

---

*最后更新：2026-07-05*
