from datetime import datetime
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

from data_pipeline import create_frequent_segment, create_recency_segment, calculate_datediff, Run
from .model import Customer, Voucher


run = Run()
run.build_segment_data('frequent_segment')
run.build_segment_data('recency_segment')


def voucher_selection(request: Customer) -> Voucher:
    """
    Create Voucher selection by data posting from endpoint
    :param request: customer's request
    :return: voucher
    """
    country_code, segment_name = request.country_code, request.segment_name
    if segment_name == 'frequent_segment':
        segment_value = create_frequent_segment(request.total_orders)
    elif segment_name == 'recency_segment':
        datediff = calculate_datediff(request.last_order_ts)
        segment_value = create_recency_segment(datediff)
    else:
        segment_value = None
    voucher_amount = run.db.get_voucher_amount_from_segment(segment_value)
    return Voucher(
        customer_id=request.customer_id,
        segment_name=segment_name,
        segment_value=segment_value,
        voucher_amount=voucher_amount
    )


api = FastAPI()


@api.get("/ping")
def ping():
    return {'status': 'works!'}


@api.post("/voucher")
async def post_voucher(request: Customer):
    try:
        voucher = voucher_selection(request)
        insertion = dict()
        insertion["timestamp"] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        insertion['country_code'] = request.country_code
        insertion['last_order_ts'] = request.last_order_ts
        insertion['first_order_ts'] = request.last_order_ts
        insertion['total_orders'] = request.total_orders
        insertion["voucher_amount"] = voucher.voucher_amount
        run.db.insert_into_main_table([insertion])
        if voucher is None:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
        return {"voucher_amount": voucher.voucher_amount}
    except BaseException as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
