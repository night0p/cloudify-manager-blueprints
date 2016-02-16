#!/bin/bash

export IS_UPGRADE=$(ctx node properties is_upgrade)
ctx logger info "HHHHHHHEEEEEEEEEEEEEEEEEERRRRRRRRRRRRRRRRRRRRRREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE"
ctx logger info "is_upgrade is set to ${IS_UPGRADE} .........................."
if [ "$IS_UPGRADE" == "True" ]; then
  ctx logger info "BYEEEEEEEEEEEEEEEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
  exit 0
fi

. $(ctx download-resource "components/utils")

JAVA_SOURCE_URL=$(ctx node properties java_rpm_source_url)


ctx logger info "Installing Java..."
set_selinux_permissive
copy_notice "java"

if [[ "$JAVA_SOURCE_URL" == *rpm ]]; then
    yum_install ${JAVA_SOURCE_URL}
fi

# Make sure the cloudify logs dir exists before we try moving the java log there
# -p will cause it not to error if the dir already exists
create_dir "/var/log/cloudify"

# Java install log is dropped in /var/log. Move it to live with the rest of the cloudify logs
if [ -f "/var/log/java_install.log" ]; then
    sudo mv "/var/log/java_install.log" "/var/log/cloudify"
fi
