from utils import mysql
import pymysql
from common import timestamp
# from 主目錄.子目錄 import 檔名(py檔)

import logging
from collections.abc import Sequence
logger = logging.getLogger("flask.app")


tableName = 'sport_category'


selectField = f"id, item_id, option_id, sort_order, updated_at, created_at"
insertField = f"item_id, option_id, sort_order, updated_at, created_at"
insertValues = f"%s, %s, %s, NOW(), NOW()"


version_setting_data_type = 'getSportItemCategories'


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
        "item_id": row["item_id"],
        "option_id": row["option_id"],
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

def create(item_id, option_id, sort_order):
    """建立設定版本

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 設定版本 }
    """

    if not item_id:
        raise ValueError("item_id 參數必填")
    if not option_id:
        raise ValueError("option_id 參數必填")
    if not sort_order:
        sort_order = 0
    conn = None
    try:
        conn = mysql.get_mysql_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # 新增一筆資料
            insert_query = f"INSERT INTO {tableName} ({insertField}) VALUES ({insertValues});"
            logger.info(insert_query, item_id, option_id, sort_order)
            cursor.execute(insert_query, (item_id, option_id, sort_order))
            conn.commit()

            select_query = f"SELECT {selectField} FROM {tableName} WHERE item_id = %s AND option_id = %s;"
            logger.info(select_query, item_id, option_id)
            cursor.execute(select_query, (item_id, option_id))
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

def updateMany(ids):
    """更新多筆設定版本

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 設定版本 }
    """

    if not isinstance(ids, Sequence):
        raise ValueError("ids 參數型態錯誤")
    if not ids:
        raise ValueError("ids 參數不可為空")

    conn = None
    try:
        conn = mysql.get_mysql_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # 這邊需要 for loop 一筆一筆更新
            for id in ids:
                update_query = f"UPDATE {tableName} SET sort_order = %s, item_id = %s, option_id = %s, updated_at = NOW() WHERE id = %s;"
                logger.info(f"{update_query} {id['excel_sort_order']} {id['excel_item_id']} {id['excel_option_id']} {id['api_id']}")
                cursor.execute(update_query, (id['excel_sort_order'], id['excel_item_id'], id['excel_option_id'], id['api_id']))
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

def update(id, item_id, option_id, sort_order):
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
            update_query = f"UPDATE {tableName} SET item_id = %s, option_id = %s, sort_order = %s, updated_at = NOW() WHERE id = %s;"
            logger.info(update_query, item_id, option_id, sort_order, id)
            cursor.execute(update_query, (item_id, option_id, sort_order, id))
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
            return {"is_success": True, "result": {"data": {"id": f"{id}"}}}
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
                delete_query = f"DELETE FROM {tableName} WHERE `id` = %s;"
                logger.info(f"{delete_query} {id}")
                cursor.execute(delete_query, (id,))
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