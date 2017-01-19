#!/usr/bin/env bash
if [ -z  ${1+x} ]; then
    echo "must specify a directory(space) to import"
    exit 1
fi
SPACE_DIR=$1

CASSANDRA_HOSTS=${CASSANDRA_HOST:-'192.0.10.1,192.0.10.2,192.0.10,3'}

for tab in $(ls ${SPACE_DIR}); do
    echo "will load $tab to ${CASSANDRA_HOSTS}"
    sstableloader -d ${CASSANDRA_HOSTS} ${SPACE_DIR}/${tab}
done
