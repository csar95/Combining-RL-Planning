import re
import sys

from utils import *

'''
It does not accept a domain with or, when, forall statements. Only not is allowed
All objects must have a type.
All predicates parameters must have a type
'''
def read_domain_file(filePath, env):
    with open(filePath) as fp:
        Lines = fp.readlines()

        currentBlock = ""
        actionName = ""

        for line in Lines:
            if not line.strip(): continue

            elif currentBlock and line.strip() == ")":
                currentBlock = ""
            elif not currentBlock and ":types" in line.strip():
                currentBlock = "types"
            elif not currentBlock and ":predicates" in line.strip():
                currentBlock = "predicates"
            elif not currentBlock and ":functions" in line.strip():
                currentBlock = "functions"
            elif not currentBlock and ":action-costs" not in line.strip() and ":action" in line.strip():
                currentBlock = "action"
                actionName = line.strip().split()[-1]
                env.actionsSchemas[actionName] = {}

            # Types need to be in different lines. Subtypes need to be all in the same line as the type.
            # ':types' needs to be alone in one line. The same with the final ')'

            elif currentBlock == "types":
                # Only 1 type in this line
                if "-" not in line.strip():
                    env.types[f"{line.strip()}"] = []
                # At least 1 subtype and the type it belongs to
                else:
                    types = line.strip().split()
                    parentType = ""
                    for t in reversed(types):
                        if not parentType:
                            parentType = t
                            if parentType not in env.types.keys():
                                env.types[f"{parentType}"] = {}
                        elif t != "-":
                            env.types[f"{parentType}"][f"{t}"] = []

            # It only accepts one predicate per line
            # ':predicates' needs to be alone in one line. The same with the final ')'

            elif currentBlock == "predicates":
                # Predicate without parameters --> It's an object-independent predicate
                if "?" not in line.strip():
                    env.objIndependentPreds.add(re.sub("[()]", "", line.strip()).strip())
                else:
                    answered = False
                    while not answered:
                        # THIS INFO COULD BE OBTAINED IF THE PREDICATE DOESN'T APPEAR IN ANY ACTION EFFECT
                        answer = input(f'Is "{line.strip()}" an immutable predicate? [y/N]\n').lower()

                        if answer == "":
                            answer = "n"

                        elif answer not in valid:
                            sys.stdout.write("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")
                            continue

                        answered = True

                        if not valid[answer]:
                            env.objDependentPreds.add(re.sub("[()]", "", line.strip()).strip())

                        else:
                            env.immutablePreds.add(re.sub("[()]", "", line.strip()).strip())

            # There can be several functions in one line
            # ':functions' needs to be alone in one line. The same with the final ')'

            elif currentBlock == "functions":
                for func in list(re.findall(r"\((.*?)\)", line.strip())):
                    env.functions.add(func)

            # The content of ':parameters', ':precondition' and ':effect' need to be all in one line
            # ':action' needs to be in one line along with the action name. The same with the final ')'

            elif currentBlock == "action":
                # Add parameters to the current action schema
                if ":parameters" in line.strip():
                    parameters = line.strip().split()

                    objectTypes = []
                    for idx, elem in enumerate(parameters):
                        if "?" in elem:  # Elem is an object --> Check the type
                            for i, x in enumerate(parameters[(idx + 1):]):
                                if x == "-":
                                    objectTypes.append((re.sub("[()]", "", elem),
                                                        re.sub("[()]", "", parameters[idx + 1 + (i + 1)])))
                                    break

                    env.actionsSchemas[actionName]["parameters"] = objectTypes

                # Add the predicates in the precondition to the current action schema
                elif ":precondition" in line.strip():
                    precondsPreds = []

                    aux = list(filter(lambda elm: elm != '(' and elm != ')', list(re.findall(r".*?:precondition.*?\(.*?and(.*).*?\)", line.strip()))[0].split()))

                    for idx, itm in enumerate(aux):
                        if '?' not in itm:
                            for p in env.objIndependentPreds.union(env.objDependentPreds.union(env.immutablePreds)):
                                if re.sub("[()]", "", itm) in p.split():
                                    predicate = f"!({re.sub('[()]', '', itm)}" if "not" in aux[idx - 1] else f"({re.sub('[()]', '', itm)}"
                                    for remainingItem in aux[(idx + 1):]:
                                        if '?' in remainingItem:
                                            predicate += f" {re.sub('[()]', '', remainingItem)}"
                                        else:
                                            break
                                    predicate += ")"
                                    precondsPreds.append(predicate)
                                    break

                    env.actionsSchemas[actionName]["precondition"] = precondsPreds

                # Add the predicates in the effect to the current action schema
                elif ":effect" in line.strip():
                    effsPreds = []
                    env.actionsSchemas[actionName]["reward"] = {}

                    aux = list(filter(lambda elm: elm != '(' and elm != ')', list(re.findall(r".*?:effect.*?\(.*?and(.*).*?\)", line.strip()))[0].split()))

                    for idx, itm in enumerate(aux):
                        if "increase" in itm:
                            if '?' not in aux[(idx + 2)]:  # E.g., (increase (total-cost) (travel-slow ?f1 ?f2))
                                metric = f"({re.sub('[()]', '', aux[(idx + 1)])})"
                                env.actionsSchemas[actionName]["reward"][metric] = get_reward_value(aux, idx, 0)
                            else:  # E.g., (increase (travel-slow ?f1 ?f2) (total-cost))
                                metric = f"({re.sub('[()]', '', aux[idx+1])}"
                                for i, remainingItem in enumerate(aux[(idx + 2):]):
                                    if '?' not in remainingItem: break
                                    metric += f" {re.sub('[()]', '', remainingItem)}"
                                metric += ')'
                                env.actionsSchemas[actionName]["reward"][metric] = get_reward_value(aux, idx, i)

                        elif '?' not in itm:
                            for p in env.objIndependentPreds.union(env.objDependentPreds.union(env.immutablePreds)):
                                if re.sub("[()]", "", itm) in p.split():
                                    predicate = f"!({re.sub('[()]', '', itm)}" if "not" in aux[idx - 1] else f"({re.sub('[()]', '', itm)}"
                                    for remainingItem in aux[(idx + 1):]:
                                        if '?' in remainingItem:
                                            predicate += f" {re.sub('[()]', '', remainingItem)}"
                                        else:
                                            break
                                    predicate += ")"
                                    effsPreds.append(predicate)
                                    break

                    env.actionsSchemas[actionName]["effect"] = effsPreds

