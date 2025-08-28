from flask import Blueprint, jsonify
from utils import mysql
# from 主目錄.子目錄 import 檔名(py檔)


import logging
logger = logging.getLogger("flask.app")


bp_posts = Blueprint('posts', __name__)


@bp_posts.route("/posts/list", methods=["POST"])
def posts_list():
    """取得所有文章

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 文章列表 }
    """

    response = {
        "is_success": True,
        "result": {
            "data": [
                { "id": 1, "title": 'Hello', "body": 'World' },
                { "id": 2, "title": 'Foo', "body": 'Bar' }
            ],
            "total": 2
        }
    }
    is_success = response["is_success"]
    result = response["result"]
    if(is_success == True):
        return jsonify(result)
    else:
        return result
    
@bp_posts.route("/posts/get", methods=["POST"])
def posts_get(id):
    """取得所有文章

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 文章列表 }
    """

    # SELECT 指定的文章 id
    response = {
        "is_success": True,
        "result": {
            "data": [
                { "id": 1, "title": 'Hello', "body": 'World' }
            ]
        }
    }
    is_success = response["is_success"]
    result = response["result"]
    if(is_success == True):
        return jsonify(result)
    else:
        return result
    
@bp_posts.route("/posts/create", methods=["POST"])
def posts_create(title, body):
    """取得所有文章

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 文章列表 }
    """

    # 檢查 title, body
    if not title or not body:
        return {"is_success": False, "result": "缺少必要參數"}

    # INSERT 新建一筆資料
    # SELECT 剛剛建立那筆資料
    response = {
        "is_success": True,
        "result": {
            "data": [
                { "id": 1, "title": 'Hello', "body": 'World' }
            ]
        }
    }
    is_success = response["is_success"]
    result = response["result"]
    if(is_success == True):
        return jsonify(result)
    else:
        return result
    
@bp_posts.route("/posts/update", methods=["POST"])
def posts_update():
    """取得所有文章

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 文章列表 }
    """

    response = {
        "is_success": True,
        "result": {
            "data": [
                { "id": 1, "title": 'Hello', "body": 'World' },
                { "id": 2, "title": 'Foo', "body": 'Bar' }
            ]
        }
    }
    is_success = response["is_success"]
    result = response["result"]
    if(is_success == True):
        return jsonify(result)
    else:
        return result

@bp_posts.route("/posts/delete", methods=["POST"])
def posts_delete():
    """取得所有文章

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 文章列表 }
    """

    response = {
        "is_success": True,
        "result": {
            "data": [
                { "id": 1, "title": 'Hello', "body": 'World' },
                { "id": 2, "title": 'Foo', "body": 'Bar' }
            ]
        }
    }
    is_success = response["is_success"]
    result = response["result"]
    if(is_success == True):
        return jsonify(result)
    else:
        return result