#!/bin/bash
set -euo pipefail

apt update -y
apt install -y fontconfig openjdk-21-jre-headless ansible wget

install -d -m 0755 /etc/apt/keyrings
wget -q -O /etc/apt/keyrings/jenkins-keyring.asc https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key 

echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" \
    > /etc/apt/sources.list.d/jenkins.list

apt update -y
apt install -y jenkins

systemctl stop jenkins
systemctl disable jenkins
rm -rf /var/lib/jenkins/* /var/log/jenkins/* /var/cache/jenkins/* /var/log/journal/* /var/log/journal/*