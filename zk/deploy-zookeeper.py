#!/usr/bin/env python3
import sys, os, getopt,re


def generate_server_conf(instances):
    conf_list = ["server.%d=zk%d:2888:3888" % (i, i) for i in range(1, len(instances) + 1)]
    return ' '.join(conf_list)


def instance_name(index):
    return "zk{index}".format(index=index)


def data_dir_map(index):
    dir = os.getenv("DATA_DIR")
    if dir is None:
        return ''
    else:
        return "-v {dir}/{instance}:/data".format(
            dir=dir,
            instance=instance_name(index))


def data_log_dir_map(index):
    dir = os.getenv("DATA_LOG_DIR")
    if dir is None:
        return ''
    else:
        return "-v {dir}/{instance}:/datalog".format(
            dir=dir,
            instance=instance_name(index))


def start_zk_cmd(index, conf):
    return \
        "docker run --restart always\
         --network zookeeper\
         --ip 192.0.2.{index}\
         --name zk{index}\
         --env  ZOO_MY_ID={index}\
         --env ZOO_SERVERS=\"{conf}\"\
         {data_dir} {data_log_dir}\
         -d \
         zookeeper:3.4.9".format(
            index=index,
            conf=conf,
            data_dir=data_dir_map(index),
            data_log_dir=data_log_dir_map(index))


def ssh_cmd(host, cmd):
    return "ssh {host} '{cmd}'".format(host=host, cmd=cmd)


def usage():
    print("""usage:./deploy-zookeeper.py [--dryrun] hosts
env: DATA_DIR     : -v $DATA_DIR/{instance}:/data
     DATA_LOG_DIR : -v $DATA_LOG_DIR/{instance}:/datalog""")

def compact(raw):
    return re.sub(r"""\s{2,}""", ' ', raw)

if __name__ == "__main__":
    options, instances = getopt.getopt(sys.argv[1:], "", ["dryrun"])
    if len(instances) == 0:
        usage()
        sys.exit(1)

    conf = generate_server_conf(instances)
    for index, host in enumerate(instances):
        cmd = ssh_cmd(host, start_zk_cmd(index + 1, conf))
        if '--dryrun' in dict(options).keys():
            print(compact(cmd))
        else:
            os.system(cmd)
