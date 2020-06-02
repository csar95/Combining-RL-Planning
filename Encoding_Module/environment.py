import re
import numpy as np
import itertools
import fast
from copy import deepcopy

from fileIO import *
from hyperparameters import *


class Environment:

    domainPath = RESOURCES_FOLDER + "transport.pddl"
    problemPath = RESOURCES_FOLDER + "transport_p1.pddl"

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

        self.stateTerms = {}

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
            self.stateTerms[f"({pred})"] = len(self.stateTerms)

        self.state = np.zeros(len(self.stateTerms), dtype=np.int64)

        # This will be useful to form the Q-table (COLUMNS -> Actions in the env., ROWS -> States)
        colorPrint("\nFinding all possible actions in this environment...", MAGENTA)
        self.get_all_actions()

        self.allActionsKeys = np.array(list(self.allActions.keys()))

        self.legalActionsPerState = {}

        self.allRewards = np.sort( self.get_all_rewards() )

        # Initialize the state encoding as per the init block in the problem file
        self.reset()

        colorPrint("\nEnvironment is ready", MAGENTA)

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
            self.stateTerms[f"({name}{objs})"] = len(self.stateTerms)  # Add each term to the dictionary with its position in the array

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
                newAction = {}
                newActionIsValid = True

                if len(tup) != len(definition["parameters"]): continue

                # Match parameters in tup with the param. names in the current action
                translation = {}
                for idx, param in enumerate(definition["parameters"]):
                    translation[re.escape(param[0])] = tup[idx]

                pattern = re.compile("|".join(translation.keys()))

                # Get rewards of the current action with the parameters substituted
                reward = {}
                for func, value in definition["reward"].items():
                    funcKey = pattern.sub(lambda m: translation[re.escape(m.group(0))], func)

                    if funcKey not in self.allFunctions:
                        newActionIsValid = False  # E.g., (increase (func) (value)) Func is not found in self.allFunctions
                        break
                    elif value.isdigit():
                        v = int(value)
                    elif pattern.sub(lambda m: translation[re.escape(m.group(0))], value) in self.allFunctions:
                        v = int(self.allFunctions[pattern.sub(lambda m: translation[re.escape(m.group(0))], value)])
                    else:
                        newActionIsValid = False  # E.g., (increase (func) (value)) Value is not found in self.allFunctions
                        break

                    reward[funcKey] = v

                if not newActionIsValid:
                    continue
                else:
                    newAction["reward"] = reward

                # Get preconditions of the current action with the parameters substituted
                preconditions = {}
                for pred in definition["precondition"]:
                    targetValue = 0 if pred[0] == '!' else 1

                    precondition = pattern.sub(lambda m: translation[re.escape(m.group(0))], pred.lstrip('!'))
                    if precondition not in self.stateTerms.keys() and\
                            ((targetValue == 1 and precondition not in self.immutableProps) or\
                            (targetValue == 0 and precondition in self.immutableProps)):
                        # The precondition predicate of the current action is:
                        # - Not present in the state keys AND
                        # - It is supposed to be True but is not in the immutableProps set OR It is supposed to be False but is in the immutableProps set
                        newActionIsValid = False
                        break

                    # I don't need to include the immutable predicates to check if an action is legal. I'm already checking those thing here
                    if precondition in self.stateTerms.keys():
                        preconditions[ self.stateTerms[precondition] ] = targetValue  # Save the position of the predicate

                if not newActionIsValid:
                    continue
                else:
                    newAction["precondition"] = preconditions

                # Get effects of the current action with the parameters substituted
                effects = {}
                for eff in definition["effect"]:
                    targetValue = 0 if eff[0] == '!' else 1

                    effect = pattern.sub(lambda m: translation[re.escape(m.group(0))], eff.lstrip('!'))
                    if effect not in self.stateTerms.keys():
                        # The effect predicate of the current action is not present in the state keys
                        # The immutableProps are not taken into account here because they cannot appear in any action effects
                        newActionIsValid = False
                        break

                    effects[ self.stateTerms[effect] ] = targetValue

                if not newActionIsValid:
                    continue
                else:
                    newAction["effect"] = effects

                # At this point newActionIsValid is True, otherwise it would have continued to the next combination of objects
                params = ""
                for elem in tup: params += (" " + elem)

                self.allActions[f"({action}{params})"] = newAction

    '''
    Saves in an array all the possible rewards that the agent can get in this domain 
    '''
    def get_all_rewards(self):
        allRewards = np.array([])
        for action in self.allActions.values():
            for rwd in action['reward'].values():
                if rwd not in allRewards:
                    allRewards = np.append(allRewards, rwd)

        return allRewards

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
    Returns an array of all legal actions from the current state
    '''
    def get_legal_actions(self, state):
        try:
            return self.legalActionsPerState[tuple(state)]
        except KeyError:
            self.legalActionsPerState[tuple(state)] = np.array(fast.get_legal_actions(state, self.allActions, self.allActionsKeys))
            return self.legalActionsPerState[tuple(state)]

    '''
    Returns whether the current state satisfies the goal state or not
    '''
    def check_proximity_to_goal(self):
        pendingPreds = len(self.goal_state)

        for pred in self.goal_state:
            targetValue = 0 if pred[0] == '!' else 1
            if self.state[ self.stateTerms[pred] ] == targetValue:
                pendingPreds -= 1

        return pendingPreds

    '''
    Takes the action string
    Returns the reward obtained after taking that action based on the increase keyword in the definition of the action
    '''
    def get_reward(self, action, gain):
        reward = -1
        for rwd in self.allActions[action]["reward"].values():
            # reward -= rwd/MAX_REWARD
            reward -= rwd

        return reward + (gain * (GOAL_REWARD / len(self.goal_state)))
        # return reward + (gain * 15)
        # return -1 + (gain * 10)

# -------------------------------------------------------------------------------------------------------------------- #

    '''
    Applies the initial state to the state array
    Returns the state array
    '''
    def reset(self):
        self.state = np.zeros(len(self.stateTerms), dtype=np.int64)

        for prop in self.init_state:
            bit = '('
            for idx, x in enumerate(list(filter(lambda elem: elem != '', prop.strip().split(" ")))):
                bit += x if idx == 0 else ' ' + x
            bit += ')'
            self.state[ self.stateTerms[bit] ] = 1

        return self.state.copy()

    '''
    Returns the index at self.allActionsKeys of the 'legal' action selected at random from all possible actions
    '''
    def sample(self):
        try:
            return np.random.choice(self.legalActionsPerState[tuple(self.state)], 1)[0]
        except KeyError:
            allActionsKeys = deepcopy(self.allActionsKeys)
            np.random.shuffle(allActionsKeys)
            return np.where(self.allActionsKeys == fast.get_random_legal_action(self.state, self.allActions, allActionsKeys))[0][0]

    '''
    Takes the index of a legal action from self.allActionsKeys and applies the effect to the state array
    Returns the state array, the value of the reward and whether the state satisfies the goal state
    '''
    def step(self, action):
        prevPendingPreds = self.check_proximity_to_goal()
        actionKey = self.allActionsKeys[action]

        for eff, value in self.allActions[actionKey]["effect"].items():
            self.state[ eff ] = value

        newPendingPreds = self.check_proximity_to_goal()
        if not newPendingPreds:
            return self.state.copy(), GOAL_REWARD, True
        else:
            return self.state.copy(), self.get_reward(actionKey, prevPendingPreds-newPendingPreds), False
