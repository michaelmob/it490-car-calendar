#!/usr/bin/env bash
set -ex

# Update package list and install python and amqp client
apt-get update
apt-get install -y python3 python3-pip

# Set helper motd
mv /tmp/motd /etc/motd

# Install services
cp /vagrant/web/services/flask.service /etc/systemd/system/
systemctl enable flask.service

# Allow password auth (temporarily, until we can copy a key over)
sed -i '/PasswordAuthentication/c\PasswordAuthentication yes' /etc/ssh/sshd_config
service ssh restart
