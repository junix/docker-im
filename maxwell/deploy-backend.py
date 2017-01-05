#!/usr/bin/env python3
__author__ = 'junix'

import sys, os, getopt, re


def env_or_nil(env_key):
    v = os.getenv(env_key)
    return v if v is not None else ''


def env_or_error(env_key):
    v = os.getenv(env_key)
    if v is None:
        raise ValueError('env %s is nil' % env_key)
    else:
        return v


def zk_env():
    zk = env_or_nil("ZOOKEEPER")
    return '' if zk == '' else '--env ZOOKEEPER={zk}'.format(zk=zk)


def name_prefix():
    v = os.getenv("NAME_PREFIX")
    return v if v is not None else ''


def compact(raw):
    return re.sub(r"""\s{2,}""", ' ', raw)


def docker_cmd(gid, pid):
    cmd = "docker run \
        --restart always \
        --network maxwell \
        --env GROUP_ID={gid} \
        --env NODE_ID={pid} \
        {zk_env} \
        --name={name}bg{gid}p{pid}\
        -d \
        junix/maxwell_backend".format(
        gid=gid,
        name=name_prefix(),
        zk_env=zk_env(),
        pid=pid)
    return compact(cmd)


def ssh_cmd(host, cmd):
    return "ssh {host} '{cmd}'".format(host=host, cmd=cmd)


def usage():
    print("""usage:deploy-backend hosts
    env: ZOOKEEPER default 192.0.2.[1-5]:2181
         GROUP_ID
         NAME_PREFIX default nil""")


if __name__ == "__main__":
    optlist, hosts = getopt.getopt(sys.argv[1:], '', ['dryrun'])
    if not hosts:
        usage()
        sys.exit(1)
    gid = int(env_or_error("GROUP_ID"))
    for index, host in enumerate(hosts):
        pid = index
        cmd = ssh_cmd(host, docker_cmd(gid, pid))
        if '--dryrun' in dict(optlist).keys():
            print(cmd)
        else:
            os.system(cmd)