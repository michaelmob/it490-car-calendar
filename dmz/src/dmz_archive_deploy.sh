#!/bin/bash

archive_location="/home/vagrant/car-calendar-archive"

echo "Only run this script from the Version Control Server, within the attached network share for the DMZ server"
echo ""

echo "Archived Versions: "
ls $archive_location
echo ""

echo "Enter Car Calendar Version Number:"
read version_number

software="car-calendar.$version_number"

echo "Enter archive or deploy (archive/deploy):"
read action

if [ $action == "archive" ]
then
	echo $software > version_info.txt
	tar -pcvzf "$software.tar.gz" /srv/car-calendar
	if [  ! -d "$archive_location/$software" ]
	then
		if [ ! -d "$archive_location" ]
		then
			mkdir $archive_location
		fi
		mkdir "$archive_location/$software"
	fi
	mv "$software.tar.gz" "$archive_location/$software"
elif [ $action == "deploy" ]
then
	cp "$archive_location/$software/$software.tar.gz" ./
	tar -pxvzf "$software.tar.gz"
	mv -f srv/car-calendar/* ./
	rm -r -f srv
	rm "$software.tar.gz"
else
	echo "Enter either pack to pack version, or unpack to unpack version"
fi
