from dotenv import load_dotenv
import os
import pymysql
from common import timestamp


import logging
logger = logging.getLogger("flask.app")

# 載入 .env 檔案
load_dotenv()

def get_mysql_connection():
    """建立連線到 MySQL 資料庫

    Raises:
        ValueError: 連線資訊缺失

    Returns:
        _type_: MySQL 連線物件
    """

    host = os.getenv('DB_HOST')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    db = os.getenv('DB_NAME')
    #print(f"host={host}, user={user}, password={password}, db={db}")  # 除錯用

    # 檢查必要的環境變量是否存在
    if not host or not user or not password or not db:
        raise ValueError("資料庫連線資訊缺少，請檢查 .env 檔案設定")

    return pymysql.connect(
        host=host,
        user=user,
        password=password,
        db=db,
        charset='utf8mb4'
    )

def get_now_time():
    """取得目前時間

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 目前時間 }
    """

    conn = None
    try:
        conn = get_mysql_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            query = "SELECT NOW() AS now_time;"
            logger.info(query)
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                return {"is_success": True, "result": result["now_time"]}
            else:
                return {"is_success": False, "result": "無法獲取數據庫時間"}
    except Exception as e:
        return {"is_success": False, "result": f"連線失敗: {e}"}
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

def get_setting_version(data_type):
    """取得設定版本

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 設定版本 }
    """

    conn = None
    try:
        conn = get_mysql_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            query = ""
            if data_type:
                query = "SELECT data_type, version, updated_at FROM setting_versions WHERE data_type = %s ORDER BY updated_at DESC;"
                cursor.execute(query, (data_type,))
                logger.info(query, data_type)
            else:
                query = "SELECT data_type, version, updated_at FROM setting_versions ORDER BY updated_at DESC;"
                cursor.execute(query)
                logger.info(query)            

            rows = cursor.fetchall()
            if rows:
                array = []
                idx = 1
                for row in rows:
                    array.append({
                        "data_type": row["data_type"],
                        "version": row["version"],
                        "updated_at": str(row["updated_at"]),
                        "updated_at_timestamp": timestamp.datetime_str_to_timestamp(str(row["updated_at"])),
                        "id": idx, # 前端 React Admin 需要 id 欄位來顯示序號
                    })
                    idx += 1
                return {"is_success": True, "result": array}
            else:
                return {"is_success": False, "result": "無法獲取設定版本"}
    except Exception as e:
        return {"is_success": False, "result": f"連線失敗: {e}"}
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass