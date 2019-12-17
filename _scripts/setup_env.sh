#!/usr/bin/env bash
cd "${0%/*}/.."

setup_env() {
  [[ ! -f "$1/src/.env" ]] && \
      cp "$1/src/_env" "$1/src/.env" && \
      echo "$1/src/_env -> $1/src/.env"
}

setup_env db
setup_env dmz
setup_env web
