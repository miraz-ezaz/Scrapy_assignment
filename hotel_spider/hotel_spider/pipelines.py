import os
import logging
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
from database_manager.database import init_db, add_listing
from hotel_spider.settings import IMAGES_STORE
from itemadapter import ItemAdapter

logger = logging.getLogger(__name__)

class SaveToDatabasePipeline:
    def __init__(self):
        self.Session = init_db()

    def process_item(self, item, spider):
        if 'images' not in item:
            logger.error(f"Item contains no images: {item}")
            raise DropItem("Item contains no images")

        session = self.Session()
        try:
            add_listing(
                session=session,
                title=item['title'],
                rating=float(item['rating']),
                location=item['location'],
                latitude=float(item['latitude']),
                longitude=float(item['longitude']),
                room_type=item['room_type'],
                price=float(item['price']),
                images=item['images']  # This should now contain the new file names
            )
            session.commit()
            logger.info(f"Item saved to database: {item}")
        except Exception as e:
            logger.error(f"Error saving item to database: {e}")
            session.rollback()
            raise DropItem(f"Error saving item to database: {e}")
        finally:
            session.close()
        return item

class CustomImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item["image_urls"]:
            yield Request(image_url)

    
    def file_path(self, request, response=None, info=None, *, item=None):
        title = request.meta['title'].replace(" ", "_")
        room_type = request.meta['room_type'].replace(" ", "_")
        idx = request.meta['idx'] + 1
        filename = f"{title}_{room_type}_{idx}.jpg"
        return filename

    def item_completed(self, results, item, info):
        image_paths = [x["path"] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        adapter = ItemAdapter(item)
        adapter["image_paths"] = image_paths
        return item
