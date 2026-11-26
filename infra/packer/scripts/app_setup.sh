#!/bin/bash

set -euo pipefail

USER_HOME="/var/lib/hall"

useradd --system --home-dir "$USER_HOME" --shell /usr/sbin/nologin hall

mkdir -p "$USER_HOME"
chown hall:hall "$USER_HOME"
chmod 750 "$USER_HOME"

apt update
apt install -y python3-venv