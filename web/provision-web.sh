#!/usr/bin/env bash
set -ex

# Update package list and install python and amqp client
apt-get update
apt-get install -y nginx python3 python3-pip
pip3 install pika flask gunicorn python-dotenv

sites_available_file='/etc/nginx/sites-available/car-calendar'
sites_enabled_file='/etc/nginx/sites-enabled/car-calendar'

# Remove files so we don't error out when it already exists (on conf change)
rm -f "$sites_available_file" "$sites_enabled_file"

# Move nginx config into sites-avilable and symlink to sites-enabled
mv '/tmp/nginx.conf' "$sites_available_file"
ln -s "$sites_available_file" "$sites_enabled_file"

# Restart nginx to reload configuration
nginx -s reload
