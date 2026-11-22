#!/bin/bash
set -euo pipefail

VERSION=16
DIR="/etc/postgresql/${VERSION}/main"

# postgresql installation
if ! [ -e "/usr/lib/systemd/system/postgresql.service" ]; then
  apt update
  apt install -y "postgresql-${VERSION}"
fi

# postgresql configuration
envsubst '${DB_LISTEN}' < /tmp/postgresql-hall.conf.tpl > "${DIR}/conf.d/hall.conf"
chown postgres:postgres "${DIR}/conf.d/hall.conf"
chmod 644 "${DIR}/conf.d/hall.conf"

HBA="${DIR}/pg_hba.conf"
HBA_APP_RULES=""
for ip in $APP_IPS; do
  HBA_APP_RULES+="$(printf 'host    %s      %s  %s/32  scram-sha-256' "$DB_NAME" "$DB_USER" "$ip")"$'\n'
done
export HBA_APP_RULES

envsubst '${HBA_APP_RULES}' < /tmp/pg_hba.conf.tpl > "${DIR}/pg_hba.conf"
chown postgres:postgres "${DIR}/pg_hba.conf"
chmod 640 "${DIR}/pg_hba.conf"

systemctl enable --now postgresql
systemctl restart postgresql

for _ in $(seq 1 30); do
  pg_isready -q -h localhost && break
  sleep 1
done
pg_isready -h localhost

# create db and user
export DB_NAME DB_USER DB_PASSWORD
cd /tmp
runuser -u postgres -- psql -v ON_ERROR_STOP=1 -q <<'SQL'
\getenv db_name DB_NAME
\getenv db_user DB_USER
\getenv db_password DB_PASSWORD

SELECT format('CREATE ROLE %I LOGIN', :'db_user')
WHERE NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = :'db_user') \gexec

SELECT format('ALTER ROLE %I LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS PASSWORD %L', :'db_user', :'db_password') \gexec

SELECT format('CREATE DATABASE %I OWNER %I', :'db_name', :'db_user')
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = :'db_name') \gexec
SELECT format('ALTER DATABASE %I OWNER TO %I', :'db_name', :'db_user') \gexec

SELECT format('REVOKE ALL ON DATABASE %I FROM PUBLIC', :'db_name') \gexec
SQL
