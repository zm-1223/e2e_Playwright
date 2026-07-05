# Tigshop 测试用例说明（TESTCASES.md）

> 被测站点：[Tigshop PC 前台](https://demo.tigshop.cn/) · [后台管理](https://demo.tigshop.cn/admin/)  
> 买家账号：`123123` / `123123`  
> 后台账号：`demo` / `demo123`（官方演示账号，买家账号无法登录后台）

---

## 1. 测试范围总览

| 层级 | 文件 | 用例数 | 说明 |
|------|------|--------|------|
| **API** | `tests/api/` | 13 | 接口数据与业务断言 |
| **UI** | `tests/ui/` | 15 | 页面元素展示与交互 |
| **E2E** | `tests/e2e/` | 1 | 前台搜索→加购→结算混合流程 |
| **合计** | | **29** | 已删除全部异常/负面用例 |

**覆盖业务场景：**

| 场景 | API | UI 前台 | UI 后台 | E2E |
|------|-----|---------|---------|-----|
| 商品列表 | ✅ | ✅ | — | — |
| 搜索 | ✅ | ✅ | — | ✅ |
| 加购 | ✅ | ✅ | — | ✅ |
| 购物车 | ✅ | ✅ | — | ✅ |
| 结算 | ✅ | ✅ | — | ✅ |
| 订单 | ✅ | ✅ | — | — |
| 优惠券 | ✅ | ✅ | ✅ | — |
| 个人中心 | ✅ | ✅ | — | — |

---

## 2. 设计要点（stable_delay / 账号隔离 / 串号）

### 2.1 stable_delay

- 配置项：`config/settings.py` → `ACTION_STABLE_DELAY = 0.5`
- 在 `BasePage.find()` / `click()` 前后调用，适配 Nuxt + Element Plus SPA 渲染抖动
- Tigshop 无 `data-test` 属性，依赖显式等待 + 固定短延迟组合定位

### 2.2 账号上下文隔离

| 机制 | 实现 |
|------|------|
| **API Session 隔离** | `api_session` fixture 为 `function` 级，每条用例独立 `requests.Session` |
| **买家 / 后台分离** | `buyer_auth_api` 与 `admin_api` 使用不同 base_url 与 token |
| **浏览器隔离** | `front_driver` / `admin_driver` / `buyer_driver` 每条用例独立 WebDriver |
| **登录态获取** | 优先 API 登录；触发人机验证时回退 UI 登录并 `sync_browser_token_to_clients` |

### 2.3 串号（测试间状态污染）防护

| 风险 | 对策 |
|------|------|
| 购物车残留影响加购/结算 | `logged_in_buyer_api` setup/teardown 调用 `cart_api.clear_cart()` |
| 同一账号订单/优惠券互相干扰 | 每条用例独立 Session；E2E 用 API 重建购物车而非复用 UI 购物车 ID |
| UI 与 API 购物车不一致 | E2E 中 UI 验证交互，API 侧 `clear_cart` + `addToCart` 保证断言可控 |

### 2.4 测试代码注释规范

以下测试文件已添加**逐行中文注释**（文件头 + 每行：作用、调用关系、自定义/框架、来源）：

| 文件 | 说明 |
|------|------|
| `tests/conftest.py` | pytest fixture、session 钩子、失败截图 |
| `tests/api/test_home_product_api.py` | 首页/商品 API（5 用例） |
| `tests/api/test_cart_order_api.py` | 购物车/订单 API（5 用例） |
| `tests/api/test_coupon_api.py` | 优惠券 API（1 用例） |
| `tests/api/test_admin_api.py` | 后台 API（2 用例） |
| `tests/ui/test_front_home_ui.py` | 前台首页 UI（4 用例） |
| `tests/ui/test_front_shop_ui.py` | 前台购物流程 UI（4 用例） |
| `tests/ui/test_front_member_ui.py` | 会员/优惠券 UI（5 用例） |
| `tests/ui/test_admin_ui.py` | 后台 UI（2 用例） |
| `tests/e2e/test_front_purchase_e2e.py` | E2E 完整购物流程（1 用例） |

---

## 3. API 用例明细

### 3.1 `test_home_product_api.py`（5）

| 用例 | 断言 |
|------|------|
| `test_home_index` | 首页 `moduleList` 非空 |
| `test_hot_categories` | 热门分类 ≥1 且含 `categoryName` |
| `test_product_list` | 商品分页 `records` 非空 |
| `test_search_products` | 关键词搜索有结果 |
| `test_product_detail` | 详情含 `productName` 与 `skuList` |

### 3.2 `test_cart_order_api.py`（5）

| 用例 | 前置 | 断言 |
|------|------|------|
| `test_add_to_cart` | 买家登录 + 清空购物车 | 加购后 `cart_item_count` 增加 |
| `test_cart_list` | 加购一件商品 | 返回含 `cartList` |
| `test_checkout_index` | 加购后 | 结算 index 含 `addressList` |
| `test_order_list` | 买家登录 | 订单列表含 `records` |
| `test_user_detail` | 买家登录 | `username == 123123` |

### 3.3 `test_coupon_api.py`（1）

| 用例 | 断言 |
|------|------|
| `test_my_coupons` | 我的优惠券列表含 `records` |

### 3.4 `test_admin_api.py`（2）

| 用例 | 断言 |
|------|------|
| `test_admin_login` | API 返回 token（验证码时 skip） |
| `test_admin_coupon_list` | 后台优惠券名称列表 ≥1 |

---

## 4. UI 用例明细

### 4.1 `test_front_home_ui.py`（4）— 未登录

| 用例 | 页面 | 关键定位 | 断言 |
|------|------|----------|------|
| `test_home_product_links` | `/` | `a[href*='/product/']` | 商品链接 ≥1 |
| `test_home_coupon_section` | `/` | `.mod_coupon` | 领券区块可见 |
| `test_category_list` | `/list?cat=1` | 商品链接 | 分类列表有商品 |
| `test_search_results` | `/search?keyword=` | `input.search-input` | URL 含 `search` |

### 4.2 `test_front_shop_ui.py`（4）— 买家已登录

| 用例 | 页面 | 关键定位 | 断言 |
|------|------|----------|------|
| `test_product_detail_display` | `/product/338` | `h1` / 标题 | 标题非空 |
| `test_add_to_cart_button` | 商品详情 | `//button[contains(.,'加入购物车')]` | 点击后有成功提示或跳转 |
| `test_cart_page_display` | `/cart` | 购物车容器 | 页面含购物车内容 |
| `test_checkout_page_display` | `/order/check` | `//button[contains(.,'提交订单')]` | 结算页加载 |

### 4.3 `test_front_member_ui.py`（5）— 买家已登录

| 用例 | 页面 | 断言 |
|------|------|------|
| `test_member_center` | `/member/index` | 含个人/会员/订单文案 |
| `test_member_nav_links` | 个人中心 | 侧栏 `/member/` 链接 ≥1 |
| `test_order_list_page` | `/member/order/list` | 含「订单」 |
| `test_coupon_center` | `/coupon/list` | 集券中心卡片可见 |
| `test_my_coupons_page` | `/member/coupon/list` | 含「优惠券」 |

### 4.4 `test_admin_ui.py`（2）

| 用例 | 页面 | 断言 |
|------|------|------|
| `test_admin_login_page` | `/admin/login/index` | 欢迎登录标题可见 |
| `test_admin_coupon_list` | `/admin/promotion/coupon/list` | 表格行 ≥1 |

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

## 6. 关键 API 端点（实测可用）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/home/home/index` | 首页 |
| GET | `/api/product/product/list?keyword=` | 搜索/列表 |
| GET | `/api/product/product/detail?id=` | 详情 |
| POST | `/api/user/login/signin` | 买家登录 |
| POST | `/api/cart/cart/addToCart` | 加购 |
| GET | `/api/cart/cart/list` | 购物车 |
| POST | `/api/cart/cart/clear` | 清空购物车 |
| POST | `/api/order/check/index` | 结算页数据 |
| GET | `/api/user/order/list` | 订单列表 |
| GET | `/api/user/coupon/list` | 我的优惠券 |
| GET | `/api/user/user/detail` | 用户信息 |
| POST | `/adminapi/login/signin` | 后台登录 |
| GET | `/adminapi/promotion/coupon/list` | 后台优惠券 |

---

## 7. 运行命令

```powershell
.\pytest.bat -m api          # 仅 API（13）
.\pytest.bat -m ui           # 仅 UI（15）
.\pytest.bat -m e2e          # 仅 E2E（1）
.\pytest.bat                 # 全部 29
```

报告：`pytest` 结束后自动生成 `reports/allure-report/index.html`

---

*最后更新：2026-07-05*
