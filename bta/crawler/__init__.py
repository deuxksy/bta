#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from kiki.commons import proxy
from kiki.commons.util import web
from requests.exceptions import ProxyError


class BaseCrawler(object):
    encoding = 'utf-8'
    count = {}
    urls = []
    headers = {'User-Agent': web.get_user_agent()}
    site = ''
    proxies = {}

    def __init__(self, *args, **kwargs):
        self.site = kwargs.get('site')
        self.proxies = proxy.get_proxies()

    def get_response(self, url, max=2):
        """Sends a GET request.

        :param url:
        :param max: (optional)
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        response = None

        # url 별 재시도 회수를 저장 하기 위한 count 값
        if url not in self.count:
            self.count[url] = 0

        # max(2) 보다 크면 proxy 를 사용하지 않고 그냥 가지고 오기
        if max < self.count[url]:
            # url count 삭제
            self.count.pop(url)
            return requests.get(url=url, headers=self.headers)

        try:
            response = requests.get(url=url, headers=self.headers, proxies=self.proxies)
        except ProxyError:
            response = requests.get(url=url, headers=self.headers, proxies=self.proxies)
        finally:
            if response is None:
                self.count[url] += 1
                self.proxies = proxy.get_proxies()
                return self.get_response(url)
            else:
                return response
