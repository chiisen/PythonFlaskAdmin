# PythonFlaskAdmin
Python Flask Admin


## Python Flask 專案通常還需要以下檔案：

requirements.txt
列出所有 Python 套件依賴，Docker 建置時會用到。

app.py
你的主程式檔案，已經存在。

views.py
放 blueprint 或路由相關程式碼，已經存在。

init.py
如果你的 src 資料夾是 Python package，建議加上。

README.md
專案說明文件，方便他人了解如何使用。

.dockerignore
列出不需要加入 Docker image 的檔案，例如 .git、__pycache__ 等。

config.py（選用）
放設定參數。

static/ 和 templates/ 資料夾（如有前端）
分別放靜態檔案和 HTML 模板。

## 基本結構範例：
PythonFlaskAdmin/  
├── Dockerfile  
├── requirements.txt  
├── .dockerignore  
├── src/  
│   ├── app.py  
│   └── views.py  
├── requirements.txt  
├── Dockerfile  
├── .dockerignore  
├── README.md  
├── config.py  
├── static/  
└── templates/  

## requirements.txt 產生方式：
```bash
pip freeze > requirements.txt
```
這會把目前環境所有已安裝套件及版本寫入 requirements.txt。

