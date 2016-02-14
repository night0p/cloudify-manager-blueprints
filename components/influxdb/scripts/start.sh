#!/bin/bash -e

export IS_UPGRADE=$(ctx node properties is_upgrade)
if [ "$IS_UPGRADE" == "true" ]; then
  exit 0
fi

INFLUXDB_ENDPOINT_IP=$(ctx node properties influxdb_endpoint_ip)

if [ -z "${INFLUXDB_ENDPOINT_IP}" ]; then
    ctx logger info "Starting InfluxDB Service..."
    sudo systemctl start cloudify-influxdb.service
fi
