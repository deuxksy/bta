#!/usr/bin/env bash

export ZZIZILY_BTA_MODE=dev
export ZZIZILY_BTA_HOME=${HOME}/apps/bta
export ZZIZILY_BTA_CRYPTO=tLZIcdBwFUx8KImvo1OuOQIy4WQoc5kf8QvyR_xiCZM=
export ZZIZILY_KIKI_CRYPTO=X_AEu2y68Q91Hmf4ooi7vUKkT5msSMvDEHDcVp-EFEI=

cd ${ZZIZILY_BTA_HOME}

source ./scripts/init.sh && ./scripts/run.sh && ./scripts/destroy.sh
