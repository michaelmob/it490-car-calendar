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

# Set up firewall
sed -i '/\-\-icmp/d' /etc/ufw/before.rules  # block pinging from unknown
ufw default deny incoming  # deny all incoming connections
ufw allow from 10.0.2.0/24 # allow from host
ufw allow from 10.0.0.2  # version control server
ufw allow from 10.0.0.3  # broker server
ufw --force enable
ufw reload
