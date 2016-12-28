#!/usr/bin/env python3
import sys, os


def generate_server_conf(instances):
    conf_list = ["server.%d=zk%d:2888:3888" % (i, i) for i in range(1, len(instances) + 1)]
    return ' '.join(conf_list)


def start_zk_cmd(index, conf):
    return \
        "docker run --restart always\
         --network starfish\
         --ip 192.0.2.{index}\
         --name zk{index}\
         --env  ZOO_MY_ID={index}\
         --env ZOO_SERVERS=\"{conf}\"\
         -d\
         zookeeper:3.4.9".format(index=index+1, conf=conf)


def ssh_cmd(host, cmd):
    return "ssh {host} '{cmd}'".format(host=host, cmd=cmd)


if __name__ == "__main__":
    instances = sys.argv[1:]
    if len(instances) == 0:
        print("usage:cmd [host]")
        sys.exit(1)

    conf = generate_server_conf(instances)
    for index, host in enumerate(instances):
        os.system(ssh_cmd(host, start_zk_cmd(index, conf)))
