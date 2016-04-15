import unittest
import gossip

class TestGossipApi(unittest.TestCase):
    def test_reconcile_creates_unknown_keys(self):
        state = gossip.initialize_with_state('localhost', {})
        state.receive('remotehost', { 'value': 'foo', 'version': 1 })
        self.assertFalse('foo' in state)
        state.reconcile()
        self.assertTrue('foo' in state)

    def test_reconcile_updates_key(self):
        pass