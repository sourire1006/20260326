import requests
from bs4 import BeautifulSoup
url = "http://www.atmovies.com.tw/movie/next/"
Data = requests.get(url)
Data.encoding = "utf-8"  #解決亂碼

sp = BeautifulSoup(Data.text, "html.parser")
lastupdate = sp.find(class_="smaller09").text.replace("更新時間：","Lastupdate:")

result=sp.select(".filmListAllX li")
info = ""  #建立一個空的字串變數(初始化)
for item in result:
  movie_id = item.find("a").get("href").replace("/movie/","").replace("/","")  #replace取代
  title = item.find(class_="filmtitle").text
  picture = "https://www.atmovies.com.tw" + item.find("img").get("src")
  hyperlink = "https://www.atmovies.com.tw" + item.find("a").get("href")
  showdate = item.find(class_="runtime").text[5:15] #[5:15] 第0個字元到第三個字元

  info += picture + "\n" + hyperlink + "\n"  #"\n"=換行符號
  info += movie_id + "\n" + title + "\n"  + showdate + "\n"
  info += lastupdate
print(info)
