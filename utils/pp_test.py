#从上层import模块的dirty opt
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

import configparser
from pyppeteer import launch
import asyncio
import json
from lib import MysqlPkg
from lib import Cookie
from lib import Downloader

async def main():
    #初始化db
    config = configparser.ConfigParser()
    config.read("../conf/mysql.conf")
    db_conf = config._sections["mysql_localhost"]
    print (db_conf)
    db = MysqlPkg.MysqlPkg(db_conf)
    
    #先查找DB已经存在的数据
    q_rs = db.query("SELECT * FROM titles WHERE 1=1")
    print (q_rs)
    
    #配置downloader
    dl = Downloader.Downloader("../conf/download.conf")

    #首次使用将会下载
    browser = await launch({"args": ["--no-sandbox"]})
    page = await browser.newPage()
    url = "https://ark.intel.com/"
    
    #设置cookies
    cookies_path = '../data/cookies/'
    ck = Cookie.Cookie(cookies_path)
    my_cookie_list = ck.load_cookie(url)
    for row in my_cookie_list:
        await page.setCookie(row)
        
    #设置cookies完毕
    await page.goto(url)
    
    title = await page.title()
    db.insert("titles", {"url": url, "title": title})
    
    new_cookie = await page.cookies()
    #回写cookies
    ck.save_cookie(url, new_cookie)

    await browser.close()
    db.close()

#执行相对简单的从db获取url
if __name__== '__main__':
    asyncio.get_event_loop().run_until_complete(main())
    print ("All task done.")
    