#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

class BtaBaseObject(object):

    time_new = None
    time_update = None

    def to_json(self, sort_keys=True, indent=4, separators=(',', ':')):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=sort_keys, separators=separators)

    def to_properties(self):
        return list(filter(lambda o: '__' not in o, self.__dir__()))


class BtaSite(BtaBaseObject):
    site = None
    url = None
    xpath_title = None
    xpath_url = None
    xpath_total = None
    xpath_average = None
    xpath_purchases = None


class BtaDeal(BtaBaseObject):
    bta_site = None
    title = None
    url = None
    start = None
    end = None


class BtaPrice(BtaBaseObject):
    bta_deal = None
    url = None
    title = None
    # 전체 구매 금액
    total = None
    # 전체 구매 건수
    purchases = None
    # 평균 구매 금액
    average = None

class BtaArchive(BtaBaseObject):
    bta_site = None
    bta_deal = None
    history = None
    size = None
