#!/usr/bin/env python

from os.path import join, dirname

from cloudify import ctx

ctx.download_resource(
    join('components', 'utils.py'),
    join(dirname(__file__), 'utils.py'))
import utils  # NOQA


CONFIG_PATH = 'components/nginx/config'


def preconfigure_nginx():

    # this is used by nginx's default.conf to select the relevant configuration
    rest_protocol = ctx.target.instance.runtime_properties['rest_protocol']

    # TODO: NEED TO IMPLEMENT THIS IN CTX UTILS
    ctx.source.instance.runtime_properties['rest_protocol'] = rest_protocol
    if rest_protocol == 'https':
        internal_rest_host = \
            ctx.target.instance.runtime_properties['internal_rest_host']
        external_rest_host = \
            ctx.target.instance.runtime_properties['external_rest_host']
        # handle certs for internal rest host
        utils.deploy_ssl_cert_and_key(cert_filename='internal_rest_host.crt',
                                      key_filename='internal_rest_host.key',
                                      cn=internal_rest_host)
        utils.deploy_ssl_cert_and_key(cert_filename='external_rest_host.crt',
                                      key_filename='external_rest_host.key',
                                      cn=external_rest_host)

    ctx.logger.info('Deploying Nginx configuration files...')
    utils.deploy_blueprint_resource(
        '{0}/{1}-rest-server.cloudify'.format(CONFIG_PATH, rest_protocol),
        '/etc/nginx/conf.d/{0}-rest-server.cloudify'.format(rest_protocol))
    utils.deploy_blueprint_resource(
        '{0}/nginx.conf'.format(CONFIG_PATH),
        '/etc/nginx/nginx.conf')
    utils.deploy_blueprint_resource(
        '{0}/default.conf'.format(CONFIG_PATH),
        '/etc/nginx/conf.d/default.conf')
    utils.deploy_blueprint_resource(
        '{0}/rest-location.cloudify'.format(CONFIG_PATH),
        '/etc/nginx/conf.d/rest-location.cloudify')
    utils.deploy_blueprint_resource(
        '{0}/fileserver-location.cloudify'.format(CONFIG_PATH),
        '/etc/nginx/conf.d/fileserver-location.cloudify')
    utils.deploy_blueprint_resource(
        '{0}/ui-locations.cloudify'.format(CONFIG_PATH),
        '/etc/nginx/conf.d/ui-locations.cloudify')
    utils.deploy_blueprint_resource(
        '{0}/logs-conf.cloudify'.format(CONFIG_PATH),
        '/etc/nginx/conf.d/logs-conf.cloudify')

    utils.systemd.enable('nginx')


preconfigure_nginx()
