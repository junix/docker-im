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
        container.restart()
