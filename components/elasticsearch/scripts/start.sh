#!/bin/bash -e

export IS_UPGRADE=$(ctx node properties is_upgrade)
if [ "$IS_UPGRADE" == "true" ]; then
  exit 0
fi

ES_ENDPOINT_IP=$(ctx node properties es_endpoint_ip)

if [ -z "${ES_ENDPOINT_IP}"]; then
    ctx logger info "Starting Elasticsearch..."
    sudo systemctl start elasticsearch.service
fi
