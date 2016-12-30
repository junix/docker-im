#!/usr/bin/env bash
if [[ "x$BROKER_ID" == "x" ]]
then
    echo "BROKER_ID not set"
    BROKER_ID=1
fi

sed -i "s/{{BROKER_ID}}/${BROKER_ID}/g" /app/config/*
sed -i "s/{{ZOOKEEPER}}/${ZOOKEEPER}/g" /app/config/*

cd /app
/app/bin/kafka-server-start.sh /app/config/server.properties
