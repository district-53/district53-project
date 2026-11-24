#!/bin/bash

set -euo pipefail

APP_IPS="${APP_IPS:-}"
APP_PORT="${APP_PORT:-8000}"
LB_STRATEGY="${LB_STRATEGY:-least_conn}"
HEALTH_PATH="${HEALTH_PATH:-/}"

case "$LB_STRATEGY" in
  least_conn)  STRATEGY_LINE="    least_conn;" ;;
  ip_hash)     STRATEGY_LINE="    ip_hash;" ;;
  round_robin) STRATEGY_LINE="    #round robin" ;;
  *) echo "ERROR: unknown LB_STRATEGY=$LB_STRATEGY" >&2; exit 1 ;;
esac


apt update -y
apt install -y nginx curl ufw

SERVERS=""
for ip in $APP_IPS; do
  SERVERS+="    server ${ip}:${APP_PORT} max_fails=3 fail_timeout=10s;"$'\n'
done
export STRATEGY_LINE SERVERS

#nginx config
envsubst '${STRATEGY_LINE} ${SERVERS}' < "/tmp/nginx-lb.conf.tpl" > "/etc/nginx/conf.d/lb.conf"

rm -f /etc/nginx/sites-enabled/default

nginx -t
systemctl enable nginx
systemctl restart nginx

