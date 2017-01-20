#!/usr/bin/env python3
import getopt
import sys
import os

from docker_cmd import DockerCmd
import utils


class OrgmanCmd(DockerCmd):
    def __init__(self, pid, offset):
        DockerCmd.__init__(self)
        self.pid = pid
        ip = utils.ip_of('orgman', pid + offset)
        name = '{prefix}{pid}'.format(
            prefix=os.getenv('NAME_PREFIX', 'orgman'),
            pid=pid)
        self.use_image('yunxuetang/orgman').\
            daemon_mode(). \
            with_name(name).\
            with_network(network='orgman', ip=ip). \
            with_env('NODE_ID', pid).\
            copy_os_env('ZOOKEEPER'). \
            copy_os_env('KAFKA_TOPIC').\
            with_mount_from_env('DATA_DIR', '/app/data'). \
            with_mount_from_env('LOG_DIR', '/app/log')


if __name__ == "__main__":
    optlist, hosts = getopt.getopt(sys.argv[1:], 'f:n:', ['dryrun'])
    if not hosts:
        print(
            "usage:./deploy-orgman.py [-n node_id_start_from] [--dryrun] hosts")
        print("env:   ZOOKEEPER=192.0.2.[1-5]:2181")
        print("       KAFKA_TOPIC")
        sys.exit(1)
    start_from = int(dict(optlist).get('-n', '0'))
    ip_offset = int(dict(optlist).get('-f', '1'))
    for index, host in enumerate(hosts):
        pid = index + start_from
        c = OrgmanCmd(offset=ip_offset, pid=pid)
        c.exec_in(host).execute(dryrun='--dryrun' in dict(optlist).keys())
