from flask import Flask
from flask_cors import CORS

import os
import logging
from datetime import datetime

import json
class PrettyColorFormatter(logging.Formatter):
    RED = "\033[31m"
    YELLOW = "\033[33m"
    LIGHTBLUE = "\033[94m"
    RESET = "\033[0m"
    def format(self, record):
        # 支援 dict/list 直接格式化
        msg = record.msg
        if isinstance(msg, (dict, list)):
            record.msg = json.dumps(msg, ensure_ascii=False, indent=2)
        else:
            try:
                obj = json.loads(msg)
                record.msg = json.dumps(obj, ensure_ascii=False, indent=2)
            except Exception:
                pass
        message = super().format(record)
        # 加顏色
        if record.levelno >= logging.ERROR:
            return f"{self.RED}{message}{self.RESET}"
        elif record.levelno == logging.WARNING:
            return f"{self.YELLOW}{message}{self.RESET}"
        elif record.levelno == logging.DEBUG:
            return f"{self.LIGHTBLUE}{message}{self.RESET}"
        return message

# 建立 log 目錄（如果不存在）
log_dir = "log"
os.makedirs(log_dir, exist_ok=True)

log_filename = os.path.join(log_dir, f"flask_app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
file_handler = logging.FileHandler(log_filename, encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(PrettyColorFormatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[file_handler, stream_handler]
)
logger = logging.getLogger("flask.app")
logger.info("Flask app logger initialized")


# 匯入 blueprint [Start]
from views import bp_views  
from posts.posts import bp_posts
from settingVersion.route import bp_settingVersion
from sportItem.route import bp_sportItem
from sportCategory.route import bp_sportCategory
from categoryGroup.route import bp_categoryGroup
from categoryOption.route import bp_categoryOption
from i18nText.route import bp_i18nText
# 匯入 blueprint [End]


app = Flask(__name__)
CORS(app)


# 註冊 blueprint [Start]
app.register_blueprint(bp_views)
app.register_blueprint(bp_posts)
app.register_blueprint(bp_settingVersion)
app.register_blueprint(bp_sportItem)
app.register_blueprint(bp_sportCategory)
app.register_blueprint(bp_categoryGroup)
app.register_blueprint(bp_categoryOption)
app.register_blueprint(bp_i18nText)
# 註冊 blueprint [End]


@app.route("/", methods=["GET", "POST"])
def hello():
    """根路由

    Returns:
        _type_: 根路由的訊息
    """

    version = "v1.0.0"

    return f"[Python Flask Admin] {version}"

if __name__ == "__main__":
    # 啟動 Flask 內建伺服器，開始接收網頁請求
    ip_address = "127.0.0.1"
    port = 5000
    logger.info(f"Starting Flask app on http://{ip_address}:{port}")
    app.run(host=ip_address, port=port)