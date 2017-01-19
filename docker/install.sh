#!/usr/bin/env bash

if [[ "${INTERNAL_IP}" == "" ]]; then
    echo 'env INTERNAL_IP must set'
fi

function install_repo_file {
    REPO=/etc/yum.repos.d/docker.repo
    echo '[dockerrepo]'> ${REPO}
    echo 'name=Docker Repository' >> ${REPO}
    echo 'baseurl=https://yum.dockerproject.org/repo/main/centos/7/' >> ${REPO}
    echo 'enabled=1' >> ${REPO}
    echo 'gpgcheck=1' >> ${REPO}
    echo 'gpgkey=https://yum.dockerproject.org/gpg' >> ${REPO}
}

function install_docker() {
    yum install -y docker-engine &&
    usermod -aG docker mos
}

function conf_docker() {
    mkdir /etc/systemd/system/docker.service.d
    CONF='/etc/systemd/system/docker.service.d/docker.conf'

    echo '[Service]' > ${CONF}
    echo 'EnvironmentFile=-/etc/sysconfig/docker' >> ${CONF}
    echo 'EnvironmentFile=-/etc/sysconfig/docker-storage' >> ${CONF}
    echo 'EnvironmentFile=-/etc/sysconfig/docker-network' >> ${CONF}
    echo 'ExecStart=' >> ${CONF}
    echo 'ExecStart=/usr/bin/dockerd $OPTIONS $DOCKER_STORAGE_OPTIONS $DOCKER_NETWORK_OPTIONS $BLOCK_REGISTRY $INSECURE_REGISTRY' >> ${CONF}

    systemctl daemon-reload

    SYS_CONF=/etc/sysconfig/docker
    echo "OPTIONS=\"-g /mnt1/docker \
--log-opt max-size=10m \
--log-opt max-file=10 \
-H tcp://${INTERNAL_IP}:2375 \
-H unix:///var/run/docker.sock \
--cluster-store=${ETCD_URL:-etcd://-127.0.0.1:4001} \
--cluster-advertise=${INTERNAL_IP}:2375\"" > ${SYS_CONF}
}

function install_systemd() {
    systemctl enable docker.service
}

install_repo_file &&
install_docker &&
install_systemd &&
conf_docker &&
systemctl start docker
