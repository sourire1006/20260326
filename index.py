from flask import Flask, render_template,request
from datetime import datetime
app = Flask(__name__)

@app.route("/")
def index():
    link = "<h1>歡迎進入徐梓恩的網站</h1>"
    link += "<a href=/mis>課程</a><hr>"
    link += "<a href=/today>現在日期時間</a><hr>"
    link += "<a href=/me>關於我</a><hr>"
    link += "<a href=/welcome?u=徐梓恩&d=靜宜行銷數位經營>Get傳值</a><hr>"
    link += "<a href=/account>post傳值</a><hr>"
    link += "<a href=/calculate>次方根號傳值</a><hr>"
    return link

@app.route("/mis")
def course():
    return "<h1>資訊管理導論</h1><a href=/>返回</a>"

@app.route("/today")
def today():
    now = datetime.now()
    return render_template("today.html", datetime=str(now))

@app.route("/me")
def me():
    return render_template("mis2026b.html")

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
