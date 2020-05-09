cpdef list get_legal_actions(dict state, frozenset immutableProps, dict allActions):
    cdef list legalActions = []
    cdef int legal

    append = legalActions.append
    items = dict.items

    for action, definition in items(allActions):

        legal = 0

        for pre, targetValue in items(definition["precondition"]):
            try:
                if state[pre] != targetValue:
                    legal = 1
                    break
            except KeyError:
                if pre not in immutableProps:
                    legal = 1
                    break

        if legal == 0: append(action)

    return legalActions
