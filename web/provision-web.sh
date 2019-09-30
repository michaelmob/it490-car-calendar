#!/usr/bin/env bash
set -ex

# update package list and install php along with php-amqplib dependencies
apt-get update
apt-get install -y nginx php7.2-fpm php7.2-bcmath composer

sites_available_file='/etc/nginx/sites-available/car-calendar'
sites_enabled_file='/etc/nginx/sites-enabled/car-calendar'

# Remove files so we don't error out when it already exists (on conf change)
rm -f "$sites_available_file" "$sites_enabled_file"

# Move nginx config into sites-avilable and symlink to sites-enabled
mv '/tmp/nginx.conf' "$sites_available_file"
ln -s "$sites_available_file" "$sites_enabled_file"

# Restart nginx to reload configuration
#systemctl restart nginx
nginx -s reload
