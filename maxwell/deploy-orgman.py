#!/usr/bin/env python3
__author__ = 'junix'

import sys, os, getopt


def docker_cmd(gid, pid):
    return \
        "docker run --restart always \
        --network starfish \
        --ip 192.0.2.{index} \
        --env NODE_ID={pid} \
        -d \
        junix/orgman".format(gid=gid, index=20 + pid, pid=pid)


def ssh_cmd(host, cmd):
    return "ssh {host} '{cmd}'".format(host=host, cmd=cmd)


if __name__ == "__main__":
    optlist, hosts = getopt.getopt(sys.argv[1:], 'g:')
    if hosts == [] or optlist == []:
        print("usage: cmd --group_id=gid hosts")
        sys.exit(1)
    gid = int(dict(optlist).get('-g'))
    for index, host in enumerate(hosts):
        pid = index + 1
        cmd = ssh_cmd(host, docker_cmd(gid, pid))
        os.system(cmd)
