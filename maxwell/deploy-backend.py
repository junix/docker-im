#!/usr/bin/env python
import sys
import os
import getopt

from docker_cmd import DockerCmd
import utils


class BackendCmd(DockerCmd):
    def __init__(self, node_id):
        DockerCmd.__init__(self)
        self.node_id = node_id
        self.group_id = int(os.getenv("GROUP_ID", '0'))
        self.image = 'yunxuetang/maxwell_backend'
        self.daemon = True
        self.name = self.full_name()
        self.network = 'maxwell'
        self.copy_os_env('ZOOKEEPER', utils.zk_env()). \
            with_restart(False). \
            copy_os_env('GROUP_ID', can_ignore=False). \
            with_mount_from_env('DATA_DIR', '/app/data'). \
            with_mount_from_env('LOG_DIR', '/app/log'). \
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
    free_ip_list = utils.free_ip_list_of('maxwell')
    for index, host in enumerate(hosts):
        dryrun = '--dryrun' in dict(optlist).keys()
        c = BackendCmd(index)
        c.exec_in(host). \
            with_network('maxwell', ip=free_ip_list.send(None)). \
            execute(dryrun=dryrun)
