from flask import Blueprint
from utils import mysql
# from 主目錄.子目錄 import 檔名(py檔)

bp = Blueprint('main', __name__)


@bp.route("/hello")
def say_hello():
    return "Hello from /hello route!"

@bp.route("/now_time")
def get_now_time():
    response = mysql.get_now_time()
    is_success = response["is_success"]
    result = response["result"]
    if(is_success == True):        
        return f"Hello! MySQL 現在時間：{result}"
    else:
        return result

