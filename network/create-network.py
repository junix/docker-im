#!/usr/bin/env python3

import os, sys


def subnet(name):
    if name == "zookeeper":
        return "192.0.2.0/24"
    elif name == "orgman":
        return "192.0.3.0/24"
    elif name == "qida":
        return "192.0.4.0/24"
    elif name == "lecai":
        return "192.0.5.0/24"
    else:
        raise ValueError("unknown net:" + name)


def create_cali_net(name):
    cmd_list = [
        "calicoctl create -f ippool-{name}.yaml".format(name=name),
        "calicoctl apply -f policy-{name}.yaml".format(name=name),
        "docker network create --driver calico --ipam-driver calico-ipam --subnet{subnet} {name}".format(
            name=name,
            subnet=subnet(name)
        )
    ]
    [os.system(cmd) for cmd in cmd_list]


if __name__ == "__main__":
    nets = sys.argv[1:]
    [create_cali_net(net) for net in nets]
