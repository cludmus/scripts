# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.crawler import CrawlerProcess


class ImageLinkPipeline:
    def process_item(self, item, spider):
        return item
    def close_spider(self, spider):
        print(str(len(spider.links_list)) +" ############################################################################ List len")
        links_set = set(spider.links_list)
        print(str(len(links_set)) + "############################################################################ Set len")
        for link in links_set:
            spider.output.write(link + "\n")
            


    
    