#!/usr/bin/env python
import os,sys

def delete_cali_net(name):
    cmd_list = [
        "docker network rm {name}".format(name = name),
        "calicoctl delete -f ippool-{name}.yaml".format(name=name),
        "calicoctl delete -f policy-{name}.yaml".format(name=name)
    ]
    [os.system(cmd) for cmd in cmd_list]


if __name__ == "__main__":
    nets = sys.argv[1:]
    [delete_cali_net(net) for net in nets]
