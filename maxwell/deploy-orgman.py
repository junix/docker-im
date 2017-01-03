#!/usr/bin/env python3
__author__ = 'junix'

import sys, os, getopt, re


def fetch_env(env_key):
    env_value = os.getenv(env_key)
    if env_value is None:
        return ''
    else:
        return "--env {env_key}={env_value}".format(env_key=env_key, env_value=env_value)


def compact(raw):
    return re.sub(r"""\s{2,}""", ' ', raw)


def docker_cmd(pid):
    cmd = "docker run --restart always \
        --network orgman \
        --ip 192.0.3.{index} \
        --env NODE_ID={node_id} \
        {zk_env} \
        {mq_env} \
        -d \
        junix/orgman".format(
        index=pid,
        node_id=pid,
        zk_env=fetch_env("ZOOKEEPER"),
        mq_env=fetch_env("KAFKA_TOPIC"))
    return compact(cmd)


def ssh_cmd(host, cmd):
    return "ssh {host} '{cmd}'".format(host=host, cmd=cmd)


if __name__ == "__main__":
    optlist, hosts = getopt.getopt(sys.argv[1:], 'n:', ['dryrun'])
    if not hosts:
        print("usage:./deploy-orgman.py [-n node_id_start_from] [--dryrun] hosts")
        print("env:   ZOOKEEPER=192.0.2.[1-5]:2181")
        print("       KAFKA_TOPIC")
        sys.exit(1)
    start_from = int(dict(optlist).get('-n', '1'))
    for index, host in enumerate(hosts):
        pid = index + start_from
        cmd = ssh_cmd(host, docker_cmd(pid))
        if '--dryrun' in dict(optlist).keys():
            print(cmd)
        else:
            os.system(cmd)
