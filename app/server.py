from fastapi import FastAPI
import logging
from app.routes import common,user
from app.settings import LOG_LEVEL,SERVICE_NAME,BASE_ROUTE
from redis import Redis
import traceback
from app.settings import REDIS_HOST,REDIS_PORT,FILE_HANDLING_BASE_PATH
import os

app = FastAPI()

@app.on_event("startup")
async def startup():
    setup_logger(app)
    setup_redis(app)
    setup_routes(app)
    setup_files(app)
    setup_db(app)

@app.on_event("shutdown")
async def shutdown():
    app.redis.close()

def setup_logger(app):
    """Set up the logger."""
    extra = {"app_name": SERVICE_NAME}
    logging.basicConfig(level=logging.INFO, format="%(asctime)s Scrape Service: %(message)s", force=True)
    logger = logging.getLogger(__name__)
    logger = logging.LoggerAdapter(logger, extra)
    logger.setLevel(logging.getLevelName(LOG_LEVEL))
    app.logger = logger


def setup_routes(app):
    """Register routes."""
    app.logger.info('setup_routes')
    routes = [common,user]
    for route in routes:
        app.include_router(route.router, tags=["atlys"], prefix=f"{BASE_ROUTE}")


def setup_redis(app):
    """Set up redis"""
    app.logger.info('setup_redis')
    try:
        app.redis = Redis(host=REDIS_HOST, port=REDIS_PORT, db=0,decode_responses=True)
        return app.redis
    except Exception as e:
        app.logger.error(f"setup_redis | error - {str(e)} | traceback - traceback - {traceback.format_exc()}")
        raise e
    
    
def setup_files(app):
    """Set up files"""
    app.logger.info('setup_files')
    os.makedirs(FILE_HANDLING_BASE_PATH,exist_ok=True)
    os.makedirs(os.path.join(FILE_HANDLING_BASE_PATH,'images'),exist_ok=True)


def setup_db(app):
    """Set up db"""
    app.logger.info('setup_db')
    filename = os.path.join(FILE_HANDLING_BASE_PATH,'data.json')
    try:
        open(filename, 'a').close()
    except Exception as e:
        app.logger.error(f"setup_db | error - {str(e)} | traceback - traceback - {traceback.format_exc()}")
        raise e