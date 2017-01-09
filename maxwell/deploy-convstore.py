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
        node_ip = '192.0.7.{index}'.format(index=ip_offset + node_id)
        self.use_image('junix/conv_store').daemon_mode(). \
            with_network(net='conv_store', ip=node_ip). \
            with_name('{prefix}{id}'.format(prefix=name_prefix, id=node_id)). \
            with_os_env('ZOOKEEPER', utils.zk_env(1, 5)). \
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
        c.exec_in(host)
        if '--dryrun' in dict(optlist).keys():
            print(utils.compact(c.command()))
        else:
            os.system(c.command())
