#!/bin/bash

set -euo pipefail

apt autoremove -y --purge
apt clean
rm -rf /var/lib/apt/lists/*
sudo dd if=/dev/zero of=/tmp/zero.bin || true
sudo rm /tmp/zero.bin

rm -f /home/vagrant/*