import os
import re
import subprocess
import json

network_dict = {
    'zookeeper': '192.0.2.0',
    'orgman': '192.0.3.0',
    'master': '192.0.4.0',
    'maxwell': '192.0.5.0',
    'conv_store': '192.0.7.0',
    'kafka': '192.0.8.0',
    'sinker': '192.0.9.0',
    'cassandra': '192.0.10.0',
}


def env_or(env_key, default_value):
    v = os.getenv(env_key)
    return v if v is not None else default_value


def compact(raw):
    return re.sub(r"""\s{2,}""", ' ', raw)


# ===========================
# === configuration utils ===
# ===========================
def zk_env(count=5, offset=0):
    instances = [ip_of('zookeeper', offset + i + 1) + ':2181' for i in range(count)]
    return ','.join(instances)


def network_of(name):
    net = network_dict.get(name)
    if not net:
        raise ValueError('unknown subnet:{net}'.format(net=name))
    return net


def ip_of(name, index):
    return re.sub('0$', str(index), network_of(name))


# ========================
# === containers utils ===
# ========================
def inspect_container(container):
    cmd = 'docker inspect {c}'.format(c=container)
    out = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
    return json.loads(out.decode('utf-8'))


def ip_of_container(container):
    ips = []
    for inspect in inspect_container(container):
        net = inspect.get('NetworkSettings', {})
        ips.append(net.get('IPAddress'))
        networks = net.get('Networks', {})
        for n in networks.values():
            ips.append(n.get('IPAddress'))
            ipam = n.get('IPAMConfig')
            if ipam:
                ips.append(ipam.get('IPv4Address'))
    return list(set([n for n in ips if n]))


def env_of_container(container):
    inspects = inspect_container(container)
    if not inspects:
        return None
    inspect = inspects[0]
    return inspect.get('Config', {}).get('Env', [])


def network_of_container(container):
    inspects = inspect_container(container)
    if not inspects:
        return None
    inspect = inspects.pop()
    return inspect.get('NetworkSettings', {}).get('Networks', {}).keys()
