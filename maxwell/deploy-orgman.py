#!/usr/bin/env python3
__author__ = 'junix'

import sys, os, getopt


def zk_addr():
    return os.getenv("ZOOKEEPER", '192.0.2.1:2181,192.0.2.2:2181,192.0.2.3:2181')


def org_msg_mq():
    return os.getenv("KAFKA_TOPIC", 'org_message')


def docker_cmd(pid):
    return \
        "docker run --restart always \
        --network orgman \
        --ip 192.0.3.{index} \
        --env NODE_ID={node_id} \
        --env ZOOKEEPER={zk} \
        --env KAFKA_TOPIC={mq} \
        -d \
        junix/orgman".format(
            index=pid,
            node_id=pid,
            zk=zk_addr(),
            mq=org_msg_mq())


def ssh_cmd(host, cmd):
    return "ssh {host} '{cmd}'".format(host=host, cmd=cmd)

if __name__ == "__main__":
    optlist, hosts = getopt.getopt(sys.argv[1:], 'n:')
    if hosts == [] or optlist == []:
        print("usage:cmd -n nid host_to_deploy")
        sys.exit(1)
    nid = int(dict(optlist).get('-n'))
    for index, host in enumerate(hosts):
        pid = index + 1
        cmd = ssh_cmd(host, docker_cmd(nid))
        print(cmd)
        os.system(cmd)
