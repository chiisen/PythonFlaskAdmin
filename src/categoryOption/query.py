from utils import mysql
import pymysql
from common import timestamp
# from 主目錄.子目錄 import 檔名(py檔)

import logging
from collections.abc import Sequence
logger = logging.getLogger("flask.app")


tableName = 'category_option'

selectField = f"id, group_id, name_key, description, sort_order, updated_at, created_at"
insertField = f"group_id, name_key, description, sort_order, updated_at, created_at"
insertValues = f"%s, %s, %s, %s, NOW(), NOW()"


version_setting_data_type = 'getCategoryOptionsList'


def get_sort_field(sort_field):
    """處理排序欄位，
    id 不做轉換
    """
    
    if sort_field == "id":
        return "id"
    return sort_field

def format_result(row):
    """格式化 result

    Returns:
        _type_: { "result": 設定資料 }
    """

    if not row:
        return None
    return {
        "id": row["id"], # 前端 React Admin 需要 id 欄位來顯示序號
        "group_id": row["group_id"],
        "name_key": row["name_key"],
        "description": row["description"],
        "sort_order": row["sort_order"],
        "updated_at": str(row["updated_at"]),
        "updated_at_timestamp": timestamp.datetime_str_to_timestamp(str(row["updated_at"])),
        "created_at": str(row["created_at"]),
        "created_at_timestamp": timestamp.datetime_str_to_timestamp(str(row["created_at"])),
    }

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
                sort_field = get_sort_field(sort['field'])
                query = f"SELECT {selectField} FROM {tableName} ORDER BY {sort_field} {sort['order']} LIMIT %s OFFSET %s;"
                query_args = (per_page, offset)

            logger.info(f"{query} {query_args}")
            cursor.execute(query, query_args)

            rows = cursor.fetchall()
            # 查詢總筆數
            count_query = f"SELECT COUNT(*) as total FROM {tableName};"
            cursor.execute(count_query)
            count_row = cursor.fetchone()
            total = count_row["total"] if count_row else 0

            if rows:
                array = [format_result(row) for row in rows]
                return {"is_success": True, "result": {"data": array, "total": total}}
            else:
                return {"is_success": False, "result": "無法獲取設定"}
    except Exception as e:
        logger.exception("Exception")
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
            logger.info(query, id)
            cursor.execute(query, (id,))

            row = cursor.fetchone()
            if row:
                return {"is_success": True, "result": {"data": format_result(row)}}
            else:
                return {"is_success": False, "result": "無法獲取設定"}
    except Exception as e:
        logger.exception("Exception")
        return {"is_success": False, "result": f"連線失敗: {e}"}
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

def create(group_id, name_key, description, sort_order):
    """建立設定版本

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 設定版本 }
    """

    if not group_id:
        raise ValueError("group_id 參數必填")
    if not name_key:
        raise ValueError("name_key 參數必填")
    # description 說明可以不用填
    if not sort_order:
        raise ValueError("sort_order 參數必填")
    conn = None
    try:
        conn = mysql.get_mysql_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # 新增一筆資料
            insert_query = f"INSERT INTO {tableName} ({insertField}) VALUES ({insertValues});"
            logger.info(insert_query, group_id, name_key, description, sort_order)
            cursor.execute(insert_query, (group_id, name_key, description, sort_order))
            conn.commit()

            # 取得剛新增的資料（用自動產生的 id）
            last_id = cursor.lastrowid
            select_query = f"SELECT {selectField} FROM {tableName} WHERE id = %s;"
            logger.info(select_query, last_id)
            cursor.execute(select_query, (last_id,))
            row = cursor.fetchone()
            if row:
                # 這邊還要更新 setting_versions 的 updated_at 時間
                update_query = f"UPDATE setting_versions SET updated_at = NOW() WHERE data_type = %s;"
                logger.info(update_query, version_setting_data_type)
                cursor.execute(update_query, (version_setting_data_type,))
                conn.commit()
                return {"is_success": True, "result": {"data": format_result(row)}}
            else:
                return {"is_success": False, "result": "無法獲取新增後的設定版本"}
    except Exception as e:
        logger.exception("Exception")
        return {"is_success": False, "result": f"連線失敗: {e}"}
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

def update(id, name_key, description, sort_order):
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
            update_query = f"UPDATE {tableName} SET name_key = %s, description = %s, sort_order = %s, updated_at = NOW() WHERE id = %s;"
            logger.info(update_query, name_key, description, sort_order, id)
            cursor.execute(update_query, (name_key, description, sort_order, id))
            conn.commit()

            # 取得更新後的資料
            select_query = f"SELECT {selectField} FROM {tableName} WHERE id = %s;"
            logger.info(select_query, id)
            cursor.execute(select_query, (id,))
            row = cursor.fetchone()
            if row:
                # 這邊還要更新 setting_versions 的 updated_at 時間
                update_query = f"UPDATE setting_versions SET updated_at = NOW() WHERE data_type = %s;"
                logger.info(update_query, version_setting_data_type)
                cursor.execute(update_query, (version_setting_data_type,))
                conn.commit()
                return {"is_success": True, "result": {"data": format_result(row)}}
            else:
                return {"is_success": False, "result": "無法獲取更新後的設定"}
    except Exception as e:
        logger.exception("Exception")
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
            logger.info(delete_query, id)
            cursor.execute(delete_query, (id,))
            conn.commit()

            # 這邊還要更新 setting_versions 的 updated_at 時間
            update_query = f"UPDATE setting_versions SET updated_at = NOW() WHERE data_type = %s;"
            logger.info(update_query, version_setting_data_type)
            cursor.execute(update_query, (version_setting_data_type,))
            conn.commit()
            
            return {"is_success": True, "result": {"data": {"id": id}}}
    except Exception as e:
        logger.exception("Exception")
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
            logger.info(delete_query, ids)
            cursor.execute(delete_query, tuple(ids))
            conn.commit()

            # 這邊還要更新 setting_versions 的 updated_at 時間
            update_query = f"UPDATE setting_versions SET updated_at = NOW() WHERE data_type = %s;"
            logger.info(update_query, version_setting_data_type)
            cursor.execute(update_query, (version_setting_data_type,))
            conn.commit()

            return {"is_success": True, "result": {"data": ids}}
    except Exception as e:
        logger.exception("Exception")
        return {"is_success": False, "result": f"連線失敗: {e}"}
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

