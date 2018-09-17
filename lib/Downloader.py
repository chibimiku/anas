#下载器的类
import requests
from requests.adapters import HTTPAdapter
import grequests
import logging
import configparser

class Downloader():
    def __init__(self, config_path, max_thread = 1):
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %I:%M:%S')
        self._load_config(config_path)
        self.referer = ""
        self.cookie = {}
        
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
        
    #下载图片到某个路径下面
    def download_image(url, headers, prefix = '', suffix = ''):
        save_path = "".join([self.save_path, "/", prefix, url.split("/")[-1], suffix])
        r = requests.get(url, stream=True, timeout=general_timeout, headers = self._get_request_header())
        if r.status_code == 200:
            with open(save_path, 'wb') as fp:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, fp)
            #判断图片格式
            filetype = imghdr.what(save_path)
            final_name = save_path + "." + filetype
            os.rename(save_path, final_name)
            logging.info ("".join(["Got from ", url, ", saving to: ", final_name]))
        else:
            logging.info ("".join(["Cannot get from ", url]))
