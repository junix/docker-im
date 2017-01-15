#!/usr/bin/env python3
import sys
import os
import getopt
import docker_cmd
import utils


class ConvStoreCmd(docker_cmd.DockerCmd):
    def __init__(self, ip_offset, node_id):
        docker_cmd.DockerCmd.__init__(self)
        name_prefix = os.getenv('NAME_PREFIX', 'convstore')
        node_ip = utils.ip_of('conv_store', ip_offset + node_id)
        self.use_image('junix/conv_store').daemon_mode(). \
            with_network(network='conv_store', ip=node_ip). \
            with_name('{prefix}{id}'.format(prefix=name_prefix, id=node_id)). \
            copy_os_env('ZOOKEEPER', utils.zk_env()). \
            with_env('NODE_ID', node_id)


if __name__ == "__main__":
    optlist, hosts = getopt.getopt(sys.argv[1:], 'f:', ['dryrun'])
    if not hosts:
        print("usage:cmd hosts")
        sys.exit(1)
    offset = int(dict(optlist).get('-f', '0'))
    for index, host in enumerate(hosts):
        pid = index + 1
        c = ConvStoreCmd(ip_offset=offset, node_id=pid)
        c.exec_in(host).execute(dryrun='--dryrun' in dict(optlist).keys())
