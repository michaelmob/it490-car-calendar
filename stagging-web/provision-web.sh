#!/usr/bin/env bash
set -ex

# Update package list and install python and amqp client
apt-get update
apt-get install -y nginx python3 python3-pip
pip3 install -r /srv/car-calendar/requirements.txt

sites_available_file='/etc/nginx/sites-available/car-calendar'
sites_enabled_file='/etc/nginx/sites-enabled/car-calendar'

# Remove files so we don't error out when it already exists (on conf change)
rm -f "$sites_available_file" "$sites_enabled_file"

# Move nginx config into sites-avilable and symlink to sites-enabled
mv '/tmp/nginx.conf' "$sites_available_file"
ln -s "$sites_available_file" "$sites_enabled_file"

# Restart nginx to reload configuration
nginx -s reload

# Link webserver run script to home directory of vagrant
ln -s /srv/car-calendar/run_dev_server /home/vagrant/
ln -s /srv/car-calendar/run_prod_server /home/vagrant/

# Setup permissions on logs
mkdir -p /var/log/car-calendar
chown -R vagrant:syslog /var/log/car-calendar

# Set helper motd
mv /tmp/motd /etc/motd

# Install services
cp /vagrant/stagging-web/services/gunicorn.service /etc/systemd/system/
systemctl --now enable gunicorn.service
