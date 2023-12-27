
import os
import time
from unicodedata import category
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium.webdriver.common.by import By
# third party lib
import requests
from urllib.parse import urlencode, quote
from selenium.webdriver import ChromeOptions
from selenium import webdriver

from pathlib import Path
from urllib3.util.retry import Retry
from lxml import etree

G_USER_AGENT = r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.133 Safari/537.36'


headers = {"User-Agent":G_USER_AGENT}  # noqa
pic_headers = {"User-Agent":G_USER_AGENT,"referer":"https://pixhost.to/"}

'''
添加功能测试文件，已集成到项目中
'''


def get_html(url,header:dict = None, cookies: dict = None,return_type: str = None, encoding: str = None):
    """
    网页请求核心函数
    """
    verify = None
    proxy = '127.0.0.1:7890'
    proxies = {
    "http": "http://%(proxy)s/" % {'proxy': proxy},
    "https": "https://%(proxy)s/" % {'proxy': proxy}
    }
    errors = ""
    if header is None:
        header = headers
    else:
        header = header
    


    for i in range(4):
        try:
            result = requests.get(str(url), headers=header, timeout=5, proxies=proxies, verify=verify,cookies=cookies)
            
            return result
            
        except Exception as e:
            print("[-]Connect retry {}/{}".format(i + 1, 4))
            errors = str(e)
    if "getaddrinfo failed" in errors:
        print("[-]Connect Failed! Please Check your proxy config")

    else:
        print("[-]" + errors)
        print('[-]Connect Failed! Please check your Proxy or Network!')
    raise Exception('Connect Failed')

def getBlogJAVSearchVal(number):
    bid = number.replace('-','+')
    return bid

def findPreviewImagesFromBlogJAV(number):
    bid = getBlogJAVSearchVal(number)
    url= 'https://blogJAV.net/?s='+bid
    bJAV_search_html = get_html(url)
    if bJAV_search_html.status_code != 200:
        print("blogjav页面错误")
        return None
    data = etree.HTML(bJAV_search_html.text)
    dlist = data.findall('.//*[@class="entry-title"]')
    p_url = ""
    for b in dlist:
        nb = etree.tostring(b).decode()
        if number in nb:
            tmp_url = b.xpath('./a/@href')[0]
            if p_url == "":
               p_url = tmp_url
            if 'FHD' in nb:
               p_url = tmp_url
        
    return p_url
    
    
def getPreviewImageUrlFromBlogJAV(url):
    
    p_html = get_html(url,header= pic_headers)
    if p_html.status_code != 200:
       print("无法加载blogJAV页面")
       return ""
    data = etree.HTML(p_html.text)
    image_list = data.xpath('/html/body/div[1]/div/div[1]/main/article/div/div/p[1]/a/img/@data-lazy-src')
    if len(image_list) == 0:
        print("未找到blogjav对应位置缩略图，请查看代码")
        return ""
    targetImageUrl = image_list[0].replace('thumbs', 'images').replace('/t', '/img')
    return targetImageUrl
def findPreviewImagesFromJAVStore(number):
    number = getRightNumber(number)
    url = f'https://javstore.net/search/{number}.html'
    p_html = get_html(url, header=headers)
    if p_html.status_code != 200:
        print("[!]加载javstore搜索页面出错")
        return ""
    data = etree.HTML(p_html.text)
    node = data.xpath('/html/body/div[1]/div[2]/div[1]/div[3]/div')
    
    
    if len(node) > 0:
        dlist = node[0].xpath('.//h3/span')
        if len(dlist) == 0:
            print("未找到javstore搜索元素")
            return ""
    else:
        print('未找到xpath对应元素，请检查')
    
    p_url = ""
    cnt = 0
    for ele in dlist:
        cnt += 1
        tmp = etree.tostring(ele).decode()
        if number in tmp:
            if p_url == "":
                p_url = ele.xpath('./a/@href')[0]
                
            if 'FHD' in tmp or 'Mosaic' in tmp:
                p_url = ele.xpath('./a/@href')[0]
                
        else:
            break
        if cnt == 3:
            break
    return p_url

def getPreviewImageUrlFromBlogJAV(url):
    
    p_html = get_html(url,header= pic_headers)
    if p_html.status_code != 200:
       print("无法加载blogJAV页面")

    data = etree.HTML(p_html.text)
    image_list = data.xpath('/html/body/div[1]/div/div[1]/main/article/div/div/p[1]/a/img/@data-lazy-src')
    targetImageUrl = image_list[0].replace('thumbs', 'images').replace('/t', '/img')
    return targetImageUrl

def getPreviewImageUrlFromJAVStore(url):
    i_html = get_html(url, header= pic_headers)
    if i_html.status_code != 200:
        print("无法加载javstore页面")
    i_url = ""
    data = etree.HTML(i_html.text)
    image_url = data.xpath('/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/a[1]/@href')
    if len(image_url) ==0 :
        print("未找到javstore图片")
        return i_url
    i_url = image_url[0]
    return i_url

