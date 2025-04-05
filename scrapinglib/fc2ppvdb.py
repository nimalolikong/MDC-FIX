# -*- coding: utf-8 -*-

import re
from lxml import etree
from .httprequest import request_session
from .parser import Parser


class Fc2ppvdb(Parser):
    source = 'msin'
    expr_number = '//div[contains(text(),"ID：")]/span/text()'
    expr_title = '/html/body/div[1]/div/div/main/div/section/div/div[1]/div[2]/h2/a/text()'
    
    expr_studio = '//div[contains(text(),"販売者：")]/span/a/text()'
    expr_director = '//div[contains(text(),"販売者：")]/span/a/text()'
    expr_actor = '//div[contains(text(),"女優：")]/span/a/text()'
    expr_label = '//div[contains(text(),"販売者：")]/span/a/text()'
    expr_series = '//div[contains(text(),"販売者：")]/span/a/text()'
    expr_release = '//div[contains(text(),"販売日：")]/span/text()'
    expr_cover = '/html/body/div[1]/div/div/main/div/section/div/div[1]/div[1]/a/img/@src'
    expr_tags = '//div[contains(text(),"タグ：")]/span/a/text()'
    expr_genres = '//div[contains(text(),"タグ：")]/span/a/text()'
    expr_runtime = "//div[contains(text(),'収録時間')]/span/text()"
    # expr_outline = '//p[@class="fo-14"]/text()'
    # expr_extrafanart = '//*[@class="item-nav"]/ul/li/a/img/@src'
    # expr_extrafanart2 = '//*[@id="cart_quantity"]/table/tr[3]/td/div/a/img/@src'

    # def extraInit(self):
    #    self.imagecut = 4

    def search(self, number: str):
        self.number = number.lower().replace('fc2-ppv-', '').replace('fc2-', '')
        self.detailurl = 'https://fc2ppvdb.com/articles/' + self.number
        self.htmlcode = self.getHtml(self.detailurl)
        if self.htmlcode != 404:        
            htmltree = etree.HTML(self.htmlcode)    
            result = self.dictformat(htmltree)
            return result
        return 404
    def getDirector(self, htmltree):
        director =  super().getDirector(htmltree)
        print(director)
        return director
    def getStudio(self, htmltree):
        studio = super().getStudio(htmltree)
        print(studio)
        return studio
    
    def getActors(self, htmltree):
        actors = htmltree.xpath(self.expr_actor)
        if actors == None:
            actors = []
        if actors == []:
            actors = self.getDirector(htmltree)
        print(actors)
        return actors

    def getTags(self, htmltree) -> list:
        

        tags = htmltree.xpath(self.expr_tags)
    
        print(tags)
        return tags

    def getRelease(self, htmltree):
        release = super().getRelease(htmltree)
        print(release)
        return release

    def getCover(self, htmltree):
        cover = super().getCover(htmltree)
        print(cover)
        return cover

    def getNum(self, htmltree):
        return 'FC2-PPV-' + self.number
    
    def getRuntime(self, htmltree):
        runtime = super().getRuntime(htmltree)
        print(runtime)
        if runtime != None:
            time = runtime.split(':')

            if(len(time) == 2):
                minutes = int(time[0])
                seconds = int(time[1])
                runtime = minutes
            elif(len(time) == 3):
                hours = int(time[0])
                minutes = int(time[1])
                seconds = int(time[2])
                runtime = hours * 60 + minutes
            return runtime
        return runtime
        
