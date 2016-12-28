#!/usr/bin/env bash
ZOO_SERVERS="server.1=zk1:2888:3888 server.2=zk2:2888:3888 server.3=zk3:2888:3888"

IMAGE="zookeeper:3.4.9"

function start_zk_cmd {
 "docker run --restart always \
 --network starfish \
 --ip 192.0.2.$1 \
 --name zk1 \
 --env  ZOO_MY_ID=$1 \
 --env ZOO_SERVERS=\"$ZOO_SERVERS\" \
 -d \
 $IMAGE"
}

ssh in-205-gd $(start_zk_cmd 1)
ssh in-204-gd $(start_zk_cmd 2)
ssh in-902-bj $(start_zk_cmd 3)

