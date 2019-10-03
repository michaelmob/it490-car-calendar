#!/usr/bin/env bash
set -ex

# Update sytem and install MySQL
apt-get update
apt-get install -y mysql-server

# Start MySQL daemon
systemctl --now enable mysql

# Create database and user
mysql -u root <<EOF
  CREATE DATABASE $MYSQL_DB;
  CREATE USER '$MYSQL_USER'@'localhost' IDENTIFIED BY '$MYSQL_PASS';
  GRANT ALL PRIVILEGES ON $MYSQL_DB.* TO '$MYSQL_USER'@'localhost';
  FLUSH PRIVILEGES;
EOF

# Install db adminer
apt-get install -y apache2 php php-mysql mysql-client
wget 'http://www.adminer.org/latest.php' -O /var/www/html/adminer.php

# Install dependencies for consuming from rabbitmq
apt-get install -y python3 python3-pip
pip3 install pika

# Install MySQL connector
apt-get install libmysqlclient-dev
pip3 install mysqlclient
