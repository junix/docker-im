#!/usr/bin/env python3
import sys
import os
import getopt

from docker_cmd import DockerCmd
from utils import zk_env


class BackendCmd(DockerCmd):
    def __init__(self, node_id):
        DockerCmd.__init__(self)
        self.node_id = node_id
        self.group_id = int(os.getenv("GROUP_ID", '0'))
        self.image = 'junix/maxwell_backend'
        self.daemon = True
        self.name = self.full_name()
        self.network = 'maxwell'
        self.copy_os_env('ZOOKEEPER', zk_env(1, 5)). \
            copy_os_env('GROUP_ID', can_ignore=False). \
            with_env('PARTITION_ID', node_id)

    def full_name(self):
        return '{prefix}g{gid}p{pid}'.format(
            prefix=os.getenv('NAME_PREFIX', 'b'),
            gid=self.group_id,
            pid=self.node_id)


def usage():
    print("""usage:deploy-backend hosts
    env: ZOOKEEPER default 192.0.2.[1-5]:2181
         GROUP_ID
         NAME_PREFIX default nil""")


if __name__ == "__main__":
    optlist, hosts = getopt.getopt(sys.argv[1:], '', ['dryrun'])
    if not hosts:
        usage()
        sys.exit(1)
    for index, host in enumerate(hosts):
        c = BackendCmd(index).exec_in(host)
        dryrun = '--dryrun' in dict(optlist).keys()
        c.execute(dryrun=dryrun)
