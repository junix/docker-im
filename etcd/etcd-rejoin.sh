#!/usr/bin/env bash
MYIP="ddddddd"
ETCD_ENDPOINTS="http://10.10.92.203:2379,http://10.10.93.174:2379,http://10.10.86.15:2379,http://10.10.94.51:2379,http://10.10.95.147:2379,http://10.10.90.194:2379,http://10.10.86.12:2379"
ETCD_ENDPOINTS="http://10.10.191.38:2379,http://10.10.181.41:2379,http://10.10.128.69:2379,10.10.116.204:2379"
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