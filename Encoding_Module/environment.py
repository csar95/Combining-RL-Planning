import re
import itertools


class Environment:

    def __init__(self):
        self.types = {}
        self.actionsSchemas = {}

        # allActions is a dictionary of this type --> '(board p7 slow0-0 n1 n2 n8)': {'(lift-at slow0-0 n1)': 1, '(passenger-at p7 n1)': 1, '(passengers slow0-0 n2)': 1, '(next n2 n8)': 1, '(can-hold slow0-0 n8)': 1}
        self.allActions = {}

        self.immutableProps = set([])
        self.state = {}

    def initialize_state(self, objDependentPreds, objIndependentPreds, init_state):
        # Add the dependent predicates (non-immutable) to the state
        for pred in objDependentPreds:
            self.form_state_elements(pred)

        # Add the independent predicates to the state
        for pred in objIndependentPreds:
            self.state[f"({pred})"] = 0

        for prop in init_state:
            bit = '('
            for idx, x in enumerate(list(filter(lambda elem: elem != '', prop.strip().split(" ")))):
                bit += x if idx == 0 else ' ' + x
            bit += ')'
            self.state[bit] = 1

    # Adds all forms of the current predicate to the environment state
    def form_state_elements(self, predicate):
        predicate = list(filter(lambda elm: elm != '', predicate.split(" ")))
        name = predicate[0]

        # Create list with the type of each object in the predicate

        objectTypes = []
        for idx, elem in enumerate(predicate):
            if "?" in elem:  # Elem is an object --> Check the type
                for i, x in enumerate(predicate[(idx + 1):]):
                    if x == "-":
                        objectTypes.append(predicate[idx + 1 + (i + 1)])
                        break

        # Get all objects of each type of object in the predicate parameters
        poolOfObjects = self.get_pool_of_objects(objectTypes)

        # Add all combinations of the objects that a predicate can have to the state dictionary (state encoding)
        for tup in list(itertools.product(*poolOfObjects)):
            objs = ""
            for elem in tup: objs += (" " + elem)
            self.state[f"({name}{objs})"] = 0  # Add each term to the dictionary initialized to 0

    # Return a set of all the possible actions that exist in this environment
    def get_all_actions(self):
        for action, definition in self.actionsSchemas.items():
            # Get all objects of each type of object in the action parameters
            poolOfObjects = self.get_pool_of_objects([param[1] for param in definition["parameters"]])

            # Add all combinations of the objects that the current action can have as parameters to the set containing
            # all possible actions in this environment
            for tup in list(itertools.product(*poolOfObjects)):
                params = ""
                for elem in tup: params += (" " + elem)

                # Match parameters in tup with the param. names in the current action
                translation = {}
                for idx, param in enumerate(definition["parameters"]):
                    translation[re.escape(param[0])] = tup[idx]

                # Get preconditions of the current action with the parameters substituted
                preconditions = {}
                for pred in definition["precondition"]:
                    targetValue = 0 if pred[0] == '!' else 1

                    pattern = re.compile("|".join(translation.keys()))
                    preconditions[ pattern.sub(lambda m: translation[re.escape(m.group(0))], pred) ] = targetValue

                self.allActions[f"({action}{params})"] = preconditions

    # Returns a list of lists where each list contains all the objects of each type in listOfObjectTypes
    def get_pool_of_objects(self, listOfObjectTypes):
        poolOfObjects = []

        for typ in listOfObjectTypes:
            for key, value in self.types.items():

                if not value: continue

                # Type doesn't have subtypes
                elif key == typ and isinstance(value, list):
                    poolOfObjects.append(value)
                    break

                # Add all objects of all subtypes of the matching type
                elif key == typ:
                    objs = []
                    for k, v in value.items():
                        objs += v
                    poolOfObjects.append(objs)
                    break

                # Search typ within the nested dictionary
                if isinstance(value, dict):
                    for k, v in value.items():
                        if not v: continue
                        elif typ == k:
                            poolOfObjects.append(v)
                            break

        return poolOfObjects

    def get_legal_actions(self):
        return set(filter(self.is_legal, self.allActions.keys()))

    # Return True if the action preconditions are satisfied in the current state
    def is_legal(self, action):
        for pre, targetValue in self.allActions[action].items():

            if pre not in self.state and pre not in self.immutableProps:
                return False
            if pre in self.state and self.state[pre] != targetValue:
                return False

        return True
