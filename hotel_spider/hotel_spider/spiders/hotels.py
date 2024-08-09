import scrapy
import random
import re
import json
from ..items import HotelSpiderItem
from datetime import datetime, timedelta




class HotelsSpider(scrapy.Spider):
    name = "hotels"
    allowed_domains = ["uk.trip.com"]
    start_urls = ["https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"]

    def start_requests(self):
        # Make a POST request to the start URL
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                method='POST',
                headers={
                    'User-Agent':
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
                },
                callback=self.parse_hotel_list
            )

    
    def parse_hotel_list(self, response):
        script_content = response.xpath('//script[contains(., "window.IBU_HOTEL")]/text()').get()
        if script_content:
            # Use regular expressions to extract the content of window.IBU_HOTEL
            match = re.search(r'window\.IBU_HOTEL\s*=\s*({.*?});', script_content, re.DOTALL)
            if match:
                hotel_data_json = match.group(1)
                
                hotel_data_dict = json.loads(hotel_data_json)
                
                city_types = ['inboundCities','outboundCities']
                city_list = [(city['name'],city['id']) for city_type in city_types for city in hotel_data_dict['initData']['htlsData'][city_type]]
                selected_city = random.choice(city_list)
                current_date = datetime.now().strftime('%Y/%m/%d')
                next_date = (datetime.now() + timedelta(days=1)).strftime('%Y/%m/%d')
                url = f'https://uk.trip.com/hotels/list?city={selected_city[1]}&checkin={current_date}&checkout={next_date}'
                yield scrapy.Request(
                url=url,
                method='POST',
                headers={
                    'User-Agent':
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
                },
                callback=self.parse
            )
                
                
                        
                
        
    
    def parse(self, response):
        script_content = response.xpath('//script[contains(., "window.IBU_HOTEL")]/text()').get()
        if script_content:
            # Use regular expressions to extract the content of window.IBU_HOTEL
            match = re.search(r'window\.IBU_HOTEL\s*=\s*({.*?});', script_content, re.DOTALL)
            if match:
                hotel_json = match.group(1)
                
                hotel_data = json.loads(hotel_json)
                hotel_list = hotel_data['initData']['firstPageList']['hotelList']
                for hotel in hotel_list:
                    item = HotelSpiderItem()
                    hotelBasicInfo = hotel['hotelBasicInfo']
                    item['title'] = hotelBasicInfo['hotelEnName']
                    item['location'] = hotelBasicInfo['hotelAddress']
                    item['rating'] = hotel.css('span.real').xpath('text()').get().strip()
                    item['room_type'] = hotel.css('span.room-panel-roominfo-name').xpath('text()').get().strip()
                    item['price'] = hotel.css('div#meta-real-price').xpath('span/div/text()').get().strip()[1:]
                    item['image_urls'] = hotel.css('img.m-lazyImg__img').xpath("@src").getall()
                    # Adding random values for latitude and longitude
                    item['latitude'] = random.uniform(-90.0, 90.0)
                    item['longitude'] = random.uniform(-180.0, 180.0)
                    yield item
                    
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
