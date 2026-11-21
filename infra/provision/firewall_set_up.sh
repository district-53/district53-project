#!/bin/bash
set -euo pipefail

ROLE="${ROLE:?}"
LB_IP="${LB_IP:?}"
APP_IPS="${APP_IPS:?}"
APP_PORT="${APP_PORT:-8000}"
SUBNET="${SUBNET:-192.168.56.0/24}"

export DEBIAN_FRONTEND=noninteractive
command -v ufw >/dev/null 2>&1 || { apt-get update -y; apt-get install -y ufw; }

ufw --force reset >/dev/null

ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp comment 'ssh'

case "$ROLE" in
  lb)
    ufw allow 80/tcp comment 'http from users'
    ;;
  app)
    ufw allow from "$LB_IP" to any port "$APP_PORT" proto tcp comment 'app only from lb'
    ;;
  db)
    for ip in $APP_IPS; do
      ufw allow from "$ip" to any port 5432 proto tcp comment 'postgres from app'
      ufw allow from "$ip" to any port 8333 proto tcp comment 'seaweedfs s3 from app'
    done
    ;;
  consul)
    ufw allow from "$SUBNET" to any port 8500 proto tcp comment 'consul ui/api'
    ufw allow from "$SUBNET" to any port 8600 comment 'consul dns'
    ufw allow from "$SUBNET" to any port 8300 proto tcp comment 'consul rpc'
    ufw allow from "$SUBNET" to any port 8301 comment 'consul lan gossip'
    ;;
  *)
    echo "ERROR: unknown ROLE=$ROLE" >&2
    exit 1
    ;;
esac

ufw --force enable
ufw status verbose