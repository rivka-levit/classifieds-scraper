import scrapy

from itemloaders.processors import MapCompose, Join


def clean(s):
    """
    Clean data. Get rid of spaces, tabs, end lines. Flatten list to a string.

    Args:
        s (list): list with one string value received from item loader

    Returns:
        str: cleaned string
    """

    return s[0].strip().replace('\t', '').replace('\n', '').replace(u'\xa0', u' ')


def clean_prop(s):
    """
    Clean data. Get rid of spaces, tabs, end lines.

    Args:
        s (str): value received from item loader

    Returns:
        str: cleaned string
    """

    return s.strip().replace('\t', '').replace('\n', '').replace(u'\xa0', u' ')


def clean_price(p):
    """
    Clean price. Get rid of `$` and `,`

    Args:
        p (list): list with one string value received from item loader

    Returns:
        str: cleaned string with price ready to be converted to float
    """

    return (p[0].strip().replace('$', '').replace(',', '').replace('\t', '').
            replace('\n', '').replace(u'\xa0', u' '))


class ClassifiedsItem(scrapy.Item):
    title = scrapy.Field(
        output_processor=clean
    )
    price = scrapy.Field(
        output_processor=clean_price
    )
    properties = scrapy.Field(
        input_processor=MapCompose(clean_prop),
        output_processor=Join(', ')
    )
    description = scrapy.Field(
        output_processor=clean
    )
