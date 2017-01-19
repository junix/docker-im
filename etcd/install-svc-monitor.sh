#!/usr/bin/env bash
cp svc-run.template svc-run
sed -i "s/__MYIP__/${INTERNAL_IP}/g" svc-run
END_EXPR=$(echo $ETCD_ENDPOINTS | sed 's/\//\\\//g')
sed -i "s/__ETCD_ENDPOINTS__/${ETCD_EXPR}/g" svc-run
mkdir /service/etcd
chmod +x ./svc-run
mv ./svc-run /service/etcd/run
