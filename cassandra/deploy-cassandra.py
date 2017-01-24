#!/usr/bin/env python
import sys
import os
import getopt
import docker_cmd
import utils


class CassandraCommand(docker_cmd.DockerCmd):
    def __init__(self, index):
        docker_cmd.DockerCmd.__init__(self)
        self.name = self.instance_name(index+1)
        ip = utils.ip_of('cassandra', index)
        seeds = [utils.ip_of('cassandra', i) for i in range(2)]

        self.use_image('cassandra'). \
            with_restart(False).\
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
                       'MAX_HEAP_SIZE',
                       'JVM_OPTS',
                       'CASSANDRA_ENDPOINT_SNITCH']
        for e in os_env_list:
            self.copy_os_env(e)

    @classmethod
    def instance_name(cls, instance_id):
        return '{name_prefix}{index}'.format(
            name_prefix=os.getenv('NAME_PREFIX', 'cassandra'),
            index=instance_id)


def usage():
    print('''usage:deploy-cassandra.py [--dryrun] hosts
env: DATA_DIR     : -v $DATA_DIR/{instance}:/data''')


if __name__ == '__main__':
    optlist, instances = getopt.getopt(sys.argv[1:], 'm:', ['dryrun'])
    options = dict(optlist)
    if not instances:
        usage()
        sys.exit(1)
    memory_limit = options.get('-m')
    for index, host in enumerate(instances):
        CassandraCommand(index). \
            exec_in(host). \
            limit_memory(memory_limit).\
            run('--dryrun' in options)
