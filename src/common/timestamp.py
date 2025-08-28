import datetime


# 將 updated_at 欄位字串 "2025-08-19 16:32:38" 轉成數值（timestamp）
def datetime_str_to_timestamp(dt_str):
    # dt_str 格式必須為 "%Y-%m-%d %H:%M:%S"
    dt_obj = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    return int(dt_obj.timestamp())

def timestamp_to_datetime_str(ts):
    # ts 為 timestamp 整數
    dt_obj = datetime.datetime.fromtimestamp(ts)
    return dt_obj.strftime("%Y-%m-%d %H:%M:%S")

