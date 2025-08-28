from flask import Blueprint, jsonify, request
from utils import mysql
# from 主目錄.子目錄 import 檔名(py檔)


import logging
logger = logging.getLogger("flask.app")


bp_settings = Blueprint('settings', __name__)


@bp_settings.route("/getSettingVersion", methods=["POST"])
def get_setting_version():
    """取得設定版本

    Returns:
        _type_: 回傳版本資訊
    """

    data_type = request.json.get("data_type") if request.json else None  # 取得 data_type 參數

    response = mysql.get_setting_version(data_type)
    is_success = response["is_success"]
    result = response["result"]
    if(is_success == True):
        return jsonify(result)
    else:
        return result