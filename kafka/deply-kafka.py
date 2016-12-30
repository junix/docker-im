#!/usr/bin/env python3
import sys, os, getopt


def instance_name(index):
    return "kafka{index}".format(index=index)


def zookeeper_env():
    zk_conn = os.getenv("ZOOKEEPER")
    if zk_conn is None:
        return ''
    else:
        return "--env ZOOKEEPER={zk}".format(zk=zk_conn)


def data_dir_map(index):
    dir = os.getenv("DATA_DIR")
    if dir is None:
        return ''
    else:
        return "-v {dir}/{instance}:/app/data".format(
            dir=dir,
            instance=instance_name(index))


def data_log_dir_map(index):
    dir = os.getenv("LOG_DIR")
    if dir is None:
        return ''
    else:
        return "-v {dir}/{instance}:/app/logs".format(
            dir=dir,
            instance=instance_name(index))


def start_kafka_cmd(index):
    return \
        "docker run --restart always\
         --network kafka\
         --ip 192.0.8.{index}\
         --name kafka{index}\
         --env BROKER_ID={index}\
         {zookeeper_env} \
         {data_dir} \
         {data_log_dir}\
         -d junix/kafka".format(
            index=index,
            zookeeper_env=zookeeper_env(),
            data_dir=data_dir_map(index),
            data_log_dir=data_log_dir_map(index))


def ssh_cmd(host, cmd):
    return "ssh {host} '{cmd}'".format(host=host, cmd=cmd)


if __name__ == "__main__":
    options,instances = getopt.getopt(sys.argv[1:], "", ["dryrun"])
    if len(instances) == 0:
        print("usage:cmd [host]")
        sys.exit(1)

    for index, host in enumerate(instances):
        cmd = ssh_cmd(host, start_kafka_cmd(index + 1))
        if '--dryrun' in dict(options).keys():
            print(cmd)
        else:
            os.system(cmd)
