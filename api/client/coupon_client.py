# =============================================================================
# api/client/coupon_client.py — 优惠券 API 客户端 （项目：api/client/coupon_client.py）
# 作用：封装买家「我的优惠券」列表及状态名提取 （项目：api/client/coupon_client.py → CouponApiClient）
# 说明：继承 BaseApiClient；conftest 的 coupon_api fixture 注入；与 admin 优惠券管理 API 不同 （项目：tests/conftest.py）
# =============================================================================

# 导入 Any/Dict/List：标注 my_coupons 返回与 status_names 列表类型 （标准库：typing）
from typing import Any, Dict, List

# 导入 BaseApiClient：复用 get 与 data_or_raise （项目：api/client/base_client.py → BaseApiClient）
from api.client.base_client import BaseApiClient


# 优惠券 API 客户端类（买家端） （项目：api/client/coupon_client.py → CouponApiClient）
class CouponApiClient(BaseApiClient):
    """优惠券 API。"""

    # 分页查询当前用户持有的优惠券：GET /user/coupon/list （项目：tests/api/test_coupon_api.py 调用）
    def my_coupons(self, page: int = 1, size: int = 10) -> Dict[str, Any]:
        # GET 带分页参数 （项目：api/client/base_client.py → BaseApiClient.get）
        response = self.get("/user/coupon/list", params={"page": page, "size": size})
        # 返回 records/total 等分页 data （项目：api/client/base_client.py → BaseApiClient.data_or_raise）
        return self.data_or_raise(response, " /user/coupon/list")

    # 从 my_coupons 结果提取 statusName 列表（如「未使用」「已使用」） （项目：tests/api/test_coupon_api.py 断言）
    def coupon_status_names(self) -> List[str]:
        # 默认取第 1 页最多 10 条 （项目：api/client/coupon_client.py → CouponApiClient.my_coupons）
        data = self.my_coupons(page=1, size=10)
        # 优惠券记录列表 （Python 内置：dict.get, or）
        records = data.get("records") or []
        # 列表推导：每条 record 的 statusName 非空则收集 （Python 内置：list comprehension）
        return [r.get("statusName", "") for r in records if r.get("statusName")]
