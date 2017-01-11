#!/usr/bin/env python
import sys
import os
import getopt
import docker_cmd


class ZkCommand(docker_cmd.DockerCmd):
    def __init__(self, instance_list, instance_index, ip_offset):
        docker_cmd.DockerCmd.__init__(self)
        self.index = instance_index
        self.offset = ip_offset
        self.name = self.instance_name(instance_index + ip_offset)
        self.conf = self.generate_server_conf(instance_list, ip_offset)
        ip = '192.0.2.{index}'.format(index=self.index + self.offset)
        self.use_image('zookeeper:3.4.9'). \
            with_restart(). \
            daemon_mode(). \
            with_network(network='zookeeper', ip=ip). \
            with_env('ZOO_MY_ID', self.index + 1). \
            with_env('ZOO_SERVERS', self.conf). \
            with_mount_from_env('DATA_DIR', '/data'). \
            with_mount_from_env('DATA_LOG_DIR', '/datalog')

    @classmethod
    def instance_name(cls, instance_id):
        return "{name_prefix}{index}".format(
            name_prefix=os.getenv('NAME_PREFIX', 'zk'),
            index=instance_id)

    @classmethod
    def generate_server_conf(cls, instance_list, ip_offset=0):
        conf_list = ["server.{index}={instance}:2888:3888".format(
            index=i + 1,
            instance=cls.instance_name(i + ip_offset)) for i in range(0, len(instance_list))]
        return ' '.join(conf_list)


def usage():
    print("""usage:./deploy-zookeeper.py [-f from_ip] [--dryrun] hosts
env: DATA_DIR     : -v $DATA_DIR/{instance}:/data
     DATA_LOG_DIR : -v $DATA_LOG_DIR/{instance}:/datalog""")


if __name__ == "__main__":
    options, instances = getopt.getopt(sys.argv[1:], "f:", ["dryrun"])
    if len(instances) == 0:
        usage()
        sys.exit(1)
    offset = int(dict(options).get('-f', '1'))
    for index, host in enumerate(instances):
        c = ZkCommand(instances, index, offset).exec_in(host)
        c.execute('--dryrun' in dict(options).keys())
