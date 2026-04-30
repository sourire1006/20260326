import requests
from bs4 import BeautifulSoup

from flask import Flask, render_template,request
from datetime import datetime

app = Flask(__name__)

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
    link = "<h1>歡迎進入徐梓恩的網站</h1>"
    link += "<a href=/mis>課程</a><hr>"
    link += "<a href=/today>現在日期時間</a><hr>"
    link += "<a href=/me>關於我</a><hr>"
    link += "<a href=/welcome?u=徐梓恩&d=靜宜行銷數位經營>Get傳值</a><hr>"
    link += "<a href=/account>post傳值</a><hr>"
    link += "<a href=/calculate>次方根號傳值</a><hr>"
    link += "<a href=/read>讀取Firestore資料</a><hr>"
    link += "<a href=/read2>查詢老師相關資料</a><hr>"
    link += "<a href=/spider>爬取本學期課程</a><hr>"
    link += "<a href=/spider1>爬取即將上映電影</a><hr>"
    link += "<a href=/spidermovie>爬取即將上映電影集合</a><hr>"
    return link

@app.route("/spidermovie")
def spidermovie():
    db = firestore.client()

    import requests
    from bs4 import BeautifulSoup
    url = "http://www.atmovies.com.tw/movie/next/"
    Data = requests.get(url)
    Data.encoding = "utf-8"  #解決亂碼

    sp = BeautifulSoup(Data.text, "html.parser")
    lastupdate = sp.find(class_="smaller09").text.replace("更新時間：","")

    result=sp.select(".filmListAllX li")
    info = ""  #建立一個空的字串變數(初始化)
    total =0
    R = ""

    for item in result:
      movie_id = item.find("a").get("href").replace("/movie/","").replace("/","")  #replace取代
      title = item.find(class_="filmtitle").text
      picture = "https://www.atmovies.com.tw" + item.find("img").get("src")
      hyperlink = "https://www.atmovies.com.tw" + item.find("a").get("href")
      showdate = item.find(class_="runtime").text[5:15] #[5:15] 第0個字元到第三個字元

      info += picture + "\n" + hyperlink + "\n"  #"\n"=換行符號
      info += movie_id + "\n" + title + "\n"  + showdate + "\n"

      doc = {
          "title": title,
          "picture": picture,
          "hyperlink": hyperlink,
          "showdate": showdate,
          "lastupdate": lastupdate
      }


      doc_ref = db.collection("電影集合").document(movie_id)
      doc_ref.set(doc)

      total += 1 
      R += f"已儲存第 {total} 部：{title}<br>" # 可選：顯示每部進度

    R += "網站最新更新日期" +  lastupdate + "<br>"
    R += f"<br><b>總共爬取 {total} 部電影到資料庫</b>"
    return R

@app.route("/spider1")
def spider1():
    # Flask 用來從網址（URL）中抓取資料的方法，q為變數詳細查詢的替代詞
    q = request.args.get("q")

    #問程式：「使用者是不是還沒輸入關鍵字？」
    if not q:

        #return ''' ... '''----這部分回傳的是一段 HTML 碼，它建構了使用者看得到的介面：
        return '''
            <h2>電影搜尋系統</h2>
            <form action="/spider1" method="get">
                <input type="text" name="q" placeholder="請輸入電影關鍵字">
                <button type="submit">搜尋</button>
            </form>
            <br><a href='/'>回首頁</a>
        '''

    R = f"<h2>搜尋到的關鍵字是：{q}</h2>"
    url = "https://www.atmovies.com.tw/movie/next/"
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"} #避免被對方網站阻擋
    data = requests.get(url, headers=headers) #真正出發去把網頁的 HTML 原始碼抓回來
    data.encoding = "utf-8" #確保中文字不會變成亂碼
    
    #BeautifulSoup: 將雜亂的 HTML 字串變成像「樹狀結構」
    sp = BeautifulSoup(data.text, "html.parser")
    result = sp.select(".filmListAllX li") #找出所有在filmListAllX標籤底下的 <li> 
    
    found = False
    #針對抓到的每一部電影，一個一個檢查
    for item in result: 
        img_tag = item.find("img")
        if img_tag:
            title = img_tag.get("alt") #電影標題通常寫在圖片的 alt的屬性

            if q in title: #只有當你輸入的關鍵字（q）出現在電影標題時，才會執行裡面的動作
                found = True
                link = "https://www.atmovies.com.tw" + item.find("a").get("href")
                img = item.find("img").get("src")
                
                R += f'<a href="{link}">{title}</a><br>'
                R += f'<img src="{img}"><br><br>'
            
    if not found:
        R += "抱歉，沒有找到這部電影的資訊"
        
    R += "<br><a href='/spider1'>重新搜尋</a> | <a href='/'>回首頁</a>"
    return R
    
#確保程式是「直接被執行」的，而不是「被當作工具包導入」
if __name__ == "__main__": 
    app.run(debug=True)

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

@app.route("/read2")
def read2():
        Result = ""
        kryword = "徐"
        db = firestore.client()
        collection_ref = db.collection("靜宜資管")
        docs = collection_ref.get()
        for doc in docs:
            teacher = doc.to_dict()
            if keyword in teacher["name"]:
                Result += str(teacher) + "<br>"

        if Result == "":
            Result = "抱歉查無此資料"
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
