#!/usr/bin/env python3
import sys, os, getopt
from utils import env_or, compact, ssh_cmd
from docker_cmd import DockerCmd


def generate_server_conf(instances, offset=0):
    conf_list = ["server.{index}={instance}:2888:3888".format(
        index=i+1,
        instance=instance_name(i + offset)) for i in range(0, len(instances))]
    return ' '.join(conf_list)


def instance_name(index):
    return "{name_prefix}{index}".format(
        name_prefix=env_or('NAME_PREFIX', 'zk'),
        index=index)


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


def start_zk_cmd(index, offset, conf):
    c = DockerCmd()
    c.use_image('zookeeper:3.4.9').\
        with_restart().\
        daemon_mode().\
        with_network('zookeeper', ip='192.0.2.{index}'.format(index=index+offset)).\
        with_env('ZOO_MY_ID', index+1).\
        with_name('zk{index}'.format(index=index+offset)).\
        with_mount_from_env('DATA_DIR', '/data'). \
        with_mount_from_env('DATA_LOG_DIR', '/datalog').\
        with_env('ZOO_SERVICES', conf)
    return c.command()


def usage():
    print("""usage:./deploy-zookeeper.py [--dryrun] hosts
env: DATA_DIR     : -v $DATA_DIR/{instance}:/data
     DATA_LOG_DIR : -v $DATA_LOG_DIR/{instance}:/datalog""")


if __name__ == "__main__":
    options, instances = getopt.getopt(sys.argv[1:], "f:", ["dryrun"])
    if len(instances) == 0:
        usage()
        sys.exit(1)
    offset = int(dict(options).get('-f', '1'))
    conf = generate_server_conf(instances, offset)
    for index, host in enumerate(instances):
        cmd = ssh_cmd(host, start_zk_cmd(index, offset, conf))
        if '--dryrun' in dict(options).keys():
            print(compact(cmd))
        else:
            os.system(cmd)
