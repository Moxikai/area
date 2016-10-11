# -*- coding: utf-8 -*-
import scrapy

from scrapy.loader import ItemLoader
from scrapy import FormRequest,Request

from area.items import AreaItem

class AreacodeSpider(scrapy.Spider):
    name = "areacode"
    #allowed_domains = ["mca.gov.cn"]
    start_urls = (
        'http://www.mca.gov.cn/article/sj/tjbz/a/2016/201603/201604281751.html',
    )
    post_url = 'http://127.0.0.1:8080/area/update'
    def parse(self, response):
        """解析表格行"""
        tr_list = response.xpath('//tr[@height="19"]')
        for tr in tr_list:
            code = tr.xpath('td[@class="xl72"][1]/text()').extract_first()
            name0 = tr.xpath('td[@class="xl72"][2]/text()').extract_first()
            name1 = tr.xpath('td[@class="xl72"][2]/font/text()').extract_first()
            name = name0 if name0 else name1 # name0,name1二选一
            if code:
                data = self.parseCode(code)
                yield Request(url=self.post_url,
                              meta={'area':{
                                  'code':code,
                                            'area_name':name,
                                            'level': data[0],
                                            'code_highlevel':data[1]
                              }},
                              dont_filter=True,
                              callback=self.postToServer,)


    def postToServer(self,response):
        """提交到服务器"""
        csrf_token = response.xpath('//input[@id="csrf_token"]/@value').extract_first()
        print csrf_token
        formdata = response.meta['area']
        formdata['csfr_token'] = csrf_token
        formdata['submit'] = 'submit'
        return FormRequest.from_response(response=response,formdata=formdata)
        
    
    def parseCode(self,code):
        """获取级别,及上级代码"""
        first = code[:2]
        second = code[2:4]
        third = code[4:]

        if first in ['11','12','31','50']:
            print '这是直辖市区域'
            if third != '00':
                print '这是直辖市辖区'
                return ('3',first+'0000')
            else:
                print '直辖市'
                return ('1','')
        else:
            print '这是非直辖市区域'
            if third != '00':
                print '这是非直辖市3级区域'
                return ('3',first+second+'00')
            elif second != '00':
                print '这是非直辖市2级区域'
                return ('2',first+'0000')
            else:
                print '这是非直辖市1级'
                return ('1','')







