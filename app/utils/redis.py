from redis import Redis
import traceback
from app.settings import REDIS_HOST,REDIS_PORT,FILE_HANDLING_BASE_PATH
from app.utils.common import get_logger
logger = get_logger()

def setup_redis():
    """Set up redis"""
    logger.info('setup_redis')
    try:
        redis = Redis(host=REDIS_HOST, port=REDIS_PORT, db=0,decode_responses=True)
        return redis
    except Exception as e:
        logger.error(f"setup_redis | error - {str(e)} | traceback - traceback - {traceback.format_exc()}")
        raise e