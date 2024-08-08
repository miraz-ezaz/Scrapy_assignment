# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HotelSpiderItem(scrapy.Item):
    title = scrapy.Field()
    rating = scrapy.Field()
    location = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    room_type = scrapy.Field()
    price = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
