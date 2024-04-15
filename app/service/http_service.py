from app.utils.common import get_logger, HTTPRequestHandler
import json
import traceback
from http import HTTPStatus
logger = get_logger()
request_handler = HTTPRequestHandler(logger)


class HTTPService:
    def get_data_from_proxy(
        self,
        request_url,
        request_method = "GET",
        request_id = None, 
    ):
        logger.info(f"HTTPService.get_data_from_proxy | request_id : {request_id} | url : {request_url}")
        try:
            headers = {}
            query_params = {}
            res = request_handler.request(request_url, headers, query_params, method=request_method)
            if res.status_code == HTTPStatus.OK.value:
                return res
            else:
                logger.error(
                    f"exception.HTTPService.get_data_from_proxy | request_id : {request_id} | http status code - {res.status_code} | response - {res}"
                )
                raise Exception(f"invalid http request")
        except Exception as e:
            logger.error(
                f"exception.HTTPService.get_data_from_proxy | error while making http request | request_id : {request_id} | e - {str(e)} | traceback - {traceback.format_exc()}"
            )
            raise e
