#!/usr/bin/env python3
__author__ = 'junix'

import sys, os, getopt, re


def env_or_nil(env_key):
    env_value = os.getenv(env_key)
    if env_value is None:
        return ''
    else:
        return "--env {env_key}={env_value}".format(env_key=env_key, env_value=env_value)


def env_or(env_key, default_value):
    env_value = os.getenv(env_key, default_value)
    return "--env {env_key}={env_value}".format(env_key=env_key, env_value=env_value)


def env_or_error(env_key):
    env_value = os.getenv(env_key)
    if env_value is None:
        raise ValueError('env %s is nil' % env_key)
    else:
        return "--env {env_key}={env_value}".format(env_key=env_key, env_value=env_value)


def compact(raw):
    return re.sub(r"""\s{2,}""", ' ', raw)


def docker_cmd(pid):
    defaut_zk = ','.join(
        ["192.0.2.1:2181",
         "192.0.2.2:2181",
         "192.0.2.3:2181",
         "192.0.2.4:2181",
         "192.0.2.5:2181"])
    cmd = "docker run \
        --restart always \
        --network sinker \
        {zk_env} \
        {group_env} \
        {partitions_env} \
        -d \
        junix/sinker".format(
        zk_env=env_or("ZOOKEEPER", defaut_zk),
        group_env=env_or_error("GROUP_ID"),
        partitions_env=env_or_error("PARTITIONS"))

    return compact(cmd)


def ssh_cmd(host, cmd):
    return "ssh {host} '{cmd}'".format(host=host, cmd=cmd)


def usage():
    print("usage:./deploy-sinker.py [-n node_id_start_from] [--dryrun] hosts")
    print("env:   ZOOKEEPER=192.0.2.[1-5]:2181")
    print("       GROUP_ID")
    print("       PARTITIONS")


if __name__ == "__main__":
    optlist, hosts = getopt.getopt(sys.argv[1:], '', ['dryrun'])
    if not hosts:
        usage()
    for index, host in enumerate(hosts):
        cmd = ssh_cmd(host, docker_cmd(index+1))
        if '--dryrun' in dict(optlist).keys():
            print(cmd)
        else:
            os.system(cmd)
