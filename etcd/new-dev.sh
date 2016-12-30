#!/bin/bash
rm -rvf /mnt1/etcd/*
etcd -name $(hostname) \
  --data-dir /mnt1/etcd \
  -initial-advertise-peer-urls http://${MYIP}:2380 \
  -listen-peer-urls http://${MYIP}:2380 \
  -listen-client-urls http://${MYIP}:2379,http://127.0.0.1:4001 \
  -advertise-client-urls http://${MYIP}:2379 \
  -initial-cluster-token etcd-cluster-starfish \
  -initial-cluster \
i901-bj=http://10.10.191.38:2380,\
i902-bj=http://10.10.181.41:2380,\
i204-gd=http://10.10.128.69:2380,\
i205-gd=http://10.10.116.204:2380\
  -initial-cluster-state new>/dev/null
