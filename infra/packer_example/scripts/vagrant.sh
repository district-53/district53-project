#!/bin/bash

set -euo pipefail

mkdir -p /home/vagrant/.ssh
chmod 700 /home/vagrant/.ssh
chown vagrant:vagrant /home/vagrant/.ssh


curl -fsSL https://raw.githubusercontent.com/hashicorp/vagrant/master/keys/vagrant.pub \
  >> /home/vagrant/.ssh/authorized_keys

chmod 600 /home/vagrant/.ssh/authorized_keys
chown vagrant:vagrant /home/vagrant/.ssh/authorized_keys

echo "UseDNS no" >> /etc/ssh/sshd_config



	
