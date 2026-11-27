#!/bin/bash

set -euo pipefail

USER_NAME="ansible"

useradd -m -s /bin/bash $USER_NAME

usermod -p '*' $USER_NAME

echo "$USER_NAME ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-$USER_NAME
chmod 440 /etc/sudoers.d/90-$USER_NAME
visudo -cf /etc/sudoers.d/90-$USER_NAME >/dev/null

mkdir -p /home/$USER_NAME/.ssh
chmod 700 /home/$USER_NAME/.ssh
chown $USER_NAME:$USER_NAME /home/$USER_NAME/.ssh


echo "$ANSIBLE_PUBKEY" >> /home/$USER_NAME/.ssh/authorized_keys
chmod 600 /home/$USER_NAME/.ssh/authorized_keys
chown $USER_NAME:$USER_NAME /home/$USER_NAME/.ssh/authorized_keys







	
