#!/usr/bin/env python3
import sys
import os
import getopt

from docker_cmd import DockerCmd
from utils import zk_env


class BackendCmd(DockerCmd):

    def __init__(self, node_id, offset):
        DockerCmd.__init__(self)
        name_prefix = os.getenv('NAME_PREFIX', 'b')
        group_id = int(os.getenv("GROUP_ID", '0'))
        self.use_image('junix/maxwell_backend').daemon_mode(). \
            with_network(net='maxwell'). \
            with_name('{prefix}g{gid}p{pid}'.format(prefix=name_prefix, gid=group_id, pid=node_id)). \
            with_os_env('ZOOKEEPER', zk_env(1, 5)). \
            with_os_env('GROUP_ID', skip=False). \
            with_env('PARTITION_ID', node_id)


def usage():
    print("""usage:deploy-backend hosts
    env: ZOOKEEPER default 192.0.2.[1-5]:2181
         GROUP_ID
         NAME_PREFIX default nil""")


if __name__ == "__main__":
    optlist, hosts = getopt.getopt(sys.argv[1:], 'f:', ['dryrun'])
    if not hosts:
        usage()
        sys.exit(1)
    offset = int(dict(optlist).get('-f', '0'))
    for index, host in enumerate(hosts):
        pid = index + 1
        c = BackendCmd(node_id=pid, offset=offset)
        c.exec_in(host)
        dryrun = '--dryrun' in dict(optlist).keys()
        c.execute(dryrun=dryrun)
