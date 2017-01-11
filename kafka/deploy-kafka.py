#!/usr/bin/env python3
import sys
import os
import getopt

from docker_cmd import DockerCmd
from utils import zk_env


class KafkaCmd(DockerCmd):

    def __init__(self, node_id):
        DockerCmd.__init__(self)
        self.node_id = node_id
        self.use_image('junix/kafka').\
            daemon_mode().\
            with_name(self.instance_name()).\
            copy_os_env('ZOOKEEPER', zk_env(offset=1, count=5)). \
            with_env('BROKER_ID', node_id). \
            with_network(network='kafka', ip='192.0.8.{pid}'.format(pid=node_id)). \
            with_mount_from_env('DATA_DIR', '/app/data'). \
            with_mount_from_env('LOG_DIR', '/app/logs')

    def instance_name(self):
        return '{prefix}{pid}'.format(prefix=os.getenv('NAME_PREFIX', 'kafka'), pid=self.node_id)


def usage():
    print('''usage:./deploy-kafka.py [--dryrun] hosts
env: ZOOKEEPER    : 192.0.2.[1-5]:2181
     DATA_DIR     : -v $DATA_DIR/{instance}:/app/data
     LOG_DIR      : -v $DATA_DIR/{instance}:/app/logs''')


if __name__ == '__main__':
    optlist, instances = getopt.getopt(sys.argv[1:], '', ['dryrun'])
    options = dict(optlist)
    if not instances:
        usage()
        sys.exit(1)

    for index, host in enumerate(instances):
        c = KafkaCmd(index + 1).exec_in(host)
        c.execute('--dryrun' in options)
