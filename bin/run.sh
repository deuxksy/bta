#!/usr/bin/env bash
cd /home/pi/apps/bta
export zzizily_bta_config=/home/pi/apps/bta/resource/local_config.ini
scrapy crawl humblebundlespider
