import subprocess
import json


class Container:
    def __init__(self, name):
        self.name = name

    def inspect(self):
        cmd = 'docker inspect {c}'.format(c=self.name)
        out = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
        return json.loads(out.decode('utf-8'))

    def inspect0(self):
        inspects = self.inspect()
        if not inspects:
            raise ValueError('No inspect of {name}'.format(name=self.name))
        return inspects[0]

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

    def ipam(self):
        networks = self.inspect0().get('NetworkSettings', {}).get('Networks', {})
        ipv4 = [(k, v.get('IPAMConfig').get('IPv4Address')) for k, v in networks.items() if v.get('IPAMConfig')]
        return ['{network}:{ip}'.format(network=network, ip=ip) for (network, ip) in ipv4 if ip]