def read_problem_file(filePath, env):
    with open(filePath) as fp:
        Lines = fp.readlines()

        currentBlock = ""
        init_state = []
        goal_state = []
        immutableProps = set([])

        for line in Lines:
            if not line.strip(): continue

            elif not currentBlock and line.strip() == ")":
                break
            elif currentBlock and line.strip() == ")":
                currentBlock = ""
            elif not currentBlock and ":objects" in line.strip():
                currentBlock = "objects"
            elif not currentBlock and ":init" in line.strip():
                currentBlock = "init"
            elif not currentBlock and ":goal" in line.strip():
                currentBlock = "goal"

            # It only accepts objects of one type per line
            # A type with subtypes cannot have objects assigned. Objects need to be assigned to the subtypes
            # ':objects' needs to be alone in one line. The same with the final ')'

            elif currentBlock == "objects":
                typ = ""

                # Iterate through the objects in this line reading from the type
                for obj in reversed(list(line.strip().split())):
                    if not typ:
                        typ = obj
                    elif obj != "-":
                        parentType = check_parent_type(typ, env.types)
                        if not parentType:
                            env.types[f"{typ}"].append(obj)
                        else:
                            env.types[f"{parentType}"][f"{typ}"].append(obj)

            # It's okay to define multiple properties in the same line
            # (= (..) 1) Function predicates need to be separated from normal predicates
            # ':init' needs to be alone in one line. The same with the final ')'

            elif currentBlock == "init":
                if "=" in line.strip():  # Function predicates. E.g.: (= (travel-fast n12 n16) 13)
                    for func in list(re.findall(r"\(.*?=(.*?\).*?)\)", line.strip())):
                        prop = "("
                        for elem in re.findall(r"\((.*?)\)", func)[0].split():
                            prop += elem if prop == "(" else f" {elem}"
                        prop += ")"
                        value = int(func.split()[-1])

                        env.allFunctions[prop] = value
                else:
                    # For each property in current line search for the ones immutable and add them to the environment
                    for prop in list(filter(lambda elm: '=' not in elm, re.findall(r"\((.*?)\)", line.strip()))):  # Omit properties with '='
                        if property_in_predicates(prop.strip().split()[0], env.immutablePreds):
                            immutableProps.add(f"({prop.strip()})")
                        else:
                            init_state.append(prop.strip())

            # It's okay to define multiple properties in the same line
            # There's need to be a space after 'not'. The final ')' for the 'and' needs to be inline with the last element
            # ':goal' needs to be alone in one line. The same with the final ')' and the keyword 'and'

            elif currentBlock == "goal":
                # For each property in current line add it to the goal state
                for prop in list(re.findall(r"\((.*?)\)", line.strip())):

                    propElems = list(filter(lambda elem: elem != '' and elem != '(' and elem != ')', prop.strip().split(" ")))

                    bit = '!(' if "not" in propElems[0] else '('
                    for idx, x in enumerate(propElems):
                        bit += '' if "not" in x else (x.strip('()') if bit == '(' or bit == '!(' else ' ' + x.strip('()'))
                    bit += ')'

                    goal_state.append(bit)

    return init_state, goal_state, frozenset(immutableProps)

