#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
import os

from cryptography.fernet import Fernet

__title__ = 'bta'
__author__ = 'SeokYoung Kim<crom@zzizily.com>'
__status__ = 'develoment'
__version__ = '0.0.1'
__date__ = '2017-03-11'
__license__ = 'MIT'
__copyright__ = 'Copyright 2017 SeokYoung Kim'

crypto = Fernet(os.getenv('ZZIZILY_BTA_CRYPTO'))
package_name = 'bta'
project_home = os.getenv('ZZIZILY_BTA_HOME')
