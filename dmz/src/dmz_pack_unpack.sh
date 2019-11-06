#!/bin/bash

echo "Pack or Unpack Version (pack/unpack)"
read action

echo "Enter Car Calendar Version Number"
read version_number

srv="srv.$version_number"
software="car-calendar.$version_number"

if [ $action == "pack" ]
then
	tar -pcvzf "$software.tar.gz" /srv/car-calendar
	#open sftp connection to version control server
	#upload the $software.tar.gz through sftp connection to the version control server
elif [ $action == "unpack" ]
then
	#open sftp connectionto the version control server
	#download the $software.tar.gz through sftp connection to the version control server
	tar -pxvzf "$software.tar.gz"
	mv -f srv/car-calendar/* ./
	rm -r -f srv
	rm "$software.tar.gz"
else
	echo "Enter either pack to pack version, or unpack to unpack version"
fi
