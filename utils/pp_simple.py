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

    #首次使用将会下载
    browser = await launch({"args": ["--no-sandbox"]})
    page = await browser.newPage()
    
    #尝试阻止下图片
    await pc.set_no_image(page)

    print ("Set done")
    #await page.goto("https://www.zhihu.com/question/51147227/answer/124329481")
    await page.goto("https://www.baidu.com")
    print (await page.title())
    
    await page.screenshot({'path': 'example.png'})
    await browser.close()

#执行相对简单的从db获取url
if __name__== '__main__':
    asyncio.get_event_loop().run_until_complete(main())
    print ("All task done.")