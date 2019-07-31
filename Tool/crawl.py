# coding=UTF-8
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

page = 5; # 要往前抓的頁數
# dateStr = datetime.datetime(2018,1,2).strftime('%Y%m%d')
domain = 'https://www.ptt.cc'
beautyIndex = domain + '/bbs/Beauty/index.html'
r = requests.get(beautyIndex, cookies={'over18':'1'})
soup = BeautifulSoup(r.text, 'html.parser')
indexSoup = BeautifulSoup(r.text, 'html.parser')
prevPage = soup.find_all('a', href=re.compile(r'/bbs/Beauty/index[0-9]{1,}\.html'))[-1].get('href')
prevPageMatch = re.search('[0-9]{1,}', prevPage)
prevPageNum = int(prevPageMatch.group(0))

for p in range(-1, page):
    if p == -1:
        crawlPageNum = prevPageNum + 1;
    else:
        crawlPageNum = prevPageNum - p;
    crawlUrl = domain + re.sub(r'[0-9]{1,}', str(crawlPageNum), prevPage)
    # print(crawlUrl)
    res = requests.get(crawlUrl, cookies={'over18':'1'})
    resSoup = BeautifulSoup(res.text, 'html.parser')
    aTags = resSoup.find_all('a')
    for tag in aTags:
        tagText = tag.string
        if (tagText is not None and (tagText.find('[正妹]') != -1 or tagText.find('[神人]') != -1)):
            tagHref = domain + (tag.get('href'))
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
                    # print(mycursor.lastrowid, "新增 title " + tagTitle + " 成功")
                else:
                    tagId = tagRes['id']

            # 新增準備爬取的文章頁面
            mycursor.execute("SELECT * FROM `CrawlUrl` WHERE `url` = %s", (tagHref, ))
            crawlUrlRes = mycursor.fetchone()
            if crawlUrlRes is None:
                mycursor.execute("INSERT INTO `CrawlUrl` SET `url` = %s, `tagId` = %s", (tagHref, tagId,))
                mydb.commit()
                # print(mycursor.lastrowid, "發現新文章 - 新增 url " + tagHref + " 成功")
            # else:
            #     print("文章 - url " + tagHref + "已存在")

# 準備爬取文章
mycursor.execute("SELECT * FROM `CrawlUrl` WHERE crawled = 'no'")
crawlUrls = mycursor.fetchall()
for crawlUrl in crawlUrls:
    r = requests.get(crawlUrl['url'], cookies={'over18':'1'})
    soup = BeautifulSoup(r.text, 'html.parser')
    images = soup.find_all(string=re.compile(r'/([\w_-]+[.](jpg|gif|png))$'))
    tagId = crawlUrl['tagId']
    articleTitle = re.sub(r'\[.{1,}\]', '', soup.find(property='og:title').get('content')).strip()

    # 新增文章
    mycursor.execute("INSERT INTO `Article` SET `crawlUrlId` = %s, `title` = %s", (crawlUrl['id'], articleTitle,))
    articleId = mycursor.lastrowid

    # 新增文章標籤
    mycursor.execute("INSERT INTO `ArticleTag` SET `articleId` = %s, `tagId` = %s", (articleId, tagId,))

    for img in images:
        img = str(img)
        # 新增文章圖片
        mycursor.execute("INSERT INTO `ArticleImage` SET `articleId` = %s, `img` = %s", (articleId, img,))

    # 更改為已爬取
    mycursor.execute("UPDATE `CrawlUrl` SET `crawled`='yes' WHERE `id` = %s", (crawlUrl['id'],))
    mydb.commit()

print('ok')