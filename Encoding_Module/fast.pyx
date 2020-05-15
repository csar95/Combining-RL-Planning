cimport numpy as np


cpdef get_random_legal_action(np.ndarray state, dict allActions, np.ndarray allActionsKeys):

    cdef int legal

    items = dict.items

    for action in allActionsKeys:

        legal = 0

        for pre, targetValue in items(allActions[action]["precondition"]):
            if state[pre] != targetValue:
                legal = 1
                break

        if legal == 0:
            return action

cpdef get_legal_actions(np.ndarray state, dict allActions, np.ndarray allActionsKeys):

    legalActions = []

    cdef int legal

    append = legalActions.append
    items = dict.items

    for idx, action in enumerate(allActionsKeys):

        legal = 0

        for pre, targetValue in items(allActions[action]["precondition"]):
            if state[pre] != targetValue:
                legal = 1
                break

        if legal == 0:
            append(idx)

    return legalActions
