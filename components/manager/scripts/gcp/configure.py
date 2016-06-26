########
# Copyright (c) 2015 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.
import fabric.api
import os

from cloudify import ctx
from gcp.compute import constants


def copy_ssh_keys():
    ctx.source.instance.runtime_properties[constants.SSH_KEYS] = \
        ctx.target.instance.runtime_properties[constants.SSH_KEYS]
    fabric.api.sudo('mkdir -p /root/.ssh')


def configure_manager(manager_plugins_path=constants.MANAGER_PLUGIN_FILES, agents_user=None, agents_public_key=None, gcp_config=None):
    fabric.api.sudo('sed -i \'s/enforcing/disabled/g\' /etc/selinux/config /etc/selinux/config')

    manager_plugins_path = os.path.dirname(manager_plugins_path or get_remote_config_path())

    fabric.api.sudo('mkdir -p /{manager_config_path}'
                    .format(manager_config_path=manager_plugins_path))
    fabric.api.sudo('rm -f /{manager_config_path}/cloudify_agent'
                    .format(manager_config_path=manager_plugins_path))
    fabric.api.sudo('rm -f /{manager_config_path}/cloudify_agent.pub'
                    .format(manager_config_path=manager_plugins_path))
    fabric.api.sudo('ssh-keygen -t rsa -f /{manager_config_path}/cloudify_agent -q -P ""'
                    .format(manager_config_path=manager_plugins_path))

    resources = _construct_resources(gcp_config,
                                     agents_user,
                                     agents_public_key)

    ctx.instance.runtime_properties['provider_context'] = {
        'resources': resources
    }


def _construct_resources(gcp_config, agents_user, agents_public_key):
    node_instances = ctx._endpoint.storage.get_node_instances()
    resources = {}
    for node_instance in node_instances:
        if node_instance.node_id in constants.SECURITY_GROUPS:
            run_props = node_instance.runtime_properties
            resources[node_instance.node_id] = {
                'id': run_props[constants.NAME],
                constants.TARGET_TAGS: run_props[constants.TARGET_TAGS],
                constants.SOURCE_TAGS: run_props[constants.SOURCE_TAGS]
            }

    resources[constants.GCP_CONFIG] = {
        constants.AUTH: gcp_config[constants.AUTH],
        constants.PROJECT: gcp_config[constants.PROJECT],
        constants.ZONE: gcp_config[constants.ZONE],
        constants.NETWORK: gcp_config[constants.NETWORK],
    }

    resources['cloudify_agent'] = {
        'user': agents_user,
    }

    if agents_public_key:
        with open(agents_public_key, "r") as key_file:
            resources['cloudify_agent'].update({'public_key': key_file.read()})

    return resources


def get_remote_config_path():
    return constants.GCP_DEFAULT_CONFIG_PATH
