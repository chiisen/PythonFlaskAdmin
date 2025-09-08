import json
from flask import Response

def check_result(logger, filename, path, method, response, app_name):
    """處理查詢結果

    Args:
        response (dict): 查詢結果

    Returns:
        Response: 回傳的 HTTP 回應
    """
    is_success = response["is_success"]
    result = response["result"]
    if isinstance(result, dict):
        if is_success == True:
            json_result = {
                k: v for k, v in [
                    ("data", result.get("data")), 
                    ("total", result.get("total")), 
                    ("id", result.get("id")), 
                    ("ids", result.get("ids"))
                ] if v is not None
            }
            resp = json.dumps(json_result, ensure_ascii=False)
            logger.debug(f"[{filename}][{path}][{method}] App: {app_name}, 成功: {json_result}")
        else:
            json_result = {
                k: v for k, v in [
                    ("data", result.get("data")), 
                    ("total", result.get("total")), 
                    ("id", result.get("id")), 
                    ("ids", result.get("ids")),
                    ("error", result.get("error"))
                ] if v is not None
            }
            resp = json.dumps(json_result, ensure_ascii=False)
            logger.warning(f"[{filename}][{path}][{method}] App: {app_name}, 失敗: {json_result}")
    else:
        # result 不是 dict，直接包成 data
        if is_success == True:
            json_result = {"data": result}
            resp = json.dumps(json_result, ensure_ascii=False)
            logger.debug(f"[{filename}][{path}][{method}] App: {app_name}, 成功: {json_result}")
        else:
            json_result = {"data": [], "error": result}
            resp = json.dumps(json_result, ensure_ascii=False)
            logger.warning(f"[{filename}][{path}][{method}] App: {app_name}, 失敗: {json_result}")

    return Response(resp, status=200, mimetype='application/json')