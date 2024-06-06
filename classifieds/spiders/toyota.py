import scrapy

from scrapy.loader import ItemLoader

from classifieds.items import ClassifiedsItem


class ToyotaSpider(scrapy.Spider):
    name = "toyota"
    allowed_domains = ["www.classifieds.co.zw"]
    start_urls = ["https://www.classifieds.co.zw/zimbabwe-cars-vehicles/Toyota"]

    def parse(self, response, **kwargs):
        gallery = response.xpath('//div[contains(@id, "listing-")]')  # noqa

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
                './/div[contains(@class, "price")]/div[@class="amount"]'
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

        next_page = response.xpath(
            '//div[@class="footer-nav"]/ul[@class="pagination"]'
            '/li[contains(@class, "active")]/following-sibling::li/a/text()'
        ).get()

        if next_page:
            url = f'https://www.classifieds.co.zw/zimbabwe-cars-vehicles/Toyota?page={next_page}'

            yield response.follow(url, callback=self.parse)
