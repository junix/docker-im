#!/usr/bin/env python

import sys
import utils

if __name__ == '__main__':
    containers = sys.argv[1:]
    if len(containers) != 1:
        print('usage:networkof.py container')
        sys.exit(1)

    for n in utils.network_of_container(containers[0]):
        print(n)
