import requests
from bs4 import BeautifulSoup

from flask import Flask, render_template,request
from datetime import datetime

import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# 判斷是在 Vercel 還是本地
if os.path.exists('serviceAccountKeyv0409.json'):
    # 本地環境：讀取檔案
    cred = credentials.Certificate('serviceAccountKeyv0409.json')
else:
    # 雲端環境：從環境變數讀取 JSON 字串
    firebase_config = os.getenv('FIREBASE_CONFIG')
    cred_dict = json.loads(firebase_config)
    cred = credentials.Certificate(cred_dict)

firebase_admin.initialize_app(cred)

app = Flask(__name__)

db = firestore.client()



@app.route("/")
def index():
    link = "<h1>歡迎進入徐梓恩的網站20260416</h1>"
    link += "<a href=/mis>課程</a><hr>"
    link += "<a href=/today>現在日期時間</a><hr>"
    link += "<a href=/me>關於我</a><hr>"
    link += "<a href=/welcome?u=徐梓恩&d=靜宜行銷數位經營>Get傳值</a><hr>"
    link += "<a href=/account>post傳值</a><hr>"
    link += "<a href=/calculate>次方根號傳值</a><hr>"
    link += "<a href=/read>讀取Firestore資料</a><hr>"
    link += "<a href=/read2>查詢老師相關資料</a><hr>"
    link += "<a href=/spider>本學期課程</a><hr>"
    return link

@app.route("/spider")
def spider():
    R = ""
    url = "https://www1.pu.edu.tw/~tcyang/course.html"
    Data = requests.get(url)
    Data.encoding = "utf-8"
    #print(Data.text)
    sp = BeautifulSoup(Data.text, "html.parser")
    result=sp.select(".team-box a")

    for i in result:
        R += i.text + i.get("href") + "<br>"
    return R

@app.route("/read2", methods=["GET", "POST"])
def read2():
    if request.method == "POST":
        keyword = "徐"
        Result == ""

        collection_ref = db.collection("靜宜資管")
        docs = collection_ref.get()
        for doc in docs:
            teacher = doc.to_dict()
            if keyword and keyword in teacher.get("name", ""):
                Result += str(teacher) + "<br>"
        if Result == "" :
            Result = "抱歉查無此資料"
        return Result   

@app.route("/read")
def read():
    Result = ""
    db = firestore.client()
    collection_ref = db.collection("靜宜資管")    
    docs = collection_ref.get()  
    docs = collection_ref.order_by("lab",direction=firestore.Query.DESCENDING).limit(5).get()  
    for doc in docs:         
        Result += str(doc.to_dict()) + "<br>"    
    return Result   

@app.route("/mis")
def course():
    return "<h1>資訊管理導論</h1><a href=/>返回</a>"

@app.route("/today")
def today():
    now = datetime.now()
    return render_template("today.html", datetime=str(now))

@app.route("/me")
def me():
    return render_template("introduce.html")

@app.route("/welcome", methods=["GET"])
def welcome():
    user = request.values.get("u")
    d = request.values.get("d")
    return render_template("welcome.html", name=user, dep=d)

@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        user = request.form["user"]
        pwd = request.form["pwd"]
        result = "您輸入的帳號是：" + user + "; 密碼為：" + pwd
        return result

    else:
        return render_template("account.html")
        
@app.route("/calculate", methods=["GET", "POST"])
def calculate(): 
    x = ""
    y = ""
    result = ""
    opt = "∧"

    if request.method == "POST":
        try:
            x = float(request.form["number_x"])
            y = float(request.form["number_y"])
            opt = request.form["opt"]
      
            if opt == "∧":
                result = x ** y
            elif opt == "√":
                if y == 0:
                    result = "錯誤"
                else :
                    result = x ** (1/y)
            else:
                result = "未知的運算符號"

            print(result)

        except Exception as e:  
            result = f"錯誤：{e}"

    return render_template("calculate.html", result=result, x=x, y=y, opt=opt)

if __name__ == "__main__":
    app.run(debug=True)
