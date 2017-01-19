#!/usr/bin/env bash
env DATA_DIR=/mnt2/kafka/data \
LOG_DIR=/mnt2/kafka/log \
KAFKA_HEAP_OPTS="-Xms1G -Xmx4G" \
./deploy-kafka.py --dryrun 10.10.53.26 10.10.60.240 10.10.39.177