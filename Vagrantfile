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
  end


  config.vm.define "web" do |subconfig|
    subconfig.vm.box = "ubuntu/bionic64"
    subconfig.vm.hostname = "web"

    subconfig.vm.network "private_network", ip: "11.11.0.3"
    subconfig.vm.network "forwarded_port", guest: 80, host: 8080

    subconfig.vm.provision "shell", path: "web/provision-web.sh"
  end


  config.vm.define "db" do |subconfig|
    subconfig.vm.box = "ubuntu/bionic64"
    subconfig.vm.hostname = "db"

    subconfig.vm.network "private_network", ip: "12.12.0.3"
    subconfig.vm.network "forwarded_port", guest: 3306, host: 3307

    subconfig.vm.provision "shell", path: "db/provision-db.sh"
  end


  config.vm.define "broker" do |subconfig|
    subconfig.vm.box = "ubuntu/bionic64"
    subconfig.vm.hostname = "broker"

    subconfig.vm.network "private_network", ip: "10.10.0.2"
    subconfig.vm.network "private_network", ip: "11.11.0.2"
    subconfig.vm.network "private_network", ip: "12.12.0.2"
    subconfig.vm.network "forwarded_port", guest: 5672, host: 5673
    subconfig.vm.network "forwarded_port", guest: 15672, host: 15673

    subconfig.vm.provision "shell", path: "broker/provision-broker.sh"
  end

end
