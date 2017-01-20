#!/usr/bin/env python
import sys
import os
import getopt

from docker_cmd import DockerCmd
import utils


class FrontendCmd(DockerCmd):

    def __init__(self, node_id):
        DockerCmd.__init__(self)
        name = 'fg{gid}p{pid}'.format(gid=os.getenv('GROUP_ID'), pid=node_id)
        self.use_image('yunxuetang/maxwell_frontend').\
            daemon_mode(). \
            with_network(network='host'). \
            with_name(name).\
            copy_os_env('ZOOKEEPER', utils.zk_env()). \
            copy_os_env('GROUP_ID', can_ignore=False). \
            copy_os_env('EXTERNAL_IP', can_ignore=False). \
            copy_os_env('EXTERNAL_PORT', default_value=2013). \
            copy_os_env('INTERNAL_IP'). \
            with_env('NODE_ID', node_id)


def usage():
    print('''usage:deploy-frontend [--dryrun] hosts
    env: ZOOKEEPER default 192.0.2.[1-5]:2181
         GROUP_ID
         EXTERNAL_PORT default 2013
         EXTERNAL_IP
         NAME_PREFIX default nil''')


if __name__ == '__main__':
    optlist, hosts = getopt.getopt(sys.argv[1:], '', ['dryrun'])
    if not hosts:
        usage()
        sys.exit(1)
    for index, host in enumerate(hosts):
        FrontendCmd(index).\
            exec_in(host).\
            execute('--dryrun' in dict(optlist))
