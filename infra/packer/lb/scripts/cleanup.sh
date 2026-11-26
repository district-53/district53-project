#!/bin/bash

set -euo pipefail

sudo apt autoremove -y
sudo apt clean
sudo rm -rf /var/lib/apt/lists/*