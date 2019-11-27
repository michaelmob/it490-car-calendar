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
  echo "=== Archiving $name $version_number ==="

  # Archive version
  archive="$HOME/archives/${name}_${version_number}.tar.gz"

  cd "/vagrant/$name"
  echo "$version_number" > './src/VERSION'
  tar -pcvzf "$archive" './src'
  rm './src/VERSION'
done <<< $(<'machines.txt')
