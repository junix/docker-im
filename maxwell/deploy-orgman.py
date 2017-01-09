#!/usr/bin/env python3
import getopt
import sys

from docker_cmd import DockerCmd


class OrgmanCmd(DockerCmd):

    def __init__(self, pid, offset):
        DockerCmd.__init__(self)
        self.pid = pid
        self.use_image('junix/orgman').daemon_mode(). \
            with_network(net='orgman', ip='192.0.3.{index}'.format(index=offset + pid)). \
            with_env('NODE_ID', pid).with_os_env('ZOOKEEPER'). \
            with_os_env('KAFKA_TOPIC').with_mount_from_env('DATA_DIR', '/app/data'). \
            with_mount_from_env('LOG_DIR', '/app/log')


if __name__ == "__main__":
    optlist, hosts = getopt.getopt(sys.argv[1:], 'f:n:', ['dryrun'])
    if not hosts:
        print(
            "usage:./deploy-orgman.py [-n node_id_start_from] [--dryrun] hosts")
        print("env:   ZOOKEEPER=192.0.2.[1-5]:2181")
        print("       KAFKA_TOPIC")
        sys.exit(1)
    start_from = int(dict(optlist).get('-n', '1'))
    ip_offset = int(dict(optlist).get('-f', '0'))
    for index, host in enumerate(hosts):
        pid = index + start_from
        c = OrgmanCmd(offset=ip_offset, pid=pid)
        c.exec_in(host)
        if '--dryrun' in dict(optlist).keys():
            c.show()
        else:
            c.execute()
