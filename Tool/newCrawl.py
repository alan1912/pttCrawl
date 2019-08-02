import re
import requests
import mysql.connector
from bs4 import BeautifulSoup

class DbAccess():
    DB_HOST = "192.168.10.10"
    DB_USER = "homestead"
    DB_PWD = "secret"
    DB_NAME = "maple7"

    def __init__(self):
        self.db = mysql.connector.connect(
            host = self.DB_HOST,
            user = self.DB_USER,
            passwd = self.DB_PWD,
            database = self.DB_NAME,
        )
        self.cursor = self.db.cursor(dictionary=True)

    def getWhere(self, where = {}):
        where = '' if len(where) == 0 else 'WHERE ' + ' AND '.join(f'`{k}` = \'{v}\'' for k,v in where.items())

        return where

    def getSetSql(self, setData = {}):
        setSql = '' if len(setData) == 0 else 'SET ' + ', '.join(f'`{k}` = %({k})s' for k,v in setData.items())

        return setSql

    def getAll(self, tableName, where={}):
        where = self.getWhere(where)
        self.cursor.execute(f'SELECT * FROM `{tableName}` {where}')
        res = self.cursor.fetchall()

        return res

    def getOne(self, tableName, where={}):
        where = self.getWhere(where)
        self.cursor.execute(f'SELECT * FROM `{tableName}` {where}')
        res = self.cursor.fetchone()

        return res

    def insert(self, tableName, data):
        setSql = self.getSetSql(data)
        self.cursor.execute(f'INSERT INTO `{tableName}` {setSql}', data)
        # self.db.commit()
        # insertId = self.cursor.lastrowid

        # return insertId

    def update(self, tableName, data, where={}):
        setSql = self.getSetSql(data)
        where = self.getWhere(where)
        self.cursor.execute(f'UPDATE `{tableName}` {setSql} {where}', data)
        # self.db.commit()

        # return insertId

    def commit(self):
        self.db.commit()

    def getLastId(self):
        return self.cursor.lastrowid

class NewCrawl():

    CRAWL_URL_DOMAIN = "https://www.ptt.cc"
    CRAWL_PAGE = 5

    def __init__(self):
        pass

    def crawlBeauty(self):
        index= '/bbs/Beauty/index'
        self.preCrawlProcess(index)
        insertCount = self.crawlProcess()

        return insertCount

    def getHtmlParserObj(self, url, cookies={}):
        r = requests.get(url, cookies=cookies)
        htmlParserObj = BeautifulSoup(r.text, 'html.parser')

        return htmlParserObj

    def preCrawlProcess(self, index):
        for p in range(-1, self.CRAWL_PAGE):
            if p == -1:
                crawlUrl = self.CRAWL_URL_DOMAIN + index + '.html'
                htmlObj = self.getHtmlParserObj(crawlUrl, {'over18':'1'})
            else:
                crawlUrls = htmlObj.find_all('a', href=re.compile(index + "[0-9]{1,}\.html"), text=re.compile("上頁"))
                if len(crawlUrls) == 0:
                    break;
                crawlUrl = self.CRAWL_URL_DOMAIN + crawlUrls[-1].get('href')
                htmlObj = self.getHtmlParserObj(crawlUrl, {'over18':'1'})

            articles = htmlObj.find_all('a', text=re.compile("(\[正妹\]|\[神人\]|\[廣告\])"))
            if len(articles) == 0:
                break;
            for article in articles:
                articleTitle = article.string
                articleUrl = self.CRAWL_URL_DOMAIN + (article.get('href'))
                tagName = re.compile('\[.{1,}\]').search(articleTitle)
                if (tagName is None):
                    continue
                tagName = tagName.group(0).replace('[', '').replace(']', '')

                db = DbAccess()
                tagRes = db.getOne('Tag', {'title': tagName})
                if tagRes is None:
                    db.insert('Tag', {'title': tagName})
                    tagId = db.getLastId()
                else:
                    tagId = tagRes['id']

                # 新增準備爬取的文章頁面
                crawlUrlRes = db.getOne('CrawlUrl', {'url': articleUrl})
                if crawlUrlRes is None:
                    db.insert('CrawlUrl', {
                        'tagId': tagId,
                        'url': articleUrl
                    })
                    db.commit()

    def crawlProcess(self):
        # 準備爬取文章
        count = 0
        db = DbAccess()
        crawlUrls = db.getAll('CrawlUrl', {'crawled': 'no'})
        for crawlUrl in crawlUrls:
            htmlObj = self.getHtmlParserObj(crawlUrl['url'], {'over18':'1'})
            images = htmlObj.find_all(string=re.compile(r'/([\w_-]+[.](jpg|gif|png))$'))
            if (len(images) == 0):
                continue
            tagId = crawlUrl['tagId']
            articleTitle = re.sub(r'\[.{1,}\]', '', htmlObj.find(property='og:title').get('content')).strip()

            # 新增文章
            db.insert('Article', {
                'crawlUrlId': crawlUrl['id'],
                'title': articleTitle
            })
            articleId = db.getLastId()

            # 新增文章標籤
            db.insert('ArticleTag', {
                'articleId': articleId,
                'tagId': tagId
            })

            # 新增文章圖片
            for img in images:
                img = str(img)
                db.insert('ArticleImage', {
                    'articleId': articleId,
                    'img': img
                })

            # 更改為已爬取
            db.update('CrawlUrl', {'crawled': 'yes'}, {'id': crawlUrl['id']})
            count = count + 1
            db.commit()

        return count

c = NewCrawl()
insertCount = c.crawlBeauty()
print(insertCount)