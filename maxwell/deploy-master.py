#!/usr/bin/env python3
__author__ = 'junix'

import sys, os, getopt, re


def env_or_nil(env_key):
    env_value = os.getenv(env_key)
    if env_value is None:
        return ''
    else:
        return "--env {env_key}={env_value}".format(env_key=env_key, env_value=env_value)


def name_prefix():
    v = os.getenv("NAME")
    return v if v is not None else ''


def compact(raw):
    return re.sub(r"""\s{2,}""", ' ', raw)


def docker_cmd(gid, pid):
    return \
        "docker run \
        --restart always \
        --network master \
        --ip 192.0.4.{index} \
        --env GROUP_ID={gid} \
        --env NODE_ID={pid} \
        {zookeeper_env} \
        --name={name}mg{gid}p{pid}\
        -d \
        junix/maxwell_master".format(
            gid=gid,
            name=name_prefix(),
            index=10 * gid + pid,
            zookeeper_env=env_or_nil("ZOOKEEPER"),
            pid=pid)


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
