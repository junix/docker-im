#!/usr/bin/env python
import sys
import os
import getopt

from docker_cmd import DockerCmd
import utils


class MasterCmd(DockerCmd):

    def __init__(self, node_id, ip_offset):
        DockerCmd.__init__(self)
        node_ip = utils.ip_of('master', ip_offset + node_id)
        name = 'mg{gid}p{pid}'.format(gid=os.getenv('GROUP_ID'), pid=node_id)
        self.use_image('yunxuetang/maxwell_master').daemon_mode(). \
            with_network(network='master', ip=node_ip). \
            with_name(name).\
            copy_os_env('ZOOKEEPER', utils.zk_env()). \
            copy_os_env('GROUP_ID', can_ignore=False). \
            with_env('NODE_ID', node_id)


def usage():
    print('''usage:deploy-master [-f | --dryrun] hosts
    env: ZOOKEEPER default 192.0.2.[1-5]:2181
         GROUP_ID
         NAME_PREFIX default nil''')


if __name__ == '__main__':
    optlist, hosts = getopt.getopt(sys.argv[1:], 'f:', ['dryrun'])
    if not hosts:
        usage()
        sys.exit(1)
    options = dict(optlist)
    offset = int(options.get('-f', '1'))
    for index, host in enumerate(hosts):
        MasterCmd(node_id=index, ip_offset=offset).\
            exec_in(host).\
            run('--dryrun' in options)
