#!/bin/bash
set -euo pipefail

#Add user admin
if ! id -u admin >/dev/null 2>&1; then
  useradd -m -s /bin/bash admin
fi
usermod -p '*' admin

echo "admin ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-admin
chmod 440 /etc/sudoers.d/90-admin
visudo -cf /etc/sudoers.d/90-admin >/dev/null


mkdir -p /home/admin/.ssh
chown admin:admin /home/admin/.ssh
chmod 700 /home/admin/.ssh
echo "$ADMIN_PUBKEY" > /home/admin/.ssh/authorized_keys
chown admin:admin /home/admin/.ssh/authorized_keys
chmod 600 /home/admin/.ssh/authorized_keys


#root off password awtorization
passwd -l root >/dev/null

cp /tmp/sshd-hardening.conf /etc/ssh/sshd_config.d/00-users_set_up.conf
chown root:root /etc/ssh/sshd_config.d/00-users_set_up.conf
chmod 644 /etc/ssh/sshd_config.d/00-users_set_up.conf

sshd -t
systemctl try-reload-or-restart ssh