#!/bin/bash

ROOT=$(cd $(dirname $0); cd ../; pwd)

rsync -rv ${ROOT}/ \
      pi@192.168.11.8:~/nassearch/ \
      --exclude venv --exclude *.pyc \
      --exclude __pycache__ --exclude data --exclude .git --exclude .DS_Store
