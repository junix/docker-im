#!/bin/bash

rm -rvf /mnt1/etcd/*

INIT_CLUSTER="\
i901-bj=http://10.10.191.38:2380,\
i204-gd=http://10.10.128.69:2380"

INTERNAL_IP=${INTERNAL_IP:127.0.0.1}

INIT_CMD="etcd -name $(hostname) \
  --data-dir /mnt1/etcd \
  -initial-advertise-peer-urls http://${INTERNAL_IP}:2380 \
  -listen-peer-urls http://${INTERNAL_IP}:2380 \
  -listen-client-urls http://${INTERNAL_IP}:2379,http://127.0.0.1:4001 \
  -advertise-client-urls http://${INTERNAL_IP}:2379 \
  -initial-cluster-token etcd-cluster-starfish \
  -initial-cluster ${INIT_CLUSTER} \
  -initial-cluster-state new>/dev/null"

bash -c ${INIT_CMD}
