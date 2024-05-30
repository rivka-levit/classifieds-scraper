import scrapy


class CarsSpider(scrapy.Spider):
    name = "cars"
    allowed_domains = ["www.classifieds.co.zw"]
    start_urls = ["https://www.classifieds.co.zw/zimbabwe-cars-vehicles"]

    def parse(self, response, **kwargs):
        pass
