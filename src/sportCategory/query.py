from utils import mysql
import pymysql
from common import timestamp
# from 主目錄.子目錄 import 檔名(py檔)

import logging
from collections.abc import Sequence
logger = logging.getLogger("flask.app")


tableName = 'sport_category'

selectField = f"item_id, option_id, updated_at, created_at"

def list(sort, pagination):
    """取得設定版本

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 設定版本 }
    """

    conn = None
    try:
        conn = mysql.get_mysql_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # 分頁參數
            page = pagination.get('page', 1) if pagination else 1
            per_page = pagination.get('perPage', 10) if pagination else 10
            offset = (page - 1) * per_page

            # 如果 sort 有值，則根據 sort 參數決定排序方式
            if not sort:
                query = f"SELECT {selectField} FROM {tableName} ORDER BY updated_at DESC LIMIT %s OFFSET %s;"
                query_args = (per_page, offset)
            else:
                if sort['field'] == "id": # 預設欄位是 id，但是 sport_category 沒有 id 欄位
                    sort['field'] = "item_id"
                query = f"SELECT {selectField} FROM {tableName} ORDER BY {sort['field']} {sort['order']} LIMIT %s OFFSET %s;"
                query_args = (per_page, offset)

            cursor.execute(query, query_args)
            logger.info(query)

            rows = cursor.fetchall()
            # 查詢總筆數
            count_query = f"SELECT COUNT(*) as total FROM {tableName};"
            cursor.execute(count_query)
            count_row = cursor.fetchone()
            total = count_row["total"] if count_row else 0

            if rows:
                array = []
                for row in rows:
                    array.append({
                        "id": f"{row['item_id']}-{row['option_id']}", # 前端 React Admin 需要 id 欄位來顯示序號
                        "item_id": row["item_id"],
                        "option_id": row["option_id"],
                        "updated_at": str(row["updated_at"]),
                        "updated_at_timestamp": timestamp.datetime_str_to_timestamp(str(row["updated_at"])),
                        "created_at": str(row["created_at"]),
                        "created_at_timestamp": timestamp.datetime_str_to_timestamp(str(row["created_at"])),
                    })
                return {"is_success": True, "result": {"data": array, "total": total}}
            else:
                return {"is_success": False, "result": "無法獲取設定"}
    except Exception as e:
        return {"is_success": False, "result": f"連線失敗: {e}"}
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

def get(item_id, option_id):
    """取得設定版本

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 設定版本 }
    """

    if not item_id:
        raise ValueError("item_id 參數必填")
    if not option_id:
        raise ValueError("option_id 參數必填")
    conn = None
    try:
        conn = mysql.get_mysql_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            query = f"SELECT {selectField} FROM {tableName} WHERE item_id = %s AND option_id = %s;"
            cursor.execute(query, (item_id, option_id))
            logger.info(query, item_id, option_id)

            row = cursor.fetchone()
            if row:
                return {
                    "is_success": True,
                    "result": {
                        "id": f"{row['item_id']}-{row['option_id']}", # 前端 React Admin 需要 id 欄位來顯示序號
                        "item_id": row["item_id"],
                        "option_id": row["option_id"],
                        "updated_at": str(row["updated_at"]),
                        "updated_at_timestamp": timestamp.datetime_str_to_timestamp(str(row["updated_at"])),
                        "created_at": str(row["created_at"]),
                        "created_at_timestamp": timestamp.datetime_str_to_timestamp(str(row["created_at"])),
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

def create(item_id, option_id):
    """建立設定版本

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 設定版本 }
    """

    if not item_id:
        raise ValueError("item_id 參數必填")
    if not option_id:
        raise ValueError("option_id 參數必填")
    conn = None
    try:
        conn = mysql.get_mysql_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # 新增一筆資料
            insert_query = f"INSERT INTO {tableName} (item_id, option_id, updated_at, created_at) VALUES (%s, %s, NOW(), NOW());"
            cursor.execute(insert_query, (item_id, option_id))
            conn.commit()
            logger.info(insert_query, item_id, option_id)

            select_query = f"SELECT {selectField} FROM {tableName} WHERE item_id = %s AND option_id = %s;"
            cursor.execute(select_query, (item_id, option_id))
            logger.info(select_query, item_id, option_id)
            row = cursor.fetchone()
            if row:
                return {
                    "is_success": True,
                    "result": {
                        "id": f"{row['item_id']}-{row['option_id']}", # 前端 React Admin 需要 id 欄位來顯示序號
                        "item_id": row["item_id"],
                        "option_id": row["option_id"],
                        "updated_at": str(row["updated_at"]),
                        "updated_at_timestamp": timestamp.datetime_str_to_timestamp(str(row["updated_at"])),
                        "created_at": str(row["created_at"]),
                        "created_at_timestamp": timestamp.datetime_str_to_timestamp(str(row["created_at"])),
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

def delete(item_id, option_id):
    """刪除設定版本

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 設定版本 }
    """

    if not item_id:
        raise ValueError("item_id 參數必填")
    if not option_id:
        raise ValueError("option_id 參數必填")
    conn = None
    try:
        conn = mysql.get_mysql_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            delete_query = f"DELETE FROM {tableName} WHERE item_id = %s AND option_id = %s;"
            cursor.execute(delete_query, (item_id, option_id))
            conn.commit()
            logger.info(delete_query, item_id, option_id)
            return {"is_success": True, "result": {"id": f"{item_id}-{option_id}"}}
    except Exception as e:
        return {"is_success": False, "result": f"連線失敗: {e}"}
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

def deleteMany(ids):
    """刪除設定版本

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 設定版本 }
    """

    # 支援傳入逗號分隔字串或單一值
    if isinstance(ids, str):
        ids = [i.strip() for i in ids.split(',') if i.strip()]
    elif not isinstance(ids, Sequence):
        raise ValueError("ids 參數型態錯誤")
    if not ids:
        raise ValueError("ids 參數不可為空")
    # ids 假設為 ['97-1', '97-2'] 其中的 '97-1' 為 item_id-option_id 組合而成，需要拆解
    # 拆解後的結果為:
    # item_ids = ['97']
    # option_ids = ['1', '2']

    conn = None
    try:
        conn = mysql.get_mysql_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # 這邊需要 for loop 一筆一筆刪除
            for id in ids:
                item_id, option_id = id.split('-', 1)
                delete_query = f"DELETE FROM {tableName} WHERE item_id = %s AND option_id = %s;"
                cursor.execute(delete_query, (item_id, option_id))
                #logger.info(delete_query, (item_id, option_id))
                logger.info(f"{delete_query} {item_id}, {option_id}")
            conn.commit()
            
            return {"is_success": True, "result": ids}
    except Exception as e:
        return {"is_success": False, "result": f"連線失敗: {e}"}
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass