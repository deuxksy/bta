#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

__title__ = 'py35'
__author__ = 'SeokYoung Kim<crom@zzizily.com>'
__status__ = 'develoment'
__version__ = '0.0.1'
__date__ = '2017-03-15'
__license__ = 'MIT'
__copyright__ = 'Copyright 2017 SeokYoung Kim'

import redis
from bta.settings import redis_pool_bta


key = 'www.humblebundle.com'
r = redis.Redis(connection_pool=redis_pool_bta)
data = r.hscan('bta_site:{site}'.format(site=key))
print (data)