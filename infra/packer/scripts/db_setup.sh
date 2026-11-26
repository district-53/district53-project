#!/bin/bash

set -euo pipefail

VERSION=18
ARCH="amd64" #arm64 for Ivanna
SEAWEEDFS_URL="https://github.com/seaweedfs/seaweedfs/releases/download/4.54/linux_${ARCH}.tar.gz"

apt update
apt install -y "postgresql-${VERSION}" "postgresql-client-${VERSION}" python3-psycopg2

systemctl stop postgresql
systemctl disable postgresql 

useradd --system --no-create-home --shell /usr/sbin/nologin seaweedfs

mkdir -p /var/lib/seaweedfs /etc/seaweedfs
chown root:seaweedfs /etc/seaweedfs
chmod 750 /etc/seaweedfs

chown seaweedfs:seaweedfs /var/lib/seaweedfs
chmod 750 /var/lib/seaweedfs

curl -fsSL -o /tmp/weed.tar.gz "$SEAWEEDFS_URL"

tar -xzf /tmp/weed.tar.gz -C /usr/local/bin weed
rm -f /tmp/weed.tar.gz



	
