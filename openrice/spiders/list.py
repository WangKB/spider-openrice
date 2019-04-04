# -*- coding: utf-8 -*-
import scrapy
from urllib import parse


class ListSpider(scrapy.Spider):
    name = 'list'

    def start_requests(self):
        district_list = ["香港島", "九龍", "新界", "離島"]
        # 10008亚洲菜,10003粵菜,10011西餐,10013中南美菜,10002中菜
        category_group_list = [
            10011,
            10013,
            10002,
            10003,
            10008
        ]
        url_template = "https://www.openrice.com/zh/hongkong/restaurants/district/{}?categoryGroupId={}&page=1"
        # url_template = "https://www.douban.com/{}{}"
        for district in district_list:
            for category_group in category_group_list:
                yield scrapy.Request(url=url_template.format(district, category_group), callback=self.parse)

    def parse(self, response):
        # save file
        self.log(response.url)
        query_dict = dict(parse.parse_qsl(parse.urlsplit(response.url).query))
        category_group = query_dict["categoryGroupId"]
        page = query_dict["page"]
        district = parse.unquote(parse.urlsplit(response.url).path.split("/")[-1])
        filename = "./data/list/list-{}-{}-{}.html".format(district, category_group, page)
        self.log(filename)
        with open(filename, 'wb') as f:
            f.write(response.body)
        # extract data
        for restaurant in response.css('h2.title-name'):
            self.log(restaurant)
            yield {
                'name': restaurant.css('a::text').get(),
                'url': restaurant.css('a::attr("href")').get()
            }
        # next page
        next_page = response.css('a.pagination-button.next.js-next::attr("href")').get()
        self.logger.debug("net_page:{}".format(next_page))
        if next_page is not None:
            yield response.follow(next_page, self.parse)
