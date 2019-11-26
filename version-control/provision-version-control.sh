#!/usr/bin/env bash
set -ex

# Update package list
apt-get update -y
apt-get upgrade -y
sed -i '/PasswordAuthentication/c\PasswordAuthentication yes' /etc/ssh/sshd_config
service ssh restart