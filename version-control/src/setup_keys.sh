#!/usr/bin/env bash

# Generate key if non-existant
KEY_PATH="$HOME/.ssh/id_rsa"
[[ -f "$KEY_PATH" ]] || \
  ssh-keygen -t rsa -N '' -f "$KEY_PATH" -C 'car@calendar.com'


# Run for each machine
while read -r ip name; do
  # Ignore empty lines
  [[ -z $ip ]] && continue

  # Check machine is up
  timeout 1 ping -c 1 $ip > /dev/null || { echo "$name is down" && continue; }

  # Copy key to machines
  ssh-copy-id -i "$KEY_PATH" vagrant@$ip
done <<< $(<'machines.txt')
