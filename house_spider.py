# -*- coding: utf-8 -*-
import unicodedata

import scrapy

class PhoneSpider(scrapy.Spider):
    name = 'houses'
    api_url = 'http://www.hitad.lk/EN/houses/?page={}'

    start_urls = [api_url.format(0)]

    def parse(self, response):
        ads = response.css('div.detail-sum')
        for ad in ads:
            sections = ad.css('div.col-lg-12')

            type = None
            category = None
            sub_category = None
            location = None
            property_type = None
            for item in sections[1].css('div.item-facets'):
                if 'Property Type' in item.css("::text")[0].extract():
                    property_type = self.preprocess(item.css("::text")[1].extract())
                elif 'Type' in item.css("::text")[0].extract():
                    type = self.preprocess(item.css("::text")[1].extract())
                elif 'Sub Category' in item.css("::text")[0].extract():
                    sub_category = self.preprocess(item.css("::text")[1].extract())
                elif 'Category' in item.css("::text")[0].extract():
                    category = self.preprocess(item.css("::text")[1].extract())

            for item in sections[1].css('div.item-facets2'):
                if 'Location' in item.css("::text")[0].extract():
                    location = self.preprocess(item.css("::text")[1].extract())

            price = self.preprocess(ad.css('span.list-price-value::text').extract_first())

            yield {
                'title': self.preprocess(ad.css('h4::text').extract_first()),
                'published_at': self.process_timestamp(sections[0].css('div.ad-info-2::text')[0].extract()),
                'type': type,
                'category': category,
                'sub_category': sub_category,
                'location': location,
                'property_type': property_type,
                'price': price,
            }

        p = response.url.split('=')[-1]
        yield scrapy.Request(url=self.api_url.format(int(p) + 25), callback=self.parse)

    def process_timestamp(self, str):
        return self.preprocess(str.replace("Date :", ''))

    def preprocess(self, text):
        if text == None: return None
        return unicodedata \
            .normalize('NFKD', text) \
            .encode('ascii', 'ignore') \
            .replace('\n', '').replace('\t', '').strip()
