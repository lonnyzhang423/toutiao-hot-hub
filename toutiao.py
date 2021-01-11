import contextlib
import traceback

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from util import logger

RETRIES = Retry(total=3,
                backoff_factor=0.5,
                status_forcelist=[k for k in range(400, 600)])

HOT_URL = "https://i-lq.snssdk.com/api/feed/hotboard_online/v1/"


@contextlib.contextmanager
def request_session():
    s = requests.session()
    try:
        s.mount("http://", HTTPAdapter(max_retries=RETRIES))
        s.mount("https://", HTTPAdapter(max_retries=RETRIES))
        yield s
    finally:
        s.close()


class Toutiao:

    def get_search(self):
        items = []
        resp = None
        try:
            with request_session() as s:
                params = {'category': 'hotboard_online',
                          'count': '50'}
                resp = s.get(HOT_URL, params=params)
                obj = resp.json()
                items = obj['data']
        except:
            logger.warn(traceback.format_exc())
        return (items, resp)


if __name__ == "__main__":
    tt = Toutiao()
    searches, resp = tt.get_search()
    logger.info('searches:%s', searches[0])
