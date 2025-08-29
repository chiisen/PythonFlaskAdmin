from flask import Blueprint, jsonify
from flask import request
# from 主目錄.子目錄 import 檔名(py檔)

import threading

import logging
logger = logging.getLogger("flask.app")


bp_posts = Blueprint('posts', __name__)


# 靜態全域快取變數
POSTS_CACHE = {
    "is_success": True,
    "result": {
        "data": [
            { "id": 1, "title": 'Hello', "body": 'World' },
            { "id": 2, "title": 'Foo', "body": 'Bar' }
        ],
        "total": 2
    }
}
POSTS_LOCK = threading.Lock()

@bp_posts.route("/posts/list", methods=["POST"])
def posts_list():
    """取得所有文章

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 文章列表 }
    """

    app_name = request.headers.get('appName')

    response = POSTS_CACHE.copy()

    is_success = response["is_success"]
    result = response["result"]
    if is_success:
        array = []
        for row in result["data"]:
            array.append({
                "id": row["id"],
                "title": row["title"],
                "body": row["body"]
            })
        json_format_result = {"data": array, "total": len(array)}
        logger.info(f"App: {app_name}, 取得文章列表成功: {result}")
        return jsonify(json_format_result)
    else:
        return result
    
@bp_posts.route("/posts/get", methods=["POST"])
def posts_get():
    """取得單筆文章

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 文章資料 }
    """

    # 從 request 取得 id
    data = request.get_json(force=True)
    post_id = data.get("id")

    # 從 POSTS_CACHE 中取得指定 id 的文章
    response = POSTS_CACHE.copy()
    is_success = response["is_success"]
    result = response["result"]
    # 過濾出指定 id 的資料
    filtered = next((post for post in result["data"] if str(post["id"]) == str(post_id)), None)
    if is_success:
        if filtered:
            json_format_result = {"data": filtered}
            return jsonify(json_format_result)
        else:
            return jsonify({"is_success": False, "result": "找不到指定 id 的資料"})
    else:
        return result
    
@bp_posts.route("/posts/create", methods=["POST"])
def posts_create():
    """建立文章

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 文章資料 }
    """

    # 從 request 取得 id, title, body
    data = request.get_json(force=True)
    title = data.get("title")
    body = data.get("body")

    # 檢查 title, body
    if not title or not body:
        return {"is_success": False, "result": "缺少必要參數"}

    new_id = None
    # 新增一筆資料到 POSTS_CACHE，需上鎖
    with POSTS_LOCK:
        # 取得目前最大 id
        posts = POSTS_CACHE["result"]["data"]
        max_id = max([post["id"] for post in posts], default=0)
        new_id = max_id + 1
        new_post = {"id": new_id, "title": title, "body": body}
        posts.append(new_post)
        POSTS_CACHE["result"]["total"] = len(posts)

    # 回傳剛剛建立的資料
    response = {
        "is_success": True,
        "result": {
            "data": new_post
        }
    }
    return jsonify(response["result"])
    
@bp_posts.route("/posts/update", methods=["POST"])
def posts_update():
    """更新文章

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 文章資料 }
    """

    # 從 request 取得 id, title, body
    data = request.get_json(force=True)
    post_id = data.get("id")
    title = data.get("title")
    body = data.get("body")

    if not post_id or not title or not body:
        return {"is_success": False, "result": "缺少必要參數"}

    updated_post = None
    with POSTS_LOCK:
        posts = POSTS_CACHE["result"]["data"]
        for post in posts:
            if post["id"] == post_id:
                post["title"] = title
                post["body"] = body
                updated_post = post
                break

    if updated_post:
        response = {
            "is_success": True,
            "result": {
                "data": [updated_post]
            }
        }
    else:
        response = {
            "is_success": False,
            "result": "找不到指定 id 的資料"
        }
    return jsonify(response["result"])

@bp_posts.route("/posts/delete", methods=["POST"])
def posts_delete():
    """刪除文章

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 文章資料 }
    """

    # 從 request 取得 id
    data = request.get_json(force=True)
    post_id = data.get("id")

    if not post_id:
        return {"is_success": False, "result": "缺少必要參數"}

    deleted_post = None
    with POSTS_LOCK:
        posts = POSTS_CACHE["result"]["data"]
        for i, post in enumerate(posts):
            if post["id"] == post_id:
                deleted_post = posts.pop(i)
                POSTS_CACHE["result"]["total"] = len(posts)
                break

    if deleted_post:
        response = {
            "is_success": True,
            "result": {
                "data": [deleted_post]
            }
        }
    else:
        response = {
            "is_success": False,
            "result": "找不到指定 id 的資料"
        }
    return jsonify(response["result"])

@bp_posts.route("/posts/deleteMany", methods=["POST"])
def posts_deleteMany():
    """刪除多筆文章

    Returns:
        _type_: { "is_success": 是否執行成功 True / False, "result": 文章列表 }
    """
     
    # 從 request 取得 ids (list)
    data = request.get_json(force=True)
    ids = data.get("ids")

    if not ids or not isinstance(ids, list):
        return {"is_success": False, "result": "缺少必要參數或格式錯誤，請傳入 ids 陣列"}

    deleted_posts = []
    with POSTS_LOCK:
        posts = POSTS_CACHE["result"]["data"]
        # 反向迭代刪除，避免 index 問題
        for post_id in sorted(ids, reverse=True):
            for i, post in enumerate(posts):
                if post["id"] == post_id:
                    deleted_posts.append(posts.pop(i))
                    break
        POSTS_CACHE["result"]["total"] = len(posts)

    if deleted_posts:
        response = {
            "is_success": True,
            "result": {
                "data": deleted_posts
            }
        }
    else:
        response = {
            "is_success": False,
            "result": "找不到指定 id 的資料"
        }
    return jsonify(response["result"])
