from flask import Blueprint, request
from . import query
# from 主目錄.子目錄 import 檔名(py檔)


import os
filename = os.path.basename(__file__)


import logging
logger = logging.getLogger("flask.app")

routeName = 'sportCategory'

bp_sportCategory = Blueprint(routeName, __name__)


from utils import check_result


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
    return check_result.check_result(logger, filename, request.path, request.method, response, app_name)

@bp_sportCategory.route(f"/{routeName}/get", methods=["POST"])
def get():
    """取得設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    id = request.json.get("id") if request.json else None  # 取得 id 參數
    response = query.get(id)
    return check_result.check_result(logger, filename, request.path, request.method, response, app_name)

@bp_sportCategory.route(f"/{routeName}/create", methods=["POST"])
def create():
    """建立設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    item_id = request.json.get("item_id") if request.json else None  # 取得 item_id 參數
    option_id = request.json.get("option_id") if request.json else None  # 取得 option_id 參數
    sort_order = request.json.get("sort_order") if request.json else None  # 取得 sort_order 參數

    response = query.create(item_id, option_id, sort_order)
    return check_result.check_result(logger, filename, request.path, request.method, response, app_name)

@bp_sportCategory.route(f"/{routeName}/update", methods=["POST"])
def update():
    """更新設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    id = request.json.get("id") if request.json else None  # 取得 id 參數
    data = request.json.get("data") if request.json else None  # 取得 data 參數
    previousData = request.json.get("previousData") if request.json else None  # 取得 previousData 參數

    item_id = previousData.get("item_id") if previousData and "item_id" in previousData else None  # 取得 item_id 參數
    option_id = data.get("option_id") if data and "option_id" in data else None  # 取得 option_id 參數

    sort_order = data.get("sort_order") if data and "sort_order" in data else None  # 取得 sort_order 參數

    response = query.update(id, item_id, option_id, sort_order)
    return check_result.check_result(logger, filename, request.path, request.method, response, app_name)

@bp_sportCategory.route(f"/{routeName}/updateMany", methods=["POST"])
def updateMany():
    """更新多筆設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    ids = request.json.get("ids") if request.json else None  # 取得 ids 參數
    data = request.json.get("data") if request.json else None  # 取得 data 參數

    sort_order = data.get("sort_order") if data and "sort_order" in data else None  # 取得 sort_order 參數

    response = query.updateMany(ids, sort_order)
    return check_result.check_result(logger, filename, request.path, request.method, response, app_name)

@bp_sportCategory.route(f"/{routeName}/delete", methods=["POST"])
def delete():
    """刪除設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    id = request.json.get("id") if request.json else None  # 取得 id 參數

    response = query.delete(id)
    return check_result.check_result(logger, filename, request.path, request.method, response, app_name)
    
@bp_sportCategory.route(f"/{routeName}/deleteMany", methods=["POST"])
def deleteMany():
    """刪除設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    ids = request.json.get("ids") if request.json else None  # 取得 ids 參數

    response = query.deleteMany(ids)
    return check_result.check_result(logger, filename, request.path, request.method, response, app_name)