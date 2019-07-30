import re
import requests
# import datetime
from bs4 import BeautifulSoup
import mysql.connector

mydb = mysql.connector.connect(
    host="192.168.10.10",
    user="homestead",
    passwd="secret",
    database="maple7",
)
mycursor = mydb.cursor(dictionary=True)

# def insert(conn, tableName, data):
#     sql = "INSERT INTO " + tableName + " (name, url) VALUES (%s, %s)"
#     val = ("RUNOOB", "https://www.runoob.com")
#     conn.execute(sql, val)

# dateStr = datetime.datetime(2018,1,2).strftime('%Y%m%d')
domain = 'https://www.ptt.cc'
beautyIndex = domain + '/bbs/Beauty/index.html'
cookies = {
    'over18':'1'
}
r = requests.get(beautyIndex, cookies=cookies)
soup = BeautifulSoup(r.text, 'html.parser')

# # 輸出排版後的 HTML 程式碼
# soup.prettify()
# # 網頁標題 HTML 標籤
# titleTag = soup.title
aTags = soup.find_all('a')
# links = []
for tag in aTags:
    tagText = tag.string
    if (tagText is not None and (tagText.find('[正妹]') != -1 or tagText.find('[神人]') != -1)):
        tagHref = tag.get('href')
        regex = re.compile(r'\[.{1,}\]')
        titleMatch = regex.match(tagText)
        if titleMatch:
            tagTitle = titleMatch.group()
            mycursor.execute("SELECT * FROM `Tag` WHERE `title` = %s", (tagTitle, ))
            tagRes = mycursor.fetchone()
            if tagRes is None:
                mycursor.execute("INSERT INTO `Tag` SET `title` = %s", (tagTitle, ))
                mydb.commit()
                tagId = mycursor.lastrowid
                print(mycursor.lastrowid, "新增 title " + tagTitle + "成功")
            else:
                tagId = tagRes['id']

        # 新增準備爬取的文章頁面
        mycursor.execute("SELECT * FROM `CrawlUrl` WHERE `url` = %s", (tagHref, ))
        crawlUrlRes = mycursor.fetchone()
        if crawlUrlRes is None:
            mycursor.execute("INSERT INTO `CrawlUrl` SET `url` = %s", (tagHref, ))
            mydb.commit()
            print(mycursor.lastrowid, "新增 url " + tagHref + "成功")
        else:
            print("url " + tagHref + "已存在")

# 準備爬取文章
mycursor.execute("SELECT * FROM `CrawlUrl` WHERE crawled = 'no'")
crawlUrls = mycursor.fetchall()
for crawlUrl in crawlUrls:
    r = requests.get(domain + crawlUrl['url'], cookies={'over18':'1'})
    soup = BeautifulSoup(r.text, 'html.parser')
    images = soup.find_all(string=re.compile(r'/([\w_-]+[.](jpg|gif|png))$'))
    print(images)
    break;