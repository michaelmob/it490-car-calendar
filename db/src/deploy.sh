#!/usr/bin/env bash
pip3 install --user -r /home/vagrant/src/requirements.txt

sudo systemctl restart log-consumer.service
sudo systemctl restart auth-consumer.service
sudo systemctl restart data-consumer.service
