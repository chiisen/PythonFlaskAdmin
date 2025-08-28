from flask import Flask
from flask_cors import CORS

import os
import logging
from datetime import datetime

# 建立 log 目錄（如果不存在）
log_dir = "log"
os.makedirs(log_dir, exist_ok=True)

log_filename = os.path.join(log_dir, f"flask_app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(log_filename, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("flask.app")
logger.info("Flask app logger initialized")


# 匯入 blueprint [Start]
from views import bp_views  
from service.settings import bp_settings
# 匯入 blueprint [End]


app = Flask(__name__)
CORS(app)

# 註冊 blueprint
app.register_blueprint(bp_views)
app.register_blueprint(bp_settings)


@app.route("/", methods=["GET", "POST"])
def hello():
    """根路由

    Returns:
        _type_: 根路由的訊息
    """

    return "Hello, World!"

if __name__ == "__main__":
    # 啟動 Flask 內建伺服器，開始接收網頁請求
    ip_address = "127.0.0.1"
    port = 5000
    logger.info(f"Starting Flask app on http://{ip_address}:{port}")
    app.run(host=ip_address, port=port)