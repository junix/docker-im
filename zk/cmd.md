
prod

env DATA_DIR=/mnt1/zookeeper/data DATA_LOG_DIR=/mnt1/zookeeper/log ./deploy-zookeeper.py \
 --dryrun in-821-bj in-822-bj in-823-bj in-824-bj in-825-bj


env NAME_PREFIX=lecai_zk ./deploy-zookeeper.py  -f 101 in-204-bj in-205-gd in-902-bj

