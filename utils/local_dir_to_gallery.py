#将本地的目录设置提供到db的同步

#从上层import模块的dirty opt
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

import configparser
import logging
import zipfile
import requests
import random
from lib import MysqlPkg
from lib import Downloader

def get_gallery_images(db, gid):
    g_info = db.fetch_first("SELECT * FROM gallerys WHERE gid=%s", gid)
    i_info = db.query("SELECT * FROM gallerys_image WHERE gid=%s", gid)
    image_arr = []
    for row in i_info:
        image_arr.append("".join(["[img]", "".join(g_info["remote_dir"], row["filename"]), "[/img]"]))

def indb_from_remote_zip(remote_zip, local_dir, remote_prefix, db, name = ""):
    #先下载远程文件
    dl = Downloader.Downloader("../conf/download.conf")
    zip_path = dl.download_image(remote_zip)
    my_unzip(zip_path, local_dir)
    filename = os.path.splitext(os.path.basename(my_unzip))[0]
    if(len(name) == 0):
        name = filename
    os.remove(zip_path) #解压后处理掉原始zip
    
#支持下载的zip文件并解压出来
def my_unzip(path_to_zip_file, directory_to_extract_to):
    #https://stackoverflow.com/questions/3451111/unzipping-files-in-python
    zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
    zip_ref.extractall(directory_to_extract_to)
    zip_ref.close()

def generate_db_data(db, name, local_path, remote_prefix, author = ""):
    local_data = os.listdir(local_path)
    if(len(local_data) == 0):
        return -1 #本地目录为空的时候不生成db数据
    folder_name = os.path.basename(local_path)
    #开始生成db数据
    db.insert("gallerys", {"name": name, "author": author, "local_dir": local_path, "remote_dir": "/".join([remote_prefix, folder_name])})
    gid = db.insert_id()
    for x in os.listdir(local_path):
        db.insert("gallerys_image", {"gid": gid, "filename": x})
    return gid

if __name__== '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %I:%M:%S')
    #初始化db
    db = MysqlPkg.mysqlpkg_fastinit("../conf/mysql.conf")
    
    rs = db.fetch_first("SELECT * FROM fetch_list WHERE id=%s", 1)

    remote_prefix = "http://127.0.0.1/remote/" #url前缀，这个后续从配置文件里读取
    #generate_db_data(db, "test", rs["local_path"], remote_prefix)
    indb_from_remote_zip('http://127.0.0.1/test.zip', "d:/web/remote/", remote_prefix, db)
    logging.warning("Task done.")