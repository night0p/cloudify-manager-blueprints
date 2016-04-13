#!/usr/bin/env python

from cloudify import ctx


def preconfigure_restservice():

    ctx.logger.info('Reading internal_rest_host property from manager_configuration...')
    internal_rest_host = ctx.target.instance.runtime_properties['internal_rest_host']
    ctx.logger.info('internal_rest_host is: {0}'.format(internal_rest_host))
    ctx.source.instance.runtime_properties['internal_rest_host'] = internal_rest_host

    ctx.logger.info('Reading external_rest_host property from manager_configuration...')
    external_rest_host = ctx.target.instance.runtime_properties['external_rest_host']
    ctx.logger.info('external_rest_host is: {0}'.format(external_rest_host))
    ctx.source.instance.runtime_properties['external_rest_host'] = external_rest_host

    ctx.logger.info('Reading security property from manager_configuration...')
    security_config = str(ctx.target.node.properties['security'])
    ctx.logger.info('security_config is: {0}'.format(security_config))
    ctx.source.instance.runtime_properties['security_configuration'] = security_config


preconfigure_restservice()