'''
Checks whether the prop_name exists in any of the predicates in the 2nd parameter
'''
def property_in_predicates(prop_name, predicates):
    for pred in predicates:
        if prop_name == re.sub('[()]', '', pred).split()[0]:
            return True
    return False

'''
Returns the parent type of typ in targetSet. If typ doesn't have parent type it returns an empty string
'''
def check_parent_type(typ, targetSet):
    for key, value in targetSet.items():
        if typ == key:
            return ""
        if isinstance(value, dict):
            for k, v in value.items():
                if typ == k:
                    return key

def get_reward_value(aux, idx, i):
    if re.sub('[()]', '', aux[idx + 2 + i]).isdigit():  # E.g., (increase (total-cost) 1)
        value = re.sub('[()]', '', aux[idx + 2 + i])
    else:  # E.g., (increase (total-cost) (travel-slow ?f1 ?f2))
        value = f"({re.sub('[()]', '', aux[idx + 2 + i])}"
        for remainingItem in aux[(idx + 3 + i):]:
            if '?' not in remainingItem: break
            value += f" {re.sub('[()]', '', remainingItem)}"
        value += ')'

    return value

'''
Transforms the prior plans from the same domain into transition tuples that will be stored in the replay buffer
'''
def get_prior_transitions(path, numsol, env):
    transitions = []

    for file in list(map(str, range(numsol))):
        filePath = path + f"/{file}.1"
        f = open(filePath, 'r')
        steps = f.readlines()

        current_state = env.reset()

        for action in steps:
            actionName = '(' + re.sub('[()]', '', action.strip()).strip() + ')'
            action = np.where(env.allActionsKeys == actionName)[0][0]

            new_state, reward, done = env.step(action)
            transitions.append((current_state, action, reward, new_state, done))

            current_state = new_state

        f.close()

    return transitions

'''
Returns a reduced version of the current state that only includes the actions listed in the prior plans
'''
def get_reduce_action_space(path, numsol):
    reducedAllActionsKeys = np.array([])

    for file in list(map(str, range(numsol))):
        filePath = path + f"/{file}.1"
        f = open(filePath, 'r')
        steps = f.readlines()

        for action in steps:
            actionName = '(' + re.sub('[()]', '', action.strip()).strip() + ')'
            if actionName not in reducedAllActionsKeys:
                reducedAllActionsKeys = np.append(reducedAllActionsKeys, actionName)

    return reducedAllActionsKeys