# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure("2") do |config|

  # dev, staging, production
  environment = 'dev'
  version_control = true


  if version_control
    config.vm.define "version-control" do |subconfig|  # 10.0.0.2
      subconfig.vm.box = "ubuntu/bionic64"
      subconfig.vm.hostname = "version-control"
      subconfig.vm.network "public_network", :mac => "000000000001"
      subconfig.vm.synced_folder "version-control/src/", "/home/vagrant/src"
      subconfig.vm.provision "shell", path: "version-control/provision-version-control.sh"
    end
  end


  config.vm.define "broker-#{environment}" do |subconfig|  # 10.0.0.3
    subconfig.vm.box = "ubuntu/bionic64"
    subconfig.vm.hostname = "broker"
    subconfig.vm.network "public_network", :mac => "000000000002"
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


  config.vm.define "dmz-#{environment}" do |subconfig|  # 10.0.0.4
    subconfig.vm.box = "ubuntu/bionic64"
    subconfig.vm.hostname = "dmz"
    subconfig.vm.network "public_network", :mac => "000000000003"
    subconfig.vm.synced_folder "dmz/src/", "/home/vagrant/src" unless version_control
    subconfig.vm.synced_folder "packages/", "/opt/packages"
    subconfig.vm.provision "shell", path: "dmz/provision-dmz.sh"
  end


  config.vm.define "web-#{environment}" do |subconfig|  # 10.0.0.5
    subconfig.vm.box = "ubuntu/bionic64"
    subconfig.vm.hostname = "web"
    subconfig.vm.network "public_network", :mac => "000000000004"
    subconfig.vm.synced_folder "web/src/", "/home/vagrant/src" unless version_control
    subconfig.vm.synced_folder "packages/", "/opt/packages"
    subconfig.vm.provision "file", source: "web/motd", destination: "/tmp/motd"
    subconfig.vm.provision "shell", path: "web/provision-web.sh"
  end


  config.vm.define "db-#{environment}" do |subconfig|  # 10.0.0.6
    subconfig.vm.box = "ubuntu/bionic64"
    subconfig.vm.hostname = "db"
    subconfig.vm.network "public_network", :mac => "000000000005"
    subconfig.vm.synced_folder "db/src/", "/home/vagrant/src" unless version_control
    subconfig.vm.synced_folder "db/logs/", "/home/vagrant/logs"
    subconfig.vm.synced_folder "packages/", "/opt/packages"
    subconfig.vm.provision "file", source: "db/motd", destination: "/tmp/motd"
    subconfig.vm.provision "file", source: "db/server1.cnf", destination: "/tmp/mysql.cnf"
    subconfig.vm.provision "shell", path: "db/provision-db.sh", env: {
      MYSQL_DB: "${MYSQL_DB:-carcalendar}",
      MYSQL_USER: "${MYSQL_USER:-db}",
      MYSQL_PASS: "${MYSQL_PASS:-dbpass}",
      MYSQL_MASTER_HOST: "db-backup",
      MYSQL_REPLICATOR_USER: "${MYSQL_REPLICATOR_USER:-replicator}",
      MYSQL_REPLICATOR_PASS: "${MYSQL_REPLICATOR_PASS:-replicatorpass}",
    }
  end


  config.vm.define "db-backup-#{environment}" do |subconfig|  # 10.0.0.7
    subconfig.vm.box = "ubuntu/bionic64"
    subconfig.vm.hostname = "db-backup"
    subconfig.vm.network "public_network", :mac => "000000000006"
    subconfig.vm.synced_folder "db/src/", "/home/vagrant/src" unless version_control
    subconfig.vm.synced_folder "db/logs/", "/home/vagrant/logs"
    subconfig.vm.synced_folder "packages/", "/opt/packages"
    subconfig.vm.provision "file", source: "db/motd", destination: "/tmp/motd"
    subconfig.vm.provision "file", source: "db/server2.cnf", destination: "/tmp/mysql.cnf"
    subconfig.vm.provision "shell", path: "db/provision-db.sh", env: {
      MYSQL_DB: "${MYSQL_DB:-carcalendar}",
      MYSQL_USER: "${MYSQL_USER:-db}",
      MYSQL_PASS: "${MYSQL_PASS:-dbpass}",
      MYSQL_MASTER_HOST: "db",
      MYSQL_REPLICATOR_USER: "${MYSQL_REPLICATOR_USER:-replicator}",
      MYSQL_REPLICATOR_PASS: "${MYSQL_REPLICATOR_PASS:-replicatorpass}",
    }
  end

end
