#!/usr/bin/env bash
if [ -z  ${CASSANDRA_HOSTS+x} ]; then
    echo "CASSANDRA_HOSTS must set"
    exit 1
fi

if [ -z  ${1+x} ]; then
    echo "must specify a directory(space) to import"
    exit 1
fi

SPACE_DIR=$1
for tab in $(ls $SPACE_DIR); do
    echo "will load $tab to ${CASSANDRA_HOSTS}"
    sstableloader -d ${CASSANDRA_HOSTS} ${tab}
done
