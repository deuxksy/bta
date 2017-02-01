class BtaSite(object):
    url = None
    last_deal = None
    xpath_title = None
    xpath_url = None
    xpath_total = None
    xpath_average = None
    xpath_sold = None


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
    total_payments = None
    num_purchases = None
    average_purchase = None
    time = None


class BtaArchive(object):
    bta_site = None
    bta_deal = None
    json = None
    end = None
    size = None
