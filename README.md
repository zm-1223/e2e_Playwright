# Practice Software Testing E2E 自动化

基于 **pytest + Selenium + requests + Allure** 的 API/UI 混合 E2E 框架，被测站点：[https://practicesoftwaretesting.com/](https://practicesoftwaretesting.com/)

---

## 小白导读

> 本节面向**第一次接触自动化测试**的同学：不讲逐行代码，只帮你建立整体地图。  
> 每个 `.py` 文件里已有**中文逐行注释**；想系统梳理设计、面试题、疑难点，请看 **[node.md](./node.md)**。

### 这个项目是做什么的？

想象你在测试一个网上商城：

1. 用户能否登录？
2. 搜索商品是否正常？
3. 点「加入购物车」按钮有没有反应？
4. 下单后订单列表里能不能查到？

手工点一遍很慢，而且每次发版都要重复。本项目用 **Python 脚本自动完成这些检查**，并在失败时生成 **Allure 报告** 和 **浏览器截图**，方便排查。

被测网站是公开的练习站点 **Practice Software Testing**（不是淘宝），API 和 UI 都是真实线上环境。

### 先搞懂 5 个词

| 术语 | 通俗解释 | 在本项目里 |
|------|----------|------------|
| **pytest** | Python 的测试运行器 | 执行 `tests/` 下的用例，统计通过/失败 |
| **Fixture** | 测试前的「准备工作」 | `conftest.py` 里自动提供浏览器、登录态、测试数据 |
| **Selenium** | 用代码控制真实浏览器 | 打开网页、点击按钮、读页面文字 |
| **requests** | 用代码发 HTTP 请求 | 调登录、搜索、下单等 API，比 UI 更快 |
| **Page Object** | 把每个页面封装成一个类 | `ui/pages/product_page.py` 里有「加购」方法，用例只调用方法，不写定位细节 |

### 项目结构像什么？

可以把它想成 **四层楼**：

```
┌─────────────────────────────────────┐
│  tests/          测试用例（你要跑的脚本） │
├─────────────────────────────────────┤
│  ui/pages/       页面操作（怎么点按钮）   │
│  api/client/     接口调用（怎么调 API）    │
├─────────────────────────────────────┤
│  utils/          工具（等待、弹窗、Token）  │
├─────────────────────────────────────┤
│  config/         配置（网址、超时、账号）   │
└─────────────────────────────────────┘
```

**原则**：用例只写「做什么 + 期望结果」；具体怎么点、怎么请求，交给 Page 和 Client。

### 三种测试，分别测什么？

| 类型 | 目录 | 数量 | 特点 | 适合学什么 |
|------|------|------|------|------------|
| **API** | `tests/api/` | 9 个 | 快、稳、无浏览器 | HTTP、登录 Token、断言状态码 |
| **UI** | `tests/ui/` | 3 个 | 开 Chrome，操作页面 | Selenium、Page Object |
| **E2E** | `tests/e2e/` | 2 个 | API + UI 一起跑 | 混合自动化、跨端协作 |

默认执行 `pytest` 会跑 **全部 14 个**；只想跑某一类时加 `-m api` / `-m ui` / `-m e2e`。

### 混合 E2E 在干什么？（核心流程）

完整购买流程见 `tests/e2e/test_full_purchase_flow.py`，逻辑可以概括为：

```
API 登录拿 Token
    ↓
把 Token 写入浏览器（跳过登录页）
    ↓
API 搜索商品（拿到稳定的 product_id）
    ↓
UI 打开商品页并点击「加购」（验证前端）
    ↓
API 创建购物车、提交订单、查订单列表（验证后端）
```

**为什么不用纯 UI？** UI 登录慢、容易被 Cloudflare 拦截；订单断言用 API 更简单。UI 只负责「必须肉眼验证的交互」。

### 推荐阅读顺序（第一次读代码）

按下面顺序打开文件，配合文件内的中文注释：

1. **`config/settings.py`** — 网址、超时、默认账号在哪里改  
2. **`tests/conftest.py`** — 浏览器和 API 客户端是怎么「自动准备好」的  
3. **`tests/api/test_auth_api.py`** — 最简单的 API 用例（登录成功/失败）  
4. **`api/client/base_client.py`** — HTTP 请求、重试、失败附报告  
5. **`ui/pages/base_page.py`** — 页面打开的通用步骤（等待、关弹窗）  
6. **`tests/e2e/test_full_purchase_flow.py`** — 一条线串起 API + UI  

### 第一次运行（最少步骤）

```powershell
# 1. 进入项目根目录（含 pyproject.toml 的文件夹）
cd D:\github-code\E2E_demo

# 2. 创建虚拟环境并安装依赖（只需做一次）
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt

# 3. 跑全部测试（推荐，不用 activate）
.\pytest.bat
```

跑完后查看报告：

```powershell
.\run_allure.bat
# 浏览器会打开 reports/allure-report/index.html
```

只想先跑 **API**（不启动浏览器，最快）：

```powershell
.\pytest.bat -m api
```

### 跑测试时，背后发生了什么？

1. **pytest** 扫描 `tests/` 下所有 `test_*.py`  
2. 每个用例执行前，**conftest** 按名字注入 `driver`、`auth_api` 等 Fixture  
3. **API 用例**：`auth_api.login()` → `requests` 发 POST → `assert` 检查返回值  
4. **UI 用例**：`WebDriverManager` 启动 Chrome → `ProductPage.add_to_cart()` → Selenium 点击  
5. 若失败：Hook 自动 **截图** 到 `reports/screenshots/`，并写入 Allure  
6. 结果写入 `reports/allure-results/`，可用 Allure 生成 HTML  

### 新手常踩的坑

| 现象 | 原因 | 解决办法 |
|------|------|----------|
| `No module named 'allure'` | 用了系统 Python 的 `pytest` | 用 `.\pytest.bat` 或 `.venv\Scripts\pytest.exe` |
| PowerShell 无法 `activate` | 执行策略限制 | 用 `.\env_dev.ps1` 或 `.\pytest.bat` |
| UI/E2E 超时或 401 | 网络慢、Token 未同步 | 看 Allure 截图；API 可先 `-m api` 确认环境正常 |
| 改了配置没生效 | 改错文件 | 账号在 `.env`；其他在 `config/settings.py` |

### 三份文档怎么配合？

| 文档 | 适合谁 | 内容 |
|------|--------|------|
| **README.md（本文）** | 零基础入门 | 概念、跑通、阅读顺序 |
| **各 `.py` 文件内注释** | 读代码时 | 逐行中文说明 |
| **[node.md](./node.md)** | 进阶 / 面试 | 架构、数据流、疑难点、面试题 |

---

## 环境准备

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows（若被策略拦截，改用 env_dev.ps1）
pip install -r requirements.txt
copy .env.example .env          # 可选，默认配置即可运行
```

需要安装 **Chrome 浏览器**；WebDriver 由 `webdriver-manager` 自动下载。

## 运行测试

配置在 **`pyproject.toml`**：`pytest` 默认扫描 `tests/` 下全部 **`test_*.py`**（共 14 个用例），**不要**加 `-m api` 等过滤（除非只想跑某一类）。

### 方式 1：项目内直接跑（推荐，无需 activate）

在项目根目录下：

```powershell
.\pytest.bat
```

等价于运行全部 API + UI + E2E 用例。

### 方式 2：终端里只输入 `pytest`

PowerShell 需先把 `.venv` 加入当前会话 PATH（只需执行一次，本窗口有效）：

```powershell
. .\env_dev.ps1
pytest
```

CMD 用户：

```cmd
call env_dev.bat
pytest
```

### 方式 3：显式指定 venv 里的 pytest

```powershell
.venv\Scripts\pytest.exe
```

### 方式 4：一键测试 + Allure 报告

```powershell
.venv\Scripts\python.exe run_e2e.py
```

> 若直接输入 `pytest` 报 `No module named 'allure'`，说明用的是系统 Python，请改用上面几种方式之一。

### 按标记筛选（可选）

```powershell
.\pytest.bat -m api          # 仅 API（9 个）
.\pytest.bat -m ui            # 仅 UI（3 个）
.\pytest.bat -m e2e           # 仅 E2E（2 个）
```

### Allure 可视化报告

```powershell
run_allure.bat
# 或
.venv\Scripts\python.exe generate_allure_report.py
```

报告路径：`reports/allure-report/index.html`

```powershell
# 已有结果，仅重新生成报告
.venv\Scripts\python.exe generate_allure_report.py --report-only
```

## 默认账号

| 项 | 值 |
|---|---|
| UI | https://practicesoftwaretesting.com |
| API | https://api.practicesoftwaretesting.com |
| 邮箱 | customer@practicesoftwaretesting.com |
| 密码 | welcome01 |

## 目录结构

```
config/                  # 配置（settings.py）
api/client/              # API 客户端（auth / product / order）
ui/pages/                # Page Object 页面对象
ui/driver/               # WebDriver 管理
tests/                   # api(9) + ui(3) + e2e(2) = 14 用例
utils/                   # 等待、弹窗、Token 同步、Allure 辅助
reports/                 # Allure 结果、HTML 报告、失败截图
pyproject.toml           # pytest 默认配置
pytest.bat / run_tests.bat   # 项目内 pytest 入口
env_dev.ps1 / env_dev.bat    # 载入 .venv 后可直输 pytest
run_e2e.py               # 一键跑测 + 生成 Allure
generate_allure_report.py
node.md                  # 进阶梳理与面试题
```

## 混合 E2E 流程（摘要）

1. API 登录获取 `access_token`
2. 注入浏览器 `localStorage['auth-token']`
3. API 搜索商品
4. UI 打开商品页并加购
5. API 创建购物车、提交订单
6. API 查询订单列表验证

## 配置说明

**账号密码**（敏感）：复制 `.env.example` 为 `.env` 后修改。

**其他配置**（站点地址、浏览器、超时等）：直接改 `config/settings.py` 中的常量。

**用例失败重试**（UI/E2E）：在测试类或方法上加装饰器，例如：

```python
@pytest.mark.flaky(reruns=2, reruns_delay=2)
class TestSearchUi:
    ...
```

`reruns=2` 表示失败后最多再跑 2 次（共 3 次机会）。异常用例一般不加此装饰器。

---

**下一步**：读代码时打开对应 `.py` 看逐行注释；想深入架构与面试准备，请阅读 **[node.md](./node.md)**。
