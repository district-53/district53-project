#!/bin/bash

set -euo pipefail

sudo dd if=/dev/zero of=/tmp/zero.bin || true
sudo rm /tmp/zero.bin

rm -f /home/vagrant/*