from flask import Blueprint, jsonify, request
from utils import mysql
# from 主目錄.子目錄 import 檔名(py檔)


import logging
logger = logging.getLogger("flask.app")


bp_settingVersion = Blueprint('settingVersion', __name__)


@bp_settingVersion.route("/settingVersion/list", methods=["POST"])
def setting_version_list():
    """取得設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    data_type = request.json.get("data_type") if request.json else None  # 取得 data_type 參數

    response = mysql.get_setting_version(data_type)
    is_success = response["is_success"]
    result = response["result"]
    if(is_success == True):
        json_format_result = {"data": result, "total": len(result)}
        json_result = jsonify(json_format_result)
        logger.info(f"App: {app_name}, 取得設定版本成功: {result}")
        return json_result
    else:
        json_format_result = {"data": [], "total": 0}
        error_result = jsonify({ "error": result })
        json_result = jsonify(json_format_result)
        logger.error(f"App: {app_name}, 取得設定版本失敗: {error_result}")
        return json_result
    
@bp_settingVersion.route("/settingVersion/get", methods=["POST"])
def setting_version_get():
    """取得設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    data_type = request.json.get("data_type") if request.json else None  # 取得 data_type 參數

    response = mysql.get_setting_version(data_type)
    is_success = response["is_success"]
    result = response["result"]
    if(is_success == True):
        json_format_result = {"data": result}
        json_result = jsonify(json_format_result)
        logger.info(f"App: {app_name}, 取得設定版本成功: {result}")
        return json_result
    else:
        json_format_result = {"data": []}
        error_result = jsonify({ "error": result })
        json_result = jsonify(json_format_result)
        logger.error(f"App: {app_name}, 取得設定版本失敗: {error_result}")
        return json_result
    
@bp_settingVersion.route("/settingVersion/create", methods=["POST"])
def setting_version_create():
    """建立設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    data_type = request.json.get("data_type") if request.json else None  # 取得 data_type 參數

    response = mysql.get_setting_version(data_type)
    is_success = response["is_success"]
    result = response["result"]
    if(is_success == True):
        json_format_result = {"data": result}
        json_result = jsonify(json_format_result)
        logger.info(f"App: {app_name}, 取得設定版本成功: {result}")
        return json_result
    else:
        json_format_result = {"data": []}
        error_result = jsonify({ "error": result })
        json_result = jsonify(json_format_result)
        logger.error(f"App: {app_name}, 取得設定版本失敗: {error_result}")
        return json_result
    
@bp_settingVersion.route("/settingVersion/update", methods=["POST"])
def setting_version_update():
    """更新設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    data_type = request.json.get("data_type") if request.json else None  # 取得 data_type 參數

    response = mysql.get_setting_version(data_type)
    is_success = response["is_success"]
    result = response["result"]
    if(is_success == True):
        json_format_result = {"data": result}
        json_result = jsonify(json_format_result)
        logger.info(f"App: {app_name}, 取得設定版本成功: {result}")
        return json_result
    else:
        json_format_result = {"data": []}
        error_result = jsonify({ "error": result })
        json_result = jsonify(json_format_result)
        logger.error(f"App: {app_name}, 取得設定版本失敗: {error_result}")
        return json_result

@bp_settingVersion.route("/settingVersion/delete", methods=["POST"])
def setting_version_delete():
    """刪除設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    app_name = request.headers.get('appName')

    data_type = request.json.get("data_type") if request.json else None  # 取得 data_type 參數

    response = mysql.get_setting_version(data_type)
    is_success = response["is_success"]
    result = response["result"]
    if(is_success == True):
        json_format_result = {"data": result}
        json_result = jsonify(json_format_result)
        logger.info(f"App: {app_name}, 取得設定版本成功: {result}")
        return json_result
    else:
        json_format_result = {"data": []}
        error_result = jsonify({ "error": result })
        json_result = jsonify(json_format_result)
        logger.error(f"App: {app_name}, 取得設定版本失敗: {error_result}")
        return json_result