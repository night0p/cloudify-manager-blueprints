import os
import sys
import unittest
import tempfile
import json
from mock import patch
from cloudify.mocks import MockCloudifyContext

sys.path.append(os.path.join(os.path.dirname(__file__),
                             '../../components'))
import utils


TEST_SERVICE_NAME = 'es'


def mock_install_ctx():
    install_node_props = {'es_rpm_source_url': 'http://www.mock.com/es.tar.gz',
                          'test_property': 'test'}
    return _create_mock_context(install_node_props)


def _create_mock_context(install_node_props):
    mock_node_props = MockNodeProperties(properties=install_node_props)
    return MockCloudifyContext(node_id='es_node',
                               node_name=TEST_SERVICE_NAME,
                               properties=mock_node_props)


def mock_upgrade_ctx(use_existing_on_upgrade=False):
    upgrade_node_props = \
        {'es_rpm_source_url': 'http://www.mock.com/new-es.tar.gz',
         'use_existing_on_upgrade': use_existing_on_upgrade,
         'test_property': 'new_value',
         'new_property': 'value'}
    return _create_mock_context(upgrade_node_props)


class MockNodeProperties(dict):

    def __init__(self, properties):
        self.update(properties)

    def get_all(self):
        return self


@patch('utils.ctx', mock_install_ctx())
@patch('utils.is_upgrade', lambda: False)
def create_install_file(service_name):
    return _create_ctx_props_file(service_name)


@patch('utils.is_upgrade', lambda: True)
def create_upgrade_file(service_name, use_existing=False):
    if use_existing:
        create_install_file(service_name)
    return _create_ctx_props_file(service_name)


@patch('utils.CtxPropertyFactory.PROPERTIES_PATH', tempfile.mkdtemp())
def _create_ctx_props_file(service_name):
    factory = utils.CtxPropertyFactory()
    props_file_path = factory._get_props_file_path(service_name)
    ctx_properties = factory.create(service_name)
    return ctx_properties, props_file_path


class TestUpgrade(unittest.TestCase):

    def test_ctx_prop_install_file_create(self):
        ctx_props, props_file_path = create_install_file(TEST_SERVICE_NAME)
        self.assertTrue(os.path.isfile(props_file_path))
        with open(props_file_path, 'r') as f:
            file_props = json.load(f)
        self.assertDictEqual(file_props, ctx_props)

    @patch('utils.ctx', mock_upgrade_ctx())
    def test_ctx_prop_upgrade_file_create(self):
        ctx_props, upgrade_props_path = create_upgrade_file(TEST_SERVICE_NAME)
        self.assertTrue(os.path.isfile(upgrade_props_path))
        with open(upgrade_props_path, 'r') as f:
            file_props = json.load(f)
        self.assertDictEqual(file_props, ctx_props)

    @patch('utils.ctx', mock_upgrade_ctx(use_existing_on_upgrade=True))
    def test_use_existing_on_upgrade(self):
        ctx_props, _ = create_upgrade_file(TEST_SERVICE_NAME,
                                           use_existing=True)
        # Assert same value used for upgrade
        self.assertEqual(ctx_props['test_property'], 'test')
        # Assert new property merged with old properties
        self.assertEqual(ctx_props['new_property'], 'value')
        self.assert_rpm_url_overridden(ctx_props)

    @patch('utils.ctx', mock_upgrade_ctx())
    def test_new_props_on_upgrade(self):
        ctx_props, _ = create_upgrade_file(TEST_SERVICE_NAME)
        self.assertEqual(ctx_props['test_property'], 'new_value')
        self.assert_rpm_url_overridden(ctx_props)

    def assert_rpm_url_overridden(self, ctx_properties):
        self.assertEqual(ctx_properties['es_rpm_source_url'],
                         'http://www.mock.com/new-es.tar.gz')
