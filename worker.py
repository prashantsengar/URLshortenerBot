import requests
import re

API_URL = 'YOURLS API URL'
YOURL_SIGN = "YOURLS API SIGNATURE"


regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def shorten(url, keyword=None):
    """
    (str),(str) -> (str)
    Shorten URL and use a KEYWORD. Returns shortened URL
    """
    if keyword:
        data={'signature':YOURL_SIGN,'action':'shorturl',
              'url':url,'format':'json','keyword':keyword}
    else:
        data={'signature':YOURL_SIGN,'action':'shorturl','url':url,'format':'json'}
    res = requests.post(API_URL, data)
    res_json = res.json()
    if res.status_code==200:
        if res_json['status']=='success':
            return res_json['shorturl']
        if res_json['code']=='error:url':
            return res_json['shorturl'],'url'
        if res_json['code']=='error:keyword':
            raise Exception('keyword')
    raise Exception('Status Code Error')
        
def expand(url):
    """
    (str) -> (str)
    Shorten URL and use a KEYWORD. Returns shortened URL
    """
    data={'signature':YOURL_SIGN,'action':'expand','shorturl':url,'format':'json'}
    res = requests.post(API_URL, data)
    if res.status_code==200:
        return res.json()['longurl']
    raise Exception('Status Code Error')
    
def is_url(url):
    """
    str -> (bool)
    """
    global regex
    if regex.match(url):
        return True
    return False

