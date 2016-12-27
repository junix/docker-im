#!/usr/bin/env bash
docker -H tcp://zk1.cloud:2375 run -d --restart=always \
      -p 2181:2181 \
      -p 2888:2888 \
      -p 3888:3888 \
      -v /var/lib/zookeeper:/var/lib/zookeeper \
      -v /var/log/zookeeper:/var/log/zookeeper  \
      --name zk1 \
      baqend/zookeeper zk1.cloud,zk2.cloud,zk3.cloud 1
docker -H tcp://zk2.cloud:2375 run -d --restart=always \
      -p 2181:2181 \
      -p 2888:2888 \
      -p 3888:3888 \
      -v /var/lib/zookeeper:/var/lib/zookeeper \
      -v /var/log/zookeeper:/var/log/zookeeper  \
      --name zk2 \
      baqend/zookeeper zk1.cloud,zk2.cloud,zk3.cloud 2
docker -H tcp://zk3.cloud:2375 run -d --restart=always \
      -p 2181:2181 \
      -p 2888:2888 \
      -p 3888:3888 \
      -v /var/lib/zookeeper:/var/lib/zookeeper \
      -v /var/log/zookeeper:/var/log/zookeeper  \
      --name zk3 \
      baqend/zookeeper zk1.cloud,zk2.cloud,zk3.cloud 3