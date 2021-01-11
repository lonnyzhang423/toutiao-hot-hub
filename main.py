import json
import logging
import os
import traceback
import urllib.parse

import requests
from requests import Response
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import util
from toutiao import Toutiao
from util import logger


def generateArchiveMd(items):
    """生成归档readme
    """
    def search(item):
        content = json.loads(item['content'])
        title = content['raw_data']['title']
        url = 'https://so.toutiao.com/search?keyword={}'.format(
            urllib.parse.quote(title))
        return '1. [{}]({})'.format(title, url)

    searchMd = '暂无数据'
    if items:
        searchMd = '\n'.join([search(item) for item in items])

    md = ''
    file = os.path.join('template', 'archive.md')
    with open(file) as f:
        md = f.read()

    now = util.current_time()
    md = md.replace("{updateTime}", now)
    md = md.replace("{searches}", searchMd)

    return md


def generateReadme(items):
    """生成readme
    """
    def search(item):
        content = json.loads(item['content'])
        title = content['raw_data']['title']
        url = 'https://so.toutiao.com/search?keyword={}'.format(
            urllib.parse.quote(title))
        return '1. [{}]({})'.format(title, url)

    searchMd = '暂无数据'
    if items:
        searchMd = '\n'.join([search(item) for item in items])

    md = ''
    file = os.path.join('template', 'archive.md')
    with open(file) as f:
        md = f.read()

    now = util.current_time()
    md = md.replace("{updateTime}", now)
    md = md.replace("{searches}", searchMd)

    return md


def saveReadme(md):
    logger.debug('readme:%s', md)
    util.write_text('README.md', md)


def saveArchiveMd(md):
    logger.debug('archive md:%s', md)
    name = util.current_date()+'.md'
    file = os.path.join('archives', name)
    util.write_text(file, md)


def saveResponse(resp: Response):
    if resp:
        text = resp.text
        logger.debug('response:%s', text)
        name = util.current_date()+'.json'
        file = os.path.join('raw', name)
        util.write_text(file, text)


def run():
    # 获取数据
    tt = Toutiao()
    searches, resp = tt.get_search()
    # 保存响应内容
    saveResponse(resp)
    # 最新数据
    readme = generateReadme(searches)
    saveReadme(readme)
    # 归档
    archiveMd = generateArchiveMd(searches)
    saveArchiveMd(archiveMd)


if __name__ == "__main__":
    run()
