# -*- coding: utf-8 -*-

import re
from lxml import etree
from urllib.parse import urlencode
from .parser import Parser
from selenium.webdriver import ChromeOptions
from selenium import webdriver
from selenium.webdriver.common.by import By
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
    expr_outline = "//div[@class='mg-b20 lh4']/text()"
    expr_outline2 = "//div[@class='mg-b20 lh4']//p"
    expr_outline3 = "//div[@class='clear mg-b20 lh4']//p/text()"
    
    expr_outline_og = '//head/meta[@property="og:description"]/@content'
    expr_runtime = "//td[contains(text(),'収録時間')]/following-sibling::td/text()"

    def search(self, number):
        if 'OVA'in number or re.search(r"[\u3040-\u309F\u30A0-\u30FF]+", number):
            print('[+]是动画名，开始在Fanza搜索')
            self.animeflag = True
        else:
            print('[+]是电影名，开始在Fanza搜索')
        
        self.number = number
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
        '''
        重要补丁，因为里番第一部通常在其系列里面是没有序号的，也就是说搜出系列所有作品都会展示，这里采用时间排序，并把搜索所有结果
        放到一个list中，再进行判断
        '''
        url = 'https://www.dmm.co.jp/search/=/searchstr='+search_number + '/limit=30/sort=date/'
        print('[+]搜索页面URL：'+url)
        '''
        这里f_number特指av番号形式，如果是动画不会影响搜索结果
        '''
        f_number = number
        if self.animeflag :
          print(f'[+]动画标题名{f_number}')
        else:
            f_number = number.replace('-','').lower()
            print(f'[+]Fanza小写番号是 {f_number}')
        search_htmlcode = self.getHtml(url)
        
        if search_htmlcode != 404:#因为有动画名，直接查找是否有满足条件的搜索结果
            print('[+]成功获取搜索结果页面！')
            temp_num = number
            s_etree = etree.HTML(search_htmlcode)
            true_url_list = s_etree.xpath('//*[@class="tmb"]/a/@href')
            title_list = s_etree.xpath('//*[@class="tmb"]/a/span[1]/img/@alt')#span是带省略号的，还有图片标签有简介救大命
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
                    result = ''
                    while index > 0:#倒序循环(才知道python实现倒序循环就是依托还是用倒序实现的，-jh  20231220)
                       index -= 1
                       
                       url = true_url_list[index]
                       print('[+]'+url)
                       
                       title = title_list[index]
                       print('[+]'+title)
                       if 'anime' in url: 
                            if result == '':
                               print(f'[+]成功得到页面url,但暂未未匹配到标题名:  {url}')
                               result = url
                            print(f'[+]商品标题{title}')
                            print(f'[+]待匹配标题{temp_num}')
                            
                            if temp_num in title:
                                print(f'[+]已匹配到标题，URL：{url}')
                                result = url
                                return result
                    if result != '':
                        url = result
                        print(f'[!]未匹配到标题，返回最后带有anime关键词的URL：{url}')
                    else:
                        url = true_url_list[0]
                        print(f'[!]未发现anime关键词，默认返回第一个URL：{url}')
                    return url#最后都没有返回第一个
                else:
                    print('[+]是电影，开始处理...')
                    index = url_count 
                    result = ''
                    while index > 0:#倒序循环(才知道python实现倒序循环就是依托还是只能用while实现的，-jh  20231220)
                       index -= 1
                       
                       url = true_url_list[index]
                       
                       if f_number in url and 'h_' not in url: 
                            if 'dvd' in url :
                                print('[+]成功获得包含番号的url，且包含dvd关键字！')
                                return url
                            if result == '':
                                print('[+]成功获得包含番号的url，暂不包含dvd关键字！')
                                result = url
                       if result == '' and 'dvd' in url:
                            print('[+]未能匹配到包含番号的结果，先获取靠后的包含dvd关键词的结果！')
                            result = url   
                    if result != '':
                        print('[!]未能完全匹配到包含番号的结果，返回满足基本条件的结果！')
                        return result
                    print('[!]未能匹配到标题和dvd关键词，将返回第一个候选结果！')                                                      
                    return true_url_list[0]    
            else:    
                print('[!]未查询到商品结果，请查看刮削名是否正确，或者直接重命名文件') 
                 
        return 404
    
    def getTrueHtmlFromFanza(self,url):
        '''
        得到在fanza打广告期间正确html地址
        '''
        ans = url
        options = ChromeOptions()
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
        driver.get(url)
        #time.sleep(1)
        driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td[2]/div[2]/div[1]/div/div[3]/p').click()
        #time.sleep(1)
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
        flag = 1
        result = self.getTreeElement(htmltree, self.expr_outline).replace("\n", "")
        if result == '':
            result = self.getTreeElement(htmltree, self.expr_outline2)
            if isinstance(result,str):
                result = result.replace("\n", "")
            else:
                result = result.xpath('string(.)').replace("\n", "")
            flag = 2
        if result == '':
            result = self.getTreeElement(htmltree, self.expr_outline3).replace("\n", "")
            flag = 3
        
        print('[!]当前得到的outline简介：'+result)
        if 'STORY' in result:
            
            print('[!]有story标签！')#出现了不该出现的story标签，尝试重新处理编码
            expr = ''
            if flag == 1:#选择成功处理的表达式
                expr = self.expr_outline
            elif flag == 2:
                expr = self.expr_outline2
            else:
                expr = self.expr_outline3
            expr = expr.replace('/text()','')#去除/text()
            ans = htmltree.xpath(expr)
            
            
            ans = etree.tostring(ans[0],encoding='unicode')#手动使用etree.tostring并重编码
            ans = str(re.sub("<.*?>","",ans))
            print('[!]处理story标签成功！')
            result = ans.replace('＜STORY＞', '').strip()
            if len(result) > 0:
                print('[!]去除story,并修改编码')  
            
        if "※ 配信方法によって収録内容が異なる場合があります。" == result:
            result = self.getTreeElement(htmltree, self.expr_outline_og)
        
        return result
        #except:
         #   return ''
    

    def getRuntime(self, htmltree):
        return str(re.search(r'\d+', super().getRuntime(htmltree)).group()).strip(" ['']")

    def getDirector(self, htmltree):
        if "anime" not in self.detailurl:
            return self.getFanzaString('監督：')
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
        results = list(filter(lambda x: x !='サンプル動画' and x != '独占配信' and x != '単体作品' and x != 'Blu-ray（ブルーレイ）' and x != '歳末新春セール' and x !='特典付き・セット商品' and x !='DMM独家' and 'セール' not in x and '独占' not in x and x != 'セル仕様' and 'キャンペーン' not in x,results))
        return results

    def getLabel(self, htmltree):
        ret = self.getFanzaString('レーベル')
        if ret == "----":
            return ''
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
        if self.animeflag:
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
        try:
            data = htmltree.xpath('//*[@id="sample-image-block"]') 
            
        except:
            raise ValueError("can not find image")
        if len(data) != 0:
            url_list = data[0].xpath('//*[@name="package-image"]/img/@src')
            
            if isinstance(url_list,str):
                result = url_list
            else:
                result = url_list[0]
        result = result.replace('s.jpg', 'l.jpg')
        
        return result

    def getExtrafanart(self, htmltree):
        #if "anime" in self.detailurl:
        #    data = htmltree.xpath('/html/body/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/div[6]')
        #else:
        #    data = htmltree.xpath('/html/body/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/div[1]/div[1]/div[2]')
        data = htmltree.xpath('//*[@id="sample-image-block"]') 

        if len(data) != 0:
          url_list = data[0].xpath('//*[@name="sample-image"]/img/@src')
          if len(url_list) != 0:
                l = len(url_list)
                url_template= url_list[0]
                url_cuts = url_template.rsplit('-', 1)

                sheet = []
                for index in range(l):                    
                    
                    sheet.append(url_cuts[0] + 'jp-' + str(index + 1) + '.jpg')
                return sheet
          
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
