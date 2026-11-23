#!/bin/bash
set -euo pipefail

if ! [ -e "/usr/lib/systemd/system/consul.service" ]; then
    apt update -y && apt install wget gpg coreutils lsb-release -y
    wget -O- https://apt.releases.hashicorp.com/gpg | \
    gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" \
    | tee /etc/apt/sources.list.d/hashicorp.list
    apt update && apt install consul -y
fi

cp /tmp/consul.hcl /etc/consul.d/consul.hcl
chown consul:consul /etc/consul.d/consul.hcl
chmod 640 /etc/consul.d/consul.hcl

consul validate /etc/consul.d

systemctl daemon-reload
systemctl enable consul
systemctl restart consul

echo "Consul server is running. UI: http://192.168.56.12:8500"