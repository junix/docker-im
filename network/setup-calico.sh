#!/bin/bash
export ETCD_ENDPOINTS=${ETCD_ENDPOINTS:-'http://10.10.92.203:2379,http://10.10.93.174:2379,http://10.10.86.15:2379,http://10.10.94.51:2379,http://10.10.95.147:2379,http://10.10.90.194:2379,http://10.10.86.12:2379'}
PROGRAM=/usr/local/bin/calicoctl
cp ./calicoctl ${PROGRAM}
chmod +x $PROGRAM
$PROGRAM node run