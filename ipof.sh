#!/usr/bin/env bash

if [[ $# == 0 ]]; then
    echo 'Usage:ipof container'
    exit 1
fi

for container in $@; do
    docker inspect -f '{{ .NetworkSettings.Networks.zookeeper.IPAMConfig.IPv4Address }}' ${container}
done

