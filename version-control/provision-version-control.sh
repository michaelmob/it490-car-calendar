#!/usr/bin/env bash
set -ex

# Update package list
apt-get update -y
apt-get upgrade -y
mkdir /home/vagrant/car_calendar_archive
mkdir /home/vagrant/car_calendar_archive/broker
mkdir /home/vagrant/car_calendar_archive/db
mkdir /home/vagrant/car_calendar_archive/dmz
mkdir /home/vagrant/car_calendar_archive/web