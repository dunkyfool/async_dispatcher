#!/bin/bash

if [ "${1}" = "up" ]; then
  docker-compose up -d
elif [ "${1}" = "down" ]; then
  docker-compose kill
  docker-compose rm -f
elif [ "${1}" = "build" ]; then
  echo "[INFO] Build API..."
  echo " "
  cd docker/api
  sh build.sh

  echo " "
  echo "[INFO] Build WORKER..."
  echo " "
  cd ../worker
  sh build.sh
  cd ../../
else
  docker-compose ${1}
fi
