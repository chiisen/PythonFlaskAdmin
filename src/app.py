from flask import Flask
from views import bp  # 匯入 blueprint

app = Flask(__name__)
app.register_blueprint(bp)  # 註冊 blueprint

@app.route("/")
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    # 啟動 Flask 內建伺服器，開始接收網頁請求
    app.run(host="127.0.0.1", port=5000)