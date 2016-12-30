#!/usr/bin/env python3
import sys, os


def instance_name(index):
    return "kafka{index}".format(index=index)


def data_dir_map(index):
    dir = os.getenv("DATA_DIR")
    if dir is None:
        return ''
    else:
        return "-v {dir}/{instance}:/app/data".format(
            dir=dir,
            instance=instance_name(index))


def data_log_dir_map(index):
    dir = os.getenv("DATA_LOG_DIR")
    if dir is None:
        return ''
    else:
        return "-v {dir}/{instance}:/app/logs".format(
            dir=dir,
            instance=instance_name(index))


def start_kafka_cmd(index):
    return \
        "docker run --restart always\
         --network zookeeper\
         --ip 192.0.8.{index}\
         --name kafka{index}\
         --env BROKER_ID={index}\
         {data_dir} {data_log_dir}\
         -d junix/kafka".format(
            index=index,
            data_dir=data_dir_map(index),
            data_log_dir=data_log_dir_map(index))


def ssh_cmd(host, cmd):
    return "ssh {host} '{cmd}'".format(host=host, cmd=cmd)


if __name__ == "__main__":
    instances = sys.argv[1:]
    if len(instances) == 0:
        print("usage:cmd [host]")
        sys.exit(1)

    for index, host in enumerate(instances):
        cmd = ssh_cmd(host, start_kafka_cmd(index + 1))
        print(cmd)
        os.system(cmd)
