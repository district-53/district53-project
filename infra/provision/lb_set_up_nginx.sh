#!/bin/bash

set -euo pipefail

APP_IPS="${APP_IPS:-}"
APP_PORT="${APP_PORT:-80}"
LB_STRATEGY="${LB_STRATEGY:-least_conn}"
HEALTH_PATH="${HEALTH_PATH:-/}"
CONF=/etc/nginx/conf.d/lb.conf

case "$LB_STRATEGY" in
  least_conn)  STRATEGY_LINE="    least_conn;" ;;
  ip_hash)     STRATEGY_LINE="    ip_hash;" ;;
  round_robin) STRATEGY_LINE="    #round robin" ;;
  *) echo "ERROR: unknown LB_STRATEGY=$LB_STRATEGY" >&2; exit 1 ;;
esac


apt-get update -y
apt-get install -y nginx curl ufw

SERVERS=""
for ip in $APP_IPS; do
  SERVERS+="    server ${ip}:${APP_PORT} max_fails=3 fail_timeout=10s;"$'\n'
done

#nginx config
cat > "$CONF" <<EOF
log_format upstreamlog '\$remote_addr -> \$upstream_addr [\$time_local] '
                       '"\$request" \$status rt=\$request_time urt=\$upstream_response_time';

upstream app_backend {
${STRATEGY_LINE}
${SERVERS}
    keepalive 32;
}

server {
    listen 80 default_server;
    server_name _;
    client_max_body_size 6m;

    access_log /var/log/nginx/lb_access.log upstreamlog;
    error_log  /var/log/nginx/lb_error.log warn;

    location / {
        proxy_pass http://app_backend;

        proxy_http_version 1.1;
        proxy_set_header Connection "";

        proxy_set_header Host              \$host;
        proxy_set_header X-Real-IP         \$remote_addr;
        proxy_set_header X-Forwarded-For   \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

        proxy_connect_timeout 3s;
        proxy_send_timeout    30s;
        proxy_read_timeout    30s;

        proxy_next_upstream error timeout http_502 http_503 http_504;
        proxy_next_upstream_tries 2;
    }

    location = /nginx_status {
        stub_status;
        allow 127.0.0.1;
        deny all;
    }
}
EOF


rm -f /etc/nginx/sites-enabled/default

nginx -t
systemctl enable nginx
systemctl restart nginx

