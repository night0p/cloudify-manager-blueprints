from cloudify import ctx
from cloudify.state import ctx_parameters as inputs


# set private ip according to the host ip
private_ip = ctx.target.instance.host_ip
ctx.logger.info('Setting manager_configuration private ip to: {0}'.
                format(private_ip))
ctx.source.instance.runtime_properties['private_ip'] = private_ip

public_ip = inputs['public_ip']
ctx.logger.info('Setting manager_configuration public ip to: {0}'.
                format(public_ip))
ctx.source.instance.runtime_properties['public_ip'] = public_ip

# set the internal manager host according to the private ip
# (public ip / private ip)
ctx.source.instance.runtime_properties['internal_manager_host'] = private_ip
ctx.logger.info('internal_manager_host set to: {0}'.format(
    ctx.source.instance.runtime_properties['internal_manager_host']))

# set the internal REST host according to the REST internal identifier
# (public ip / private ip)
rest_host_internal_identifier = inputs['rest_host_internal_identifier']
ctx.logger.info('rest_host_internal_identifier is: {0}'.format(
    rest_host_internal_identifier))
if rest_host_internal_identifier == 'private_ip':
    ctx.source.instance.runtime_properties['internal_rest_host'] = private_ip
elif rest_host_internal_identifier == 'public_ip':
    ctx.source.instance.runtime_properties['internal_rest_host'] = public_ip
else:
    # how to raise exception here?
    ctx.logger.info('invalid rest_host_internal_identifier: {0}'.format(
        rest_host_internal_identifier))
ctx.logger.info('internal_rest_host set to: {0}'.format(
    ctx.source.instance.runtime_properties['internal_rest_host']))

# set the external REST host according to the REST external identifier
# (public ip / private ip)
rest_host_external_identifier = inputs['rest_host_external_identifier']
ctx.logger.info('rest_host_external_identifier is: {0}'.format(
    rest_host_external_identifier))
if rest_host_external_identifier == 'private_ip':
    ctx.source.instance.runtime_properties['external_rest_host'] = private_ip
elif rest_host_external_identifier == 'public_ip':
    ctx.source.instance.runtime_properties['external_rest_host'] = public_ip
else:
    # how to raise exception here?
    ctx.logger.info('invalid rest_host_external_identifier: {0}'.format(
        rest_host_external_identifier))
ctx.logger.info('external_rest_host set to: {0}'.format(
    ctx.source.instance.runtime_properties['external_rest_host']))
