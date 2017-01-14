#!/usr/bin/env python

import sys
from container import Container

if __name__ == '__main__':
    containers = sys.argv[1:]
    if len(containers) != 1:
        print('usage:envof.py container')
        sys.exit(1)

    container = Container(containers[0])
    for e in container.env():
        print(e)
