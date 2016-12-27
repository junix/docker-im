#!/usr/bin/env bash
docker run --restart always --network starfish --ip 192.0.2.1 -d --env  ZOO_MY_ID=1 --name zk1 --env ZOO_SERVERS="server.1=zk1:2888:3888 server.2=zk2:2888:3888 server.3=zk3:2888:3888" zookeeper:3.4.9

docker run --restart always --network starfish --ip 192.0.2.2 -d --env  ZOO_MY_ID=2 --name zk2 --env ZOO_SERVERS="server.1=zk1:2888:3888 server.2=zk2:2888:3888 server.3=zk3:2888:3888" zookeeper:3.4.9

docker run --restart always --network starfish --ip 192.0.2.3 -d --env  ZOO_MY_ID=3 --name zk3 --env ZOO_SERVERS="server.1=zk1:2888:3888 server.2=zk2:2888:3888 server.3=zk3:2888:3888" zookeeper:3.4.9


