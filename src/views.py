from flask import Blueprint, jsonify
from utils import mysql
# from 主目錄.子目錄 import 檔名(py檔)


import logging
logger = logging.getLogger("flask.app")


bp_views = Blueprint('views', __name__)


@bp_views.route("/hello", methods=["GET"])
def say_hello():
    """說 hello 的路由

    Returns:
        _type_: 回傳路由 /hello 的訊息
    """

    return "Hello from /hello route!"

@bp_views.route("/now_time", methods=["GET"])
def get_now_time():
    """取得目前時間

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 目前時間 }
    """

    response = mysql.get_now_time()
    is_success = response["is_success"]
    result = response["result"]
    if(is_success == True):        
        return f"Hello! MySQL 現在時間：{result}"
    else:
        return result

@bp_views.route("/posts", methods=["GET"])
def get_posts():
    """取得所有文章

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 文章列表 }
    """

    response = {
        "is_success": True,
        "result": [
                    { "id": 1, "title": 'Hello', "body": 'World' },
                    { "id": 2, "title": 'Foo', "body": 'Bar' }
                ]
    }
    is_success = response["is_success"]
    result = response["result"]
    if(is_success == True):
        return jsonify(result)
    else:
        return result
