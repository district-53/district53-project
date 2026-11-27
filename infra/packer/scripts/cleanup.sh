#!/bin/bash

set -euo pipefail

sudo apt autoremove -y --purge
sudo apt clean


rm -f /home/vagrant/*
rm -rf /opt/consul/*
sudo rm -rf /var/lib/apt/lists/*

sudo dd if=/dev/zero of=/tmp/zero.bin || true
sudo rm /tmp/zero.bin