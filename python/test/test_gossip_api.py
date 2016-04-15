import unittest
import gossip

class TestGossipApi(unittest.TestCase):
    def test_reconcile_creates_unknown_keys(self):
        state = gossip.initialize('localhost')
        state.receive('remotehost', { 'foo': ('foo', 1) })
        self.assertFalse('foo' in state)
        state.reconcile()
        self.assertTrue('foo' in state)

    def test_reconcile_updates_key(self):
        state = gossip.initialize('localhost', {'foo': (False, 1)})
        state.receive('remotehost', { 'foo': (True, 2) })
        self.assertFalse(state['foo'])
        state.reconcile()
        self.assertTrue(state['foo'])

    def test_initial_state(self):
        state = gossip.initialize('localhost', {'foo': (True, 1)})
        self.assertTrue('foo' in state)
