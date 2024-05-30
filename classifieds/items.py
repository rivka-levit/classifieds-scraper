import scrapy


class ClassifiedsItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    properties = scrapy.Field()
    description = scrapy.Field()
