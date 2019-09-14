# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure("2") do |config|

  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  config.vm.define "dmz" do |subconfig|
    subconfig.vm.box = "ubuntu/bionic64"
    subconfig.vm.hostname = "dmz"
    subconfig.vm.network "public_network"
    subconfig.vm.network "private_network", ip: "10.0.0.10"
  end

  config.vm.define "web" do |subconfig|
    subconfig.vm.box = "ubuntu/bionic64"
    subconfig.vm.hostname = "web"
    subconfig.vm.network "private_network", ip: "10.0.0.11"
    subconfig.vm.network "forwarded_port", guest: 80, host: 10080
    subconfig.vm.provision "shell", inline: <<-SHELL
      apt update && apt install -y nginx
    SHELL
  end

  config.vm.define "db" do |subconfig|
    subconfig.vm.box = "ubuntu/bionic64"
    subconfig.vm.hostname = "db"
    subconfig.vm.network "private_network", ip: "10.0.0.12"
    subconfig.vm.network "forwarded_port", guest: 3306, host: 13306
    subconfig.vm.provision "shell", inline: <<-SHELL
      echo 'mysql setup here'
    SHELL
  end

  config.vm.define "rabbitmq" do |subconfig|
    subconfig.vm.box = "ubuntu/bionic64"
    subconfig.vm.hostname = "rabbitmq"
    subconfig.vm.network "private_network", ip: "10.0.0.13"
    subconfig.vm.network "forwarded_port", guest: 5672, host: 15672

    subconfig.vm.provision "shell", inline: <<-SHELL
      apt update && apt install -y rabbitmq-server
    SHELL
  end

end
