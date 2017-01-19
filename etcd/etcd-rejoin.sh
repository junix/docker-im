#!/usr/bin/env bash
MYIP="ddddddd"
ETCD_ENDPOINTS="http://10.10.31.56:2379,http://10.10.53.26:2379,http://10.10.60.240:2379,http://10.10.39.177:2379,http://10.10.38.126:2379"

CURRENT_ID=$(etcdctl --peers $ETCD_ENDPOINTS member list | grep "peerURLs=http://${MYIP}:2380" | awk -F: '{print $1}' | sed  's/\[.*\]//')

if [[ "x$CURRENT_ID" != "x" ]]
then
    etcdctl --peers $ETCD_ENDPOINTS member remove $CURRENT_ID
    sleep 1
fi

rm -rf /mnt1/etcd/*

res=$(etcdctl --peers $ETCD_ENDPOINTS member add $(hostname) http://${MYIP}:2380 | grep ETCD_)

echo $res | sed 's/^/export /g' >/tmp/etcd_join_env

source /tmp/etcd_join_env

CMD="etcd --listen-client-urls http://${MYIP}:2379,http://127.0.0.1:4001 \
     --data-dir /mnt1/etcd \
     --advertise-client-urls http://${MYIP}:2379 \
     --listen-peer-urls http://${MYIP}:2380 \
     --initial-advertise-peer-urls http://${MYIP}:2380"

exec setuidgid root $CMD>/dev/null