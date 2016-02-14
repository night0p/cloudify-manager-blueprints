#!/bin/bash -e

export IS_UPGRADE=$(ctx node properties is_upgrade)
if [ "$IS_UPGRADE" == "true" ]; then
  exit 0
fi

ctx logger info "Starting Management Worker Service..."
sudo systemctl start cloudify-mgmtworker.service
