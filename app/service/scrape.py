import json
from bs4 import BeautifulSoup
from requests import get
from app.model.scrape_model import ScrapeRequestDto
from app.model.request_validation import ScrapeRequestModel
from app.service.communication_service import CommunicationService
from app.utils.common import get_logger
from app.service.http_service import HTTPService
import traceback
from app.utils.db import DataHandler
import uuid
from app.settings import FILE_HANDLING_BASE_PATH
import os
from app.utils.redis import setup_redis

logger = get_logger()
httpService = HTTPService()

class ScrapeService:
    def __init__(self,scrape_request :ScrapeRequestModel ) -> None:
        self.scrape_request = scrape_request
        self.redis = setup_redis()

    def scrape_service(self):
        logger.info('service.scrape.ScrapeService.scrape_service')
        scrape_request_obj = self.scrape_request
        message = ""
        db = DataHandler()
        try:
            master_product_list_to_insert,master_product_list_to_update = [],[]
            for i in range(1,scrape_request_obj.page+1):
                request_url = scrape_request_obj.url.rstrip("/") + "/" + str(i)
                http_response = httpService.get_data_from_proxy(request_url)
                products_to_insert,products_to_update = self.get_formatted_data(http_response)
                master_product_list_to_insert.extend(products_to_insert)
                master_product_list_to_update.extend(products_to_update)
            message = f"{len(master_product_list_to_insert)} products inserted. {len(master_product_list_to_update)} products updated."
            if master_product_list_to_insert:
                db.insert(master_product_list_to_insert)
            if master_product_list_to_update:
                self.update_data(master_product_list_to_update)
            CommunicationService.send_notification(message)
            return True,message
        except Exception as e:
            logger.error(f"service.scrape.ScrapeService.scrape_service | error - {str(e)} | traceback - traceback - {traceback.format_exc()}")
            return False,str(e)

    def update_data(self,products_to_update):
        logger.info('service.scrape.ScrapeService.products_to_update')
        try:
            db = DataHandler()
            all_products = db.get()
            all_products = json.loads(all_products) 
            for i,original_product in enumerate(all_products):
                for updated_product in products_to_update:
                    if original_product['product_title'] == updated_product['product_title']:
                        original_product[i] = updated_product
            db.update(all_products)
        except Exception as e:
            logger.error(f"service.scrape.ScrapeService.update_data | error - {str(e)} | traceback - traceback - {traceback.format_exc()}")
            raise e

    def get_formatted_data(self,http_response):
        logger.info('service.scrape.ScrapeService.get_formatted_data')
        try:
            soup = BeautifulSoup(http_response.content,"lxml")
            soup.prettify()
            products = soup.find_all(name='li',class_ = ["product","type-product"])
            products_to_insert = []
            products_to_update = []
            for product in products:
                product_price = None
                if not product.find('bdi'):
                    continue
                elif product.find('bdi').text:
                    product_price = float(product.find('bdi').text.replace('₹',''))
                product_title = product.find('div',class_ = 'addtocart-buynow-btn').a['data-title']
                img_url = product.img["data-lazy-src"]
                filepath = self.save_image(img_url)
                data = {
                    "path_to_image" :filepath,
                    "product_title":product_title,
                    "product_price":product_price,
                }
                handle_data = self.check_how_to_handle_data(data)
                if handle_data==1:
                    products_to_insert.append(data)
                elif handle_data==2:
                    products_to_update.append(data)
            return products_to_insert,products_to_update
        except Exception as e:
            logger.error(f"service.scrape.ScrapeService.get_formatted_data | error - {str(e)} | traceback - traceback - {traceback.format_exc()}")
            raise e
        
    def check_how_to_handle_data(self,data : dict):
        """
        return 
            1 for insert
            2 for update
            0 for no-action
        """
        logger.info('service.scrape.ScrapeService.check_how_to_handle_data')
        product_title = data['product_title']
        product_price = data['product_price']
        try:
            cached_price = self.redis.get(product_title)
            if cached_price:
                cached_price = float(cached_price)
            
            if not cached_price:
                self.redis.set(product_title,product_price)
                return 1
            elif product_price!=cached_price:
                self.redis.set(product_title,product_price)
                return 2
            else:
                return 0
        except Exception as e:
            logger.error(f"service.scrape.ScrapeService.check_how_to_handle_data | error - {str(e)} | traceback - traceback - {traceback.format_exc()}")

    def save_image(self,img_url: str):
        logger.info('service.scrape.ScrapeService.save_image')
        http_response = httpService.get_data_from_proxy(img_url)
        filename = img_url.split('/')[-1]
        filename = os.path.join(FILE_HANDLING_BASE_PATH,'images',filename)
        if http_response.status_code == 200:
            with open(filename, "wb") as file:
                file.write(http_response.content)
            return filename
        else:
            logger.error(f'service.scrape.ScrapeService.save_image | file could not be saved - {img_url}')
            return None