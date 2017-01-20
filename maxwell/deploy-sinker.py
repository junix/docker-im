#!/usr/bin/env python
import sys
import os
import getopt
from docker_cmd import DockerCmd
from utils import zk_env


class SinkerCmd(DockerCmd):

    def __init__(self, node_id):
        DockerCmd.__init__(self)
        name_prefix = os.getenv('NAME_PREFIX', 'sinker')
        self.use_image('yunxuetang/sinker').\
            daemon_mode(). \
            with_network(network='sinker'). \
            with_name('{prefix}{id}'.format(prefix=name_prefix, id=node_id)). \
            copy_os_env('ZOOKEEPER', zk_env()). \
            copy_os_env('GROUP_ID', can_ignore=False). \
            copy_os_env('PARTITIONS', can_ignore=False). \
            with_env('NODE_ID', node_id)


def usage():
    print("usage:./deploy-sinker.py [-n node_id_start_from] [--dryrun] hosts")
    print("env:   ZOOKEEPER=192.0.2.[1-5]:2181")
    print("       GROUP_ID")
    print("       PARTITIONS")


if __name__ == "__main__":
    optlist, hosts = getopt.getopt(sys.argv[1:], 'm:c:', ['dryrun'])
    if not hosts:
        usage()
    options = dict(optlist)
    memory_limit = options.get('-m', '500m')
    cpu_shares = options.get('-c', '512')
    for index, host in enumerate(hosts):
        SinkerCmd(index).\
            exec_in(host).\
            limit_memory(memory_limit).\
            limit_cpu_shares(cpu_shares).\
            execute(dryrun='--dryrun' in dict(optlist).keys())
