import json

class BtaSite(object):
    site = None
    url = None
    xpath_title = None
    xpath_url = None
    xpath_total = None
    xpath_average = None
    xpath_purchases = None


class BtaDeal(object):
    bta_site = None
    title = None
    url = None
    start = None
    end = None


class BtaPrice(object):
    bta_deal = None
    url = None
    title = None
    total = None
    purchases = None
    average = None
    time = None

    def toJSON(self, sort_keys=True, indent=4, separators=(',', ':')):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=sort_keys, separators=separators)


class BtaArchive(object):
    bta_site = None
    bta_deal = None
    history = None
    size = None
