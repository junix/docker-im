#!/usr/bin/env python
import sys
import os
import getopt
import docker_cmd
import utils


class CassandraCommand(docker_cmd.DockerCmd):
    def __init__(self, instance_index, ip_offset):
        docker_cmd.DockerCmd.__init__(self)
        pos = instance_index + ip_offset + 1
        self.offset = ip_offset
        self.name = self.instance_name(pos)
        ip = utils.ip_of('cassandra', pos)
        seeds = [utils.ip_of('cassandra', ip_offset + i + 1) for i in range(2)]

        self.use_image('cassandra'). \
            with_restart(). \
            daemon_mode(). \
            with_network(network='cassandra', ip=ip). \
            with_env('CASSANDRA_BROADCAST_ADDRESS', ip). \
            with_env('CASSANDRA_CLUSTER_NAME', 'ConvStore'). \
            with_env('CASSANDRA_SEEDS', ','.join(seeds)). \
            with_mount_from_env('DATA_DIR', '/var/lib/cassandra')
        os_env_list = ['CASSANDRA_LISTEN_ADDRESS',
                       'CASSANDRA_BROADCAST_ADDRESS',
                       'CASSANDRA_RPC_ADDRESS',
                       'CASSANDRA_START_RPC',
                       'CASSANDRA_SEEDS',
                       'CASSANDRA_CLUSTER_NAME',
                       'CASSANDRA_NUM_TOKENS',
                       'CASSANDRA_DC',
                       'CASSANDRA_RACK',
                       'CASSANDRA_ENDPOINT_SNITCH']
        for e in os_env_list:
            self.copy_os_env(e)

    @classmethod
    def instance_name(cls, instance_id):
        return '{name_prefix}{index}'.format(
            name_prefix=os.getenv('NAME_PREFIX', 'cassandra'),
            index=instance_id)


def usage():
    print('''usage:deploy-cassandra.py [-f from_ip] [--dryrun] hosts
env: DATA_DIR     : -v $DATA_DIR/{instance}:/data''')


if __name__ == '__main__':
    optlist, instances = getopt.getopt(sys.argv[1:], 'f:', ['dryrun'])
    options = dict(optlist)
    if not instances:
        usage()
        sys.exit(1)
    ip_off = int(dict(options).get('-f', '0'))
    for index, host in enumerate(instances):
        CassandraCommand(index, ip_off). \
            exec_in(host). \
            execute('--dryrun' in options)