import os
import re
import subprocess

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


def exec_cmd(cmd):
    out = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
    return out.decode('utf-8')


def run(cmd, dryrun=False):
    if dryrun:
        print(cmd)
    else:
        os.system(cmd)


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
    ip_offset = int(os.getenv('IP_OFFSET', '1'))
    return re.sub('0$', str(index + ip_offset), network_of(name))


def assigned(res):
    return ('is not assigned' not in res) and ('is not currently assigned' not in res)


def assigned_ip_list_of(name):
    cmd = 'calicoctl ipam show --ip={ip}'
    for index in range(1, 255):
        ip = ip_of(name, index)
        res = exec_cmd(cmd.format(ip=ip))
        if assigned(res):
            yield ip


def free_ip_list_of(name):
    cmd = 'calicoctl ipam show --ip={ip}'
    for index in range(1, 255):
        ip = ip_of(name, index)
        res = exec_cmd(cmd.format(ip=ip))
        if not assigned(res):
            yield ip


def docker_ps(column='NAME', list_all=True):
    cmd = 'docker ps -a' if list_all else 'docker ps'
    lines = exec_cmd(cmd).split('\n')
    title = lines[0]
    cs = re.split('\W+', title)
    cs = cs[cs.index(column.upper()):]
    for c in lines[1:]:
        if len(cs) > 1:
            yield c[title.index(cs[0]):title.index(cs[1])].strip()
        else:
            yield c[title.index(cs[0]):].strip()
