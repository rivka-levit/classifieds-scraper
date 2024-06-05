"""
Pipelines for processing items.
"""
import mysql.connector
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


class MySQLPipeline:
    """Store items in MySQL database."""

    def __init__(self, db_host, db_name, db_user, db_pass):
        self.host = db_host
        self.database = db_name
        self.username = db_user
        self.password = db_pass

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_host=crawler.settings.get('MYSQL_HOST'),
            db_name=crawler.settings.get('MYSQL_DATABASE'),
            db_user=crawler.settings.get('MYSQL_USER'),
            db_pass=crawler.settings.get('MYSQL_PASSWORD'),
        )

    def open_spider(self, spider):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.username,
            password=self.password
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            f"""CREATE DATABASE IF NOT EXISTS {self.database}"""
        )
        self.cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.database}.classifieds (
                id INT PRIMARY KEY AUTO_INCREMENT,
                title TEXT,
                price VARCHAR(15),
                properties TEXT,
                description TEXT
            )"""
        )

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        self.cursor.execute(f"""
            INSERT INTO {self.database}.classifieds (title, price, properties, description)
            VALUES (%s, %s, %s, %s)
        """,
            (adapter.get('title', ''), adapter.get('price', ''),
             adapter.get('properties', ''), adapter.get('description', ''))
        )

        self.conn.commit()

        return item
