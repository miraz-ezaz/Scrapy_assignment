import scrapy
import random
from ..items import HotelSpiderItem

class HotelsSpider(scrapy.Spider):
    name = "hotels"
    allowed_domains = ["uk.trip.com"]
    start_urls = ["https://uk.trip.com/hotels/list?city=338&checkin=2024/8/8&checkout=2024/08/09"]

    def parse(self, response):
        hotels = response.css('ul.long-list').xpath('//li').xpath('following-sibling::li')
        for hotel in hotels:
            title = hotel.css('span.name').xpath('./text()').get()
            if title:
                item = HotelSpiderItem()
                item['title'] = title.strip()
                item['location'] = (', ').join([children.xpath('./text()').get().strip() for children in hotel.css('p.transport').xpath("./span") if not children.xpath("@class").extract()])
                item['rating'] = hotel.css('span.real').xpath('text()').get().strip()
                item['room_type'] = hotel.css('span.room-panel-roominfo-name').xpath('text()').get().strip()
                item['price'] = hotel.css('div#meta-real-price').xpath('span/div/text()').get().strip()[1:]
                item['image_urls'] = hotel.css('img.m-lazyImg__img').xpath("@src").getall()
                # Adding random values for latitude and longitude
                item['latitude'] = random.uniform(-90.0, 90.0)
                item['longitude'] = random.uniform(-180.0, 180.0)
                yield item
