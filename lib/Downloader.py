#下载器的类
import requests
import grequests
import logging
import configparser
import shutil
import imghdr
import os

class Downloader():
    def __init__(self, config_path, max_thread = 1):
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %I:%M:%S')
        self._load_config(config_path)
        self.referer = ""
        self.cookie = {}
        self.timeout = 30
        self.sub_download_dir = ""
        self.db_ok = False
        
    #从配置项里读取参数
    def _load_config(self, config_path):
        #初始化db
        config = configparser.ConfigParser()
        config.read(config_path)
        dl_conf = config._sections["download_local_storage"]
        self.useragent = dl_conf["useragent"]
        self.wap_useragent = dl_conf["wap_useragent"]
        self.save_path = dl_conf["save_path"]
        try:
            self.max_thread = int(dl_conf["max_thread"])
        except Exception as e:
            logging.error(e)
            self.max_thread = 1
            
    #支持从db做记录
    def init_db(self, db):
        self.db = db
        self.db_ok = True
            
    def set_sub_download_dir(self, dir):
        self.sub_download_dir = dir
        
    def set_save_path(self, save_path):
        self.save_path = save_path
        
    def set_useragent(self, useragent):
        self.useragent = useragent
        
    def set_referer(self, referer):
        self.referer = referer
        
    def set_cookie(self, new_cookie):
        self.cookie = new_cookie
        
    def _get_request_header(self):
        return {'User-Agent': self.useragent, 'referer': self.referer}
        
    #获取整个下载路径
    def get_full_save_path(self):
        if(len( self.sub_download_dir) > 0):
            return "/".join([self.save_path, self.sub_download_dir])
        else:
            return self.save_path
        
    #下载图片到某个路径下面
    def download_image(self, url, prefix = '', suffix = '', overwrite = False):
        logging.info ("".join(["Going to fetch url:", url]))
        dir_to_save = "".join([self.save_path, "/", self.sub_download_dir, "/"])
        if not os.path.exists(dir_to_save):
            os.makedirs(dir_to_save)
        save_file_path = "".join([dir_to_save, prefix, url.split("/")[-1], suffix])
        skip_fetch = False
        if(os.path.isfile(save_file_path)): #判断文件已经存在
            logging.warning(save_file_path + " exists.")
            if(overwrite):
                os.remove(save_file_path) #删除掉文件
            else:
                return False #直接返回，不进行抓取了
        r = requests.get(url, stream=True, timeout=self.timeout, headers = self._get_request_header())
        if r.status_code == 200:
            with open(save_file_path, 'wb') as fp:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, fp)
            #判断图片格式 现在貌似没有需要了
            #filetype = imghdr.what(save_file_path)
            #final_name = save_file_path + "." + filetype
            logging.info ("".join(["Got from ", url, ", saving to: ", save_file_path]))
        else:
            logging.info ("".join(["Cannot get from ", url]))
        return save_file_path