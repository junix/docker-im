
prod

env DATA_DIR=/mnt1/zookeeper/data DATA_LOG_DIR=/mnt1/zookeeper/log ./deploy-zookeeper.py \
 --dryrun in-803-bj in-805-bj in-807-bj in-808-bj in-809-bj


env NAME_PREFIX=lecai_zk ./deploy-zookeeper.py  -f 101 in-204-bj in-205-gd in-902-bj

