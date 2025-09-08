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
    # id 為 item_id-option_id 組合而成，需要拆解
    if id and '-' in id:
        item_id, option_id = id.split('-', 1)
    else:
        item_id, option_id = None, None
    response = query.get(item_id, option_id)
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

    response = query.create(item_id, option_id)
    return check_result.check_result(logger, filename, request.path, request.method, response, app_name)

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