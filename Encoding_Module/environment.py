import itertools


class Environment:

    def __init__(self):
        self.types = {}
        self.actionsSchemas = {}
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

        # Create a list of lists where each list contains all the objects of one type

        pool_of_objects = []
        for typ in objectTypes:
            for key, value in self.types.items():
                if key == typ and isinstance(value, list):  # Type doesn't have subtypes
                    pool_of_objects.append(value)
                    break
                elif key == typ:  # Add all objects of all subtypes of the matching type
                    objs = []
                    for k, v in value.items():
                        objs += v
                    pool_of_objects.append(objs)
                    break
                if isinstance(value, dict):  # Search typ within the nested dictionary
                    for k, v in value.items():
                        if typ == k:
                            pool_of_objects.append(v)
                            break

        # Add all combination of the objects that a predicate can have to the state dictionary (state encoding)

        for tup in list(itertools.product(*pool_of_objects)):
            objs = ""
            for elem in tup: objs += (" " + elem)
            self.state[f"({name}{objs})"] = 0  # Add each term to the dictionary initialized to 0

    def get_available_actions(self, ):
        pass
