#!/bin/bash

set -euo pipefail


sudo apt update
sudo apt install -y openssh-server python3 ca-certificates curl gnupg chrony ufw 


