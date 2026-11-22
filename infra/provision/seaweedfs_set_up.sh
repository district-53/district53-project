#!/bin/bash
set -euo pipefail

SEAWEED_VERSION="4.54"
SEAWEED_IP="${SEAWEED_IP:?}"
S3_ACCESS_KEY="${S3_ACCESS_KEY:?}"
S3_SECRET_KEY="${S3_SECRET_KEY:?}"

if ! id seaweedfs; then
    useradd -s /usr/sbin/nologin -r -U seaweedfs

if ! [ -e /etc/systemd/system/seaweedfs.service ]; then
  ARCH="$(dpkg --print-architecture)"
  wget -q -O /tmp/weed.tar.gz "https://github.com/seaweedfs/seaweedfs/releases/download/${SEAWEED_VERSION}/linux_${ARCH}.tar.gz"
  tar -xzf /tmp/weed.tar.gz -C /usr/local/bin weed
  rm /tmp/weed.tar.gz
fi

if ! id seaweedfs; then
    useradd -s /usr/sbin/nologin -r -U seaweedfs

mkdir -p /var/lib/seaweedfs /etc/seaweedfs
chown root:seaweedfs /etc/seaweedfs
chmod 750 /etc/seaweedfs

chown seaweedfs:seaweedfs /var/lib/seaweedfs
chmod 750 /var/lib/seaweedfs


touch /etc/seaweedfs/s3.json
chown root:seaweedfs /etc/seaweedfs/s3.json
chmod 640 /etc/seaweedfs/s3.json
envsubst '${S3_ACCESS_KEY} ${S3_SECRET_KEY}' < /tmp/seaweedfs-s3.json.tpl > /etc/seaweedfs/s3.json

envsubst '${SEAWEED_IP}' < /tmp/seaweedfs.service.tpl > /etc/systemd/system/seaweedfs.service
chown root:root /etc/systemd/system/seaweedfs.service
chmod 644 /etc/systemd/system/seaweedfs.service

systemctl daemon-reload
systemctl enable seaweedfs
systemctl restart seaweedfs

echo "SeaweedFS is running. S3 endpoint: http://${SEAWEED_IP}:8333"