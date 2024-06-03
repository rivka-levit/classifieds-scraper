"""
Pipelines for processing items.
"""

from itemadapter import ItemAdapter

from scrapy.exceptions import DropItem


class ClassifiedsRemoveDuplicatesPipeline:
    """Remove duplicate items with repeated title and description."""

    def __init__(self):
        self.title_descr = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if (adapter['title'], adapter['description']) in self.title_descr:
            raise DropItem(f'Duplicate title and description found: {item}')

        self.title_descr.add((item["title"], item["description"]))
        return item


class ClassifiedsRemoveNoPricePipeline:
    """Remove items that don't have a price."""

    def process_item(self, item, spider):  # noqa
        adapter = ItemAdapter(item)
        if not adapter.get('price'):
            raise DropItem(f'Price is missing: {item}')

        return item
