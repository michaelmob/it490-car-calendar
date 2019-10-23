#!/usr/bin/env bash
set -ex

apt-get update -y
apt-get upgrade -y
apt-get install python3 -y 
apt-get install python3-pip -y 
apt-get install python3.6 -y 
pip3 install google-api-python-client
pip3 install google_auth_oauthlib
pip3 install httplib2
pip3 install oauth2client
pip3 install datetime
pip3 install bs4
pip3 install /opt/packages/amqp
pip3 install /opt/packages/logger
pip3 install python-env
mkdir -p /var/log/car-calendar
chown -R vagrant:syslog /var/log/car-calendar