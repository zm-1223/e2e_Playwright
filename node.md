# E2E 自动化项目知识梳理（node.md）

> 项目：Practice Software Testing 混合 E2E 框架  
> 站点：[https://practicesoftwaretesting.com/](https://practicesoftwaretesting.com/)  
> 技术栈：pytest + Selenium + requests + Allure + pytest-rerunfailures

---

## 文档导航（读哪一份？）

| 文档 | 定位 | 适合场景 |
|------|------|----------|
| **[README.md](./README.md)** | 小白导读 + 快速上手 | 第一次 clone 项目、跑通测试、建立整体地图 |
| **各 `.py` 文件内中文注释** | 逐行代码说明 | 打开具体文件读实现细节（非本文档重复内容） |
| **node.md（本文）** | 架构梳理 + 疑难点 + 面试题 | 理解设计取舍、排查问题、面试复习 |

建议路径：**README 小白导读 → 按推荐顺序读带注释的源码 → 本文查漏补缺**。

---

## 目录

1. [项目总览与目录结构](#1-项目总览与目录结构)
2. [核心设计思维](#2-核心设计思维)
3. [分层架构与数据流](#3-分层架构与数据流)
4. [编程基础知识点](#4-编程基础知识点)
5. [疑难点与注意点](#5-疑难点与注意点)
6. [进阶代码讲解（节选）](#6-进阶代码讲解节选)
7. [面试题与参考答案](#7-面试题与参考答案)
8. [学习路径建议](#8-学习路径建议)

---

## 1. 项目总览与目录结构

### 1.1 项目是做什么的

本项目是一个**可运行的 E2E 自动化演示框架**，针对公开练习站点 Practice Software Testing，覆盖：

| 测试层 | 目录 | 作用 |
|---|---|---|
| API 测试 | `tests/api/` | 纯接口：登录、搜索、加购、下单 |
| UI 测试 | `tests/ui/` | 浏览器：登录态、商品页、加购 |
| 混合 E2E | `tests/e2e/` | API 登录 + UI 操作 + API 断言 |

### 1.2 目录结构

```
E2E_demo/
├── config/settings.py       # 配置中心（敏感信息走 .env，其余为常量；含逐行中文注释）
├── api/client/              # API 客户端（requests 封装）
├── ui/
│   ├── driver/              # WebDriver 工厂
│   └── pages/               # Page Object 页面对象
├── utils/                   # 横切能力：等待、弹窗、Token 同步、Allure 辅助
│   ├── wait_helper.py       # 页面就绪等待、操作重试
│   ├── popup_handler.py     # 突发弹窗关闭
│   ├── session_sync.py      # API Token → 浏览器 localStorage
│   └── allure_helper.py     # 截图/JSON 附件
├── tests/
│   ├── conftest.py          # 全局 Fixture + pytest Hook（含数据准备、失败截图）
│   ├── api/ ui/ e2e/        # 三类测试（7 个 test_*.py，共 14 用例）
├── reports/                 # Allure 结果、HTML 报告与失败截图
├── pyproject.toml           # pytest 全局配置（原 pytest.ini 已合并至此）
├── pytest.bat / run_tests.bat   # Windows 下直接用 venv 的 pytest
├── env_dev.ps1 / env_dev.bat    # 载入 .venv 后可直输 pytest
├── run_e2e.py               # 一键跑测 + 生成 Allure 并打开浏览器
├── generate_allure_report.py
├── requirements.txt
├── .env.example             # 仅账号密码
├── README.md                # 小白导读 + 快速上手
└── node.md                  # 本文档（架构 / 疑难点 / 面试题）
```

> **说明**：项目内全部 `.py` 文件均已添加**逐行中文注释**，便于编程小白阅读；本文第 6 节仅摘录关键片段并解释设计意图，完整细节以源码注释为准。

### 1.3 默认测试账号

| 项 | 值 |
|---|---|
| UI | https://practicesoftwaretesting.com |
| API | https://api.practicesoftwaretesting.com |
| 邮箱 | customer@practicesoftwaretesting.com |
| 密码 | welcome01 |

### 1.4 用例清单（14 个）

| 文件 | 标记 | 数量 | 说明 |
|---|---|---|---|
| `test_auth_api.py` | api | 3 | 登录成功 / 密码错误 / 未登录 |
| `test_product_api.py` | api | 4 | 搜索 / 详情 / 加购 / 404 |
| `test_order_api.py` | api | 2 | 下单查单 / 未登录下单 |
| `test_search_ui.py` | ui, flaky | 2 | 导航可见 / 商品加购 |
| `test_exception_ui.py` | ui, exception | 1 | 无效商品页 |
| `test_full_purchase_flow.py` | e2e, smoke, flaky | 1 | 完整混合流程 |
| `test_exception_e2e.py` | e2e, exception | 1 | 无效 Token |

---

## 2. 核心设计思维

### 2.1 测试金字塔思维

```
        /  E2E  \        ← 少量、慢、贵，验证关键链路
       / UI 测试 \
      /  API 测试  \     ← 多、快、稳，验证接口契约
     /_______________\
```

- **API 多、E2E 少**：接口失败定位快，E2E 只验证「跨端协作」是否成立。
- 本项目 API 9 个、E2E 2 个，符合金字塔比例。

### 2.2 分层解耦思维

| 层 | 职责 | 不应做的事 |
|---|---|---|
| **测试用例** | 编排步骤 + 断言 | 不写 Selenium 定位细节 |
| **conftest Fixture** | 公共数据与环境准备 | 不写业务断言 |
| **Page Object** | 页面元素与操作 | 不断言业务结果 |
| **API Client** | HTTP 请求与解析 | 不知道 UI 存在 |
| **utils** | 等待、弹窗、Token 同步、报告附件 | 不包含用例断言 |

**好处**：UI 改版只改 Page Object；API 变更只改 Client；Fixture 复用数据准备；用例保持可读。

### 2.3 混合 E2E 思维（API + UI）

传统纯 UI E2E 痛点：登录慢、数据准备慢、断言困难。

本项目策略：

1. **API 登录** → 拿 `access_token`（快、稳）
2. **注入 localStorage** → UI 跳过登录表单（绕过 Cloudflare 登录页）
3. **API 搜索/下单** → 数据准备与最终断言走接口
4. **UI 只负责** → 打开商品页、点击加购（验证前端交互）

这是业界常见的 **「接口辅助 UI E2E」** 模式。

### 2.4 DRY 与 Fixture 思维

重复出现的「搜索第一个商品 → 创建购物车 → 加购」写在 **`tests/conftest.py`** 的 Fixture 中：

| Fixture | 作用 |
|---|---|
| `first_product` | 已登录，搜索并返回第一个商品 |
| `cart_with_product` | 已登录，创建 cart 并加购 |
| `guest_cart_with_product` | 未登录 cart，用于 401 异常测试 |

测试用例只关心：**Given 已有购物车 → When 提交订单 → Then 列表中有订单**。

E2E 混合流程的步骤则**直接写在用例里**（见 `test_full_purchase_flow.py`），便于一眼看清完整链路。

### 2.5 失败可观测性思维

自动化失败时最怕「不知道为什么挂」：

- Allure 报告：`@allure.epic` / `@allure.feature` / `@allure.title`
- 失败截图（`pytest_runtest_makereport` Hook）
- API 失败自动附响应体（`json_or_raise`）
- 关键结果 `attach_json` 附到报告
- UI 用例 `@pytest.mark.flaky` 应对偶发超时

---

## 3. 分层架构与数据流

### 3.1 混合 E2E 完整流程

```
┌─────────────┐     POST /users/login      ┌──────────────┐
│  auth_api   │ ─────────────────────────▶ │  API Server  │
└─────────────┘ ◀── access_token ─────────── └──────────────┘
       │
       │ sync_token_to_clients
       ▼
┌─────────────┐     localStorage.setItem   ┌──────────────┐
│   driver    │ ─────────────────────────▶ │  Angular UI  │
└─────────────┘     refresh + 等待 nav     └──────────────┘
       │
       │ product_page.open + add_to_cart
       ▼
┌─────────────┐     POST /carts + /invoices ┌──────────────┐
│ product_api │ ─────────────────────────▶ │  API Server  │
│  order_api  │ ◀── invoice + orders ────── └──────────────┘
└─────────────┘
```

### 3.2 Fixture 依赖关系（简化）

```
api_session (function)
    ├── auth_api ──┐
    ├── product_api ── 共享同一 Session（Token 互通）
    └── order_api ──┘

logged_in_api → 依赖 auth_api，登录并 yield，teardown 登出

driver → WebDriver 裸实例
authenticated_driver → driver + inject_auth_token
product_page → authenticated_driver + ProductPage

first_product → logged_in_api + product_api.search → data[0]
cart_with_product → first_product + create_cart + add_to_cart
guest_cart_with_product → 无 logged_in_api（用于 401 测试）
```

### 3.3 PST 站点 API 要点

| 接口 | 方法 | 说明 |
|---|---|---|
| `/users/login` | POST | body: `{email, password}` → `access_token` |
| `/users/me` | GET | 需 Bearer Token |
| `/products/search?q=` | GET | 返回 `{data: [...]}` |
| `/carts` | POST | 创建购物车 |
| `/carts/{id}` | POST | body: `{product_id, quantity}` |
| `/postcode-lookup` | GET | 获取合法账单地址 |
| `/invoices` | POST | 提交订单（需登录 + cart_id） |

---

## 4. 编程基础知识点

### 4.1 pytest

| 概念 | 本项目用法 |
|---|---|
| **Fixture** | `conftest.py` 提供 driver、API 客户端、测试数据 |
| **scope** | `session`（URL）、`function`（每条用例独立 Session/Driver） |
| **yield Fixture** | `logged_in_api` yield 后执行 logout 清理 |
| **mark** | `@pytest.mark.api` / `ui` / `e2e` / `exception` / `flaky` |
| **Hook** | `pytest_runtest_makereport` 失败截图 |
| **Hook** | `pytest_sessionstart` 写 Allure 环境文件 |
| **pytest.raises** | API 异常用例断言 HTTP 状态码 |

### 4.2 Selenium

| 概念 | 本项目用法 |
|---|---|
| **隐式等待** | `driver.implicitly_wait(10)` 全局元素查找 |
| **显式等待** | `WebDriverWait + EC.visibility_of_element_located` |
| **Page Object** | 每页一个类，继承 `BasePage` |
| **StaleElement** | `click` 内 `retry_action` 重试 |
| **localStorage 注入** | `execute_script` 写入 `auth-token` |
| **弹窗处理** | `PopupHandler.dismiss_all()` 在 open/click 前调用 |

### 4.3 requests

| 概念 | 本项目用法 |
|---|---|
| **Session** | 复用 TCP 连接，共享 Cookie/Header |
| **Bearer Token** | `Authorization: Bearer {token}` |
| **raise_for_status** | 4xx/5xx 抛 `HTTPError` |
| **网络重试** | 仅对 `ConnectionError`/`Timeout` 重试 |

### 4.4 Python 语法（本项目用到）

| 语法 | 出现位置 |
|---|---|
| **@pytest.fixture** | `conftest.py` 声明夹具 |
| **@pytest.mark.flaky** | UI/E2E 用例失败重试 |
| **Generator Fixture** | `yield` 前后置（driver、logged_in_api） |
| **hookwrapper** | `pytest_runtest_makereport` 中 `yield` 后取 report |
| **`*clients` 可变参数** | `sync_token_to_clients(token, *clients)` |
| **with pytest.raises** | API 异常测试断言 HTTPError 与 status_code |

---

## 5. 疑难点与注意点

### 5.1 Cloudflare 与 Headless

**现象**：Headless 模式下 UI 可能被 Cloudflare 拦截，登录页元素找不到。

**本项目处理**：
- `config/settings.py` 中 `HEADLESS = False` 为默认
- 混合 E2E 用 API Token 注入 localStorage，**绕过 UI 登录表单**

**注意**：CI 环境若必须 Headless，需评估是否加 Cloudflare bypass 或纯 API 测试。

### 5.2 Token 与 Session 共享

`auth_api`、`product_api`、`order_api` 共用同一个 `requests.Session`。

- `auth_api.login()` 调用 `set_token()` 后，**三个客户端自动带 Token**
- 异常测试 `guest_cart_with_product` **不能**依赖 `logged_in_api`，否则 Session 已有 Token，401 测不出来

### 5.3 UI 购物车 vs API 购物车

UI 点击「Add to cart」和 API `POST /carts` 可能产生**不同购物车实例**。

本项目 E2E 策略：
- UI 加购：验证前端交互
- API 再建 cart 下单：保证订单断言可控

不要假设 UI 加购后 API 能直接拿到同一个 cart_id。

### 5.4 隐式等待 vs 显式等待

| 类型 | 优点 | 缺点 |
|---|---|---|
| 隐式等待 | 全局生效，写法简单 | 所有 find_element 都等，可能拖慢 |
| 显式等待 | 精确、可控 | 每个关键点都要写 |

本项目：**两者结合**——全局 10s 隐式 + 关键操作用 `WebDriverWait`。

### 5.5 `wait_for_page_ready` 吞掉异常

```python
except Exception:
    pass  # 超时不抛异常
```

**原因**：SPA（Angular）可能 long-polling，`readyState=complete` 后 DOM 仍在变。

**风险**：页面未真就绪就操作，可能偶发失败 → UI 用例加 `@pytest.mark.flaky`。

### 5.6 API 重试范围

`BaseApiClient._request_with_retry` **只重试网络异常**，不重试 HTTP 500/408。

408 Request Timeout 是业务层超时，需用例级 `flaky` 或加大超时，不能靠网络重试。

### 5.7 pytest Hook 截图时机

`pytest_runtest_makereport` 在 `call` 阶段失败时截图。

- 纯 API 测试无 driver → 跳过截图（正常）
- 需确保 funcargs 中有 `driver` 或 `authenticated_driver`

### 5.8 敏感配置

仅 `USER_EMAIL`、`USER_PASSWORD` 从 `.env` 读取，其余写死在 `settings.py`。

- `.env` 加入 `.gitignore`
- 不要把真实密码提交 Git

### 5.9 弹窗处理局限

`PopupHandler` 只能处理常见 CSS 关闭按钮、ESC、JS alert，**无法绕过 Cloudflare 人机验证**。Cloudflare 需从 Headless 策略或 Token 注入侧解决。

---

## 6. 进阶代码讲解（节选）

> 以下片段配合源码内逐行注释阅读；完整文件请直接打开对应 `.py`。

### 6.1 conftest 数据准备 Fixture

```python
@pytest.fixture(scope="function")
def first_product(logged_in_api, product_api, test_data) -> dict:
    result = product_api.search(test_data["keyword"])
    assert result.get("data"), f"关键词 '{test_data['keyword']}' 无搜索结果"
    return result["data"][0]
```

| 行 | 含义 |
|---|---|
| `logged_in_api` | 保证 Session 已登录、带 Bearer Token |
| `product_api.search(...)` | 调用 Client 搜索，返回 `{data: [...]}` |
| `assert result.get("data")` | 无结果立刻失败，错误信息含 keyword |
| `return result["data"][0]` | 取第一个商品 dict，供后续用例/Ficture 使用 |

```python
@pytest.fixture(scope="function")
def cart_with_product(logged_in_api, product_api, first_product) -> dict:
    cart = product_api.create_cart()
    product_api.add_to_cart(cart["id"], first_product["id"])
    return cart
```

| 行 | 含义 |
|---|---|
| `create_cart()` | POST /carts，返回含 `id` 的 cart |
| `add_to_cart(cart_id, product_id)` | POST /carts/{id} 加购 |
| `return cart` | 用例可直接 `order_api.submit_order(cart["id"])` |

```python
@pytest.fixture(scope="function")
def guest_cart_with_product(product_api, test_data) -> dict:
    result = product_api.search(test_data["keyword"])
    assert result.get("data"), ...
    product = result["data"][0]
    cart = product_api.create_cart()
    product_api.add_to_cart(cart["id"], product["id"])
    return cart
```

| 行 | 含义 |
|---|---|
| **无** `logged_in_api` | Session 无 Authorization Header |
| 搜索/建 cart 不需登录 | PST 站点允许匿名搜索和建 cart |
| 用于 `test_submit_order_unauthorized` | 提交订单时应 401 |

---

### 6.2 API 异常断言：`pytest.raises`

```python
def test_login_wrong_password(self, auth_api, test_data):
    with pytest.raises(requests.HTTPError) as exc:
        auth_api.login(test_data["email"], test_data["wrong_password"])
    assert exc.value.response.status_code == 401
```

| 行 | 含义 |
|---|---|
| `with pytest.raises(...)` | 块内必须抛出 `HTTPError`，否则测试失败 |
| `auth_api.login(...)` | Client 内 `json_or_raise` 遇 4xx 会 raise |
| `exc.value.response` | `HTTPError` 携带原始 Response 对象 |
| `.status_code == 401` | 精确断言业务错误码 |

多状态码场景（如无效 Token）：

```python
assert exc.value.response.status_code in (401, 403)
```

---

### 6.3 混合 E2E 用例 `test_full_purchase_flow.py`

```python
login = auth_api.login(test_data["email"], test_data["password"])
token = login["access_token"]
sync_token_to_clients(token, product_api, order_api)
sync_api_token_to_browser(driver, token, base_url)
```

| 行 | 含义 |
|---|---|
| `login(...)` | API 登录，Token 写入 auth_api 的 Session |
| `sync_token_to_clients` | 把 Token 同步到 product_api、order_api（同一 Session 其实已共享，显式调用更清晰） |
| `sync_api_token_to_browser` | localStorage 注入 + 等待 My Account 导航 |

```python
search = product_api.search(test_data["keyword"])
product = search["data"][0]
product_page.open_product(product["id"])
assert product["name"].split()[0].lower() in product_page.get_product_title().lower()
product_page.add_to_cart()
```

| 行 | 含义 |
|---|---|
| API 搜索 | 拿稳定 product_id |
| UI 打开详情 | 验证页面标题与 API 返回 name 一致 |
| `add_to_cart()` | 验证前端加购按钮可用 |

```python
cart = product_api.create_cart()
product_api.add_to_cart(cart["id"], product["id"])
invoice = order_api.submit_order(cart["id"])
attach_json(invoice, name="提交订单结果")
orders = order_api.list_orders()
assert invoice_number in str(orders) or product["name"] in str(orders)
```

| 行 | 含义 |
|---|---|
| 另建 API cart 下单 | 与 UI cart 分离，保证断言可控 |
| `attach_json` | 订单结果写入 Allure 便于排查 |
| 字符串包含断言 | 验证新订单出现在列表中 |

---

### 6.4 API 基类 `api/client/base_client.py`

#### 网络层重试

```python
def _request_with_retry(self, method: str, path: str, **kwargs: Any) -> requests.Response:
    for attempt in range(1, API_RETRY_COUNT + 1):
        try:
            if method == "GET":
                return self.session.get(self._url(path), **kwargs)
            ...
        except (requests.ConnectionError, requests.Timeout) as exc:
            if attempt >= API_RETRY_COUNT:
                raise
            time.sleep(API_RETRY_DELAY)
```

| 行 | 含义 |
|---|---|
| 默认 3 次尝试 | 配置见 `settings.API_RETRY_COUNT` |
| 只捕获网络异常 | **不**重试 HTTP 500/408 |
| `time.sleep` | 退避间隔 |

#### 失败自动附 Allure

```python
def raise_or_attach(self, response, context="") -> None:
    try:
        response.raise_for_status()
    except requests.HTTPError:
        attach_text(f"URL: {response.url}\nStatus: ...\nBody: ...", ...)
        raise

def json_or_raise(self, response, context="") -> Dict[str, Any]:
    self.raise_or_attach(response, context)
    return response.json()
```

- 成功：`raise_for_status` 通过 → 解析 JSON  
- DELETE 无 body：只用 `raise_or_attach`

---

### 6.5 Page Object 基类 `ui/pages/base_page.py`

#### 带重试的 click

```python
def click(self, by: By, locator: str) -> None:
    def _do_click():
        self.popup.dismiss_all()
        self.find_clickable(by, locator).click()
        stable_delay()

    retry_action(
        _do_click,
        exceptions=(ElementClickInterceptedException, StaleElementReferenceException),
    )
```

| 行 | 含义 |
|---|---|
| `dismiss_all()` | 点击前关弹窗 |
| `find_clickable` | 等待元素可点击 |
| `retry_action` | Stale/Intercepted 时最多重试 3 次 |

#### open 页面标准流程

```python
def open(self, path: str = "") -> None:
    url = f"{self.base_url}/{path.lstrip('/')}" if path else self.base_url
    self.driver.get(url)
    wait_for_page_ready(self.driver, timeout=self.timeout)
    self.popup.dismiss_all()
```

- **打开 → 等 ready → 关弹窗**，子类如 `ProductPage.open_product` 调用 `self.open(f"product/{id}")`。

---

### 6.6 Token 同步 `utils/session_sync.py`

```python
def inject_auth_token(driver, token, base_url=None):
    url = (base_url or UI_BASE_URL).rstrip("/")
    driver.get(url)                    # ① 必须先打开域，否则 localStorage 无效
    wait_for_page_ready(driver)
    driver.execute_script(
        "window.localStorage.setItem(arguments[0], arguments[1]);",
        AUTH_TOKEN_KEY,                # ② 'auth-token'
        token,
    )
    driver.refresh()                   # ③ 刷新让 Angular 读 Token
    wait_for_page_ready(driver)
    PopupHandler(driver).dismiss_all()
```

```python
def sync_api_token_to_browser(driver, token, base_url=None):
    inject_auth_token(driver, token, base_url)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(("css selector", "[data-test='nav-my-account']"))
    )
```

- 等待 My Account 导航 = UI 登录态生效的同步点。

```python
def sync_token_to_clients(token: str, *clients) -> None:
    for client in clients:
        client.set_token(token)
```

- E2E 中把 Token 显式同步到多个 API Client。

---

### 6.7 弹窗处理 `utils/popup_handler.py`

```python
def dismiss_all(self) -> int:
    if not AUTO_DISMISS_POPUP:
        return 0
    closed = 0
    closed += self._press_escape()           # ESC 关模态框
    for selector in self.selectors:
        if self._try_click_selector(selector):  # 点关闭按钮
            closed += 1
    closed += self._accept_alert_if_present()   # JS alert
    return closed
```

| 调用位置 | 时机 |
|---|---|
| `conftest.driver` | 浏览器打开首页后 |
| `session_sync.inject_auth_token` | Token 注入 refresh 后 |
| `BasePage.open/click/...` | 每次页面操作前 |

---

### 6.8 conftest 失败截图 Hook

```python
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver") or item.funcargs.get("authenticated_driver")
        if drv is not None:
            try:
                attach_screenshot(drv, name=f"失败截图_{item.name}")
            except Exception:
                pass
```

| 行 | 含义 |
|---|---|
| `hookwrapper=True` | yield 后拿到测试结果 |
| `report.when == "call"` | 只在测试主体阶段，不含 setup |
| `item.funcargs` | 从 Fixture 注入参数取 driver |

---

### 6.9 两种重试机制对比

#### 用例级：`@pytest.mark.flaky`

```python
@pytest.mark.flaky(reruns=2, reruns_delay=2)
class TestSearchUi:
    ...
```

- 整条用例失败后最多再跑 2 次（共 3 次）
- 插件：`pytest-rerunfailures`
- 不加在 `@pytest.mark.exception` 用例上

#### 操作级：`retry_action`（`utils/wait_helper.py`）

```python
def retry_action(func, retries=None, delay=1.0, exceptions=(Exception,)):
    for attempt in range(1, max_retries + 1):
        try:
            return func()
        except exceptions as exc:
            if attempt >= max_retries:
                raise
            time.sleep(delay)
```

| | retry_action | flaky |
|---|---|---|
| 粒度 | 单次 click | 整条用例 |
| 场景 | StaleElement | UI 整体超时 |
| 耗时 | 秒级 | 整条用例重跑 |

---

## 7. 面试题与参考答案

### 7.1 基础概念

**Q1：什么是 Page Object Model（POM）？本项目如何体现？**

**答**：POM 将每个页面封装成类，元素定位与操作集中在 Page 类，测试用例只调用业务语义方法（如 `add_to_cart()`）。本项目 `ui/pages/product_page.py` 定义 `[data-test='add-to-cart']` 定位，用例写 `product_page.add_to_cart()`，定位变更只改 Page 一处。

---

**Q2：pytest Fixture 的 scope 有哪些？本项目怎么选？**

**答**：`function` / `class` / `module` / `package` / `session`。  
- `base_url` 用 `session`：整个测试会话 URL 不变。  
- `driver`、`api_session` 用 `function`：每条用例隔离，避免状态污染。  
- `logged_in_api` 用 `yield`：用例结束后 logout 清理。

---

**Q3：隐式等待和显式等待的区别？**

**答**：隐式等待是 driver 全局设置，每次 `find_element` 都会等；显式等待针对特定条件用 `WebDriverWait` 轮询。本项目两者结合，click 前用 `element_to_be_clickable`。

---

**Q4：requests.Session 有什么好处？**

**答**：复用 TCP 连接；Cookie 和 Header 在 Session 内共享。本项目三个 API Client 共用同一 Session，login 一次后 product_api/order_api 自动带 Token。

---

### 7.2 项目设计

**Q5：为什么做 API + UI 混合 E2E，而不是纯 UI？**

**答**：API 登录快且稳；Headless 易触发 Cloudflare；订单断言走 API 更简单；UI 只覆盖必须验证的前端交互。

---

**Q6：`first_product` 和 `guest_cart_with_product` Fixture 区别？**

**答**：  
- `first_product` 依赖 `logged_in_api`，Session 带 Token。  
- `guest_cart_with_product` 不依赖 `logged_in_api`，用于 401 权限测试。  
误用 `cart_with_product` 会导致 401 断言失败。

---

**Q7：如何理解测试金字塔？**

**答**：底层大量快速 API/单元测试，顶层少量 E2E。本项目 API 9 个 + E2E 2 个符合该比例。

---

### 7.3 进阶 / 框架

**Q8：`pytest.raises` 如何断言 HTTP 状态码？**

**答**：

```python
with pytest.raises(requests.HTTPError) as exc:
    auth_api.login(email, wrong_password)
assert exc.value.response.status_code == 401
```

`HTTPError` 的 `response` 属性即原始 Response，可读 status_code 和 body。

---

**Q9：`pytest_runtest_makereport` 的 hookwrapper 模式是什么？**

**答**：`hookwrapper=True` 时 Hook 必须 `yield` 一次。yield 后通过 `outcome.get_result()` 拿到 TestReport。本项目在失败时附截图。

---

**Q10：`@pytest.mark.flaky` 和 `retry_action` 有什么区别？**

**答**：flaky 是用例级整条重跑；retry_action 是操作级（如 click 内）捕获 StaleElement 重试。

---

**Q11：`json_or_raise` 的设计意图？**

**答**：统一校验 HTTP 状态、解析 JSON、失败时 attach 响应到 Allure，避免每个 Client 方法重复错误处理。

---

**Q12：Allure 报告中 epic / feature / title 层级？**

**答**：  
- `@allure.epic`：业务域  
- `@allure.feature`：模块  
- `@allure.title`：用例标题  
- 需要步骤树时可在用例内用 `with allure.step("步骤名"):`  

---

**Q13：`PopupHandler` 做了什么？在哪些地方被调用？**

**答**：ESC 关模态框、CSS 选择器点关闭按钮、accept JS alert。在 `conftest.driver`、`session_sync`、`BasePage` 各操作前调用。配置见 `settings.AUTO_DISMISS_POPUP` 和 `POPUP_CLOSE_SELECTORS`。

---

### 7.4 实战排查

**Q14：UI 用例本地通过、CI 失败，怎么排查？**

**答**：看 Allure 截图；检查 Headless/Cloudflare；检查 chromedriver 版本；StaleElement 已有 retry_action；必要时加 flaky 或加大 EXPLICIT_WAIT。

---

**Q15：API 测试返回 408 Timeout 怎么办？**

**答**：408 不会被网络重试；可加 flaky、检查远端负载、清理遗留 cart。

---

**Q16：为什么不把所有配置都放 .env？**

**答**：`.env` 适合敏感信息（账号密码）。URL、超时等写 `settings.py` 常量更直观。

---

**Q17：Selenium 4 与 webdriver-manager 如何协作？**

**答**：`ChromeDriverManager().install()` 下载匹配驱动，通过 `ChromeService` 注入 WebDriver。并设置隐式等待和页面加载超时。

---

**Q18：如何实现「失败自动截图」？**

**答**：`conftest.py` 注册 `pytest_runtest_makereport`，失败时 `attach_screenshot(driver)` 写入 Allure。

---

## 8. 学习路径建议

### 三阶段学习

| 阶段 | 做什么 | 读什么 |
|------|--------|--------|
| **入门** | 跑通测试、看懂目录 | [README.md 小白导读](./README.md) |
| **读代码** | 跟着注释理解实现 | `settings.py` → `conftest.py` → `test_auth_api.py` → `base_client.py` → `base_page.py` → `test_full_purchase_flow.py` |
| **进阶** | 设计取舍、面试、排查 | 本文第 2–5 节 + 第 7 节面试题 |

### 推荐阅读顺序（与 README 一致）

1. `config/settings.py` — 全局配置  
2. `api/client/base_client.py` + `auth_client.py` — HTTP 封装  
3. `tests/conftest.py` — Fixture 与 Hook（含数据准备）  
4. `utils/session_sync.py` + `popup_handler.py` — 混合 E2E 与弹窗  
5. `ui/pages/base_page.py` + `product_page.py` — POM  
6. `tests/api/test_auth_api.py` — API 用例 + pytest.raises  
7. `tests/e2e/test_full_purchase_flow.py` — 完整混合流程（步骤全在用例内）  

### 动手练习

| 练习 | 目标 |
|---|---|
| 给 `CartPage` 写 UI 用例 | 练习 Page Object + Fixture |
| 新增 `@pytest.mark.parametrize` 搜索关键词 | 练习数据驱动 |
| 给 `order_page` 加 UI 查单断言 | 练习 E2E 扩展 |
| 在 E2E 用例中加 `with allure.step(...)` | 练习 Allure 步骤报告 |
| 扩展 `POPUP_CLOSE_SELECTORS` | 练习弹窗适配 |

### 常用命令

```powershell
# 推荐：项目内入口（无需 activate）
.\pytest.bat
.\pytest.bat -m api -v
.\pytest.bat -m ui -v
.\pytest.bat tests/e2e/test_full_purchase_flow.py -v

# 一键测试 + Allure HTML
.\run_allure.bat
# 或
.venv\Scripts\python.exe run_e2e.py

# 仅根据已有结果生成报告
.venv\Scripts\python.exe generate_allure_report.py --report-only
```

---

*文档与项目代码同步；pytest 配置见 `pyproject.toml`；源码逐行注释见各 `.py` 文件。最后更新：2026-07-04*
