import os
import json
import traceback
from app.settings import FILE_HANDLING_BASE_PATH
from app.utils.common import get_logger
logger = get_logger()

class DataHandler():
    def __init__(self) -> None:
        self.db = os.path.join(FILE_HANDLING_BASE_PATH,'data.json')

    def insert(self,product_list : list):
        logger.info('utils.db.insert')
        try:
            existing_data = self.get()
            f = open(self.db, "w")
            if existing_data:
                existing_data = json.loads(existing_data)
                product_list.extend(existing_data) 
            f.write(json.dumps(product_list))
            f.close()
        except Exception as e:
            logger.error(f"utils.db.insert | error - {str(e)} | traceback - traceback - {traceback.format_exc()}")
            raise e

    def update(self,product_list : list):
        logger.info('utils.db.insert')
        try:
            f = open(self.db, "w")
            f.write(json.dumps(product_list))
            f.close()
        except Exception as e:
            logger.error(f"utils.db.insert | error - {str(e)} | traceback - traceback - {traceback.format_exc()}")
            raise e

    def get(self):
        logger.info('utils.db.get')
        try:
            f = open(self.db, "r")
            # return json.load(f)
            return f.read()
        except Exception as e:
            logger.error(f"utils.db.get | error - {str(e)} | traceback - traceback - {traceback.format_exc()}")
            raise e