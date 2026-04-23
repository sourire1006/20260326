import requests
from bs4 import BeautifulSoup

	url = "https://www.atmovies.com.tw/movie/next/"
	Data = requests.get(url)
	Data.encoding = "utf-8"
	#print(Data.text)
	sp = BeautifulSoup(Data.text, "html.parser")
	result=sp.select(".filmListAllX li")
	for item in result:
		print(item.find("img").get("alt")) #名稱
		print("https://www.atmovies.com.tw/" + item.find("a").get("href")) #連結
		print("https://www.atmovies.com.tw/" + item.find("img").get("src")) #圖片
		print()



