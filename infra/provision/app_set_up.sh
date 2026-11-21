#!/bin/bash
set -euo pipefail

APP_DIR="/opt/hall"
VENV_DIR="/opt/venv"
ENV_DIR="/etc/hall"
ENV_FILE="${ENV_DIR}/app.env"
APP_USER="hall"
APP_PORT="${APP_PORT:-8000}"

if [[ -z "${DB_PASSWORD:-}" ]]; then
  echo "ERROR: DB_PASSWORD is empty (check infra/secrets/db_password)" >&2
  exit 1
fi
if [[ -z "${SECRET_KEY:-}" ]]; then
  echo "ERROR: SECRET_KEY is empty (check infra/secrets/secret_key)" >&2
  exit 1
fi
if [[ -z "${S3_ACCESS_KEY:-}" ]]; then
  echo "ERROR: S3_ACCESS_KEY is empty (check infra/secrets/s3_access_key)" >&2
  exit 1
fi
if [[ -z "${S3_SECRET_KEY:-}" ]]; then
  echo "ERROR: S3_SECRET_KEY is empty (check infra/secrets/s3_secret_key)" >&2
  exit 1
fi

APP_HOME="/var/lib/${APP_USER}"
if ! id -u "$APP_USER" >/dev/null 2>&1; then
  useradd --system --home-dir "$APP_HOME" --shell /usr/sbin/nologin "$APP_USER"
fi
install -d -m 750 -o "$APP_USER" -g "$APP_USER" "$APP_HOME"

# env file
install -d -m 750 -o root -g "$APP_USER" "$ENV_DIR"

cat > "$ENV_FILE" <<EOF
DATABASE_URL=postgresql+psycopg2://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:5432/${DB_NAME}
SECRET_KEY=${SECRET_KEY}
FLASK_DEBUG=0
S3_ENDPOINT=${S3_ENDPOINT}
S3_ACCESS_KEY=${S3_ACCESS_KEY}
S3_SECRET_KEY=${S3_SECRET_KEY}
S3_BUCKET=${S3_BUCKET}
EOF
chown root:"$APP_USER" "$ENV_FILE"
chmod 640 "$ENV_FILE"

# python venv
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y python3-venv

if [[ ! -x "${VENV_DIR}/bin/python" ]]; then
  python3 -m venv "${VENV_DIR}"
fi
"${VENV_DIR}/bin/pip" install -q -r "${APP_DIR}/requirements.txt"


# table creation
if [[ "${RUN_INIT_DB:-0}" == "1" ]]; then
  cd "$APP_DIR"
  runuser -u "$APP_USER" -- "$VENV_DIR/bin/flask" --app app init-db
  runuser -u "$APP_USER" -- "$VENV_DIR/bin/flask" --app app add-houses
  runuser -u "$APP_USER" -- "$VENV_DIR/bin/flask" --app app add-people
fi


# systemd service
cat > "/etc/systemd/system/hall.service" <<EOF
[Unit]
Description=Hall app
After=network-online.target
Wants=network-online.target

[Service]
User=${APP_USER}
WorkingDirectory=${APP_DIR}
EnvironmentFile=${ENV_FILE}
ExecStart=${VENV_DIR}/bin/gunicorn -b 0.0.0.0:${APP_PORT} --workers 2 --threads 4 --worker-class gthread --access-logfile - app:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable hall
systemctl restart hall