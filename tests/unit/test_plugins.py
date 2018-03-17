# -*- coding: utf-8 -*-

from searx.testing import SearxTestCase
from searx import plugins
from mock import Mock


def get_search_mock(query, **kwargs):
    return Mock(search_query=Mock(query=query, **kwargs),
                result_container=Mock(answers=dict()))


class PluginStoreTest(SearxTestCase):

    def test_PluginStore_init(self):
        store = plugins.PluginStore()
        self.assertTrue(isinstance(store.plugins, list) and len(store.plugins) == 0)

    def test_PluginStore_register(self):
        store = plugins.PluginStore()
        testplugin = plugins.Plugin()
        store.register(testplugin)

        self.assertTrue(len(store.plugins) == 1)

    def test_PluginStore_call(self):
        store = plugins.PluginStore()
        testplugin = plugins.Plugin()
        store.register(testplugin)
        setattr(testplugin, 'asdf', Mock())
        request = Mock()
        store.call([], 'asdf', request, Mock())

        self.assertFalse(testplugin.asdf.called)

        store.call([testplugin], 'asdf', request, Mock())
        self.assertTrue(testplugin.asdf.called)


class SelfIPTest(SearxTestCase):

    def test_PluginStore_init(self):
        store = plugins.PluginStore()
        store.register(plugins.self_info)

        self.assertTrue(len(store.plugins) == 1)

        # IP test
        request = Mock(remote_addr='127.0.0.1')
        request.headers.getlist.return_value = []
        search = get_search_mock(query='ip', pageno=1)
        store.call(store.plugins, 'post_search', request, search)
        self.assertTrue('127.0.0.1' in search.result_container.answers["ip"]["answer"])

        search = get_search_mock(query='ip', pageno=2)
        store.call(store.plugins, 'post_search', request, search)
        self.assertFalse('ip' in search.result_container.answers)

        # User agent test
        request = Mock(user_agent='Mock')
        request.headers.getlist.return_value = []

        search = get_search_mock(query='user-agent', pageno=1)
        store.call(store.plugins, 'post_search', request, search)
        self.assertTrue('Mock' in search.result_container.answers["user-agent"]["answer"])

        search = get_search_mock(query='user-agent', pageno=2)
        store.call(store.plugins, 'post_search', request, search)
        self.assertFalse('user-agent' in search.result_container.answers)

        search = get_search_mock(query='user-agent', pageno=1)
        store.call(store.plugins, 'post_search', request, search)
        self.assertTrue('Mock' in search.result_container.answers["user-agent"]["answer"])

        search = get_search_mock(query='user-agent', pageno=2)
        store.call(store.plugins, 'post_search', request, search)
        self.assertFalse('user-agent' in search.result_container.answers)

        search = get_search_mock(query='What is my User-Agent?', pageno=1)
        store.call(store.plugins, 'post_search', request, search)
        self.assertTrue('Mock' in search.result_container.answers["user-agent"]["answer"])

        search = get_search_mock(query='What is my User-Agent?', pageno=2)
        store.call(store.plugins, 'post_search', request, search)
        self.assertFalse('user-agent' in search.result_container.answers)

class HashPluginTest(SearxTestCase):

    def test_PluginStore_init(self):
        store = plugins.PluginStore()
        store.register(plugins.hash_plugin)

        self.assertTrue(len(store.plugins) == 1)

        request = Mock(remote_addr='127.0.0.1')
        request.headers.getlist.return_value = []

        # MD5
        search = get_search_mock(query=b'md5 test', pageno=1)
        store.call(store.plugins, 'post_search', request, search)
        self.assertTrue('md5 hash function: 098f6bcd4621d373cade4e832627b4f6' in search.result_container.answers)

        search = get_search_mock(query=b'md5 test', pageno=2)
        store.call(store.plugins, 'post_search', request, search)
        self.assertFalse('md5 hash function: 098f6bcd4621d373cade4e832627b4f6' in search.result_container.answers)

        # SHA1
        search = get_search_mock(query=b'sha1 test', pageno=1)
        store.call(store.plugins, 'post_search', request, search)
        self.assertTrue('sha1 hash function: a94a8fe5ccb19ba61c4c0873d391e987982fbbd3' in search.result_container.answers)

        # SHA224
        search = get_search_mock(query=b'sha224 test', pageno=1)
        store.call(store.plugins, 'post_search', request, search)
        self.assertTrue('sha224 hash function: 90a3ed9e32b2aaf4c61c410eb925426119e1a9dc53d4286ade99a809' in search.result_container.answers)

        # SHA256
        search = get_search_mock(query=b'sha256 test', pageno=1)
        store.call(store.plugins, 'post_search', request, search)
        self.assertTrue('sha256 hash function: 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08' in search.result_container.answers)

        # SHA384
        search = get_search_mock(query=b'sha384 test', pageno=1)
        store.call(store.plugins, 'post_search', request, search)
        self.assertTrue('sha384 hash function: 768412320f7b0aa5812fce428dc4706b3cae50e02a64caa16a782249bfe8efc4b' \
          '7ef1ccb126255d196047dfedf17a0a9' in search.result_container.answers)

        # SHA512
        search = get_search_mock(query=b'sha512 test', pageno=1)
        store.call(store.plugins, 'post_search', request, search)
        self.assertTrue('sha512 hash function: ee26b0dd4af7e749aa1a8ee3c10ae9923f618980772e473f8819a5d4940e0db27a' \
'c185f8a0e1d5f84f88bc887fd67b143732c304cc5fa9ad8e6f57f50028a8ff' in search.result_container.answers)
