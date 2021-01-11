import contextlib
import traceback

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from util import logger

retries = Retry(total=3,
                backoff_factor=0.5,
                status_forcelist=[k for k in range(400, 600)])

HOT_URL = "https://i-lq.snssdk.com/api/feed/hotboard_online/v1/?category=hotboard_online&count=50"


@contextlib.contextmanager
def request_session(url: str):
    s = requests.session()
    try:
        s.mount("http://", HTTPAdapter(max_retries=retries))
        s.mount("https://", HTTPAdapter(max_retries=retries))
        yield s
    finally:
        s.close()


class Toutiao:

    def get_search(self):
        items = []
        resp = None
        try:
            with request_session() as s:
                resp = s.get(HOT_URL)
                text = resp.text

        except:
            logger.warn(traceback.format_exc())
        return (items, resp)
