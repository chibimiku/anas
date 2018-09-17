#从上层import模块的dirty opt
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

import configparser
from pyppeteer import launch
import asyncio
import json
import logging
import time
from lib import MysqlPkg
from lib import Cookie
from lib import Downloader
from lib import PuppeteerCombo as pc

async def main():
    #初始化db
    db = MysqlPkg.mysqlpkg_fastinit("../conf/mysql.conf")
    
    #配置downloader
    dl = Downloader.Downloader("../conf/download.conf")

    #首次使用将会下载
    browser = await launch({"args": ["--no-sandbox"]})
    page = await browser.newPage()
    
    fetch_tbl_name = "fetch_list"
    
    #获取需要抓取的list
    fetch_list = db.query("SELECT * FROM " + fetch_tbl_name + " WHERE status=0")
    
    for row in fetch_list:
        print (row)
        url = row["url"]
        #设置cookies
        cookies_path = '../data/cookies/'
        ck = Cookie.Cookie(cookies_path)
        my_cookie_list = ck.load_cookie(url)
        for cookie_row in my_cookie_list:
            await page.setCookie(cookie_row)
        #设置cookies完毕
        
        try:
            await page.goto(url)
            #get weibo image
            author_name = await pc.get_element_content_by_selector(page, ".weibo-top h3[class*='m-text-cut']")
            author_id_tmp = await pc.get_element_attr_by_selector(page, ".weibo-top a[class*='m-img-box']", "href")
            author_id = author_id_tmp.split("/")[-1]
            logging.info ("Got user:" + author_name)
            dl.set_sub_download_dir(author_name)
            imgs = await pc.get_elements_attr_by_selector(page, ".f-bg-img", "style.backgroundImage")
            if(len(imgs) > 0):
                for i in range(0, len(imgs)):
                    imgs[i] = imgs[i].replace("orj360", "large").replace('url("', "", )[:-2] #去掉
            print (imgs)
            for img in imgs:
                dl.download_image(img)
            db.update(fetch_tbl_name, {"status": 1, "fetch_timestamp": time.time(), "local_path": dl.get_full_save_path(), "author_name": author_name, "author_id": author_id}, "id=%s", row["id"])
        except Exception as e:
            db.update(fetch_tbl_name, {"status": -1, "comment": e}, "id=%s", row["id"])
            
        new_cookie = await page.cookies()
        #回写cookies
        ck.save_cookie(url, new_cookie)

    await browser.close()
    db.close()

#执行相对简单的从db获取url
if __name__== '__main__':
    asyncio.get_event_loop().run_until_complete(main())
    print ("All task done.")
    