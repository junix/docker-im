#!/usr/bin/env python
import sys
import os
import getopt

from docker_cmd import DockerCmd
import utils


class KafkaCmd(DockerCmd):

    def __init__(self, broker_id):
        DockerCmd.__init__(self)
        self.node_id = broker_id
        self.use_image('yunxuetang/kafka:2.9.1').\
            daemon_mode().\
            with_name(self.instance_name()).\
            copy_os_env('ZOOKEEPER', utils.zk_env()). \
            copy_os_env('KAFKA_HEAP_OPTS', '-Xms1G -Xmx4G'). \
            with_env('BROKER_ID', broker_id). \
            with_network(network='kafka', ip=utils.ip_of('kafka', broker_id)). \
            with_mount_from_env('DATA_DIR', '/app/data'). \
            with_mount_from_env('LOG_DIR', '/app/logs')

    def instance_name(self):
        return '{prefix}{pid}'.format(prefix=os.getenv('NAME_PREFIX', 'kafka'), pid=self.node_id)


def usage():
    print('''usage:deploy-kafka.py [--dryrun] hosts
env: ZOOKEEPER    : 192.0.2.[1-5]:2181
     NAME_PREFIX  : kafka
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
        c.run('--dryrun' in options)
