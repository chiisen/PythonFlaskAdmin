from flask import Blueprint, request
from . import query
# from 主目錄.子目錄 import 檔名(py檔)


import os
filename = os.path.basename(__file__)


import logging
logger = logging.getLogger("flask.app")

routeName = 'sportItem'

bp_sportItem = Blueprint(routeName, __name__)


from utils import check_result


@bp_sportItem.route(f"/{routeName}/list", methods=["POST"])
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
    
@bp_sportItem.route(f"/{routeName}/get", methods=["POST"])
def get():
    """取得設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    id = request.json.get("id") if request.json else None  # 取得 id 參數

    response = query.get(id)
    return check_result.check_result(logger, filename, request.path, request.method, response, app_name)
    
@bp_sportItem.route(f"/{routeName}/create", methods=["POST"])
def create():
    """建立設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    name_key = request.json.get("name_key") if request.json else None  # 取得 name_key 參數
    description = request.json.get("description") if request.json else None  # 取得 description 參數
    link_type = request.json.get("link_type") if request.json else None  # 取得 link_type 參數
    link_sub_type = request.json.get("link_sub_type") if request.json else None  # 取得 link_sub_type 參數

    response = query.create(name_key, description, link_type, link_sub_type)
    return check_result.check_result(logger, filename, request.path, request.method, response, app_name)
    
@bp_sportItem.route(f"/{routeName}/update", methods=["POST"])
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
    link_type = data.get("link_type") if data and "link_type" in data else None  # 取得 link_type 參數
    link_sub_type = data.get("link_sub_type") if data and "link_sub_type" in data else None  # 取得 link_sub_type 參數
    updated_at = data.get("updated_at") if data and "updated_at" in data else None  # 取得 updated_at 參數

    response = query.update(id, name_key, description, link_type, link_sub_type, updated_at)
    return check_result.check_result(logger, filename, request.path, request.method, response, app_name)

@bp_sportItem.route(f"/{routeName}/delete", methods=["POST"])
def delete():
    """刪除設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    id = request.json.get("id") if request.json else None  # 取得 id 參數

    response = query.delete(id)
    return check_result.check_result(logger, filename, request.path, request.method, response, app_name)
    
@bp_sportItem.route(f"/{routeName}/deleteMany", methods=["POST"])
def deleteMany():
    """刪除設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    ids = request.json.get("ids") if request.json else None  # 取得 ids 參數

    response = query.deleteMany(ids)
    return check_result.check_result(logger, filename, request.path, request.method, response, app_name)