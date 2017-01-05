#!/usr/bin/env python3
__author__ = 'junix'

import sys, os, getopt


def zk_addr():
    defaut_zk = ','.join(
        ["192.0.2.1:2181",
         "192.0.2.2:2181",
         "192.0.2.3:2181",
         "192.0.2.4:2181",
         "192.0.2.5:2181"])
    return os.getenv("ZOOKEEPER", defaut_zk)


def docker_cmd(pid):
    return \
        "docker run --restart always \
        --network conv_store \
        --ip 192.0.7.{index} \
        --env NODE_ID={node_id} \
        --env ZOOKEEPER={zk} \
        -d \
        junix/conv_store".format(
            index=pid,
            node_id=pid,
            zk=zk_addr())

def ssh_cmd(host, cmd):
    return "ssh {host} '{cmd}'".format(host=host, cmd=cmd)

if __name__ == "__main__":
    hosts = sys.argv[1:]
    if hosts == []:
        print("usage:cmd hosts")
        sys.exit(1)
    for index, host in enumerate(hosts):
        pid = index + 1
        cmd = ssh_cmd(host, docker_cmd(pid))
        print(cmd)
        os.system(cmd)
