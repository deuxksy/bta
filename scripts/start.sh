#!/usr/bin/env bash

export ZZIZILY_BTA_MODE=prod
export ZZIZILY_BTA_CRYPTO=tLZIcdBwFUx8KImvo1OuOQIy4WQoc5kf8QvyR_xiCZM=
export ZZIZILY_BTA_HOME=${HOME}/apps/bta

cd ${ZZIZILY_BTA_HOME}

source ${ZZIZILY_BTA_HOME}/scripts/init.sh && ${ZZIZILY_BTA_HOME}/scripts/run.sh && ${ZZIZILY_BTA_HOME}/scripts/destroy.sh
