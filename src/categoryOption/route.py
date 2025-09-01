from flask import Blueprint, jsonify, request
from . import query
# from 主目錄.子目錄 import 檔名(py檔)


import logging
logger = logging.getLogger("flask.app")

routeName = 'categoryOption'

bp_categoryOption = Blueprint('categoryOption', __name__)


@bp_categoryOption.route(f"/{routeName}/list", methods=["POST"])
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

@bp_categoryOption.route(f"/{routeName}/get", methods=["POST"])
def get():
    """取得設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    id = request.json.get("id") if request.json else None  # 取得 id 參數

    response = query.get(id)
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

@bp_categoryOption.route(f"/{routeName}/create", methods=["POST"])
def create():
    """建立設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    group_id = request.json.get("group_id") if request.json else None  # 取得 group_id 參數
    name_key = request.json.get("name_key") if request.json else None  # 取得 name_key 參數
    description = request.json.get("description") if request.json else None  # 取得 description 參數
    sort_order = request.json.get("sort_order") if request.json else None  # 取得 sort_order 參數

    response = query.create(group_id, name_key, description, sort_order)
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

@bp_categoryOption.route(f"/{routeName}/update", methods=["POST"])
def update():
    """更新設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    id = request.json.get("id") if request.json else None  # 取得 id 參數
    data = request.json.get("data") if request.json else None  # 取得 data 參數

    name_key = data.get("name_key") if data and "name_key" in data else None  # 取得 name_key 參數
    description = data.get("description") if data and "description" in data else None  # 取得 description 參數
    sort_order = data.get("sort_order") if data and "sort_order" in data else None  # 取得 sort_order 參數
    updated_at = data.get("updated_at") if data and "updated_at" in data else None  # 取得 updated_at 參數

    response = query.update(id, name_key, description, sort_order, updated_at)
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

@bp_categoryOption.route(f"/{routeName}/delete", methods=["POST"])
def delete():
    """刪除設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    id = request.json.get("id") if request.json else None  # 取得 id 參數

    response = query.delete(id)
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

@bp_categoryOption.route(f"/{routeName}/deleteMany", methods=["POST"])
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