#!/usr/bin/env python

import sys
import getopt
import utils
from container import Container

if __name__ == '__main__':
    optlist, containers = getopt.getopt(sys.argv[1:], '', ['--dryrun'])
    options = dict(optlist)
    if len(containers) != 1:
        print('usage:restart [--dryrun] container')
        sys.exit(1)
    dryrun = '--dryrun' in options
    for c in containers:
        container = Container(containers[0])
        ips = container.ip()
        for ip in ips:
            cmd = 'calicoctl ipam release --ip={ip}'.format(ip=ip)
            utils.run(cmd, dryrun)
        cmd = 'docker start {container}'.format(container=containers[0])
        utils.run(cmd, dryrun)
