#!/usr/bin/env python

import sys
import utils

if __name__ == '__main__':
    containers = sys.argv[1:]
    if len(containers) != 1:
        print('usage:envof.py container')
        sys.exit(1)
    print(utils.env_of_container(containers[0]))
