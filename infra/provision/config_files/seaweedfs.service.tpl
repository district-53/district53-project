[Unit]
Description=SeaweedFS (master, volume, filer, S3)
After=network-online.target
Wants=network-online.target

[Service]
User=seaweedfs
Group=seaweedfs
ExecStart=/usr/local/bin/weed server \
  -ip=${SEAWEED_IP} \
  -dir=/var/lib/seaweedfs \
  -master.volumeSizeLimitMB=1024 \
  -s3 -s3.port=8333 -s3.config=/etc/seaweedfs/s3.json
Restart=on-failure

[Install]
WantedBy=multi-user.target
