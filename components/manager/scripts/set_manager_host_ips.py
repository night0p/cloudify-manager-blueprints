from cloudify import ctx
import os

# TODO: ask NirC if this is ok
ctx.logger.info('Setting Private Manager IP Runtime Property.')
manager_private_ip = ctx.source.instance.host_ip
ctx.logger.info('Manager Private IP is: {0}'.format(manager_private_ip))

ctx.logger.info('Setting Public Manager IP Runtime Property.')
for env_var in os.environ.keys():
    print '***** DEBUG env var: {0}'.format(env_var)

manager_ip = os.environ['public_ip']

ctx.logger.info('Manager Public IP is: {0}'.format(manager_ip))
ctx.source.instance.runtime_properties['public_ip'] = manager_ip

manager_public_ip = ctx.source.instance.runtime_properties['public_ip']
ctx.logger.info('Manager public IP is: {0}'.format(manager_public_ip))
# ctx.target.instance.runtime_properties['manager_host_ip'] = manager_private_ip
ctx.target.instance.runtime_properties['manager_host_ip'] = manager_public_ip