class Index:
    def __init__(self, symbol: str):
        self._name = symbol
        self._states = [-1]
        self._result = -1

    def add_state(self, state: int):
        self._result = state
        self._states.append(state)

    @property
    def states(self):
        return self._states

    @property
    def name(self):
        return self._name
    
    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, result: int):
        self._result = result