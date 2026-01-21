import scrapy


class AgentItem(scrapy.Item):
    name = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    source = scrapy.Field()   # "html" or "xhr"
