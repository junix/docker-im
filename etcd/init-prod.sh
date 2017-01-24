#!/bin/bash

rm -rvf /mnt1/etcd/*

INIT_CLUSTER="\
i821-bj=http://10.10.31.56:2380,\
i822-bj=http://10.10.53.26:2380,\
i823-bj=http://10.10.60.240:2380,\
i824-bj=http://10.10.39.177:2380,\
i825-bj=http://10.10.38.126:2380"

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
