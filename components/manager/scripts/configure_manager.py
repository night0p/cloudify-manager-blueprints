from cloudify import ctx
from cloudify.state import ctx_parameters as inputs
import socket


def get_hostname():
    return socket.gethostname()


ctx.logger.info('Reading rest_host_for_internal_requests Property...')
rest_host_for_internal_requests = ctx.node.properties.rest_host_for_internal_requests
ctx.logger.info('rest_host_for_internal_requests is: {0}'.format(rest_host_for_internal_requests))

ctx.logger.info('Reading rest_host_for_external_requests Property...')
rest_host_for_external_requests = ctx.node.properties.rest_host_for_external_requests
ctx.logger.info('rest_host_for_external_requests is: {0}'.format(rest_host_for_external_requests))

ctx.logger.info('got hostname: {0}'.format(get_hostname()))

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