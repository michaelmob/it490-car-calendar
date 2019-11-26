#!/bin/bash
archive_location="vagrant@10.10.0.4:/home/vagrant/car_calendar_archive/dmz/"
working_location="/srv/car-calendar/"
echo "Enter Car Calendar Version Number:"
read version_number
software="dmz.$version_number"
echo "Enter archive or deploy (archive/deploy):"
read action
if [ $action == "archive" ]
then
        tar -pcvzf "$software.tar.gz" /srv/car-calendar
        scp "$software.tar.gz" "$archive_location"
        rm "$software.tar.gz"
        echo $software > version_info.txt
elif [ $action == "deploy" ]
then
        scp "$archive_location/$software.tar.gz" ./
        tar -pxvzf "$software.tar.gz"
        #rm -r -f /srv/
        mv -f srv/* /srv/
        rm "$software.tar.gz"
        echo $software > version_info.txt
else
        echo "Enter either archive to archive version, or deploy to deploy version"
fi