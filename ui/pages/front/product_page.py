# =============================================================================
# 文件名: product_page.py
# 模块路径: ui/pages/front/product_page.py
# 作用: 商品详情页 Page Object，封装 SKU 选择、加购等操作
# 调用关系: 继承 BasePage；被 tests/ui/test_front_shop_ui.py、tests/e2e/* 调用
# 类型: 自定义（项目）
# 来源: E2E_demo 项目
# =============================================================================
# 导入 By，定义元素定位方式（第三方：selenium.webdriver.common.by → By）
from selenium.webdriver.common.by import By
# 导入 WebDriverWait，用于轮询等待浏览器标题渲染（第三方：selenium.webdriver.support.ui → WebDriverWait）
from selenium.webdriver.support.ui import WebDriverWait

# 导入 Page Object 基类（项目：ui/pages/base_page.py → BasePage）
from ui.pages.base_page import BasePage

# 商品不存在时浏览器标题的特征词，用于区分 404 页与真实商品页（项目：ui/pages/front/product_page.py）
_NOT_FOUND_TITLE_TOKENS = ("404", "未找到", "不存在")


# 商品详情页类：映射 /product/{id} 页面（项目：ui/pages/front/product_page.py → FrontProductPage）
class FrontProductPage(BasePage):
    """商品详情页 /product/{id}。"""

    # 商品标题元素定位元组，兼容 h1 与多种 class（第三方：selenium → By.CSS_SELECTOR）
    PRODUCT_TITLE = (By.CSS_SELECTOR, "h1, .product-name, .product-title")
    # “加入购物车”按钮 XPath 定位（第三方：selenium → By.XPATH）
    ADD_TO_CART = (By.XPATH, "//button[contains(.,'加入购物车')]")
    # SKU 规格单选按钮定位元组（第三方：selenium → By.CSS_SELECTOR）
    SKU_RADIO = (By.CSS_SELECTOR, ".el-radio, .spe .el-radio")
    # 购物车角标/数量徽章定位元组（第三方：selenium → By.CSS_SELECTOR）
    CART_BADGE = (By.CSS_SELECTOR, ".cart-count, .badge, [class*='cart']")

# 作用：定义函数/方法 open_product；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/front/product_page.py)
    def open_product(self, product_id) -> None:
        # Tigshop 商品详情路由为 /item/{商品编号}，编号形如 SN+6位零填充数字 id（如 338→SN000338）；已是 SNxxx 编号则直接使用（第三方：Python 内置 str/int）
        product_sn = product_id if str(product_id).upper().startswith("SN") else f"SN{int(product_id):06d}"
        # 打开指定商品编号的详情页 /item/{sn}（项目：ui/pages/base_page.py → BasePage.open）
        self.open(f"item/{product_sn}")

# 作用：定义函数/方法 select_first_sku_if_needed；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/front/product_page.py)
    def select_first_sku_if_needed(self) -> None:
        # 查找页面上所有 SKU 单选项（第三方：selenium → WebDriver.find_elements）
        radios = self.driver.find_elements(*self.SKU_RADIO)
        # 若存在 SKU 选项，则点击第一个完成规格选择（Python 内置：if；第三方：selenium → WebElement.click）
        if radios:
# 作用：点击页面元素；调用关系：Selenium WebElement.click；自定义/框架：框架(Selenium)；来源(selenium)
            radios[0].click()

# 作用：定义函数/方法 get_product_title；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/front/product_page.py)
    def get_product_title(self) -> str:
        # 商品名异步渲染进浏览器标签标题(document.title)，open_product 刚导航完可能仍为空/旧值；轮询等待其出现且非404，避免读到空标题（第三方：selenium → WebDriverWait）
        try:
            WebDriverWait(self.driver, self.timeout).until(
                lambda d: (d.title or "").strip()
                and not any(tok in d.title for tok in _NOT_FOUND_TITLE_TOKENS)
            )
        except Exception:
            pass
        # 返回浏览器标题(商品名)，比 DOM 内 .name(含"站点导航"等干扰)更可靠（第三方：selenium → WebDriver.title）
        return (self.driver.title or "").strip()

# 作用：定义函数/方法 add_to_cart；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/front/product_page.py)
    def add_to_cart(self) -> None:
        # 若有 SKU 则先选择第一个规格（项目：ui/pages/front/product_page.py → FrontProductPage.select_first_sku_if_needed）
        self.select_first_sku_if_needed()
        # 点击“加入购物车”按钮（项目：ui/pages/base_page.py → BasePage.click）
        self.click(*self.ADD_TO_CART)

# 作用：定义函数/方法 title_visible；调用关系：见函数体调用链；自定义/框架：自定义；来源(ui/pages/front/product_page.py)
    def title_visible(self) -> bool:
        # 复用 get_product_title 的等待逻辑：能取到非空(且非404)商品名即视为详情页正常加载（项目：get_product_title）
        return bool(self.get_product_title())
