# =============================================================================
# ui/pages/admin/__init__.py — 后台 Page Object 子包 （项目：ui/pages/admin/__init__.py）
# 作用：标识 admin 为 ui.pages 子包；对外导出 BasePage （Python 内置：包机制）
# 调用关系：测试通过 ui.pages.admin.login_page 等导入后台页面类 （项目：tests/ui/test_admin_ui.py）
# =============================================================================
from ui.pages.base_page import BasePage  # 作用：导出基类；调用关系：AdminLoginPage 等继承；自定义；来源(项目 ui/pages/base_page.py)

__all__ = ["BasePage"]  # 作用：控制包公开 API；Python 内置：__all__