def imageUrlFromBlogJAV(number):
    blog_page_url = findPreviewImagesFromBlogJAV(number)
    preview_url_1 = ""
    if blog_page_url != "":
      preview_url_1 = getPreviewImageUrlFromBlogJAV(blog_page_url)
    return preview_url_1
def imageUrlFromJAVStore(number):
    javstore_page_url = findPreviewImagesFromJAVStore(number)
    preview_url_2 = ""
    if javstore_page_url != "":
      preview_url_2 = getPreviewImageUrlFromJAVStore(javstore_page_url)
    return preview_url_2

def multiThreadToGetUrl(number):
    with ThreadPoolExecutor(max_workers=2) as t:
        obj_list = []
        obj1 = t.submit(imageUrlFromBlogJAV, number)
        obj_list.append(obj1)
        obj2 = t.submit(imageUrlFromJAVStore, number)
        obj_list.append(obj2)
        url_list = []
        for future in as_completed(obj_list):
            url = future.result()
            if url != "":
                url_list.append(url)
        for url in url_list:
            print("Get Preview Image! url is " +url)
        return url_list 

###得到fanzaExtrafanart        
def getExtraFanartFromFANZA(url,cookie):
    options = ChromeOptions()
    proxy = '127.0.0.1:7890'
    options.add_argument(('--proxy-server=' + proxy))
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(1)
    driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td[2]/div[2]/div[1]/div/div[3]/p').click()
    time.sleep(1)
    html = driver.page_source
    
    driver.close()
    data = etree.HTML(html).xpath('/html/body/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/div[1]/div[1]/div[2]')
    
    
  
    url_list = data[0].xpath('//*[@name="sample-image"]/img/@src')
    print(len(url_list))
    print(url_list[0])
   # print(len(data))
def getFanzaTrueUrlbysearchNumber(number):
    url = 'https://www.dmm.co.jp/search/=/searchstr='+number
    f_number = number.replace('-','').lower()
    print(f_number)
    search_htmlcode = get_html(url)
    print(search_htmlcode.status_code)
    if search_htmlcode.status_code != 404 and f_number in search_htmlcode.text:
        s_etree = etree.HTML(search_htmlcode.text)
        true_url = s_etree.xpath('//*[@id="list"]/li[1]/div/p[2]/a/@href')
        if len(true_url) != 0:
            print('成功查找到商品链接')
            return true_url[0]
        else:
            print('未能得到商品链接元素')
    return 404

def getRightNumber(number):
    num = number.upper()
    if '-' in num:
        return num
    index = 0
    while num[index].isdigit():
        index += 1 
    head = index    
    while num[index].isdigit() == False:
             index = index + 1
    prefix = num[head:index]
    suffix = num[index:]
    return prefix + '-' + suffix
if __name__ == '__main__':
    #number = 'MIDV-530'
   # multiThreadToGetUrl(number)
    url = 'https://www.dmm.co.jp/search/=/searchstr=%E3%82%AD%E3%83%A1%E6%81%8B%EF%BC%81%20%E9%AB%98%E5%B6%BA%E3%81%AE%E8%8F%AF%E3%81%A8%E5%B9%BC%E3%81%AA%E3%81%98%E3%81%BF%E3%81%8C%E3%82%AD%E3%83%9E%E3%81%A3%E3%81%9F%E7%90%86%E7%94%B1%20%E4%B8%8A%E5%B7%BB%E9%AD%94%E6%B3%95%E3%81%AE%E8%96%AC%E3%81%A7%E6%81%8B%E3%81%AE%E6%88%90%E5%B0%B1%E3%82%92/limit=30/sort=date/'
    
    
    
    h = get_html(url)
    
    print(h.status_code)
    
    outline = h.xpath('/html/body/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/div[3]/p/story')
    print(len(outline))
    print(outline)
    #h = headers
    #print(headers)
    #cookie = {'Cookie':'notified_popup_id=%2C67; app_uid=Z/6RlWOIviUZaYQR+3BhAg==; secid=2765d77a680079246360d122d7eddce2; login_secure_id=2765d77a680079246360d122d7eddce2; cdp_id=f3IKAYM3GXGnRM3b; cklg=ja; adpf_uid=gszdlLmNTMUxFjCb; guest_id=CwdAXx9XVwdUVFJP; age_check_done=1; is_intarnal=true; i3_ab=7678; mbox=session#1702888502494-604220#1702890428|check#true#1702888628; ckcy=1; _dd_s=logs=1&id=ebadc9ea-b761-4361-b462-e1660d93c264&created=1702888502942&expire=1702889643092'}
    #h.update(cookie)
    #print(h)

   # getExtraFanartFromFANZA(url)
    
    #number = 'midv-530'
    #true_url = getFanzaTrueUrlbysearchNumber(number)
    #url = findPreviewImagesFromJAVStore(number)
    #print(url)

    


