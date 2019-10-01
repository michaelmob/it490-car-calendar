#!/usr/bin/env bash
set -ex

apt-get update
apt-get upgrade
apt-get install python3
apt-get install python3-pip
apt-get install python3.6
pip install googleapiclient
pip install httplib2
pip install oauth2client
pip install datetime