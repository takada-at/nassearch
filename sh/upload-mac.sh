#!/bin/bash

ROOT=$(cd $(dirname $0); cd ../; pwd)
PYTHON=${ROOT}/venv/bin/python
GSUTIL=$HOME/google-cloud-sdk/bin/gsutil
TODAY=$(date +'%Y-%m-%d')
LOG=${ROOT}/data/log/upload-${TODAY}

${PYTHON} ${ROOT}/batch.py save $ROOT/data/mac.csv 2>&1 | tee -a ${LOG}
${GSUTIL} cp ${ROOT}/data/files.csv \
          gs://tkd-nas-data/rawdata/ \
    2>&1 | tee -a ${LOG}


