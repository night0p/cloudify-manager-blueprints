#!/usr/bin/env python

import tempfile
import os
from os.path import join, dirname

from cloudify import ctx
from cloudify.state import ctx_parameters as inputs

ctx.download_resource(
    join('components', 'utils.py'),
    join(dirname(__file__), 'utils.py'))
import utils  # NOQA


def preconfigure_restservice():

    rest_service_home = '/opt/manager'

    ctx.logger.info('Deploying REST Security configuration file...')
    sec_config = str(ctx.target.node.properties['security'])
    ctx.logger.info('security config: {0}'.format(sec_config))
    fd, path = tempfile.mkstemp()
    os.close(fd)
    with open(path, 'w') as f:
        f.write(sec_config)
    utils.move(path, os.path.join(rest_service_home, 'rest-security.conf'))

    utils.systemd.configure('restservice')


preconfigure_restservice()

ctx.logger.info('Reading rest_host_for_internal_requests Property...')
rest_host_for_internal_requests = ctx.node.properties['rest_host_for_internal_requests']
ctx.logger.info('rest_host_for_internal_requests is: {0}'.format(rest_host_for_internal_requests))

ctx.logger.info('Reading rest_host_for_external_requests Property...')
rest_host_for_external_requests = ctx.node.properties['rest_host_for_external_requests']
ctx.logger.info('rest_host_for_external_requests is: {0}'.format(rest_host_for_external_requests))

ctx.logger.info('got hostname: {0}'.format(utils.get_hostname()))

# TODO: ask NirC if this is ok
ctx.logger.info('Setting Private Manager IP Runtime Property.')
manager_private_ip = ctx.node.instance.host_ip
ctx.logger.info('Manager Private IP is: {0}'.format(manager_private_ip))

ctx.logger.info('Setting Public Manager IP Runtime Property.')
manager_ip = inputs['public_ip']
ctx.logger.info('Manager Public IP is: {0}'.format(manager_ip))
ctx.source.instance.runtime_properties['public_ip'] = manager_ip

manager_public_ip = ctx.source.instance.runtime_properties['public_ip']
ctx.logger.info('Manager public IP is: {0}'.format(manager_public_ip))
# ctx.target.instance.runtime_properties['manager_host_ip'] = manager_private_ip
ctx.target.instance.runtime_properties['manager_host_ip'] = manager_public_ip
