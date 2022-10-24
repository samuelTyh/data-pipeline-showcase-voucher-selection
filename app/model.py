from typing import Optional
import pydantic


class Customer(pydantic.BaseModel):
    customer_id: Optional[int] = None
    country_code: Optional[str] = None
    last_order_ts: Optional[str] = None
    first_order_ts: Optional[str] = None
    total_orders: Optional[int] = None
    segment_name: Optional[str] = None


class Voucher(pydantic.BaseModel):
    customer_id: Optional[int] = None
    segment_name: Optional[str] = None
    segment_value: Optional[str] = None
    voucher_amount: Optional[int] = None
