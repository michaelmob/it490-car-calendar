#!/usr/bin/env bash
set -ex

# Update package list and install required packages
apt-get update -y
apt-get install -y python3 python3-pip

# Install pip packages
pip3 install -r /srv/car-calendar/requirements.txt

# Setup permissions on logs
mkdir -p /var/log/car-calendar
chown -R vagrant:syslog /var/log/car-calendar

# Install services
cp /vagrant/dmz/services/dmz-consumer.service /etc/systemd/system/

systemctl --now enable dmz-consumer.service
