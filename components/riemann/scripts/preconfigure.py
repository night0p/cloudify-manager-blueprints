#!/usr/bin/env python

import os
from os.path import join, dirname

from cloudify import ctx

ctx.download_resource(
    join('components', 'utils.py'),
    join(dirname(__file__), 'utils.py'))
import utils  # NOQA


manager_host = ctx.target.instance.runtime_properties['internal_manager_host']
rest_host = ctx.target.instance.runtime_properties['internal_rest_host']
rest_protocol = ctx.target.instance.runtime_properties['rest_protocol']
rest_port = ctx.target.instance.runtime_properties['rest_port']
security_enabled = ctx.target.instance.runtime_properties['security_enabled']
ssl_enabled = ctx.target.instance.runtime_properties['ssl_enabled']
cloudify_username = ctx.target.instance.runtime_properties['cloudify_username']
cloudify_password = ctx.target.instance.runtime_properties['cloudify_password']
verify_certificate = ctx.target.instance.runtime_properties['verify_certificate']
ssl_certificate = ctx.target.instance.runtime_properties['ssl_certificate']


ctx.source.instance.runtime_properties['manager_host'] = manager_host
ctx.source.instance.runtime_properties['rest_host'] = rest_host
ctx.source.instance.runtime_properties['rest_protocol'] = rest_protocol
ctx.source.instance.runtime_properties['rest_port'] = rest_port
ctx.source.instance.runtime_properties['security_enabled'] = security_enabled
ctx.source.instance.runtime_properties['ssl_enabled'] = ssl_enabled
ctx.source.instance.runtime_properties['cloudify_username'] = cloudify_username
ctx.source.instance.runtime_properties['cloudify_password'] = cloudify_password
ctx.source.instance.runtime_properties['verify_certificate'] = verify_certificate
ctx.source.instance.runtime_properties['ssl_certificate'] = ssl_certificate


ctx.logger.info('***** debug: Riemann uses manager_host: {0}'.format(manager_host))
ctx.logger.info('***** debug: Riemann uses rest_host: {0}'.format(rest_host))
ctx.logger.info('***** debug: Riemann uses rest_protocol: {0}'.format(rest_protocol))
ctx.logger.info('***** debug: Riemann uses rest_port: {0}'.format(rest_port))
ctx.logger.info('***** debug: Riemann uses security_enabled: {0}'.format(security_enabled))
ctx.logger.info('***** debug: Riemann uses ssl_enabled: {0}'.format(ssl_enabled))
ctx.logger.info('***** debug: Riemann uses cloudify_username: {0}'.format(cloudify_username))
ctx.logger.info('***** debug: Riemann uses cloudify_password: {0}'.format(cloudify_password))
ctx.logger.info('***** debug: Riemann uses verify_certificate: {0}'.format(verify_certificate))
ctx.logger.info('***** debug: Riemann uses ssl_certificate: {0}'.format(ssl_certificate))
