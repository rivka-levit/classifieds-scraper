# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ClassifiedsItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    properties = scrapy.Field()
    description = scrapy.Field()
