#!/usr/bin/env bash
set -ex

# Update sytem and install MySQL
apt-get update
apt-get install -y mysql-server

# Install db adminer
apt-get install -y apache2 php php-mysql mysql-client
wget 'http://www.adminer.org/latest.php' -O /var/www/html/adminer.php

# Start MySQL daemon
systemctl --now enable mysql

# Create database and user
mysql -u root <<EOF
  CREATE DATABASE $MYSQL_DB;
  CREATE USER '$MYSQL_USER'@'localhost' IDENTIFIED BY '$MYSQL_PASS';
  GRANT ALL PRIVILEGES ON $MYSQL_DB.* TO '$MYSQL_USER'@'localhost';
  FLUSH PRIVILEGES;
EOF
