# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure("2") do |config|

  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  config.vm.define "dmz" do |subconfig|
    subconfig.vm.box = "ubuntu/bionic64"
    subconfig.vm.hostname = "dmz"
    subconfig.vm.network "private_network", ip: "10.10.0.3"
    subconfig.vm.provision "shell", path: "dmz/provision-dmz.sh"
    subconfig.vm.synced_folder "dmz/src/", "/srv/car-calendar"
    subconfig.vm.synced_folder "dmz/logs/", "/var/log/car-calendar"
    subconfig.vm.synced_folder "packages/", "/opt/packages"
  end
  
  
  config.vm.define "stagging-dmz" do |subconfig|
    subconfig.vm.box = "ubuntu/bionic64"
    subconfig.vm.hostname = "stagging-dmz"
    subconfig.vm.network "private_network", ip: "10.10.0.3"
    subconfig.vm.provision "shell", path: "stagging-dmz/provision-dmz.sh"
    subconfig.vm.synced_folder "stagging-dmz/src/", "/srv/car-calendar"
    subconfig.vm.synced_folder "stagging-dmz/logs/", "/var/log/car-calendar"
    subconfig.vm.synced_folder "packages/", "/opt/packages"
  end


  config.vm.define "dev-dmz" do |subconfig|
    subconfig.vm.box = "ubuntu/bionic64"
    subconfig.vm.hostname = "dev-dmz"
    subconfig.vm.network "private_network", ip: "10.10.0.3"
    subconfig.vm.provision "shell", path: "dev-dmz/provision-dmz.sh"
    subconfig.vm.synced_folder "dev-dmz/src/", "/srv/car-calendar"
    subconfig.vm.synced_folder "dev-dmz/logs/", "/var/log/car-calendar"
    subconfig.vm.synced_folder "packages/", "/opt/packages"
  end
  
  
  config.vm.define "web" do |subconfig|
    subconfig.vm.box = "ubuntu/bionic64"
    subconfig.vm.hostname = "web"
    subconfig.vm.network "private_network", ip: "11.11.0.4"
    subconfig.vm.network "forwarded_port", guest: 5000, host: 5000
    subconfig.vm.network "forwarded_port", guest: 80, host: 8080
    subconfig.vm.synced_folder "web/src/", "/srv/car-calendar"
    subconfig.vm.synced_folder "packages/", "/opt/packages"

    subconfig.vm.provision "file", source: "web/motd", destination: "/tmp/motd"
    subconfig.vm.provision "file",
      source: "web/nginx.conf",
      destination: "/tmp/nginx.conf"
    subconfig.vm.provision "shell", path: "web/provision-web.sh"
  end


  config.vm.define "stagging-web" do |subconfig|
    subconfig.vm.box = "ubuntu/bionic64"
    subconfig.vm.hostname = "stagging-web"
    subconfig.vm.network "private_network", ip: "11.11.0.4"
    subconfig.vm.network "forwarded_port", guest: 5000, host: 5000
    subconfig.vm.network "forwarded_port", guest: 80, host: 8080
    subconfig.vm.synced_folder "stagging-web/src/", "/srv/car-calendar"
    subconfig.vm.synced_folder "packages/", "/opt/packages"

    subconfig.vm.provision "file", source: "stagging-web/motd", destination: "/tmp/motd"
    subconfig.vm.provision "file",
      source: "stagging-web/nginx.conf",
      destination: "/tmp/nginx.conf"
    subconfig.vm.provision "shell", path: "stagging-web/provision-web.sh"
  end
  
  
  config.vm.define "dev-web" do |subconfig|
    subconfig.vm.box = "ubuntu/bionic64"
    subconfig.vm.hostname = "dev-web"
    subconfig.vm.network "private_network", ip: "11.11.0.4"
    subconfig.vm.network "forwarded_port", guest: 5000, host: 5000
    subconfig.vm.network "forwarded_port", guest: 80, host: 8080
    subconfig.vm.synced_folder "dev-web/src/", "/srv/car-calendar"
    subconfig.vm.synced_folder "packages/", "/opt/packages"

    subconfig.vm.provision "file", source: "dev-web/motd", destination: "/tmp/motd"
    subconfig.vm.provision "file",
      source: "dev-web/nginx.conf",
      destination: "/tmp/nginx.conf"
    subconfig.vm.provision "shell", path: "dev-web/provision-web.sh"
  end

  config.vm.define "db" do |subconfig|
    subconfig.vm.box = "ubuntu/bionic64"
    subconfig.vm.hostname = "db"
    subconfig.vm.network "private_network", ip: "12.12.0.3"
    subconfig.vm.network "forwarded_port", guest: 80, host: 3380
    #subconfig.vm.synced_folder "db/data/", "/var/lib/mysql"
    subconfig.vm.synced_folder "db/src/", "/srv/car-calendar"
    subconfig.vm.synced_folder "db/logs/", "/var/log/car-calendar"
    subconfig.vm.synced_folder "packages/", "/opt/packages"

    subconfig.vm.provision "file", source: "db/motd", destination: "/tmp/motd"
    subconfig.vm.provision "shell", path: "db/provision-db.sh", env: {
      MYSQL_DB: "${MYSQL_DB:-carcalendar}",
      MYSQL_USER: "${MYSQL_USER:-db}",
      MYSQL_PASS: "${MYSQL_PASS:-dbpass}",
    }
  end
  
  
  config.vm.define "db-backup" do |subconfig|
    subconfig.vm.box = "ubuntu/bionic64"
    subconfig.vm.hostname = "db-backup"
    subconfig.vm.network "private_network", ip: "12.12.0.3"
    subconfig.vm.network "forwarded_port", guest: 80, host: 4000
    #subconfig.vm.synced_folder "db/data/", "/var/lib/mysql"
    subconfig.vm.synced_folder "db-backup/src/", "/srv/car-calendar"
    subconfig.vm.synced_folder "db-backup/logs/", "/var/log/car-calendar"
    subconfig.vm.synced_folder "packages/", "/opt/packages"

    subconfig.vm.provision "file", source: "db-backup/motd", destination: "/tmp/motd"
    subconfig.vm.provision "shell", path: "db-backup/provision-db.sh", env: {
      MYSQL_DB: "${MYSQL_DB:-carcalendar}",
      MYSQL_USER: "${MYSQL_USER:-db}",
      MYSQL_PASS: "${MYSQL_PASS:-dbpass}",
    }
  end
  
  config.vm.define "stagging-db" do |subconfig|
    subconfig.vm.box = "ubuntu/bionic64"
    subconfig.vm.hostname = "stagging-db"
    subconfig.vm.network "private_network", ip: "12.12.0.3"
    subconfig.vm.network "forwarded_port", guest: 80, host: 3380
    #subconfig.vm.synced_folder "db/data/", "/var/lib/mysql"
    subconfig.vm.synced_folder "stagging-db/src/", "/srv/car-calendar"
    subconfig.vm.synced_folder "stagging-db/logs/", "/var/log/car-calendar"
    subconfig.vm.synced_folder "packages/", "/opt/packages"

    subconfig.vm.provision "file", source: "stagging-db/motd", destination: "/tmp/motd"
    subconfig.vm.provision "shell", path: "stagging-db/provision-db.sh", env: {
      MYSQL_DB: "${MYSQL_DB:-carcalendar}",
      MYSQL_USER: "${MYSQL_USER:-db}",
      MYSQL_PASS: "${MYSQL_PASS:-dbpass}",
    }
  end
  
  
  config.vm.define "stagging-db-backup" do |subconfig|
    subconfig.vm.box = "ubuntu/bionic64"
    subconfig.vm.hostname = "stagging-db-backup"
    subconfig.vm.network "private_network", ip: "12.12.0.3"
    subconfig.vm.network "forwarded_port", guest: 80, host: 3380
    #subconfig.vm.synced_folder "db/data/", "/var/lib/mysql"
    subconfig.vm.synced_folder "stagging-db-backup/src/", "/srv/car-calendar"
    subconfig.vm.synced_folder "stagging-db-backup/logs/", "/var/log/car-calendar"
    subconfig.vm.synced_folder "packages/", "/opt/packages"

    subconfig.vm.provision "file", source: "stagging-db-backup/motd", destination: "/tmp/motd"
    subconfig.vm.provision "shell", path: "stagging-db-backup/provision-db.sh", env: {
      MYSQL_DB: "${MYSQL_DB:-carcalendar}",
      MYSQL_USER: "${MYSQL_USER:-db}",
      MYSQL_PASS: "${MYSQL_PASS:-dbpass}",
    }
  end
  
  
  config.vm.define "dev-db" do |subconfig|
    subconfig.vm.box = "ubuntu/bionic64"
    subconfig.vm.hostname = "dev-db"
    subconfig.vm.network "private_network", ip: "12.12.0.3"
    subconfig.vm.network "forwarded_port", guest: 80, host: 3380
    #subconfig.vm.synced_folder "db/data/", "/var/lib/mysql"
    subconfig.vm.synced_folder "dev-db/src/", "/srv/car-calendar"
    subconfig.vm.synced_folder "dev-db/logs/", "/var/log/car-calendar"
    subconfig.vm.synced_folder "packages/", "/opt/packages"

    subconfig.vm.provision "file", source: "dev-db/motd", destination: "/tmp/motd"
    subconfig.vm.provision "shell", path: "dev-db/provision-db.sh", env: {
      MYSQL_DB: "${MYSQL_DB:-carcalendar}",
      MYSQL_USER: "${MYSQL_USER:-db}",
      MYSQL_PASS: "${MYSQL_PASS:-dbpass}",
    }
  end



	config.vm.define "dev-db-backup" do |subconfig|
    subconfig.vm.box = "ubuntu/bionic64"
    subconfig.vm.hostname = "dev-db-backup"
    subconfig.vm.network "private_network", ip: "12.12.0.3"
    subconfig.vm.network "forwarded_port", guest: 80, host: 3380
    #subconfig.vm.synced_folder "db/data/", "/var/lib/mysql"
    subconfig.vm.synced_folder "dev-db-backup/src/", "/srv/car-calendar"
    subconfig.vm.synced_folder "dev-db-backup/logs/", "/var/log/car-calendar"
    subconfig.vm.synced_folder "packages/", "/opt/packages"

    subconfig.vm.provision "file", source: "dev-db-backup/motd", destination: "/tmp/motd"
    subconfig.vm.provision "shell", path: "dev-db-backup/provision-db.sh", env: {
      MYSQL_DB: "${MYSQL_DB:-carcalendar}",
      MYSQL_USER: "${MYSQL_USER:-db}",
      MYSQL_PASS: "${MYSQL_PASS:-dbpass}",
    }
  end

  config.vm.define "broker" do |subconfig|
    subconfig.vm.box = "ubuntu/bionic64"
    subconfig.vm.hostname = "broker"
    subconfig.vm.network "private_network", ip: "10.10.0.2"
    subconfig.vm.network "private_network", ip: "11.11.0.2"
    subconfig.vm.network "private_network", ip: "12.12.0.2"
    subconfig.vm.network "forwarded_port", guest: 5672, host: 5672
    subconfig.vm.network "forwarded_port", guest: 15672, host: 15672

    subconfig.vm.provision "shell", path: "broker/provision-broker.sh", env: {
      RABBITMQ_LOG_USER: "${RABBITMQ_LOG_USER:-log}",
      RABBITMQ_LOG_PASS: "${RABBITMQ_LOG_PASS:-logpass}",
      RABBITMQ_WEB_USER: "${RABBITMQ_WEB_USER:-web}",
      RABBITMQ_WEB_PASS: "${RABBITMQ_WEB_PASS:-webpass}",
      RABBITMQ_DMZ_USER: "${RABBITMQ_DMZ_USER:-dmz}",
      RABBITMQ_DMZ_PASS: "${RABBITMQ_DMZ_PASS:-dmzpass}",
      RABBITMQ_ADMIN_USER: "${RABBITMQ_ADMIN_USER:-admin}",
      RABBITMQ_ADMIN_PASS: "${RABBITMQ_ADMIN_PASS:-adminpass}",
    }
  end
  
  config.vm.define "stagging-broker" do |subconfig|
    subconfig.vm.box = "ubuntu/bionic64"
    subconfig.vm.hostname = "stagging-broker"
    subconfig.vm.network "private_network", ip: "10.10.0.2"
    subconfig.vm.network "private_network", ip: "11.11.0.2"
    subconfig.vm.network "private_network", ip: "12.12.0.2"
    subconfig.vm.network "forwarded_port", guest: 5672, host: 5672
    subconfig.vm.network "forwarded_port", guest: 15672, host: 15672

    subconfig.vm.provision "shell", path: "stagging-broker/provision-broker.sh", env: {
      RABBITMQ_LOG_USER: "${RABBITMQ_LOG_USER:-log}",
      RABBITMQ_LOG_PASS: "${RABBITMQ_LOG_PASS:-logpass}",
      RABBITMQ_WEB_USER: "${RABBITMQ_WEB_USER:-web}",
      RABBITMQ_WEB_PASS: "${RABBITMQ_WEB_PASS:-webpass}",
      RABBITMQ_DMZ_USER: "${RABBITMQ_DMZ_USER:-dmz}",
      RABBITMQ_DMZ_PASS: "${RABBITMQ_DMZ_PASS:-dmzpass}",
      RABBITMQ_ADMIN_USER: "${RABBITMQ_ADMIN_USER:-admin}",
      RABBITMQ_ADMIN_PASS: "${RABBITMQ_ADMIN_PASS:-adminpass}",
    }
  end
  
  config.vm.define "dev-broker" do |subconfig|
    subconfig.vm.box = "ubuntu/bionic64"
    subconfig.vm.hostname = "dev-broker"
    subconfig.vm.network "private_network", ip: "10.10.0.2"
    subconfig.vm.network "private_network", ip: "11.11.0.2"
    subconfig.vm.network "private_network", ip: "12.12.0.2"
    subconfig.vm.network "forwarded_port", guest: 5672, host: 5672
    subconfig.vm.network "forwarded_port", guest: 15672, host: 15672

    subconfig.vm.provision "shell", path: "dev-broker/provision-broker.sh", env: {
      RABBITMQ_LOG_USER: "${RABBITMQ_LOG_USER:-log}",
      RABBITMQ_LOG_PASS: "${RABBITMQ_LOG_PASS:-logpass}",
      RABBITMQ_WEB_USER: "${RABBITMQ_WEB_USER:-web}",
      RABBITMQ_WEB_PASS: "${RABBITMQ_WEB_PASS:-webpass}",
      RABBITMQ_DMZ_USER: "${RABBITMQ_DMZ_USER:-dmz}",
      RABBITMQ_DMZ_PASS: "${RABBITMQ_DMZ_PASS:-dmzpass}",
      RABBITMQ_ADMIN_USER: "${RABBITMQ_ADMIN_USER:-admin}",
      RABBITMQ_ADMIN_PASS: "${RABBITMQ_ADMIN_PASS:-adminpass}",
    }
  end
  
  
  config.vm.define "version-control" do |subconfig|
    subconfig.vm.box = "ubuntu/bionic64"
    subconfig.vm.hostname = "version-control"
    subconfig.vm.network "private_network", ip: "10.10.0.4"
    subconfig.vm.network "private_network", ip: "11.11.0.5"
    subconfig.vm.network "private_network", ip: "12.12.0.4"
	subconfig.vm.network "forwarded_port", guest: 137, host: 137
    subconfig.vm.network "forwarded_port", guest: 138, host: 138
	subconfig.vm.network "forwarded_port", guest: 139, host: 139
    subconfig.vm.network "forwarded_port", guest: 445, host: 445
    subconfig.vm.provision "shell", path: "version-control/provision-version-control.sh"
  end

end
