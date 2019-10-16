#!/usr/bin/env bash
set -ex

apt-get update
apt-get upgrade
apt-get install python3
apt-get install python3-pip
apt-get install python3.6
apt-get install python3.6-pip
pip3 install google-api-python-client
pip3 install google_auth_oauthlib
pip3 install httplib2
pip3 install oauth2client
pip3 install datetime
pip3 install bs4