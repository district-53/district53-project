#!/bin/bash
set -euo pipefail

SERVICE_NAME="consul"

if ! [ -e "/usr/lib/systemd/system/$SERVICE_NAME.service" ]; then
    apt-get update -y && apt-get install wget gpg coreutils lsb-release -y
    wget -O- https://apt.releases.hashicorp.com/gpg | \
    gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" \
    | tee /etc/apt/sources.list.d/hashicorp.list
    apt-get update && apt-get install consul -y
fi

install -o consul -g consul -m 640 \
  /tmp/consul.hcl /etc/consul.d/consul.hcl

consul validate /etc/consul.d

systemctl daemon-reload
systemctl enable consul
systemctl restart consul

echo "Consul server is running. UI: http://192.168.56.12:8500"