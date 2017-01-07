__author__ = 'junix'

import os,re


def env_or(env_key, default_value):
    v = os.getenv(env_key)
    return v if v is not None else default_value


def compact(raw):
    return re.sub(r"""\s{2,}""", ' ', raw)


def ssh_cmd(host, cmd):
    return "ssh {host} '{cmd}'".format(host=host, cmd=cmd)
