#!/usr/bin/env python

from os.path import join, dirname

from cloudify import ctx

ctx.download_resource(
    join('components', 'utils.py'),
    join(dirname(__file__), 'utils.py'))
import utils  # NOQA


target_runtime_props = ctx.target.instance.runtime_properties
source_runtime_props = ctx.source.instance.runtime_properties

# security setting from the manager configuration
manager_host = target_runtime_props['internal_manager_host']
rest_host = target_runtime_props['internal_rest_host']
rest_protocol = target_runtime_props['rest_protocol']
rest_port = target_runtime_props['rest_port']
security_enabled = target_runtime_props['security_enabled']
ssl_enabled = target_runtime_props['ssl_enabled']

# security settings from Riemann's configuration # currently ignored by riemann
cloudify_username = ctx.node.properties.rest_username
cloudify_password = ctx.node.properties.rest_password
verify_certificate = ctx.node.properties.verify_manager_certificate
ssl_certificate = ctx.node.properties.manager_ssl_certificate


source_runtime_props['manager_host'] = manager_host
source_runtime_props['rest_host'] = rest_host
source_runtime_props['rest_protocol'] = rest_protocol
source_runtime_props['rest_port'] = rest_port
source_runtime_props['security_enabled'] = security_enabled
source_runtime_props['ssl_enabled'] = ssl_enabled


ctx.logger.info('***** debug: Riemann uses manager_host: {0}'.
                format(manager_host))
ctx.logger.info('***** debug: Riemann uses rest_host: {0}'.
                format(rest_host))
ctx.logger.info('***** debug: Riemann uses rest_protocol: {0}'.
                format(rest_protocol))
ctx.logger.info('***** debug: Riemann uses rest_port: {0}'.
                format(rest_port))
ctx.logger.info('***** debug: Riemann uses security_enabled: {0}'.
                format(security_enabled))
ctx.logger.info('***** debug: Riemann uses ssl_enabled: {0}'.
                format(ssl_enabled))
ctx.logger.info('***** debug: Riemann uses cloudify_username: {0}'.
                format(cloudify_username))
ctx.logger.info('***** debug: Riemann uses cloudify_password: {0}'.
                format(cloudify_password))
ctx.logger.info('***** debug: Riemann uses verify_manager_certificate: {0}'.
                format(verify_certificate))
ctx.logger.info('***** debug: Riemann uses manager_ssl_certificate: {0}'.
                format(ssl_certificate))
