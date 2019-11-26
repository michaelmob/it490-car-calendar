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
cp /vagrant/prod-dmz/services/dmz-consumer.service /etc/systemd/system/

systemctl --now enable dmz-consumer.service

chmod +x /home/vagrant/dmz_archive_deploy.sh
tr -d '\r' <dmz_archive_deploy.sh> new_dmz_archive_deploy.sh
mv new_dmz_archive_deploy.sh dmz_archive_deploy.sh