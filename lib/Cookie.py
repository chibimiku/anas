#处理cookie的类
from urllib.parse import urlparse
from pathlib import Path
import json

class Cookie():
    def __init__(self, local_path):
        self.local_path = local_path
        
    def save_cookie(self, url, new_cookie):
        json_cookie = json.dumps(new_cookie)
        cookies_file = self._get_real_cookie_path(url)
        with open (cookies_file, 'w+', encoding="utf-8") as wfp:
            wfp.write(json_cookie)
        return True
    
    def load_cookie(self, url):
        cookies_file = self._get_real_cookie_path(url)
        my_file = Path(cookies_file)
        if(not my_file.is_file()):
            return []
        with open (cookies_file) as fp:
            my_cookie = fp.read()
        if(len(my_cookie) > 0):
            try:
                my_cookie_list = json.loads(my_cookie)
            except Exception as e:
                print (e)
                return []
        else:
            return []
        return my_cookie_list
        
    def load_cookie_dict(self, url):
        ret_dict = {}
        tmp = self.load_cookie(url)
        for row in tmp:
            ret_dict[row["name"]] = row["value"]
        return ret_dict
        
    def _get_real_cookie_path(self, url):
        parsed_uri = urlparse(url)
        return "".join([self.local_path, parsed_uri.netloc, "_cookie.txt"])
        