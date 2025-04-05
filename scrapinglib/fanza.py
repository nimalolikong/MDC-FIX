# -*- coding: utf-8 -*-

import re
from lxml import etree
from urllib.parse import urlencode
from .parser import Parser
from selenium.webdriver import ChromeOptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from urllib.parse import  quote
class Fanza(Parser):
    source = 'fanza'
    #在每个网站内判断是不是动画
    animeflag = False
    expr_title = '//*[starts-with(@id, "title")]/text()'
    expr_actor = "//td[contains(text(),'出演者')]/following-sibling::td/span/a/text()"
    # expr_cover = './/head/meta[@property="og:image"]/@content'
    expr_extrafanart = '//a[@name="sample-image"]/img/@src'
    expr_outline = "//div[@class='mg-b20 lh4']"
    expr_outline2 = "//div[@class='mg-b20 lh4']//p"
    expr_outline3 = "//div[@class='clear mg-b20 lh4']//p"
    
    expr_outline_og = '//head/meta[@property="og:description"]/@content'
    expr_runtime = "//td[contains(text(),'収録時間')]/following-sibling::td/text()"

    def search(self, number):
        self.cookies = {"age_check_done": "1"}
        if 'OVA'in number or re.search(r"[\u3040-\u309F\u30A0-\u30FF]", number) or ' ' in number:
            print('[+]是动画名，开始在Fanza搜索')
            self.animeflag = True
        else:
            print('[+]是电影名，开始在Fanza搜索')
        
        self.number = number
        self.oldMatchFlag = False
        self.outnumber = number
        if self.specifiedUrl:
            self.detailurl = self.specifiedUrl
            durl = "https://www.dmm.co.jp/age_check/=/declared=yes/?"+ urlencode({"rurl": self.detailurl})
            print(durl)
            self.htmltree = self.getHtmlTree(durl)
            result = self.dictformat(self.htmltree)
            return result
        # fanza allow letter + number + underscore, normalize the input here
        # @note: I only find the usage of underscore as h_test123456789
        #fanza_search_number = number
        
        #if fanza_search_number.startswith("h-"):
        #    fanza_search_number = fanza_search_number.replace("h-", "h_")
        #fanza_search_number = re.sub(r"[^0-9a-zA-Z_]", "", fanza_search_number).lower()
        
        page_url = self.getFanzaTrueUrlbySearchNumber(number)
        self.detailurl = page_url
        '''
        修改为直接搜索number返回正确url

        '''
        
        url = "https://www.dmm.co.jp/age_check/=/declared=yes/?"+ urlencode({"rurl": self.detailurl})
        self.htmlcode = self.getHtml(url)
        if self.htmlcode != 404 \
                and 'Sorry! This content is not available in your region.' not in self.htmlcode:
            if 'fn-popup' in self.htmlcode:
                self.htmlcode = self.getTrueHtmlFromFanza(url)
            self.htmltree = etree.HTML(self.htmlcode)
            if self.htmltree is not None:
               result = self.dictformat(self.htmltree)
               return result
        return 404
    
        
    def getFanzaTrueUrlbySearchNumber(self,number):

        '''
        搜索前先进行httpurl-string格式转换
        只影响日语字符
        '''
        search_number = quote(number)#使用quote函数进行转换
        result = ''
        '''
        重要补丁，因为里番第一部通常在其系列里面是没有序号的，也就是说搜出系列所有作品都会展示，这里采用时间排序，并把搜索所有结果
        放到一个list中，再进行判断
        '''
        page_url = 'https://www.dmm.co.jp/search/=/searchstr='+search_number + '/limit=30/sort=date'
        search_url = "https://www.dmm.co.jp/age_check/=/declared=yes/?"+ urlencode({"rurl": page_url})
        print('[+]搜索页面URL：'+search_url)
        oprofile = webdriver.FirefoxOptions()
        oprofile.accept_insecure_certs = True
        oprofile.page_load_strategy = 'eager'
        oprofile.add_argument('--headless')
        oprofile.add_argument('--disable-gpu')
        oprofile.add_argument('--window-size=1920x1080')
        oprofile.set_preference("network.proxy.type", 1)
        oprofile.set_preference("network.proxy.http", "127.0.0.1")
        oprofile.set_preference("network.proxy.http_port", 7890)
        oprofile.set_preference('network.proxy.socks', '127.0.0.1')
        oprofile.set_preference('network.proxy.socks_port', 7890)
        oprofile.set_preference('network.proxy.socks_remote_dns', False)
        oprofile.set_preference("network.proxy.ssl", "127.0.0.1")
        oprofile.set_preference("network.proxy.ssl_port", 7890)
        driver = webdriver.Firefox(options=oprofile)
        driver.get(search_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "mx-3") and contains(@class, "mt-1.5")]/a[2]')))
        '''
        这里f_number特指av番号形式，如果是动画不会影响搜索结果
        '''
        f_number = number
        if self.animeflag :
          print(f'[+]动画标题名{f_number}')
        else:
            f_number = number.replace('-','').lower()
            print(f'[+]Fanza小写番号是 {f_number}')
        
        if driver.page_source:#因为有动画名，直接查找是否有满足条件的搜索结果
            print('[+]成功获取搜索结果页面！')
            temp_num = number
            true_url_list_ele = driver.find_elements(By.XPATH, '//div[contains(@class, "mx-3") and contains(@class, "mt-1.5")]/a[2]')
            true_url_list = [true_url_list_ele.__getattribute__('get_attribute')('href') for true_url_list_ele in true_url_list_ele]
            title_list = driver.find_elements(By.XPATH, '//div[contains(@class, "mx-3") and contains(@class, "mt-1.5")]/a[2]/p')#更新fanza新匹配规则
            url_count = len(true_url_list)
            if len(title_list)== url_count:
                print('[+]商品标题名和URL个数对应')
            else:
                print('[!]标题名个数和URL个数不匹配！请检查代码！')
            print(f'[+]在Fanza搜到了{url_count}个结果')   
            if url_count != 0:
                if self.animeflag:
                    print('[+]是动画,将最后开始寻找最后包含anime关键字的url')
                    index = url_count 
                    while index > 0:#倒序循环(才知道python实现倒序循环就是依托还是用倒序实现的，-jh  20231220)
                       index -= 1
                       
                       url = true_url_list[index]
                       print('[+]'+url)
                       
                       title = title_list[index].text
                       print('[+]'+title)
                       if 'anime' in url and 'mono' in url: 
                            if result == '':
                               print(f'[+]成功得到页面url,但暂未未匹配到标题名:  {url}')
                               result = url
                            print(f'[+]商品标题{title}')
                            print(f'[+]待匹配标题{temp_num}')
                            
                            if temp_num in title and '限定版' not in title:
                                print(f'[+]已匹配到标题，URL：{url}')
                                result = url
                                break
                    if result == '':
                        result = true_url_list[0]
                        print(f'[!]未匹配到标题，返回第一个URL：{result}')
                else:
                    print('[+]是电影，开始处理...')
                    index = url_count 
                    while index > 0:#倒序循环(才知道python实现倒序循环就是依托还是只能用while实现的，-jh  20231220)
                       index -= 1
                       
                       url = true_url_list[index]
                       title = title_list[index].text

                       if f_number in url and 'h_' not in url: 
                            if 'dvd' in url :
                                if 'ブルーレイディスク' in title and result == '':
                                    print('[+]成功获得包含番号和dvd关键词的url，且是蓝光，不优先刮削！')
                                    result = url
                                else:
                                    print('[+]成功获得包含番号和dvd关键词的url，且是DVD，优先刮削！')
                                    result = url
                                    break
                            if result == '':
                                print('[+]成功获得包含番号的url，暂不包含dvd关键字！')
                                result = url
                       if result == '' and 'dvd' in url:
                            print('[+]未能匹配到包含番号的结果，先获取靠后的包含dvd关键词的结果！')
                            result = url   
                    if result == '':
                        print('[!]未能匹配到包含番号和dvd关键词的结果，将返回第一个候选结果！')         
                        result = true_url_list[0]
        if result == '':
            print('[!]未查询到商品结果，请查看刮削名是否正确，或者直接重命名文件') 
        driver.close()
        return result
    
    def getTrueHtmlFromFanza(self,url):
        '''
        得到在fanza打广告期间正确html地址
        '''
        ans = url
        oprofile = webdriver.FirefoxOptions()
        oprofile.accept_insecure_certs = True
        oprofile.page_load_strategy = 'eager'
        oprofile.set_preference("network.proxy.type", 1)
        oprofile.set_preference("network.proxy.http", "127.0.0.1")
        oprofile.set_preference("network.proxy.http_port", 7890)
        oprofile.set_preference('network.proxy.socks', '127.0.0.1')
        oprofile.set_preference('network.proxy.socks_port', 7890)
        oprofile.set_preference('network.proxy.socks_remote_dns', False)
        oprofile.set_preference("network.proxy.ssl", "127.0.0.1")
        oprofile.set_preference("network.proxy.ssl_port", 7890)
        driver = webdriver.Firefox(options=oprofile)
        """"
        options = ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--disable-gpu')
        '''
        默认使用http代理，如果开启其他代理请自行修改源码
        '''
        proxy = self.proxies['http'].replace('http://','')
        print('[+]Selenuim 代理已经连通，地址：'+proxy)
        options.add_argument(('--proxy-server=' + proxy))
        '''
        有时会反复进行ssl连接,请查看是否开启了全局连接
        '''
        driver = webdriver.Chrome(options=options)
        """
        driver.get(url)
        #time.sleep(1)
        #driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td[2]/div[2]/div[1]/div/div[3]/p').click()
        #time.sleep(1)
        driver.find_element(By.XPATH,'//p[contains(@class,"btn-close")]').click()
        ans = driver.page_source

        driver.close()
        return ans
    def getAnimeFlag(self):
            
        return self.animeflag     
        
        
        
    def getAnimeNum(self,htmltree):
        return self.getFanzaString('品番：')
    def getNum(self, htmltree):
        # for some old page, the input number does not match the page
        # for example, the url will be cid=test012
        # but the hinban on the page is test00012
        # so get the hinban first, and then pass it to following functions
        
        self.fanza_hinban = self.getFanzaString('品番：')
        self.number = self.fanza_hinban
        number_lo = self.number.lower()
        if (re.sub('-|_', '', number_lo) == self.fanza_hinban or
            number_lo.replace('-', '00') == self.fanza_hinban or
            number_lo.replace('-', '') + 'so' == self.fanza_hinban
        ):
            self.number = self.number
        
        return self.outnumber

    def getStudio(self, htmltree):
        return self.getFanzaString('メーカー')

    def getOutline(self, htmltree):
        #try:
        
        result = self.getTreeElement(htmltree, self.expr_outline)

        if result == '':
            result = self.getTreeElement(htmltree, self.expr_outline2)
            
        if result == '':
            result = self.getTreeElement(htmltree, self.expr_outline3)
        
        if isinstance(result,str):
            result = result.replace("\n", "")
        else:
            result = result.xpath('string(.)').replace("\n", "")    
        if "「コンビニ受取」" in result:
            index = result.find("「コンビニ受取」")
            result = result[:index]
            result.strip()
        if "商品について" in result:
            index = result.find("商品について")
            result = result[index+8:]
            result.strip()
        print('[!]当前得到的outline简介：'+result)
        
            
        if "※ 配信方法によって収録内容が異なる場合があります。" == result:
            result = self.getTreeElement(htmltree, self.expr_outline_og)
        
        return result
        #except:
         #   return ''
    

    def getRuntime(self, htmltree):
        print("[!]获取runtime播放时长")
        runtime_tmp = re.search(r'\d+', super().getRuntime(htmltree))
        print("[!]匹配runtime结构：")
        print(runtime_tmp)

        if runtime_tmp != None:
            
            runtime = str(runtime_tmp.group()).strip(" ['']")
            print("播放时长："+runtime)
            return runtime

        else:
            return ""

    def getDirector(self, htmltree):
        if "anime" not in self.detailurl:
            return self.getFanzaString('監督：')
        elif self.getLabel(htmltree) == 'ばにぃうぉ～か～' or self.getLabel(htmltree) == 'あんてきぬすっ':
            return '雷火剣'
        return ''

    
    def getActors(self, htmltree):
        if "anime" in self.detailurl:
            return self.getLabel(htmltree)
        return super().getActors(htmltree)
        

    def getRelease(self, htmltree):
        result = ''
        if 'dvd' in self.detailurl:
            result = self.getFanzaString('発売日：')
        elif 'rental' in self.detailurl:
            result = self.getFanzaString('貸出開始日：')
        elif 'anime' in self.detailurl:
            result = self.getFanzaString('発売日：')
            if result == '' or result == '----':
               print('[!]未找到発売日，尝试寻找配信開始日')
               result = self.getFanzaString('配信開始日：')
               if result == '' or result == '----':
                   print('[!]未找到配信開始日')
        elif result == '' or result == '----':
            result = self.getFanzaString('配信開始日：')
            
        return result.replace("/", "-").strip('\\n')

    def getTags(self, htmltree):
        results =  self.getFanzaStrings('ジャンル：')#去除无效信息tag,待增加

        results = list(filter(lambda x: x !='サンプル動画' and x != '独占配信' and x != '単体作品' and x != 'Blu-ray（ブルーレイ）' and x != '歳末新春セール' and x !='特典付き・セット商品' and x !='DMM独家' and 'セール' not in x and '独占' not in x and x != 'セル仕様' and 'キャンペーン' not in x and '大感謝祭' not in x,results))
        if self.animeflag == True:
          maker = self.getLabel(htmltree)  
          if maker != '':
            results.append(maker)
        return results

    def getLabel(self, htmltree):
        ret = self.getFanzaString('レーベル')
        if ret == "----":
            return ''
        if ret == "Queen Bee（メディアバンク）":
            ret = "Queen Bee"
        if ret == "King Bee（メディアバンク）":
            ret = "King Bee"
        if ret == "Pink Pineapple":
            ret = "ピンクパイナップル"
        return ret


    def getSeries(self, htmltree):
        ret = self.getFanzaString('シリーズ：')
        if ret == "----":
            return ''
        return ret
    
    """ 
    def getCover(self, htmltree):
        cover_number = self.number
        try:
            result = htmltree.xpath('//*[@id="' + cover_number + '"]/@href')[0]
        except:
            # sometimes fanza modify _ to \u0005f for image id
            if "_" in cover_number:
                cover_number = cover_number.replace("_", r"\u005f")
            try:
                result = htmltree.xpath('//*[@id="' + cover_number + '"]/@href')[0]
            except:
                # (TODO) handle more edge case
                # print(html)
                # raise exception here, same behavior as before
                # people's major requirement is fetching the picture
                raise ValueError("can not find image")
        return result
     """
    def getCover(self, htmltree):
        result = ""
        print('[!]开始下载封面...')
        if self.animeflag:
            print('[!]是动画，尝试旧版匹配...')
            cover_number = self.number
            try:
                result = htmltree.xpath('//*[@id="' + cover_number + '"]/@href')[0]
            except:
                # sometimes fanza modify _ to \u0005f for image id
                if "_" in cover_number:
                    cover_number = cover_number.replace("_", r"\u005f")
                try:
                    result = htmltree.xpath('//*[@id="' + cover_number + '"]/@href')[0]
                except:
                    print('[!]旧版匹配cover失败！启用新版匹配。')
            if result != '':
                print('[!]旧版匹配cover成功！')
                return result
        print('[!]尝试新版匹配...')
        try:
            data = htmltree.xpath('//*[@id="sample-image-block"]') 
            
        except:
            raise ValueError("can not find image")
        if len(data) != 0:
            print('[!]尝试懒加载检测...')
            pkg_url = data[0].xpath('//*[@name="package-image"]/img/@data-lazy')
            
            result = ''
            if isinstance(pkg_url,str) and 'ps.jpg' in pkg_url:
                result = pkg_url
                print('[!]是懒加载，封面缩略图链接为：'+result)
            elif isinstance(pkg_url,list) and pkg_url != []:
                for u in pkg_url:
                        if 's.jpg' in u:
                            result = u
                            print('[!]是懒加载，封面缩略图链接为：'+result)
                            break
                
            elif result == '':
                print('[!]尝试正常加载检测...')
                pkg_url = data[0].xpath('//*[@name="package-image"]/img/@src')
                
                    
                    
                        
                
                if isinstance(pkg_url,str):
                    result = pkg_url 
                    print('[!]是正常加载，封面缩略图链接为：'+result)   
                else:
                    
                    for u in pkg_url:
                        if 's.jpg' in u:
                            result = u
                            print('[!]是正常加载，封面缩略图链接为：'+result)
                            break
        
        result = result.replace('s.jpg', 'l.jpg')
        print('[!]封面缩略图链接为：'+result)
        return result

    def getExtrafanart(self, htmltree):
        #if "anime" in self.detailurl:
        #    data = htmltree.xpath('/html/body/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/div[6]')
        #else:
        #    data = htmltree.xpath('/html/body/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/div[1]/div[1]/div[2]')
        data = htmltree.xpath('//*[@id="sample-image-block"]') 
        print('[!]开始刮削截图...')
        if len(data) != 0:                    
          lazy_url_list = data[0].xpath('//*[@name="sample-image"]/img/@data-lazy')
          tmp_images_list = data[0].xpath('//*[@name="sample-image"]/img/@src')
          
          true_images_list = []
          for url in tmp_images_list:
              if "dummy_ps.gif" not in url:
                  true_images_list.append(url)
          for url in lazy_url_list:
              if url not in true_images_list:
                  true_images_list.append(url)
          
          if true_images_list == []:
              print("[!]刮削extrafanart失败")   
              return ''
          results = []
          for img_url in true_images_list:
                    url_cuts = img_url.rsplit('-', 1)
                    results.append(url_cuts[0] + 'jp-' + url_cuts[1])
          
          
          
          return results
        
        print("[!]刮削extrafanart失败")
        return ''

    def getTrailer(self, htmltree):
        htmltext = re.search(r'<script type=\"application/ld\+json\">[\s\S].*}\s*?</script>', self.htmlcode)
        if htmltext:
            htmltext = htmltext.group()
            url = re.search(r'\"contentUrl\":\"(.*?)\"', htmltext)
            if url:
                url = url.group(1)
                url = url.rsplit('_', 2)[0] + '_mhb_w.mp4'
                return url
        return ''

    def getFanzaString(self, expr):
        result1 = str(self.htmltree.xpath("//td[contains(text(),'"+expr+"')]/following-sibling::td/a/text()")).strip(" ['']")
        result2 = str(self.htmltree.xpath("//td[contains(text(),'"+expr+"')]/following-sibling::td/text()")).strip(" ['']")
        return result1+result2

    def getFanzaStrings(self, string):
        result1 = self.htmltree.xpath("//td[contains(text(),'" + string + "')]/following-sibling::td/a/text()")
        if len(result1) > 0:
            return result1
        result2 = self.htmltree.xpath("//td[contains(text(),'" + string + "')]/following-sibling::td/text()")
        return result2
    def getTitle(self, htmltree):
        result = htmltree.xpath(self.expr_title)
        if len(result) == 0:
            return ''
        
        title= str(re.sub("\【.*?\】","",result[0]))
        if "（ブルーレイディスク）" in title:#不想要蓝光标识和后面的内容
            index = title.find("（")
            title = title[:index]
            title.strip()
        return title.replace('セル版','').strip()
