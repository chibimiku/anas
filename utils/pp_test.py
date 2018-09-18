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
import traceback
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
    await pc.disable_img(page)
    
    fetch_tbl_name = "fetch_list"
    
    #获取需要抓取的list
    fetch_list = db.query("SELECT * FROM " + fetch_tbl_name + " WHERE status=0")

    #设置cookies
    cookies_path = '../data/cookies/'
    
    #infos
    update_infos = []

    for row in fetch_list:
        url = row["url"]

        ck = Cookie.Cookie(cookies_path)
        my_cookie_list = ck.load_cookie(url)
        print ("load cookie completed")
        for cookie_row in my_cookie_list:
            await page.setCookie(cookie_row)
        #设置cookies完毕
        try:
            print ("Going to fetch " + url)
            await page.goto(url, {"timeout": 150000})
            #尝试获取web版weibo image
            if('m.weibo.cn' in url):
                #get weibo image
                author_name = await pc.get_element_content_by_selector(page, ".weibo-top h3[class*='m-text-cut']")
                author_id_tmp = await pc.get_element_attr_by_selector(page, ".weibo-top a[class*='m-img-box']", "href")
                author_id = author_id_tmp.split("/")[-1]
                imgs = await pc.get_elements_attr_by_selector(page, ".f-bg-img", "style.backgroundImage")
                if(len(imgs) > 0):
                    for i in range(0, len(imgs)):
                        imgs[i] = imgs[i].replace("orj360", "large").replace('url("', "", )[:-2] #去掉
            elif('//weibo.com' in url or '//www.weibo.com' in url):
                author_name = await pc.get_element_content_by_selector(page, ".WB_info a")
                #author_id_tmp = await pc.get_element_attr_by_selector(page, ".choose_box img", "src")
                #author_id = author_id_tmp.split("/")[-1]
                author_id = 0
                imgs = await pc.get_elements_attr_by_selector(page, ".choose_box img", "src")
                if(len(imgs) > 0):
                    for i in range(0, len(imgs)):
                        imgs[i] = imgs[i].replace("thumb150", "large")
                else:
                    imgs = await pc.get_elements_attr_by_selector(page, ".media_box .WB_pic img", "src")
                    if(len(imgs) > 0):
                        for i in range(0, len(imgs)):
                            imgs[i] = imgs[i].replace("thumb150", "large")
            else:
                logging.error("Cannot analy...")
            logging.info ("Got user:" + author_name)
            dl.set_sub_download_dir(author_name)
            if(len(imgs) == 0):
                raise Exception('nothing image got...')
            print (imgs)
            for img in imgs:
                dl.download_image(img)
            print ("Download task done.")
            up_dict = {"status": 1, "fetch_timestamp": time.time(), "local_path": dl.get_full_save_path(), "author_name": author_name, "author_id": author_id}
            update_infos.append({"insert_dict": up_dict, "id": row["id"]})
            db.update(fetch_tbl_name, {"status": 1, "fetch_timestamp": time.time(), "local_path": dl.get_full_save_path(), "author_name": author_name, "author_id": author_id}, "id=%s", row["id"])
            #db.update(fetch_tbl_name, {"status": 1, "fetch_timestamp": time.time(), "local_path": dl.get_full_save_path(), "author_name": author_name, "author_id": author_id}, "id=" + str(row["id"]))
        except Exception as e:
            db.update(fetch_tbl_name, {"status": -1, "comment": e}, "id=%s", str(row["id"]))
            traceback.print_exc()
            
        new_cookie = await page.cookies()
        #回写cookies
        ck.save_cookie(url, new_cookie)
        print ("saving cookies done. entry new loop")
    print ("Fetch task done")
    await browser.close()
    db.close()
    return update_infos

#执行相对简单的从db获取url
if __name__== '__main__':
    asyncio.get_event_loop().run_until_complete(main())
    '''
    fetch_tbl_name = "fetch_list"
    db = MysqlPkg.mysqlpkg_fastinit("../conf/mysql.conf")
    for row in update_infos:
        db.update(fetch_tbl_name, row[""], "id=%s", row["id"])
    '''
    print ("All task done.")
    