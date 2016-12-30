#!/usr/bin/env bash
if [[ "x$BROKER_ID" == "x" ]]
then
    echo "BROKER_ID not set"
    exit 1
fi

if [[ "x$ZOOKEEPER" == "x" ]]
then
    ZOOKEEPER="192.0.2.1:2181,192.0.2.2:2181,192.0.2.3:2181,192.0.2.4:2181,192.0.2.5:2181"
fi

sed -i "s/{{BROKER_ID}}/${BROKER_ID}/g" /app/config/*
sed -i "s/{{ZOOKEEPER}}/${ZOOKEEPER}/g" /app/config/*

cd /app
/app/bin/kafka-server-start.sh /app/config/server.properties
