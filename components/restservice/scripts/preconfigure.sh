#!/bin/bash -e

export IS_UPGRADE=$(ctx node properties is_upgrade)
if [ "$IS_UPGRADE" == "true" ]; then
  exit 0
fi

. $(ctx download-resource "components/utils")

CONFIG_REL_PATH="components/restservice/config"
REST_SERVICE_HOME="/opt/manager"

ctx logger info "Deploying REST Security configuration file..."
sec_settings=$(ctx -j target node properties security)
# TODO: do not print to stdout
echo $sec_settings | sudo tee "${REST_SERVICE_HOME}/rest-security.conf"
configure_systemd_service "restservice"
