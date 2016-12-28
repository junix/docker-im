#!/usr/bin/env python
import os, sys


def subnet(name):
    if name == "zookeeper":
        return "192.0.2.0"
    elif name == "orgman":
        return "192.0.3.0"
    elif name == "qida":
        return "192.0.4.0"
    elif name == "lecai":
        return "192.0.5.0"
    else:
        raise ValueError("unknown net:" + name)


def create_pool_yaml(name):
    spec = \
"""- apiVersion: v1
  kind: ipPool
  metadata:
    cidr: {subnet}/24
""".format(subnet=subnet(name))
    fd = open("ippool-{name}.yaml".format(name=name), "w")
    fd.write(spec)
    fd.close()

def delete_cali_net(name):
    create_pool_yaml(name)
    cmd_list = [
        "docker network rm {name}".format(name=name),
        "calicoctl delete -f ippool-{name}.yaml".format(name=name)
    ]
    [os.system(cmd) for cmd in cmd_list]

if __name__ == "__main__":
    nets = sys.argv[1:]
    [delete_cali_net(net) for net in nets]
