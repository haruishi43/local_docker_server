#!/bin/sh

docker container stop $(docker ps -aq --filter "label=manager=dhole")
docker container rm $(docker ps -aq --filter "label=manager=dhole")
printf y | docker image prune -a
printf y | docker system prune
