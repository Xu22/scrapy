# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem
from scrapy.http import Request


class DbSpider(scrapy.Spider):
    name = 'db'
    allowed_domains = ['movie.douban.com']
    header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
    #
    start_urls = [
        'https://movie.douban.com/top250',
    ]
    # def start_url(self):
    #     return [Request("https://movie.douban.com/top250",callback=self.parse,meta={"cookiejar":1})]
    def parse(self, response):
        selector = scrapy.Selector(response)
        # 解析出各个电影
        movies = selector.xpath('//div[@class="item"]')
        # 存放电影信息
        item = DoubanItem()

        for movie in movies:

            # 电影各种语言名字的列表
            titles = movie.xpath('.//span[@class="title"]/text()').extract()
            # 将中文名与英文名合成一个字符串
            name = ''
            for title in titles:
                name += title.strip()
            item['name'] = name
            # 电影信息列表
            infos = movie.xpath('.//div[@class="bd"]/p/text()').extract()
            # 电影信息合成一个字符串
            fullInfo = ''
            for info in infos:
                fullInfo += info.strip()
            item['info'] = fullInfo
            # 提取评分信息
            item['rating'] = movie.xpath('.//span[@class="rating_num"]/text()').extract()[0].strip()
            # 提取评价人数
            item['num'] = movie.xpath('.//div[@class="star"]/span[last()]/text()').extract()[0].strip()[:-3]
            # 提取经典语句，quote可能为空
            quote = movie.xpath('.//span[@class="inq"]/text()').extract()
            if quote:
                quote = quote[0].strip()
            else:
                quote = ' '
            item['quote'] = quote
            # 提取电影图片
            item['img_url'] = movie.xpath('.//img/@src').extract()[0].strip()

            yield item

        next_page = selector.xpath('//span[@class="next"]/a/@href').extract()

        if next_page:
            url = 'https://movie.douban.com/top250' + next_page[0]
            yield scrapy.Request(url, callback=self.parse,dont_filter=False)
    # def next(self,response):
    #     print("此时已经登陆完成并爬取了个人中心的数据")
    #     title=response.xpath("/html/head/title/text()").extract()
    #     note=response.xpath("//div[@class='note']/p/text()").extract()
    #     print(title[0])
    #     print(note[0])