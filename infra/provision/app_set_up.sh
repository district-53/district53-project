#!/bin/bash
set -euo pipefail

APP_DIR="/opt/hall"
ENV_DIR="/etc/hall"
ENV_FILE="${ENV_DIR}/app.env"
USER_HOME="/var/lib/hall"

for var in DB_PASSWORD SECRET_KEY S3_ACCESS_KEY S3_SECRET_KEY; do
  if [ -z "${!var}" ]; then
    echo "ERROR: ${var} is empty" >&2
    exit 1
  fi
done

if ! id -u hall >/dev/null 2>&1; then
  useradd --system --home-dir "$USER_HOME" --shell /usr/sbin/nologin hall
  mkdir -p "$USER_HOME"
  chown hall:hall "$USER_HOME"
  chmod 750 "$USER_HOME"
fi

# env file
mkdir -p "$ENV_DIR"
chown root:hall "$ENV_DIR"
chmod 750 "$ENV_DIR"

touch "$ENV_FILE"
chown root:hall "$ENV_FILE"
chmod 640 "$ENV_FILE"
envsubst '${DB_USER} ${DB_PASSWORD} ${DB_HOST} ${DB_NAME} ${SECRET_KEY} ${APP_PORT} ${S3_ENDPOINT} ${S3_ACCESS_KEY} ${S3_SECRET_KEY} ${S3_BUCKET}' < "/tmp/app.env.tpl" > "$ENV_FILE"

# python venv
apt update
apt install -y python3-venv

if [[ ! -x "/opt/venv/bin/python" ]]; then
  python3 -m venv /opt/venv
fi
"/opt/venv/bin/pip" install -q -r /opt/hall/requirements.txt


# table creation
if [[ "${RUN_INIT_DB:-0}" == "1" ]]; then
  cd "$APP_DIR"
  runuser -u hall -- /opt/venv/bin/flask --app app init-db
  runuser -u hall -- /opt/venv/bin/flask --app app add-houses
  runuser -u hall -- /opt/venv/bin/flask --app app add-people
fi


# systemd service
cp /tmp/hall.service /etc/systemd/system/hall.service
chown root:root "/etc/systemd/system/hall.service"
chmod 644 "/etc/systemd/system/hall.service"

systemctl daemon-reload
systemctl enable hall
systemctl restart hall