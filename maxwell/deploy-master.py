#!/usr/bin/env python3
import sys
import os
import getopt

from docker_cmd import DockerCmd
import utils


class MasterCmd(DockerCmd):

    def __init__(self, node_id, ip_offset):
        DockerCmd.__init__(self)
        name_prefix = os.getenv('NAME_PREFIX', 'm')
        group_id = int(os.getenv("GROUP_ID", '0'))
        node_ip = utils.ip_of('master', ip_offset + node_id + 1)
        self.use_image('junix/maxwell_master').daemon_mode(). \
            with_network(network='master', ip=node_ip). \
            with_name('{prefix}g{gid}p{pid}'.format(prefix=name_prefix, gid=group_id, pid=node_id)). \
            copy_os_env('ZOOKEEPER', utils.zk_env()). \
            copy_os_env('GROUP_ID', can_ignore=False). \
            with_env('NODE_ID', node_id)


def usage():
    print("""usage:deploy-master hosts
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
        c = MasterCmd(node_id=index, ip_offset=offset)
        c.exec_in(host)
        if '--dryrun' in dict(optlist).keys():
            c.show()
        else:
            c.execute()
