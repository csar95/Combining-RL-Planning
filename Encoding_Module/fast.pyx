cimport numpy as np


cpdef get_random_legal_action(np.ndarray state, dict allActions, np.ndarray allActionKeys):

    cdef int legal

    items = dict.items

    for action in allActionKeys:

        legal = 0

        for pre, targetValue in items(allActions[action]["precondition"]):
            if state[pre] != targetValue:
                legal = 1
                break

        if legal == 0: return action

cpdef get_legal_actions(np.ndarray state, dict allActions, np.ndarray allActionKeys):

    legalActions = set([])

    cdef int legal

    add = legalActions.add
    items = dict.items

    for action in allActionKeys:

        legal = 0

        for pre, targetValue in items(allActions[action]["precondition"]):
            if state[pre] != targetValue:
                legal = 1
                break

        if legal == 0:
            add(action)

    return legalActions
