#!/usr/bin/env python

import os
import sys
import utils
import getopt


class NetworkAdmin:
    def __init__(self, options, networks):
        self.network_list = networks
        self.to_create = '-c' in options or '--create' in options
        self.to_delete = '-d' in options or '--delete' in options
        self.dryrun = '--dryrun' in options
        for n in self.network_list:
            utils.network_of(n)

    def create_pool_yaml(self, network):
        file_name = 'ippool-{net}.yaml'.format(net=network)
        spec_file = open(file_name, 'w+')
        spec_file.write(self.pool_spec(network))
        spec_file.close()

    @classmethod
    def pool_spec(cls, network):
        return '''- apiVersion: v1
  kind: ipPool
  metadata:
    cidr: {subnet}/24
    '''.format(subnet=utils.network_of(network))

    def create_cali_net(self, network):
        self.create_pool_yaml(network)
        return [
            'calicoctl create -f ippool-{name}.yaml'.format(name=network),
            'calicoctl apply -f policy-full-connect.yaml',
            'docker network create --driver calico --ipam-driver calico-ipam --subnet={subnet}/24 {name}'.format(
                name=network,
                subnet=utils.network_of(network))]

    def delete_cali_net(self, network):
        self.create_pool_yaml(network)
        return [
            'docker network rm {name}'.format(name=network),
            'calicoctl delete -f ippool-{name}.yaml'.format(name=network)
        ]

    @classmethod
    def usage(cls):
        print('''usage: network-admin.py [-c | --create] | [-d | --delete] network''')

    def execute(self):
        if self.to_create:
            for n in self.network_list:
                self.execute_cmd(self.create_cali_net(n))
        elif self.to_delete:
            for n in self.network_list:
                self.execute_cmd(self.delete_cali_net(n))
        else:
            self.usage()

    def execute_cmd(self, cmd_list):
        for c in cmd_list:
            if self.dryrun:
                print(c)
            else:
                os.system(c)


if __name__ == '__main__':
    optlist, network_list = getopt.getopt(sys.argv[1:], 'cd', ['create', 'delete', 'dryrun'])
    admin = NetworkAdmin(dict(optlist), network_list)
    admin.execute()
