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
elif [ "${1}" = "push" ]; then
  read -p 'Enter git comment: ' x
  git add .
  git commit -m "${x}"
  git push

# test command  
elif [ "${1}" = "ini" ]; then
  redis-cli --scan --pattern '*'
  curl 'localhost:5000/action?ip=localhost&type=initialize'
  sleep 5
  redis-cli --scan --pattern '*'
elif [ "${1}" = "update" ]; then
  redis-cli hgetall today
  curl 'localhost:5000/action?ip=localhost&type=todayTaskUpdate&project=ets_1.0'
  curl 'localhost:5000/action?ip=localhost&type=todayTaskUpdate&project=ets_2.0'
  curl 'localhost:5000/action?ip=localhost&type=todayTaskUpdate&project=ets_3.0'
  sleep 5
  redis-cli hgetall today
elif [ "${1}" = "trigger" ]; then
  curl 'localhost:5000/action?ip=localhost&type=trigger&project=ets_1.0'
  curl 'localhost:5000/action?ip=localhost&type=trigger&project=ets_2.0'
  curl 'localhost:5000/action?ip=localhost&type=trigger&project=ets_3.0'
  sleep 5
  docker ps 
elif [ "${1}" = "info" ]; then
  curl "localhost:5000/action?ip=localhost&type=updateInfo&project=ets_1.0&info=${2}"
  sleep 5 
  redis-cli hgetall today
elif [ "${1}" = "check" ]; then
  curl "localhost:5000/action?ip=localhost&type=shutdownCheck&project=${2}"
  sleep 5
  docker ps

else
  docker-compose ${1}
fi
