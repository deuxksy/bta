# !/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys

from bta.crawler.humblebundle import HumbleBundle


def get_args():
    try:
        parser = argparse.ArgumentParser(description='default argument')
        parser.add_argument("-t", "--task", help="실행할 종류의 process 를 선택해주세요 (price,other)", required=False)
        return parser.parse_args()
    except:
        sys.exit(1)


if __name__ == '__main__':
    HumbleBundle(site_key='www.humblebundle.com').run()
