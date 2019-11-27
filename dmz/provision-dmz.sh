#!/usr/bin/env bash
set -ex

# Update package list and install required packages
apt-get update -y
apt-get install -y python3 python3-pip

# Install services
cp /vagrant/dmz/services/dmz-consumer.service /etc/systemd/system/
systemctl enable dmz-consumer.service

# Allow password auth (temporarily, until we can copy a key over)
sed -i '/PasswordAuthentication/c\PasswordAuthentication yes' /etc/ssh/sshd_config
service ssh restart
