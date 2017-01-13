#!/usr/bin/env python

import sys
import utils

if __name__ == '__main__':
    containers = sys.argv[1:]
    if len(containers) == 0:
        print('usage:ipof.py containers')
        sys.exit(1)
    for c in containers:
        ips = utils.ip_of_container(c)
        if len(ips) == 0:
            print('none')
        else:
            print(','.join(ips))
