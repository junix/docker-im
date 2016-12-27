#!/usr/bin/env bash
START_ZK1='docker run --restart always --network starfish --ip 192.0.2.1 -d --env  ZOO_MY_ID=1 --name zk1 --env ZOO_SERVERS="server.1=zk1:2888:3888 server.2=zk2:2888:3888 server.3=zk3:2888:3888" zookeeper:3.4.9'

START_ZK2='docker run --restart always --network starfish --ip 192.0.2.2 -d --env  ZOO_MY_ID=2 --name zk2 --env ZOO_SERVERS="server.1=zk1:2888:3888 server.2=zk2:2888:3888 server.3=zk3:2888:3888" zookeeper:3.4.9'

START_ZK3='docker run --restart always --network starfish --ip 192.0.2.3 -d --env  ZOO_MY_ID=3 --name zk3 --env ZOO_SERVERS="server.1=zk1:2888:3888 server.2=zk2:2888:3888 server.3=zk3:2888:3888" zookeeper:3.4.9'

ssh in-205-bj START_ZK1
ssh in-204-bj START_ZK2
ssh in-902-gd START_ZK3

