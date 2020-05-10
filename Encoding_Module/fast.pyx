cimport numpy as np


cpdef get_random_legal_action(dict state, frozenset immutableProps, dict allActions, np.ndarray allActionKeys):

    cdef int legal

    items = dict.items

    for action in allActionKeys:

        legal = 0

        for pre, targetValue in items(allActions[action]["precondition"]):
            try:
                if state[pre] != targetValue:
                    legal = 1
                    break
            except KeyError:
                if pre not in immutableProps:
                    legal = 1
                    break

        if legal == 0: return action
