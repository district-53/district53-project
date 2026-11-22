#!/bin/bash
set -euo pipefail

SEAWEED_VERSION="4.54"
SEAWEED_IP="${SEAWEED_IP:?}"
S3_ACCESS_KEY="${S3_ACCESS_KEY:?}"
S3_SECRET_KEY="${S3_SECRET_KEY:?}"
ARCH="$(dpkg --print-architecture)"

if ! id seaweedfs; then
    useradd -s /usr/sbin/nologin -r -U seaweedfs
fi

if ! command -v weed; then
    wget -q -O /tmp/seaweedfs.tar.gz \
        "https://github.com/seaweedfs/seaweedfs/releases/download/${SEAWEED_VERSION}/linux_${ARCH}.tar.gz"
    tar -xzf /tmp/seaweedfs.tar.gz -C /tmp
    install -m 755 /tmp/weed /usr/local/bin/weed
fi

install -d -g seaweedfs -m 750 /etc/seaweedfs 
install -d -o seaweedfs -g seaweedfs -m 750 /var/lib/seaweedfs

envsubst '${SEAWEED_IP}' < /tmp/seaweedfs/seaweedfs.service.tpl > /etc/systemd/system/seaweedfs.service
envsubst '${S3_ACCESS_KEY} ${S3_SECRET_KEY}' < /tmp/seaweedfs/s3.json.tpl > /tmp/seaweedfs/s3.json
install -g seaweedfs -m 640 /tmp/seaweedfs/s3.json /etc/seaweedfs/s3.json
rm -rf /tmp/seaweedfs

systemctl daemon-reload
systemctl enable seaweedfs
systemctl restart seaweedfs

echo "SeaweedFS is running. S3 endpoint: http://${SEAWEED_IP}:8333"