#!/usr/bin/env python

import tempfile
import os
from os.path import join, dirname

from cloudify import ctx

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

ctx.logger.info('Reading internal_rest_host property from manager_configuration...')
internal_rest_host = ctx.target.node.properties['internal_rest_host']
ctx.logger.info('internal_rest_host is: {0}'.format(internal_rest_host))

ctx.logger.info('Reading external_rest_host property from manager_configuration...')
external_rest_host = ctx.target.node.properties['external_rest_host']
ctx.logger.info('external_rest_host is: {0}'.format(external_rest_host))
