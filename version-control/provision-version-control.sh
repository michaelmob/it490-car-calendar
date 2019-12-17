#!/usr/bin/env bash

# Set up firewall
sed -i '/\-\-icmp/d' /etc/ufw/before.rules  # block pinging from unknown
ufw default deny incoming  # deny all incoming connections
ufw allow from 10.0.2.0/24 # allow from host
ufw allow from 10.0.0.0/24
ufw --force enable
ufw reload
