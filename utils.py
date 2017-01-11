import os
import re

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


def zk_env(count=5, offset=0):
    instances = [ip_of('zookeeper', offset + i + 1) for i in range(count)]
    return ','.join(instances)


def network_of(name):
    net = network_dict.get(name)
    if not net:
        raise ValueError('unknown subnet:{net}'.format(net=name))
    return net


def ip_of(name, index):
    return re.sub('0$', str(index), network_of(name))
