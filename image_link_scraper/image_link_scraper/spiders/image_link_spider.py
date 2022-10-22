import scrapy, os
from scrapy.crawler import CrawlerProcess
import sys
from os.path import dirname
from pathlib import Path
from multiprocessing import Process

#The following line (which leads to the folder containing "scrapy.cfg") fixed the problem
sys.path.append(dirname(dirname(dirname(Path(__file__).absolute()))))

class ImageLinkSpider(scrapy.Spider):
    name = "image_link"
    custom_settings = {
        'ITEM_PIPELINES': {
            'image_link_scraper.pipelines.ImageLinkPipeline': 400
        }
    }

    def __init__(self, arg, count):
        self.arg = arg
        self.count = count
        self.links_list = []
        print(count)
        print(arg)
        tag = arg.split("=")[1]

        if not os.path.exists("./results/"+tag):
            os.makedirs("./results/"+tag)
        
        self.output = open("./results/" + tag + "/" + tag + ".txt", "w")

    # image-gallery-image__image   (class)
    # get src
    def start_requests(self):
        for i in range(1, self.count+1):
            url = "https://wallpaper.mob.org/gallery/" + self.arg + "/" + str(i) + "/"
            yield scrapy.Request(url=url, callback=self.parse) 

    def parse(self, response):
        # data-src is lazy loading property, image will not load immeadeatly.
        img_links = response.css('img.image-gallery-image__image::attr(src)').getall() + response.css('img.image-gallery-image__image::attr(data-src)').getall() 
        self.links_list.extend(img_links)



def run_crawler(marg, mcount):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0',   
    })
    process.crawl(ImageLinkSpider, arg=marg, count=mcount)
    process.start()
        
if __name__ == "__main__":
    f = open("././categories_extracted.txt")
    ccc = 0
    for line in f:
        ccc += 1
        print(str(ccc) + " ###############################################################################")
        mcountstring = line.split(" ")[-1]
        #mcount = round(int(mcountstring)/60)
        mcount = 7
        marg = line[:-len(mcountstring)-1]
        p = Process(target=run_crawler, args=(marg, mcount))
        p.start()
        p.join()
    
    

    