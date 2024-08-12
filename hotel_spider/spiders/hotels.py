import scrapy
import random
import re
import json
from ..items import HotelSpiderItem
from datetime import datetime, timedelta
import time




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
                callback=self.parse,
                dont_filter = True
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
                    hotelBasicInfo = hotel['hotelBasicInfo']
                    #print(hotelBasicInfo)
                    #Check if images is loaded or not
                    if not hotelBasicInfo["hotelMultiImgs"]:
                        print("Image Not Loaded. Try Again to run the crawler.")
                        break
                    
                    else:

                        item = HotelSpiderItem()
                        item['title'] = hotelBasicInfo['hotelEnName']
                        item['location'] = hotelBasicInfo['hotelAddress']
                        item['price'] = hotelBasicInfo['price']
                        item['rating'] = hotel['commentInfo']["commentScore"]
                        item['room_type'] = hotel["roomInfo"]["physicalRoomName"]
                        item['latitude'] = hotel["positionInfo"]["coordinate"]["lat"]
                        item['longitude'] = hotel["positionInfo"]["coordinate"]["lng"]
                        item['image_urls'] = [imageDict['url'] for image in hotelBasicInfo["hotelMultiImgs"] for imageDict in image ]
                        item['images'] = [f"images/{item['title']}_{id+1}.jpg" for id in range(len(item['image_urls']))]
                        
                        yield item
                    
     