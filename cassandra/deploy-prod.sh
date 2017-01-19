#!/usr/bin/env bash

env DATA_DIR=/mnt2/cassandra \
JVM_OPTS='-Xms4G -Xmx4G' \
./deploy-cassandra.py  --dryrun  10.10.31.56 10.10.53.26 10.10.60.240
