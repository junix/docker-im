#!/usr/bin/env python
import sys
import os
import getopt
import docker_cmd
import utils


class ConvStoreCmd(docker_cmd.DockerCmd):
    def __init__(self, ip_offset, node_id):
        docker_cmd.DockerCmd.__init__(self)
        name = 'convstore{id}'.format(id=node_id)
        node_ip = utils.ip_of('conv_store', ip_offset + node_id)
        self.use_image('yunxuetang/conv_store').\
            daemon_mode(). \
            with_network(network='conv_store', ip=node_ip). \
            with_name(name).\
            copy_os_env('ZOOKEEPER', utils.zk_env()). \
            with_env('NODE_ID', node_id)


if __name__ == '__main__':
    optlist, hosts = getopt.getopt(sys.argv[1:], 'f:', ['dryrun'])
    if not hosts:
        print('usage:deploy-convstore [-f | --dryrun] hosts')
        sys.exit(1)
    options = dict(optlist)
    offset = int(dict(optlist).get('-f', '1'))
    for index, host in enumerate(hosts):
        ConvStoreCmd(ip_offset=offset, node_id=index).\
            exec_in(host).\
            run(dryrun='--dryrun' in options)
