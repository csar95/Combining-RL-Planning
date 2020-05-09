import re
import random
import itertools
import speedUp

from fileIO import *


class Environment:

    domainPath = RESOURCES_FOLDER + "domain.pddl"
    problemPath = RESOURCES_FOLDER + "problem.pddl"

    def __init__(self):
        self.objIndependentPreds = set([])
        self.objDependentPreds = set([])
        self.immutablePreds = set([])

        self.types = {}
        self.functions = set([])
        self.actionsSchemas = {}

        # allActions is a dictionary of this type --> '(board p7 slow0-0 n1 n2 n8)': {'(lift-at slow0-0 n1)': 1, '(passenger-at p7 n1)': 1, '(passengers slow0-0 n2)': 1, '(next n2 n8)': 1, '(can-hold slow0-0 n8)': 1}
        self.allActions = {}
        # allFunctions is a dictionary of this type --> '(travel-slow n0 n1)': 6, '(travel-slow n0 n2)': 7, '(travel-slow n0 n3)': 8, '(travel-slow n0 n4)': 9, ..., '(total-cost)': 0
        self.allFunctions = {}

        self.state = {}

        # Reading domain file. Obtain the object dependent and independent properties
        colorPrint("Reading domain file...", MAGENTA)
        read_domain_file(self.domainPath, self)

        # Reading problem file. Detect the immutable properties and the type of each object
        colorPrint("\nReading problem file...", MAGENTA)
        self.init_state, self.goal_state, self.immutableProps = read_problem_file(self.problemPath, self)

        # Add the dependent predicates (non-immutable) to the state
        for pred in self.objDependentPreds:
            self.form_state_elements(pred)

        # Add the independent predicates to the state
        for pred in self.objIndependentPreds:
            self.state[f"({pred})"] = 0

        # This will be useful to form the Q-table (COLUMNS -> Actions in the env., ROWS -> States)
        colorPrint("\nFinding all possible actions in this environment...", MAGENTA)
        self.get_all_actions()

        # Initialize the state encoding as per the init block in the problem file
        self.reset()

        colorPrint("\nENVIRONMENT IS READY\n", MAGENTA)

    '''
    Adds all forms of the current predicate to the environment state
    '''
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

    '''
    Finds a set of all the possible actions that exist in this environment
    '''
    def get_all_actions(self):
        for action, definition in self.actionsSchemas.items():
            # Get all objects of each type of object in the action parameters
            poolOfObjects = self.get_pool_of_objects([param[1] for param in definition["parameters"]])

            # Add all combinations of the objects that the current action can have as parameters to the set containing
            # all possible actions in this environment
            for tup in list(itertools.product(*poolOfObjects)):
                params = ""
                for elem in tup: params += (" " + elem)

                newAction = {}

                # Match parameters in tup with the param. names in the current action
                translation = {}
                for idx, param in enumerate(definition["parameters"]):
                    translation[re.escape(param[0])] = tup[idx]

                pattern = re.compile("|".join(translation.keys()))

                # Get rewards of the current action with the parameters substituted
                newActionIsValid = True
                reward = {}
                for func, value in definition["reward"].items():
                    if value.isdigit():
                        v = int(value)
                    elif pattern.sub(lambda m: translation[re.escape(m.group(0))], value) in self.allFunctions:
                        v = int(self.allFunctions[pattern.sub(lambda m: translation[re.escape(m.group(0))], value)])
                    else:
                        newActionIsValid = False
                        break

                    reward[ pattern.sub(lambda m: translation[re.escape(m.group(0))], func) ] = v

                if not newActionIsValid:
                    continue
                else:
                    newAction["reward"] = reward

                # Get preconditions of the current action with the parameters substituted
                preconditions = {}
                for pred in definition["precondition"]:
                    targetValue = 0 if pred[0] == '!' else 1
                    preconditions[ pattern.sub(lambda m: translation[re.escape(m.group(0))], pred.lstrip('!')) ] = targetValue

                newAction["precondition"] = preconditions

                # Get effects of the current action with the parameters substituted
                effects = {}
                for eff in definition["effect"]:
                    targetValue = 0 if eff[0] == '!' else 1
                    effects[ pattern.sub(lambda m: translation[re.escape(m.group(0))], eff.lstrip('!')) ] = targetValue

                newAction["effect"] = effects

                self.allActions[f"({action}{params})"] = newAction

    '''
    Returns a list of lists where each list contains all the objects of each type in listOfObjectTypes
    '''
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

    '''
    Returns all legal actions from the current state
    '''
    def get_legal_actions(self):
        legalActions = set([])

        add = legalActions.add
        items = dict.items
        state = self.state
        immutableProps = self.immutableProps

        for action, definition in items(self.allActions):

            legal = True
            for pre, targetValue in items(definition["precondition"]):
                try:
                    if state[pre] != targetValue:
                        legal = False
                        break
                except KeyError:
                    if pre not in immutableProps:
                        legal = False
                        break

            if legal: add(action)

        return legalActions

    '''
    Returns whether the action preconditions are satisfied in the current state or not
    '''
    def is_legal(self, action):
        state = self.state
        immutableProps = self.immutableProps

        for pre, targetValue in self.allActions[action]["precondition"].items():
            try:
                if state[pre] != targetValue:
                    return False
            except KeyError:
                if pre not in immutableProps:
                    return False

        return True

    '''
    Returns whether the current state satisfies the goal state or not
    '''
    def is_done(self):
        for pred in self.goal_state:
            targetValue = 0 if pred[0] == '!' else 1
            if self.state[pred] != targetValue:
                return False

        return True

    '''
    Returns the reward obtained taking this action based on the increase keyword in the definition of the action
    '''
    def get_reward(self, action):
        reward = 0
        for rwd in self.allActions[action]["reward"].values():
            reward -= rwd
        return -1 if reward == 0 else reward  # Default reward (penalty) for taking a step: -1

# -------------------------------------------------------------------------------------------------------------------- #

    def reset(self):
        for prop in self.init_state:
            bit = '('
            for idx, x in enumerate(list(filter(lambda elem: elem != '', prop.strip().split(" ")))):
                bit += x if idx == 0 else ' ' + x
            bit += ')'
            self.state[bit] = 1

        return self.state

    def sample(self):
        return random.sample(speedUp.get_legal_actions(self.state, self.immutableProps, self.allActions), 1)[0]
        # return random.sample(self.get_legal_actions(), 1)[0]

    def step(self, action):
        for eff, value in self.allActions[action]["effect"].items():
            self.state[eff] = value

        return self.state, self.get_reward(action), self.is_done()
