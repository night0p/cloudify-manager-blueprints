#!/bin/bash -e
. $(ctx download-resource "components/utils")

rest_protocol=$(ctx target instance runtime-properties rest_protocol)
rest_port=$(ctx target instance runtime-properties rest_port)
security_enabled=$(ctx target instance runtime-properties security_enabled)
ssl_enabled=$(ctx target instance runtime-properties ssl_enabled)
cloudify_username=$(ctx -j target node properties security.admin_username)
cloudify_password=$(ctx -j target node properties security.admin_password)
verify_certificate=$(ctx target instance runtime-properties verify_certificate)
ssl_certificate=$(ctx target instance runtime-properties ssl_certificate)

ctx source instance runtime-properties rest_protocol ${rest_protocol}
ctx source instance runtime-properties rest_port ${rest_port}
ctx source instance runtime-properties security_enabled ${security_enabled}
ctx source instance runtime-properties ssl_enabled ${ssl_enabled}
ctx source instance runtime-properties cloudify_username ${cloudify_username}
ctx source instance runtime-properties cloudify_password ${cloudify_password}
ctx source instance runtime-properties verify_certificate ${verify_certificate}
ctx source instance runtime-properties ssl_certificate ${ssl_certificate}

ctx logger info "***** debug: Riemann uses rest_protocol: ${rest_protocol}"
ctx logger info "***** debug: Riemann uses rest_port: ${rest_port}"
ctx logger info "***** debug: Riemann uses security_enabled: ${security_enabled}"
ctx logger info "***** debug: Riemann uses ssl_enabled: ${ssl_enabled}"
ctx logger info "***** debug: Riemann uses cloudify_username: ${cloudify_username}"
ctx logger info "***** debug: Riemann uses cloudify_password: ${cloudify_password}"
ctx logger info "***** debug: Riemann uses verify_certificate: ${verify_certificate}"
ctx logger info "***** debug: Riemann uses ssl_certificate: ${ssl_certificate}"
