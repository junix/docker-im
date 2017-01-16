#!/usr/bin/env python3
import sys
import os
import getopt

from docker_cmd import DockerCmd
import utils


class FrontendCmd(DockerCmd):

    def __init__(self, node_id):
        DockerCmd.__init__(self)
        name_prefix = os.getenv('NAME_PREFIX', 'f')
        group_id = int(os.getenv("GROUP_ID", '0'))
        self.use_image('junix/maxwell_frontend').daemon_mode(). \
            with_network(network='host'). \
            with_name('{prefix}g{gid}p{pid}'.format(prefix=name_prefix, gid=group_id, pid=node_id)). \
            copy_os_env('ZOOKEEPER', utils.zk_env()). \
            copy_os_env('GROUP_ID', can_ignore=False). \
            copy_os_env('EXTERNAL_IP', can_ignore=False). \
            copy_os_env('EXTERNAL_PORT', default_value=2013). \
            with_env('NODE_ID', node_id)


def usage():
    print("""usage:deploy-frontend hosts
    env: ZOOKEEPER default 192.0.2.[1-5]:2181
         GROUP_ID
         EXTERNAL_PORT default 2013
         EXTERNAL_IP
         NAME_PREFIX default nil""")


if __name__ == "__main__":
    optlist, hosts = getopt.getopt(sys.argv[1:], '', ['dryrun'])
    if not hosts:
        usage()
        sys.exit(1)
    for index, host in enumerate(hosts):
        FrontendCmd(index).\
            exec_in(host).\
            execute('--dryrun' in dict(optlist).keys())
