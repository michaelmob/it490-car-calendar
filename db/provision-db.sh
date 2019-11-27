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
apt-get install -y apache2 php php-mysql mysql-client libmysqlclient-dev
wget 'http://www.adminer.org/latest.php' -O /var/www/html/adminer.php

# Install python and pip and openssl
apt-get install -y python3 python3-pip libssl-dev

# Set helper motd
mv /tmp/motd /etc/motd

# Create database tables
for i in $(ls /vagrant/db/sql/*.sql | sort -g); do
  [ -f "$i" ] || break
  mysql -u root <<< $(sed "1i USE $MYSQL_DB;" "$i")
done

# Install services
cp /vagrant/db/services/log-consumer.service /etc/systemd/system/
cp /vagrant/db/services/auth-consumer.service /etc/systemd/system/
cp /vagrant/db/services/data-consumer.service /etc/systemd/system/

systemctl enable log-consumer.service
systemctl enable auth-consumer.service
systemctl enable data-consumer.service

# Allow password auth (temporarily, until we can copy a key over)
sed -i '/PasswordAuthentication/c\PasswordAuthentication yes' /etc/ssh/sshd_config
service ssh restart
