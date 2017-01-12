import os
import re

__author__ = 'junix'


class DockerCmd:
    @classmethod
    def ssh_cmd(cls, host, cmd):
        return "ssh {host} '{cmd}'".format(host=host, cmd=cmd)

    @classmethod
    def compact(cls, raw):
        return re.sub(r"""\s{2,}""", ' ', raw)

    def __init__(self):
        self.image = None
        self.restart = True
        self.daemon = True
        self.network = None
        self.name = None
        self.ip = None
        self.env = {}
        self.mount = {}
        self.remote_exec_host = None

    def use_image(self, image_name):
        if not image_name:
            raise ValueError('image can not be nil')
        self.image = image_name
        return self

    def with_restart(self, turn_on=True):
        self.restart = turn_on
        return self

    def with_network(self, network, ip=None):
        self.network = network
        self.ip = ip
        return self

    def daemon_mode(self, turn_on=True):
        self.daemon = turn_on
        return self

    def with_name(self, name):
        self.name = name
        return self

    def with_env(self, key, value):
        self.env[key] = value
        return self

    def copy_os_env(self, key, default_value=None, can_ignore=True):
        value = os.getenv(key, default_value)
        if not value:
            if can_ignore:
                return self
            raise ValueError(key + " is nil")
        self.env[key] = value
        return self

    def with_mount(self, device, dir, append_instance_name=False):
        self.mount[dir] = device if not append_instance_name else device + '/{instance}'
        return self

    def with_mount_from_env(self, device_env, dir, append_instance_name=True):
        device = os.getenv(device_env)
        if not device:
            return self

        self.mount[dir] = device if not append_instance_name else device + '/{instance}'
        return self

    def exec_in(self, host):
        self.remote_exec_host = host
        return self

    def command(self):
        if not self.image:
            raise ValueError('image name is nil')
        basic = 'docker run'
        restart = ''
        network = '--network {net}'.format(net=self.network) if self.network else ''
        ip = '--ip {ip}'.format(ip=self.ip) if self.ip else ''
        name = '--name {name}'.format(name=self.name) if self.name else ''
        mode = '-d' if self.daemon else '-it'
        env_list = ' '.join(['--env {key}="{value}"'.format(key=k, value=v) for k, v in self.env.items()])
        mounts = ' '.join(['-v {device}:{dir}'.format(dir=k, device=v.format(instance=self.name))
                           for k, v in self.mount.items()])
        cmd = ' '.join([basic, restart, network, ip, name, env_list, mounts, mode, self.image])
        if not self.remote_exec_host:
            return cmd
        return self.ssh_cmd(self.remote_exec_host, cmd)

    def show(self):
        print(self.command())
        return self

    def execute(self, dryrun=False):
        if dryrun:
            self.show()
        else:
            os.system(self.command())
