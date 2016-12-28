#!/usr/bin/env python3

import os, sys, getopt


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


def create_cali_net(name):
    create_pool_yaml(name)
    cmd_list = [
        "calicoctl create -f ippool-{name}.yaml".format(name=name),
        "calicoctl apply -f policy-full-connect.yaml".format(name=name),
        "docker network create --driver calico --ipam-driver calico-ipam --subnet={subnet}/24 {name}".format(
            name=name,
            subnet=subnet(name)
        )
    ]
    [os.system(cmd) for cmd in cmd_list]

def delete_cali_net(name):
    create_pool_yaml(name)
    cmd_list = [
        "docker network rm {name}".format(name=name),
        "calicoctl delete -f ippool-{name}.yaml".format(name=name)
    ]
    [os.system(cmd) for cmd in cmd_list]

if __name__ == "__main__":
    optlist, nets = getopt.getopt(sys.argv[1:], "cd", ["create", "delete"])
    keys = dict(optlist).keys()
    if '-c' in keys or '--create' in keys:
        [create_cali_net(n) for n in nets]
    elif '-d' in keys or '--delete' in keys:
        [delete_cali_net(n) for n in nets]
    else:
        print("usage: cmd [-c | -d] networks")
