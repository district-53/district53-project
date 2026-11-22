#!/bin/bash
set -euo pipefail

PG_VERSION=16
PKG="postgresql-client-${PG_VERSION}"

if [ -e "/usr/lib/postgresql/${PG_VERSION}/bin/psql" ]; then
  echo "${PKG} already installed"
  exit 0
fi

apt update
apt install -y "$PKG"
psql --version
