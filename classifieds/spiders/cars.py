import scrapy

from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from classifieds.items import ClassifiedsItem


class CarsSpider(scrapy.Spider):
    name = "cars"
    allowed_domains = ["www.classifieds.co.zw"]
    start_urls = ["https://www.classifieds.co.zw/zimbabwe-cars-vehicles/Toyota"]
    # rules = (
    #     Rule(
    #         LinkExtractor(
    #             restrict_xpaths='//div[@class="listings"]'
    #
    #         ),
    #         callback='parse',
    #         follow=False
    #     ),
    # )

    def parse(self, response, **kwargs):
        gallery = response.xpath('//div[contains(@id, "listing-")]')
        print(len(gallery))

        for listing in gallery:

            item = ItemLoader(
                ClassifiedsItem(),
                response=response,
                selector=listing
            )
            item.add_xpath(
                'title',
                './/div[contains(@class, "details")]/'
                'h5[@class="listing-title"]/a/text()'
            )
            item.add_xpath(
                'price',
                '//div[contains(@class, "price")]/div[@class="amount"]'
                '/div[contains(@class, "usd-price-tooltip")]/text()'
            )
            item.add_xpath(
                'properties',
                './/div[contains(@class, "properties")]/ul/li[@class="property"]'
                '/text()'
            )
            item.add_xpath(
                'description',
                '//div[@class="line-clamp-3"]/p/text()'
            )

            yield item.load_item()
