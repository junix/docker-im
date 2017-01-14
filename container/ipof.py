#!/usr/bin/env python

import sys
from container import Container

if __name__ == '__main__':
    containers = sys.argv[1:]
    if len(containers) != 1:
        print('usage:ipof.py container')
        sys.exit(1)
    container = Container(containers.pop())
    ips = container.ip()
    if len(ips) == 0:
        print('none')
    else:
        print(','.join(ips))