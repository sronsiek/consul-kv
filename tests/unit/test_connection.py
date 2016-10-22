from consul_kv import Connection
from consul_kv.api import DEFAULT_KV_ENDPOINT
from tests.testcase import TestCase


class TestConnection(TestCase):
    def setUp(self):
        self.put_kv = self.set_up_patch('consul_kv.put_kv')
        self.put_kv_txn = self.set_up_patch('consul_kv.put_kv_txn')
        self.get_kv = self.set_up_patch('consul_kv.get_kv')
        self.delete_kv = self.set_up_patch('consul_kv.delete_kv')
        self.kv_endpoint = 'http://some_host:8500/v1/kv/'
        self.txn_endpoint = 'http://some_host:8500/v1/txn/'
        self.conn = Connection(endpoint=self.kv_endpoint)
        self.mapping = {
            'some/key/1': 'some_value_1',
            'some/key/2': 'some_value_2'
        }

    def test_connection_has_correct_kv_endpoint(self):
        self.assertEqual(self.conn.kv_endpoint, self.kv_endpoint)

    def test_connection_uses_default_kv_endpoint_if_none_specified(self):
        conn = Connection()

        self.assertEqual(conn.kv_endpoint, DEFAULT_KV_ENDPOINT)

    def test_connection_put_calls_put_kv_with_kv_endpoint(self):
        self.conn.put('key1', 'value1')

        self.put_kv.assert_called_once_with(
            'key1', 'value1', endpoint=self.kv_endpoint
        )

    def test_connection_put_mapping_calls_put_kv_txn_with_txn_endpoint(self):
        self.conn.put_mapping(self.mapping)

        self.put_kv_txn.assert_called_once_with(
            self.mapping, endpoint=self.txn_endpoint
        )

    def test_connection_get_calls_get_kv_with_kv_endpoint(self):
        self.conn.get('key1')

        self.get_kv.assert_called_once_with(
            k='key1', recurse=False, endpoint=self.kv_endpoint
        )

    def test_connection_get_recurses_if_specified(self):
        self.conn.get('key2', recurse=True)

        self.get_kv.assert_called_once_with(
            k='key2', recurse=True, endpoint=self.kv_endpoint
        )

    def test_connection_delete_calls_delete_kv_with_kv_endpoint(self):
        self.conn.delete('key1')

        self.delete_kv.assert_called_once_with(
            k='key1', recurse=False, endpoint=self.kv_endpoint
        )

    def test_connection_delete_recurses_if_specified(self):
        self.conn.delete('key2', recurse=True)

        self.delete_kv.assert_called_once_with(
            k='key2', recurse=True, endpoint=self.kv_endpoint
        )