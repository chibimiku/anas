#将本地的目录设置提供到db的同步

#从上层import模块的dirty opt
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

import configparser
import logging
from lib import MysqlPkg

if __name__== '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %I:%M:%S')
    #初始化db
    db = MysqlPkg.mysqlpkg_fastinit("../conf/mysql.conf")
    
    rs = db.fetch_first("SELECT * FROM fetch_list WHERE id=%s", 1)
    local_path = rs["local_path"]
    print (local_path)
    for x in os.listdir(local_path):
        print (x)
        
    remote_prefix = "http://127.0.0.1/info/" #url前缀，这个后续从配置文件里读取
    #开始生成db数据
    #db.insert("gallerys", {"name": "test", "author": rs["author_name"], "local_dir": local_path, "remote_dir": remote_prefix + ""})
    
    logging.warning("Task done.")