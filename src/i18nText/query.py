from utils import mysql
import pymysql
import datetime
# from 主目錄.子目錄 import 檔名(py檔)

import logging
from collections.abc import Sequence
logger = logging.getLogger("flask.app")


tableName = 'i18n_text'

# key 是 MySQL 保留字，要加上反引號
selectField = f"`id`,`key`, lang, text, updated_at, created_at"
insertField = f"`key`, lang, text, updated_at, created_at"
insertValues = f"%s, %s, %s, NOW(), NOW()"

def get_sort_field(sort_field):
    """處理排序欄位，
    將 id 轉為 key，因為 id 為 key 更名，因為前端只讀 id
    """
    
    if sort_field == "id" or sort_field == "key":
        return "`key`" # key 是 MySQL 保留字，要加上反引號
    return sort_field

def format_result(row):
    """格式化 result

    Returns:
        _type_: { "result": 設定資料 }
    """

    if not row:
        return None
    return {
        "id": row["id"],
        "key": row["key"],
        "lang": row["lang"],
        "text": row["text"],
        "updated_at": str(row["updated_at"]),
        "created_at": str(row["created_at"]),
    }

def list(sort, pagination, lang):
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
                if not lang:
                    query = f"SELECT {selectField} FROM {tableName} ORDER BY updated_at DESC LIMIT %s OFFSET %s;"
                    query_args = (per_page, offset)
                else:
                    query = f"SELECT {selectField} FROM {tableName} WHERE lang = %s ORDER BY updated_at DESC LIMIT %s OFFSET %s;"
                    query_args = (lang, per_page, offset)
            else:
                sort_field = get_sort_field(sort['field'])
                order_field = sort['order']
                if not lang:
                    query = f"SELECT {selectField} FROM {tableName} ORDER BY {sort_field} {order_field} LIMIT %s OFFSET %s;"
                    query_args = (per_page, offset)
                else:
                    query = f"SELECT {selectField} FROM {tableName} WHERE lang = %s ORDER BY {sort_field} {order_field} LIMIT %s OFFSET %s;"
                    query_args = (lang, per_page, offset)

            logger.info(query)
            cursor.execute(query, query_args)

            rows = cursor.fetchall()
            # 查詢總筆數
            count_query = f"SELECT COUNT(*) as total FROM {tableName};"
            logger.info(count_query)
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
            query = f"SELECT {selectField} FROM {tableName} WHERE `id` = %s;"
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

def create(key, lang, text):
    """建立設定版本

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 設定版本 }
    """

    if not key:
        raise ValueError("key 參數必填")
    # description 說明可以不用填
    if not lang:
        raise ValueError("lang 參數必填")
    if not text:
        raise ValueError("text 參數必填")
    conn = None
    try:
        conn = mysql.get_mysql_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # 新增一筆資料
            insert_query = f"INSERT INTO {tableName} ({insertField}) VALUES ({insertValues});"
            logger.info(insert_query, key, lang, text)
            cursor.execute(insert_query, (key, lang, text))
            conn.commit()            

            select_query = f"SELECT {selectField} FROM {tableName} WHERE `key` = %s;"
            logger.info(select_query, key)
            cursor.execute(select_query, (key,))
            row = cursor.fetchone()
            if row:
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

def update(id, text):
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
            update_query = f"UPDATE {tableName} SET text = %s, updated_at = %s WHERE `id` = %s;"
            # updated_at 一律更新為目前時間
            updated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logger.info(update_query, text, updated_at, id)
            cursor.execute(update_query, (text, updated_at, id))
            conn.commit()

            # 取得更新後的資料
            select_query = f"SELECT {selectField} FROM {tableName} WHERE `id` = %s;"
            logger.info(select_query, id)
            cursor.execute(select_query, (id,))
            row = cursor.fetchone()
            if row:
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
            delete_query = f"DELETE FROM {tableName} WHERE `id` = %s;"
            logger.info(delete_query, id)
            cursor.execute(delete_query, (id,))
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
    elif not isinstance(ids, Sequence):
        raise ValueError("ids 參數型態錯誤")
    if not ids:
        raise ValueError("ids 參數不可為空")
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

