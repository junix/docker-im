#!/usr/bin/env bash
cp svc-run.template svc-run
sed -i "s/__INTERNAL_IP__/${INTERNAL_IP}/g" svc-run
ETCD_EXPR=$(echo $ETCD_ENDPOINTS | sed 's/\//\\\//g')
sed -i "s/__ETCD_ENDPOINTS__/${ETCD_EXPR}/g" svc-run
mkdir /service/etcd
chmod +x ./svc-run
mv ./svc-run /service/etcd/run
