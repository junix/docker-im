#!/usr/bin/env python
import getopt
import sys
import os

from docker_cmd import DockerCmd
import utils


class OrgmanCmd(DockerCmd):
    def __init__(self, node_id, offset):
        DockerCmd.__init__(self)
        self.pid = node_id
        ip = utils.ip_of('orgman', node_id + offset)
        name = 'orgman{pid}'.format(pid=node_id)
        self.use_image('yunxuetang/orgman').\
            daemon_mode(). \
            with_name(name).\
            with_network(network='orgman', ip=ip). \
            with_env('NODE_ID', node_id).\
            copy_os_env('ZOOKEEPER'). \
            copy_os_env('KAFKA_TOPIC').\
            with_mount_from_env('DATA_DIR', '/app/data'). \
            with_mount_from_env('LOG_DIR', '/app/log')


if __name__ == '__main__':
    optlist, hosts = getopt.getopt(sys.argv[1:], 'f:n:', ['dryrun'])
    if not hosts:
        print('''usage:./deploy-orgman.py [-n node_id_start_from] [--dryrun] hosts
    env:   ZOOKEEPER=192.0.2.[1-5]:2181')
           DATA_DIR
           LOG_DIR
           KAFKA_TOPIC''')
        sys.exit(1)
    options = dict(optlist)
    start_from = int(options.get('-n', '0'))
    ip_offset = int(options.get('-f', '1'))
    for index, host in enumerate(hosts):
        pid = index + start_from
        OrgmanCmd(offset=ip_offset, node_id=pid).\
            exec_in(host).\
            execute(dryrun='--dryrun' in options)
