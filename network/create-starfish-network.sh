#!/usr/bin/env bash
set -ex
calicoctl create -f ipPool-starfish.yaml
docker network create \
  --driver calico \
  --ipam-driver calico-ipam \
  --subnet=192.0.2.0/24 \
  starfish