#!/usr/bin/env python

from os.path import join, dirname

from cloudify import ctx

ctx.download_resource(
    join('components', 'utils.py'),
    join(dirname(__file__), 'utils.py'))
import utils  # NOQA


CONFIG_PATH = 'components/riemann/config'


def install_riemann():
    langohr_source_url = ctx.node.properties['langohr_jar_source_url']
    daemonize_source_url = ctx.node.properties['daemonize_rpm_source_url']
    riemann_source_url = ctx.node.properties['riemann_rpm_source_url']
    # Needed for Riemann's config
    cloudify_resources_url = ctx.node.properties['cloudify_resources_url']
    rabbitmq_username = ctx.node.properties['rabbitmq_username']
    rabbitmq_password = ctx.node.properties['rabbitmq_password']

    riemann_config_path = '/etc/riemann'
    riemann_log_path = '/var/log/cloudify/riemann'
    langohr_home = '/opt/lib'
    extra_classpath = '{0}/langohr.jar'.format(langohr_home)

    # Confirm username and password have been supplied for broker before
    # continuing.
    # Components other than logstash and riemann have this handled in code.
    # Note that these are not directly used in this script, but are used by the
    # deployed resources, hence the check here.
    if not rabbitmq_username or not rabbitmq_password:
        utils.error_exit(
            'Both rabbitmq_username and rabbitmq_password must be supplied '
            'and at least 1 character long in the manager blueprint inputs.')

    ctx.instance.runtime_properties['rabbitmq_endpoint_ip'] = \
        utils.get_rabbitmq_endpoint_ip()

    ctx.logger.info('Installing Riemann...')
    utils.set_selinux_permissive()

    utils.copy_notice('riemann')
    utils.mkdir(riemann_log_path)
    utils.mkdir(langohr_home)
    utils.mkdir(riemann_config_path)
    utils.mkdir('{0}/conf.d'.format(riemann_config_path))

    langohr = utils.download_cloudify_resource(langohr_source_url)
    utils.sudo(['cp', langohr, extra_classpath])
    ctx.logger.info('Applying Langohr permissions...')
    utils.sudo(['chmod', '644', extra_classpath])
    utils.yum_install(daemonize_source_url)
    utils.yum_install(riemann_source_url)

    utils.logrotate('riemann')

    ctx.logger.info('Downloading cloudify-manager Repository...')
    manager_repo = utils.download_cloudify_resource(cloudify_resources_url)
    ctx.logger.info('Extracting Manager Repository...')
    utils.untar(manager_repo, '/tmp')
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

install_riemann()
