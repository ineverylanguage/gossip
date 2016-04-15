class VersionedObject(object):
    def __init__(self, value, version):
        self.value = value
        self.version = version

    def __cmp__(self, other):
        return cmp(self.version, other.version)

    def __repr__(self):
        return "<{}:v{}>".format(self.value, self.version)

NULL_VERSION = VersionedObject(None, -1)

def versioned_or_tuple(x):
    if hasattr(x, 'value'):
        return (x.value, x.version)
    else:
        return x

class WorldState(object):
    def __init__(self, initial_state=None):
        self._max_version = -1
        self._values = {}
        if initial_state:
            self._values = { k: VersionedObject(*versioned_or_tuple(v)) for k,v in initial_state.items() }
            self._max_version = max((x.version for x in self._values.values()))

    def __getitem__(self, key):
        return self._values[key]

    def __setitem__(self, key, value):
        old_version = self._max_version
        self._max_version += 1
        try:
            self._values[key] = VersionedObject(value, self._max_version)
        except:
            self._max_version = old_version

    def __contains__(self, key):
        return key in self._values

    def items(self):
        return self._values.items()

    def get(self, key, default_=None):
        return self._values.get(key, default_)

def _pick_participant(lhs, rhs):
    if lhs > rhs:
        return lhs
    else:
        return rhs

class ParticipantMap(object):
    def __init__(self, key, state=None):
        self._my_name = key
        my_state = WorldState(state)
        self._state = {self._my_name: my_state}

    def receive(self, key, state):
        if key == self._my_name:
            raise RuntimeError('trying to receive update for self, which is wrong')

        self._state[key] = WorldState(state)


    def __contains__(self, key):
        return key in self._state[self._my_name]


    @property
    def me(self):
        return self._state[self._my_name]

    def reconcile(self):
        my_version = self.me._max_version
        updated_participants = (k for k,v in self._state.items() if v._max_version > my_version)
        new_state = {}
        for participant_key in updated_participants:
            participant_map = self._state[participant_key]
            for k,v in participant_map.items():
                if k in self.me:
                    new_state[k] = _pick_participant(self.me[k], v)
                else:
                    new_state[k] = v
        self._state[self._my_name] = WorldState(new_state)

    def __getitem__(self, key):
        global NULL_VERSION
        return self.me.get(key, NULL_VERSION).value

def initialize(my_key, state=None):
    return ParticipantMap(my_key, state)

__all__ = ['initialize_with_state']