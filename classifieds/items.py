import scrapy

from itemloaders.processors import MapCompose, Join


def clean(s):
    return s[0].strip().replace('\t', '').replace('\n', '').replace(u'\xa0', u' ').strip('\t')


def clean_prop(s):
    return s.strip().replace('\t', '').replace('\n', '').replace(u'\xa0', u' ').strip('\t')


class ClassifiedsItem(scrapy.Item):
    title = scrapy.Field(
        output_processor=clean
    )
    price = scrapy.Field(
        output_processor=clean
    )
    properties = scrapy.Field(
        input_processor=MapCompose(clean_prop),
        output_processor=Join(', ')
    )
    description = scrapy.Field(
        output_processor=clean
    )
