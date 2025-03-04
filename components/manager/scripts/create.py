#!/usr/bin/env python

import os
from os.path import join, dirname

from cloudify import ctx

ctx.download_resource(
    join('components', 'utils.py'),
    join(dirname(__file__), 'utils.py'))
import utils  # NOQA


def deploy_manager_sources():
    """Deploys all manager sources from a single archive.
    """
    archive_path = ctx.node.properties['manager_resources_package']
    archive_checksum_path = \
        ctx.node.properties['manager_resources_package_checksum_file']
    skip_checksum_validation = ctx.node.properties['skip_checksum_validation']
    if archive_path:
        sources_agents_path = os.path.join(
            utils.CLOUDIFY_SOURCES_PATH, 'agents')
        agent_archives_path = utils.AGENT_ARCHIVES_PATH
        utils.mkdir(agent_archives_path)
        # this will leave this several hundreds of MBs archive on the
        # manager. should find a way to clean it after all operations
        # were completed and bootstrap succeeded as it is not longer
        # necessary
        resources_archive_path = \
            utils.download_cloudify_resource(archive_path)
        # This would ideally go under utils.download_cloudify_resource but as
        # of now, we'll only be validating the manager resources package.

        if not skip_checksum_validation:
            skip_if_failed = False
            if not archive_checksum_path:
                skip_if_failed = True
                archive_checksum_path = archive_path + '.md5'
            resources_archive_md5_path = \
                utils.download_cloudify_resource(archive_checksum_path)
            if not utils.validate_md5_checksum(resources_archive_path,
                                               resources_archive_md5_path):
                    if skip_if_failed:
                        ctx.logger.warn('Checksum validation failed. '
                                        'Continuing as no checksum file was '
                                        'explicitly provided.')
                    else:
                        utils.error_exit(
                            'Failed to validate checksum for {0}'.format(
                                resources_archive_path))
            else:
                ctx.logger.info('Resources Package downloaded successfully...')
        else:
            ctx.logger.info(
                'Skipping resources package checksum validation...')

        utils.untar(
            resources_archive_path,
            utils.CLOUDIFY_SOURCES_PATH,
            skip_old_files=True)

        def splitext(filename):
            # not using os.path.splitext as it would return .gz instead of
            # .tar.gz
            if filename.endswith('.tar.gz'):
                return '.tar.gz'
            elif filename.endswith('.exe'):
                return '.exe'
            else:
                utils.exit_error(
                    'Unknown agent format for {0}. '
                    'Must be either tar.gz or exe'.format(filename))

        def normalize_agent_name(filename):
            # this returns the normalized name of an agent upon which our agent
            # installer retrieves agent packages for installation.
            # e.g. Ubuntu-trusty-agent_3.4.0-m3-b392.tar.gz returns
            # ubuntu-trusty-agent
            return filename.split('_', 1)[0].lower()

        for agent_file in os.listdir(sources_agents_path):

            agent_id = normalize_agent_name(agent_file)
            agent_extension = splitext(agent_file)
            utils.move(
                os.path.join(sources_agents_path, agent_file),
                os.path.join(agent_archives_path, agent_id + agent_extension))


deploy_manager_sources()
