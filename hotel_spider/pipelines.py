import os
import logging
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
from database_manager.database import init_db, add_listing
from hotel_spider.settings import IMAGES_STORE
from itemadapter import ItemAdapter
import requests
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

class SaveToDatabasePipeline:
    def __init__(self):
        self.Session = init_db()

    def process_item(self, item, spider):
        # if 'images' not in item:
        #     logger.error(f"Item contains no images: {item}")
        #     raise DropItem("Item contains no images")

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

class CustomImageDownloadPipeline:
    def process_item(self, item, spider):
        if 'image_urls' in item:
            images = []

            # Download each image using requests
            for idx, image_url in enumerate(item['image_urls']):
                try:
                    response = requests.get(image_url, stream=True)
                    response.raise_for_status()  # Check for request errors
                    image_path = self.save_image(response, item, idx)
                    images.append(image_path)
                except RequestException as e:
                    spider.log(f"Failed to download image {image_url}: {e}")
                    continue

            
        else:
            raise DropItem("Missing image_urls in item")

        return item

    def save_image(self, response, item, idx):
        # Create the directory to save images if it doesn't exist
        images_dir = "images"
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)

        # Generate the filename using title and idx (serial number)
        title = item['title'].replace(" ", "_")
        filename = f"{title}_{idx + 1}.jpg"
        file_path = os.path.join(images_dir, filename)

        # Save the image to the file
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        return file_path
        
    
