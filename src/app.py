from flask import Flask
app = Flask(__name__)
@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/hello")
def say_hello():
    return "Hello from /hello route!"

if __name__ == "__main__":
    # 啟動 Flask 內建伺服器，開始接收網頁請求
    app.run(host="127.0.0.1", port=5000)