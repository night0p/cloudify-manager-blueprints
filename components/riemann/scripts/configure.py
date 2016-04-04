#!/usr/bin/env python

import os
from os.path import join, dirname

from cloudify import ctx

ctx.download_resource(
    join('components', 'utils.py'),
    join(dirname(__file__), 'utils.py'))
import utils  # NOQA


CONFIG_PATH = 'components/riemann/config'


def configure_riemann():
    riemann_config_path = '/etc/riemann'
    ctx.logger.info('Deploying Riemann manager.config...')
    utils.move(
        '/tmp/plugins/riemann-controller/riemann_controller/resources/manager.config',  # NOQA
        '{0}/conf.d/manager.config'.format(riemann_config_path))

    ctx.logger.info('Deploying Riemann conf...')
    utils.deploy_blueprint_resource(
        '{0}/main.clj'.format(CONFIG_PATH),
        '{0}/main.clj'.format(riemann_config_path))

    # our riemann configuration will (by default) try to read these environment
    # variables. If they don't exist, it will assume
    # that they're found at "localhost"
    # export MANAGEMENT_IP=""
    # export RABBITMQ_HOST=""

    # we inject the management_ip for both of these to Riemann's systemd
    # config.
    # These should be potentially different
    # if the manager and rabbitmq are running on different hosts.
    utils.systemd.configure('riemann')
    utils.clean_var_log_dir('riemann')

configure_riemann
