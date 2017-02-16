
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


class BtaArchive(object):
    bta_site = None
    bta_deal = None
    history = None
    size = None
