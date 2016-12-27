#!/usr/bin/env bash
set -ex
docker network rm starfish
calicoctl delete -f ipPool-starfish.yaml
