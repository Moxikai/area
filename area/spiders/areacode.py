# -*- coding: utf-8 -*-
import scrapy

from scrapy.loader import ItemLoader

from area.items import AreaItem

class AreacodeSpider(scrapy.Spider):
    name = "areacode"
    allowed_domains = ["mca.gov.cn"]
    start_urls = (
        'http://www.mca.gov.cn/article/sj/tjbz/a/2016/201603/201604281751.html',
    )

    def parse(self, response):
        """解析表格行"""
        tr_list = response.xpath('//tr[@height="19"]')
        for tr in tr_list:
            code = tr.xpath('td[@class="xl72"][1]/text()').extract_first()
            name0 = tr.xpath('td[@class="xl72"][2]/text()').extract_first()
            name1 = tr.xpath('td[@class="xl72"][2]/font/text()').extract_first()
            name = name0 if name0 else name1 # name0,name1二选一
            data = self.parseCode(**{'code':code,'name':name})
            yield data



    def parseCode(self,**kwargs):
        """获取级别,及上级代码"""
        # 剔除直辖市
        # 截取前两位字母
        first_code = kwargs['code'][:2]
        third_code = kwargs['code'][-2:] # 第三组数字
        second_code = kwargs['code'][-4:-2]
        if first_code in ['11','12','31','50']:
            # 截取最后两位
            if third_code != '00':
                kwargs['level'] = 3
                kwargs['code_highlevel'] = first_code+'0000'
                return kwargs
            else:
                kwargs['level'] = 1
                kwargs['code_highlevel'] = ''
        else:
            #检测第三极位置
            third_code = int(kwargs['code'][-2:]) # 截取最后两位
            if third_code != '00':
                #第三层级
                kwargs['level'] = 3
                kwargs['code_highlevel'] = kwargs['code'][:-2]+'00'
                return kwargs

            if second_code != '00':
                #第二层级
                level = 2
                code_highlevel = first_code+'0000'
                return (level,code_highlevel)
            kwargs['level'] = 1
            kwargs['code_highlevel'] = ''
            return kwargs






