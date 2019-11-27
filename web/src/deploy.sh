#!/usr/bin/env bash
pip3 install --user -r /home/vagrant/src/requirements.txt
sudo systemctl restart flask.service
