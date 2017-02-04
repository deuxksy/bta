#!/usr/bin/env bash
cd /home/pi/apps/bta
export ZZIZILY_BTA_CONFIG=/home/pi/apps/bta/resource/local_config.ini
scrapy crawl humblebundlespider
