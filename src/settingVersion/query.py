from utils import mysql
import pymysql
from common import timestamp
# from 主目錄.子目錄 import 檔名(py檔)

import logging
from collections.abc import Sequence
logger = logging.getLogger("flask.app")


tableName = 'setting_versions'

selectField = f"id, data_type, version, updated_at, created_at"

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
                        "id": row["id"], # 前端 React Admin 需要 id 欄位來顯示序號
                        "data_type": row["data_type"],
                        "version": row["version"],
                        "updated_at": str(row["updated_at"]),
                        "updated_at_timestamp": timestamp.datetime_str_to_timestamp(str(row["updated_at"])),
                        "created_at": str(row["created_at"]),
                        "created_at_timestamp": timestamp.datetime_str_to_timestamp(str(row["created_at"])),
                    })
                return {"is_success": True, "result": {"data": array, "total": total}}
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

def get(id):
    """取得設定版本

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 設定版本 }
    """

    if not id:
        raise ValueError("id 參數必填")
    conn = None
    try:
        conn = mysql.get_mysql_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            query = f"SELECT {selectField} FROM {tableName} WHERE id = %s;"
            cursor.execute(query, (id,))
            logger.info(query, id)

            row = cursor.fetchone()
            if row:
                return {
                    "is_success": True,
                    "result": {
                        "id": row["id"],
                        "data_type": row["data_type"],
                        "version": row["version"],
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

def create(data_type, version):
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
        conn = mysql.get_mysql_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # 新增一筆資料
            insert_query = f"INSERT INTO {tableName} (data_type, version, updated_at) VALUES (%s, %s, NOW());"
            cursor.execute(insert_query, (data_type, version))
            conn.commit()
            logger.info(insert_query, data_type, version)

            # 取得剛新增的資料（用自動產生的 id）
            last_id = cursor.lastrowid
            select_query = f"SELECT {selectField} FROM {tableName} WHERE id = %s;"
            cursor.execute(select_query, (last_id,))
            logger.info(select_query, last_id)
            row = cursor.fetchone()
            if row:
                return {
                    "is_success": True,
                    "result": {
                        "id": row["id"],
                        "data_type": row["data_type"],
                        "version": row["version"],
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

def update(id, version, updated_at):
    """更新設定版本

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 設定版本 }
    """

    if not id:
        raise ValueError("id 參數必填")
    conn = None
    try:
        conn = mysql.get_mysql_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            update_query = f"UPDATE {tableName} SET version = %s, updated_at = %s WHERE id = %s;"
            cursor.execute(update_query, (version, updated_at, id))
            logger.info(update_query, version, updated_at, id)
            conn.commit()

            # 取得更新後的資料
            select_query = f"SELECT {selectField} FROM {tableName} WHERE id = %s;"
            cursor.execute(select_query, (id,))
            logger.info(select_query, id)
            row = cursor.fetchone()
            if row:
                return {
                    "is_success": True,
                    "result": {
                        "id": row["id"],
                        "data_type": row["data_type"],
                        "version": row["version"],
                        "updated_at": str(row["updated_at"]),
                        "updated_at_timestamp": timestamp.datetime_str_to_timestamp(str(row["updated_at"])),
                        "created_at": str(row["created_at"]),
                        "created_at_timestamp": timestamp.datetime_str_to_timestamp(str(row["created_at"])),
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

def delete(id):
    """刪除設定版本

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 設定版本 }
    """

    if not id:
        raise ValueError("id 參數必填")
    conn = None
    try:
        conn = mysql.get_mysql_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            delete_query = f"DELETE FROM {tableName} WHERE id = %s;"
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

def deleteMany(ids):
    """刪除設定版本

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 設定版本 }
    """

    # 支援傳入逗號分隔字串或單一值
    if isinstance(ids, str):
        ids = [i.strip() for i in ids.split(',') if i.strip()]
    elif isinstance(ids, int):
        ids = [ids]
    elif not isinstance(ids, Sequence):
        raise ValueError("ids 參數型態錯誤")
    if not ids:
        raise ValueError("ids 參數不可為空")
    conn = None
    try:
        conn = mysql.get_mysql_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # 產生 SQL IN 條件
            format_strings = ','.join(['%s'] * len(ids))
            delete_query = f"DELETE FROM {tableName} WHERE id IN ({format_strings});"
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

