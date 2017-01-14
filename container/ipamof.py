#!/usr/bin/env python

import sys
from container import Container

if __name__ == '__main__':
    containers = sys.argv[1:]
    if len(containers) == 0:
        print('usage:ipof.py containers')
        sys.exit(1)
    container = Container(containers[0])
    ipams = container.ipam()
    if not ipams or len(ipams) == 0:
        print('none')
    else:
        print(','.join(ipams))
