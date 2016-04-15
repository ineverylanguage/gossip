class WorldState:
    def __contains__(self, key):
        return False

class ParticipantMap:
    def __init__(self, key, state):
        self._my_name = key
        self._state = {key: WorldState()}
        self._max_version = -1

    def receive(self, key, state):
        pass

    def __contains__(self, key):
        return key in self._state[self._my_name]

    def reconcile(self):
        pass


def initialize_with_state(my_key, state):
    return ParticipantMap(my_key, state)

__all__ = ['initialize_with_state']