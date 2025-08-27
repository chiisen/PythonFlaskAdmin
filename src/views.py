from flask import Blueprint
import pymysql
from dotenv import load_dotenv
import os

bp = Blueprint('main', __name__)

# 載入 .env 檔案
load_dotenv()

def get_mysql_connection():
    host = os.getenv('DB_HOST')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    db = os.getenv('DB_NAME')
    print(f"host={host}, user={user}, password={password}, db={db}")  # 除錯用

    # 檢查必要的環境變量是否存在
    if not host or not user or not password or not db:
        raise ValueError("資料庫連線資訊缺少，請檢查 .env 檔案設定")

    return pymysql.connect(
        host=host,
        user=user,
        password=password,
        db=db,
        charset='utf8mb4'
    )

@bp.route("/hello")
def say_hello():
    return "Hello from /hello route!"

@bp.route("/now_time")
def get_now_time():
    conn = None
    try:
        conn = get_mysql_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT NOW() AS now_time;")
            result = cursor.fetchone()
            if result:
                return f"Hello! MySQL 現在時間：{result['now_time']}"
            else:
                return "無法獲取數據庫時間"
    except Exception as e:
        return f"連線失敗: {e}"
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass