#!/usr/bin/env bash

#echo "Enter Car Calendar Version Number:"
#read version_number


# Get version number
version_number="$1"
[[ -z "$version_number" ]] && echo 'No version specified!' && exit 1


# Specific machines through args or default
extra_args="${@:2}"
machines="${extra_args:-db dmz web}"
mkdir -p "$HOME/archives"


# Run for each machine
while read -r ip name; do
  # Only run for specified machines
  [[ "$machines" =~ "$name" ]] || continue

  # Check that archive exists
  archive="$HOME/archives/${name}_${version_number}.tar.gz"
  [[ ! -f "$archive" ]] && echo "$name $version_number does not exist" && continue

  # Deploy version
  echo "=== Deploying $name $version_number ==="
  scp "$archive" vagrant@$ip:src.tar.gz
  ssh vagrant@$ip 'tar -xvf src.tar.gz; ./src/deploy.sh; exit' &
done <<< $(<'machines.txt')
