from flask import Blueprint, jsonify, request
from . import query
# from 主目錄.子目錄 import 檔名(py檔)


import logging
logger = logging.getLogger("flask.app")

routeName = 'i18nText'

bp_i18nText = Blueprint(routeName, __name__)


@bp_i18nText.route(f"/{routeName}/list", methods=["POST"])
def list():
    """取得設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    sort = request.json.get("sort") if request.json else None  # 取得 sort 參數
    pagination = request.json.get("pagination") if request.json else None  # 取得 pagination 參數

    response = query.list(sort, pagination)
    is_success = response["is_success"]
    result = response["result"]
    if(is_success == True):
        json_format_result = {"data": result["data"], "total": result["total"]}
        json_result = jsonify(json_format_result)
        logger.info(f"App: {app_name}, 取得成功: {result}")
        return json_result
    else:
        json_format_result = {"data": [], "total": 0}
        error_result = jsonify({ "error": result })
        json_result = jsonify(json_format_result)
        logger.error(f"App: {app_name}, 取得失敗: {error_result}")
        return json_result

@bp_i18nText.route(f"/{routeName}/get", methods=["POST"])
def get():
    """取得設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    id = request.json.get("id") if request.json else None  # 取得 id 參數
    # id 為 key-lang 組合而成，需要拆解
    if id and '-' in id:
        key, lang = id.split('-', 1)
    else:
        key, lang = None, None

    response = query.get(key, lang)
    is_success = response["is_success"]
    result = response["result"]
    if(is_success == True):
        json_format_result = {"data": result}
        json_result = jsonify(json_format_result)
        logger.info(f"App: {app_name}, 取得成功: {result}")
        return json_result
    else:
        json_format_result = {"data": []}
        error_result = jsonify({ "error": result })
        json_result = jsonify(json_format_result)
        logger.error(f"App: {app_name}, 取得失敗: {error_result}")
        return json_result

@bp_i18nText.route(f"/{routeName}/create", methods=["POST"])
def create():
    """建立設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    key = request.json.get("key") if request.json else None  # 取得 key 參數
    lang = request.json.get("lang") if request.json else None  # 取得 lang 參數
    text = request.json.get("text") if request.json else None  # 取得 text 參數

    response = query.create(key, lang, text)
    is_success = response["is_success"]
    result = response["result"]
    if(is_success == True):
        json_format_result = {"data": result}
        json_result = jsonify(json_format_result)
        logger.info(f"App: {app_name}, 建立成功: {result}")
        return json_result
    else:
        json_format_result = {"data": []}
        error_result = jsonify({ "error": result })
        json_result = jsonify(json_format_result)
        logger.error(f"App: {app_name}, 建立失敗: {error_result}")
        return json_result

@bp_i18nText.route(f"/{routeName}/update", methods=["POST"])
def update():
    """更新設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    id = request.json.get("id") if request.json else None  # 取得 id 參數
    # id 為 key-lang 組合而成，需要拆解
    if id and '-' in id:
        key, lang = id.split('-', 1)
    else:
        key, lang = None, None
    data = request.json.get("data") if request.json else None  # 取得 data 參數
    text = data.get("text") if data and "text" in data else None  # 取得 text 參數
    updated_at = data.get("updated_at") if data and "updated_at" in data else None  # 取得 updated_at 參數

    response = query.update(key, lang, text, updated_at)
    is_success = response["is_success"]
    result = response["result"]
    if(is_success == True):
        json_format_result = {"data": result}
        json_result = jsonify(json_format_result)
        logger.info(f"App: {app_name}, 更新成功: {result}")
        return json_result
    else:
        json_format_result = {"data": []}
        error_result = jsonify({ "error": result })
        json_result = jsonify(json_format_result)
        logger.error(f"App: {app_name}, 更新失敗: {error_result}")
        return json_result

@bp_i18nText.route(f"/{routeName}/delete", methods=["POST"])
def delete():
    """刪除設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    id = request.json.get("id") if request.json else None  # 取得 id 參數
    # id 為 key-lang 組合而成，需要拆解
    if id and '-' in id:
        key, lang = id.split('-', 1)
    else:
        key, lang = None, None

    response = query.delete(key, lang)
    is_success = response["is_success"]
    result = response["result"]
    if(is_success == True):
        json_format_result = {"data": result}
        json_result = jsonify(json_format_result)
        logger.info(f"App: {app_name}, 刪除成功: {result}")
        return json_result
    else:
        json_format_result = {"data": []}
        error_result = jsonify({ "error": result })
        json_result = jsonify(json_format_result)
        logger.error(f"App: {app_name}, 刪除失敗: {error_result}")
        return json_result

@bp_i18nText.route(f"/{routeName}/deleteMany", methods=["POST"])
def deleteMany():
    """刪除設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    ids = request.json.get("ids") if request.json else None  # 取得 ids 參數

    response = query.deleteMany(ids)
    is_success = response["is_success"]
    result = response["result"]
    if(is_success == True):
        json_format_result = {"data": result}
        json_result = jsonify(json_format_result)
        logger.info(f"App: {app_name}, 刪除成功: {result}")
        return json_result
    else:
        json_format_result = {"data": []}
        error_result = jsonify({ "error": result })
        json_result = jsonify(json_format_result)
        logger.error(f"App: {app_name}, 刪除失敗: {error_result}")
        return json_result