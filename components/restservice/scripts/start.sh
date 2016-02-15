#!/bin/bash -e

export IS_UPGRADE=$(ctx node properties is_upgrade)
if [ "$IS_UPGRADE" == "true" ]; then
  ctx logger info "Restarting Rest Service after upgrade.."
  sudo systemctl restart cloudify-restservice.service
else
  ctx logger info "Starting Rest Service via Gunicorn..."
  sudo systemctl start cloudify-restservice.service  
fi

