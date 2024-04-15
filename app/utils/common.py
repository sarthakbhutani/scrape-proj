import logging
from http import HTTPStatus
LOG_LEVEL  = "INFO"
EXTERNAL_API_CALL_RETRY_COUNT = 3
EXTERNAL_API_CALL_RETRY_TIME_DIFF_SECONDS = 2

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import requests
import traceback

def get_logger():
    extra = {"app_name": "NoticeConsumer"}
    logging.basicConfig(level=logging.INFO, format="%(asctime)s Scrape Service: %(message)s", force=True)
    logger = logging.getLogger(__name__)
    logger.setLevel(LOG_LEVEL)
    logger = logging.LoggerAdapter(logger, extra)
    return logger


class HTTPRequestHandler:
    def __init__(
        self,
        logger,
        retry_count=EXTERNAL_API_CALL_RETRY_COUNT,
        retry_wait_time=EXTERNAL_API_CALL_RETRY_TIME_DIFF_SECONDS,
        request_time_out=None,
    ) -> None:
        self.retry_count = retry_count
        self.retry_wait_time = retry_wait_time
        self.logger = logger
        self.accepted_status = [HTTPStatus.OK.value]
        self.request_time_out = request_time_out
        retries_for_get = Retry(
            total=EXTERNAL_API_CALL_RETRY_COUNT,  # Total retries
            backoff_factor=1,  # Exponential backoff (0.2,0.4,0.8,)*backoff_factor
            status_forcelist=[408, 429, 500, 502, 503, 504, 500, 400],
        )  # Retry for these status codes
        session_for_get = requests.Session()
        session_for_get.mount("http://", HTTPAdapter(max_retries=retries_for_get))
        session_for_get.mount("https://", HTTPAdapter(max_retries=retries_for_get))
        self.session_for_get = session_for_get
        self.connection_timeout_error = 0

    def request(self, url, headers=None, query_params=None, json_payload=None, method="GET"):
        self.logger.info(f"HTTPRequestHandler.request stating method {method}")
        try:
            response = self.session_for_get.request(
                method=method,
                url=url,
                params=query_params,
                headers=headers,
                json=json_payload,
                timeout=self.request_time_out if self.request_time_out else None,
            )
            self.logger.info(
                f"HTTPRequestHandler.request | url {url} | response code {response.status_code if response else ''}"
            )
            if not response.status_code not in (self.accepted_status):
                self.logger.error(
                    f"HTTPRequestHandler.request response received {response} with response code {response.status_code if response else ''}"
                )

        except (ConnectionError, TimeoutError) as err:
            self.logger.error(
                f"HTTPRequestHandler.request Entered into (ConnectionError, TimeoutError) err {str(err)}, trace:: {traceback.format_exc()}"
            )
            self.connection_timeout_error += 1
            if self.connection_timeout_error < 2:
                return self.request(url, headers, query_params, json_payload, method)
            else:
                self.logger.error(
                    f"HTTPRequestHandler.request | Not retrying the request as self.connection_timeout_error is {self.connection_timeout_error}"
                )
            raise ex

        except Exception as ex:
            self.logger.error(f"HTTPRequestHandler.request exception {str(ex)}, trace:: {traceback.format_exc()}")
            raise ex

        return response

