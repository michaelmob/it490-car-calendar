#!/usr/bin/env bash
set -ex

# Update sytem and install MySQL
apt-get update
apt-get install -y mysql-server

# Start MySQL daemon
mv /tmp/mysql.cnf /etc/mysql/mysql.cnf
systemctl --now enable mysql

# Create database and user
mysql -u root <<EOF
  CREATE DATABASE $MYSQL_DB;
  CREATE USER '$MYSQL_USER'@'localhost' IDENTIFIED BY '$MYSQL_PASS';
  GRANT ALL PRIVILEGES ON $MYSQL_DB.* TO '$MYSQL_USER'@'localhost';
  FLUSH PRIVILEGES;

  CREATE USER '$MYSQL_REPLICATOR_USER'@'%' IDENTIFIED BY '$MYSQL_REPLICATOR_PASS';
  GRANT REPLICATION SLAVE ON *.* TO '$MYSQL_REPLICATOR_USER'@'%' IDENTIFIED BY '$MYSQL_REPLICATOR_PASS';
  FLUSH PRIVILEGES;
EOF

systemctl restart mysql
master_status=$(mysql -u root <<< 'SHOW MASTER STATUS;')
fields=( $(echo $master_status | grep -oP 'mysql-bin.* ') )

mysql -u root <<EOF
  SHOW MASTER STATUS;
  CHANGE MASTER TO MASTER_HOST = '$MYSQL_MASTER_HOST',
    MASTER_USER = '$MYSQL_REPLICATOR_USER',
    MASTER_PASSWORD = '$MYSQL_REPLICATOR_PASS',
    MASTER_LOG_FILE = '${fields[0]}',
    MASTER_LOG_POS = ${fields[1]}; 
  START SLAVE;
EOF

# Create database tables
if [[ "$HOSTNAME" = 'db' ]]; then
  for i in $(ls /vagrant/db/sql/*.sql | sort -g); do
    [ -f "$i" ] || break
    mysql -u root <<< $(sed "1i USE $MYSQL_DB;" "$i")
  done
fi

mysql -u root <<< 'START SLAVE;'

# Install db adminer
apt-get install -y apache2 php php-mysql mysql-client libmysqlclient-dev
wget 'http://www.adminer.org/latest.php' -O /var/www/html/adminer.php

# Install python and pip and openssl
apt-get install -y python3 python3-pip libssl-dev

# Set helper motd
mv /tmp/motd /etc/motd

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

# Set up firewall
sed -i '/\-\-icmp/d' /etc/ufw/before.rules  # block pinging from unknown
ufw default deny incoming  # deny all incoming connections
ufw allow from 10.0.2.0/24 # allow from host
ufw allow from 10.0.0.2  # version control server
ufw allow from 10.0.0.3  # broker server
ufw allow from 10.0.0.6  # db
ufw allow from 10.0.0.7  # db-backup
ufw --force enable
ufw reload
