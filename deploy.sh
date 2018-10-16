#!/bin/bash
export HOST_IP=<host-ip>
cd /home/ubuntu/microservice
docker-compose scale connectionleakfilter=0
docker rm $(docker ps -q -f status=exited)
docker rmi -f swiftops/ms-connleakfilterservice && docker pull swiftops/ms-connleakfilterservice && docker-compose up -d --remove-orphans
