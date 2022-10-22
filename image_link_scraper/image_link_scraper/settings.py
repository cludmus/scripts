BOT_NAME = 'image_link_scraper'

SPIDER_MODULES = ['image_link_scraper.spiders']
NEWSPIDER_MODULE = 'image_link_scraper.spiders'

ITEM_PIPELINES = {
    'image_link_scraper.pipelines.ImageLinkPipeline': 400,
}