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

# Install python and pip and requirements
apt-get install -y python3 python3-pip
pip3 install -r /srv/car-calendar/requirements.txt

# Setup permissions on logs
mkdir -p /var/log/car-calendar
chown -R vagrant:syslog /var/log/car-calendar

# Set helper motd
mv /tmp/motd /etc/motd

# Create database tables
for i in $(ls /vagrant/dev-db-backup/sql/*.sql | sort -g); do
  [ -f "$i" ] || break
  mysql -u root <<< $(sed "1i USE $MYSQL_DB;" "$i")
done

# Install services
cp /vagrant/dev-db/services/log-consumer.service /etc/systemd/system/
cp /vagrant/dev-db/services/auth-consumer.service /etc/systemd/system/
cp /vagrant/dev-db/services/data-consumer.service /etc/systemd/system/

systemctl --now enable log-consumer.service
systemctl --now enable auth-consumer.service
systemctl --now enable data-consumer.service

chmod +x /home/vagrant/db_bk_archive_deploy.sh
tr -d '\r' <db_bk_archive_deploy.sh> new_db_bk_archive_deploy.sh
mv new_db_bk_archive_deploy.sh db_bk_archive_deploy.sh