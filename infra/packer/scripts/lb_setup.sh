#!/bin/bash

set -euo pipefail

apt update -y
apt install -y nginx

rm -f /etc/nginx/sites-enabled/default
systemctl stop nginx
systemctl disable nginx

