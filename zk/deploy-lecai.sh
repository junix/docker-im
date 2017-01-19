#!/usr/bin/env bash

env DATA_DIR=/mnt1/zookeeper/data \
 DATA_LOG_DIR=/mnt1/zookeeper/log \
 NAME_PREFIX=lecai_zk \
 ./deploy-zookeeper.py --dryrun \
 -f 101 in-821-bj in-822-bj in-823-bj in-824-bj in-825-bj

