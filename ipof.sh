#!/usr/bin/env bash

if [ -z ${1+x} ]; then
    echo 'Usage:ipof container'
    exit 1
fi

CONTAINER=$1

docker inspect -f '{{ .NetworkSettings.Networks.zookeeper.IPAMConfig.IPv4Address }}' ${CONTAINER}
