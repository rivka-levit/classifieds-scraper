# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from scrapy.exceptions import DropItem


class ClassifiedsRemoveDuplicatesPipeline:
    def __init__(self):
        self.title_descr = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if (adapter['title'], adapter['description']) in self.title_descr:
            raise DropItem(f'Duplicate title and description found: {item}')

        self.title_descr.add((item["title"], item["description"]))
        return item


class ClassifiedsRemoveNoPricePipeline:
    def process_item(self, item, spider):  # noqa
        adapter = ItemAdapter(item)
        if not adapter.get('price'):
            raise DropItem(f'Price is missing: {item}')

        return item
