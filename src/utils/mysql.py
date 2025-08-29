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

def setting_version_list(sort):
    """取得設定版本

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 設定版本 }
    """

    conn = None
    try:
        conn = get_mysql_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # 如果 sort 有值，則根據 sort 參數決定排序方式
            if not sort:
                query = "SELECT data_type, version, updated_at, id FROM setting_versions ORDER BY updated_at DESC;"
            else:
                query = f"SELECT data_type, version, updated_at, id FROM setting_versions ORDER BY {sort['field']} {sort['order']};"

            cursor.execute(query)
            logger.info(query)            

            rows = cursor.fetchall()
            if rows:
                array = []
                for row in rows:
                    array.append({
                        "data_type": row["data_type"],
                        "version": row["version"],
                        "updated_at": str(row["updated_at"]),
                        "updated_at_timestamp": timestamp.datetime_str_to_timestamp(str(row["updated_at"])),
                        "id": row["id"], # 前端 React Admin 需要 id 欄位來顯示序號
                    })
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

def setting_version_get(id):
    """取得設定版本

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 設定版本 }
    """

    if not id:
        raise ValueError("id 參數必填")
    conn = None
    try:
        conn = get_mysql_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            query = "SELECT data_type, version, updated_at, id FROM setting_versions WHERE id = %s;"
            cursor.execute(query, (id,))
            logger.info(query, id)

            row = cursor.fetchone()
            if row:
                return {
                    "is_success": True,
                    "result": {
                        "data_type": row["data_type"],
                        "version": row["version"],
                        "updated_at": str(row["updated_at"]),
                        "updated_at_timestamp": timestamp.datetime_str_to_timestamp(str(row["updated_at"])),
                        "id": row["id"],
                    }
                }
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

def setting_version_create(data_type, version):
    """建立設定版本

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 設定版本 }
    """

    if not data_type:
        raise ValueError("data_type 參數必填")
    if not version:
        version = "1.0.0"
    conn = None
    try:
        conn = get_mysql_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # 新增一筆資料
            insert_query = "INSERT INTO setting_versions (data_type, version, updated_at) VALUES (%s, %s, NOW());"
            cursor.execute(insert_query, (data_type, version))
            conn.commit()
            logger.info(insert_query, data_type, version)

            # 取得剛新增的資料（用自動產生的 id）
            last_id = cursor.lastrowid
            select_query = "SELECT data_type, version, updated_at, id FROM setting_versions WHERE id = %s;"
            cursor.execute(select_query, (last_id,))
            logger.info(select_query, last_id)
            row = cursor.fetchone()
            if row:
                return {
                    "is_success": True,
                    "result": {
                        "data_type": row["data_type"],
                        "version": row["version"],
                        "updated_at": str(row["updated_at"]),
                        "updated_at_timestamp": timestamp.datetime_str_to_timestamp(str(row["updated_at"])),
                        "id": row["id"],
                    }
                }
            else:
                return {"is_success": False, "result": "無法獲取新增後的設定版本"}
    except Exception as e:
        return {"is_success": False, "result": f"連線失敗: {e}"}
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

def setting_version_update(id, version):
    """更新設定版本

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 設定版本 }
    """

    if not id:
        raise ValueError("id 參數必填")
    conn = None
    try:
        conn = get_mysql_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            if version:
                update_query = "UPDATE setting_versions SET version = %s, updated_at = NOW() WHERE id = %s;"
                cursor.execute(update_query, (version, id))
                logger.info(update_query, version, id)
            else:
                update_query = "UPDATE setting_versions SET updated_at = NOW() WHERE id = %s;"
                cursor.execute(update_query, (id,))
                logger.info(update_query, id)
            conn.commit()

            # 取得更新後的資料
            select_query = "SELECT data_type, version, updated_at, id FROM setting_versions WHERE id = %s;"
            cursor.execute(select_query, (id,))
            logger.info(select_query, id)
            row = cursor.fetchone()
            if row:
                return {
                    "is_success": True,
                    "result": {
                        "data_type": row["data_type"],
                        "version": row["version"],
                        "updated_at": str(row["updated_at"]),
                        "updated_at_timestamp": timestamp.datetime_str_to_timestamp(str(row["updated_at"])),
                        "id": row["id"],
                    }
                }
            else:
                return {"is_success": False, "result": "無法獲取更新後的設定版本"}
    except Exception as e:
        return {"is_success": False, "result": f"連線失敗: {e}"}
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

def setting_version_delete(id):
    """刪除設定版本

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 設定版本 }
    """

    if not id:
        raise ValueError("id 參數必填")
    conn = None
    try:
        conn = get_mysql_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            delete_query = "DELETE FROM setting_versions WHERE id = %s;"
            cursor.execute(delete_query, (id,))
            conn.commit()
            logger.info(delete_query, id)
            return {"is_success": True, "result": {"id": id}}
    except Exception as e:
        return {"is_success": False, "result": f"連線失敗: {e}"}
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

def setting_version_deleteMany(ids):
    """刪除設定版本

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 設定版本 }
    """

    # 支援傳入逗號分隔字串或單一值
    if isinstance(ids, str):
        ids = [i.strip() for i in ids.split(',') if i.strip()]
    elif isinstance(ids, int):
        ids = [ids]
    elif not isinstance(ids, (list, tuple)):
        raise ValueError("ids 參數型態錯誤")
    if not ids:
        raise ValueError("ids 參數不可為空")
    conn = None
    try:
        conn = get_mysql_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # 產生 SQL IN 條件
            format_strings = ','.join(['%s'] * len(ids))
            delete_query = f"DELETE FROM setting_versions WHERE id IN ({format_strings});"
            cursor.execute(delete_query, tuple(ids))
            conn.commit()
            logger.info(delete_query, ids)
            return {"is_success": True, "result": ids}
    except Exception as e:
        return {"is_success": False, "result": f"連線失敗: {e}"}
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass