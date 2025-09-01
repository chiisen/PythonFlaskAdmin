from flask import Blueprint, jsonify, request
from . import query
# from 主目錄.子目錄 import 檔名(py檔)


import logging
logger = logging.getLogger("flask.app")

routeName = 'sportCategory'

bp_sportCategory = Blueprint('sportCategory', __name__)


@bp_sportCategory.route(f"/{routeName}/list", methods=["POST"])
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

@bp_sportCategory.route(f"/{routeName}/get", methods=["POST"])
def get():
    """取得設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    id = request.json.get("id") if request.json else None  # 取得 id 參數
    # id 為 item_id-option_id 組合而成，需要拆解
    if id and '-' in id:
        item_id, option_id = id.split('-', 1)
    else:
        item_id, option_id = None, None
    response = query.get(item_id, option_id)
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

@bp_sportCategory.route(f"/{routeName}/create", methods=["POST"])
def create():
    """建立設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    item_id = request.json.get("item_id") if request.json else None  # 取得 item_id 參數
    option_id = request.json.get("option_id") if request.json else None  # 取得 option_id 參數

    response = query.create(item_id, option_id)
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

@bp_sportCategory.route(f"/{routeName}/delete", methods=["POST"])
def delete():
    """刪除設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    id = request.json.get("id") if request.json else None  # 取得 id 參數

    # id 為 item_id-option_id 組合而成，需要拆解
    if id and '-' in id:
        item_id, option_id = id.split('-', 1)
    else:
        item_id, option_id = None, None
    response = query.delete(item_id, option_id)
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
    
@bp_sportCategory.route(f"/{routeName}/deleteMany", methods=["POST"])
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