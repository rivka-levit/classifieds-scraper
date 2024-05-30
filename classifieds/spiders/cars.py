import scrapy

from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from classifieds.items import ClassifiedsItem


class CarsSpider(CrawlSpider):
    name = "cars"
    allowed_domains = ["www.classifieds.co.zw"]
    start_urls = ["https://www.classifieds.co.zw/zimbabwe-cars-vehicles/Toyota"]
    rules = (
        Rule(
            LinkExtractor(
                restrict_xpaths='//div[@class="listings"]'

            ),
            callback='parse',
            follow=True
        ),
    )

    def parse(self, response, **kwargs):
        pass
