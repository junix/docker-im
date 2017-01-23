import subprocess
import json
import utils


class Container:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def inspect(self):
        cmd = 'docker inspect {c}'.format(c=self.name)
        out = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
        return json.loads(out.decode('utf-8'))

    def inspect0(self):
        inspects = self.inspect()
        if not inspects:
            raise ValueError('No inspect of {name}'.format(name=self.name))
        return inspects[0]

    def status(self):
        inspect = self.inspect0()
        return inspect.get('State', {}).get('Status')

    def is_running(self):
        inspect = self.inspect0()
        return inspect.get('State', {}).get('Running', False)

    def ip(self):
        ips = []
        for inspect in self.inspect():
            net = inspect.get('NetworkSettings', {})
            ips.append(net.get('IPAddress'))
            networks = net.get('Networks', {})
            for n in networks.values():
                ips.append(n.get('IPAddress'))
                ipam = n.get('IPAMConfig')
                if ipam:
                    ips.append(ipam.get('IPv4Address'))
        return list(set([n for n in ips if n]))

    def env(self):
        return self.inspect0().get('Config', {}).get('Env', [])

    def network(self):
        return self.inspect0().get('NetworkSettings', {}).get('Networks', {}).keys()

    def mount(self):
        mounts = self.inspect0().get('Mounts', [])
        for m in mounts:
            yield '{src}:{dst}'.format(
                src=m.get('Source'),
                dst=m.get('Destination'))

    def ipam(self):
        networks = self.inspect0().get('NetworkSettings', {}).get('Networks', {})
        for k, v in networks.items():
            ipam_config = v.get('IPAMConfig')
            if ipam_config:
                ipv4_address = ipam_config.get('IPv4Address')
                if ipv4_address:
                    yield '{network}:{ip}'.format(network=k, ip=ipv4_address)

    def release_ip(self):
        for ip in self.ip():
            cmd = 'calicoctl ipam release --ip={ip}'.format(ip=ip)
            utils.run(cmd)

    def start(self):
        cmd = 'docker start {container}'.format(container=self.name)
        utils.run(cmd)

    def stop(self):
        cmd = 'docker stop {container}'.format(container=self.name)
        utils.run(cmd)

    def restart(self):
        if self.is_running():
            self.stop()
        self.release_ip()
        self.start()
