#!/usr/bin/env bash

export ZZIZILY_BTA_MODE=prod
export ZZIZILY_BTA_HOME=${HOME}/apps/bta
export ZZIZILY_BTA_CRYPTO=${ZZIZILY_BTA_CRYPTO}
export ZZIZILY_KIKI_CRYPTO=${ZZIZILY_KIKI_CRYPTO}

cd ${ZZIZILY_BTA_HOME}

source ${ZZIZILY_BTA_HOME}/scripts/init.sh && ${ZZIZILY_BTA_HOME}/scripts/run.sh && ${ZZIZILY_BTA_HOME}/scripts/destroy.sh
