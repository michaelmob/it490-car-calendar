#!/usr/bin/env bash
set -ex

# Update package list
apt-get update -y
apt-get upgrade -y
apt install tasksel -y
tasksel install samba-server
cp /etc/samba/smb.conf /etc/samba/smb.conf_backup
bash -c 'grep -v -E "^#|^;" /etc/samba/smb.conf_backup | grep . > /etc/samba/smb.conf'
useradd -m dmzadmin -p dmzpass
smbpasswd -a dmzadmin -s
dmzpass
dmzpass
bash -c 'echo "[homes]
   comment = Home Directories
   browseable = yes
   read only = no
   create mask = 0700
   directory mask = 0700
   valid users = %S" >> /etc/samba/smb.conf'
mkdir /home/vagrant/car_calendar_archive
chmod 777 /home/vagrant/car_calendar_archive
bash -c 'echo "[public]
   comment = public anonymous access
   path = /home/vagrant/car_calendar_archive
   browsable =yes
   create mask = 0660
   directory mask = 0771
   writable = yes
   guest ok = yes" >> /etc/samba/smb.conf'
systemctl restart smbd
sudo ufw allow samba
smbclient -L localhost
