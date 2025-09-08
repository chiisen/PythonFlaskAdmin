from flask import Blueprint, request
from . import query
# from 主目錄.子目錄 import 檔名(py檔)


import os
filename = os.path.basename(__file__)


import logging
logger = logging.getLogger("flask.app")

routeName = 'settingVersion'

bp_settingVersion = Blueprint(routeName, __name__)


from utils import check_result


@bp_settingVersion.route(f"/{routeName}/list", methods=["POST"])
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
    
@bp_settingVersion.route(f"/{routeName}/get", methods=["POST"])
def get():
    """取得設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    id = request.json.get("id") if request.json else None  # 取得 id 參數

    response = query.get(id)
    return check_result.check_result(logger, filename, request.path, request.method, response, app_name)
    
@bp_settingVersion.route(f"/{routeName}/create", methods=["POST"])
def create():
    """建立設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    data_type = request.json.get("data_type") if request.json else None  # 取得 data_type 參數
    version = request.json.get("version") if request.json else None  # 取得 version 參數

    response = query.create(data_type, version)
    return check_result.check_result(logger, filename, request.path, request.method, response, app_name)
    
@bp_settingVersion.route(f"/{routeName}/update", methods=["POST"])
def update():
    """更新設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    id = request.json.get("id") if request.json else None  # 取得 id 參數(因為 id 必填，但是不允許修改，所以不放在 data 裡面)    
    data = request.json.get("data") if request.json else None  # 取得 data 參數
    
    version = data.get("version") if data and "version" in data else None  # 取得 version 參數
    updated_at = data.get("updated_at") if data and "updated_at" in data else None  # 取得 updated_at 參數

    response = query.update(id, version, updated_at)
    return check_result.check_result(logger, filename, request.path, request.method, response, app_name)

@bp_settingVersion.route(f"/{routeName}/delete", methods=["POST"])
def delete():
    """刪除設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    id = request.json.get("id") if request.json else None  # 取得 id 參數

    response = query.delete(id)
    return check_result.check_result(logger, filename, request.path, request.method, response, app_name)
    
@bp_settingVersion.route(f"/{routeName}/deleteMany", methods=["POST"])
def deleteMany():
    """刪除設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    ids = request.json.get("ids") if request.json else None  # 取得 ids 參數

    response = query.deleteMany(ids)
    return check_result.check_result(logger, filename, request.path, request.method, response, app_name)