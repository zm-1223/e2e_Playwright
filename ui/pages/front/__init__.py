# =============================================================================
# ui/pages/front/__init__.py — 前台 Page Object 子包 （项目：ui/pages/front/__init__.py）
# 作用：标识 front 为 ui.pages 子包；对外导出 BasePage 供类型引用 （Python 内置：包机制）
# 调用关系：测试与 conftest 通过 ui.pages.front.login_page 等具体模块导入 （项目：tests/conftest.py）
# =============================================================================
from ui.pages.base_page import BasePage  # 作用：导出基类；调用关系：子类 FrontLoginPage 等继承；自定义；来源(项目 ui/pages/base_page.py)

__all__ = ["BasePage"]  # 作用：定义 from ui.pages.front import * 时导出的符号；Python 内置：__all__
