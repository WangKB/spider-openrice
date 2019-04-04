# -*- coding: utf-8 -*-
import csv

import scrapy


class DetailSpider(scrapy.Spider):
    name = 'detail'

    def start_requests(self):
        host = "https://www.openrice.com{}"
        with open('links.csv', newline='', encoding="utf8") as links_file:
            links_reader = csv.DictReader(links_file)
            for row in links_reader:
                print(row["name"])
                yield scrapy.Request(url=host.format(row["url"]), callback=self.parse, meta={'name': row["name"]})

    def parse(self, response):
        name = response.meta.get('name')
        filename = "./data/detail/detail-{}.html".format(name)
        self.log(filename)
        with open(filename, 'wb') as f:
            f.write(response.body)
        # extract data
        labels = response.css('div.header-poi-categories a::text').getall()
        detail = {
            'name': response.css('div.poi-name span.name::text').get(),
            'sub_name': response.css('div.smaller-font-name::text').get(),
            'score': response.css('div.header-score::text').get(),
            'price': response.css('div.header-poi-price a::text').get(),
            'labels': "/".join(labels),
            'introduction': response.css('section.introduction-section div.content::text').get(),
            'address': response.css('div.address-info-section div.content a::text').get(),
        }
        for key, value in detail.items():
            if value is not None:
                detail[key] = value.strip()
        yield detail
