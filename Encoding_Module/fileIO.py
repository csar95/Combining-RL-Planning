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
            elif not currentBlock and ":action-costs" not in line.strip() and ":action" in line.strip():
                currentBlock = "action"
                actionName = list(filter(lambda elm: elm != '', line.strip().split(" ")))[-1]
                env.actionsSchemas[actionName] = {}

            # Types need to be in different lines. Subtypes need to be all in the same line as the type.
            # ':types' needs to be alone in one line. The same with the final ')'

            elif currentBlock == "types":
                # Only 1 type in this line
                if "-" not in line.strip():
                    env.types[f"{line.strip()}"] = []
                # At least 1 subtype and the type it belongs to
                else:
                    types = list(filter(lambda elm: elm != '', line.strip().split(" ")))
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

            # The content of ':parameters', ':precondition' and ':effect' need to be all in one line
            # ':action' needs to be in one line along with the action name. The same with the final ')'

            elif currentBlock == "action":
                # Add parameters to the current action schema
                if ":parameters" in line.strip():
                    parameters = list(filter(lambda elm: elm != '', line.strip().split(" ")))

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

                    aux = list(filter(lambda elm: elm != '' and elm != '(' and elm != ')' and elm != ":precondition" and "and" not in elm, line.strip().split(" ")))

                    for idx, itm in enumerate(aux):
                        if '?' not in itm:
                            for p in env.objIndependentPreds.union(env.objDependentPreds.union(env.immutablePreds)):
                                if re.sub("[()]", "", itm) in list(filter(lambda elm: elm != '', p.split(" "))):
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

                    aux = list(filter(lambda elm: elm != '' and elm != '(' and elm != ')' and elm != ":effect" and
                                                  "and" not in elm, line.strip().split(" ")))

                    for idx, itm in enumerate(aux):
                        if '?' not in itm:
                            for p in env.objIndependentPreds.union(env.objDependentPreds.union(env.immutablePreds)):
                                if re.sub("[()]", "", itm) in list(filter(lambda elm: elm != '', p.split(" "))):
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
        foundObjects = False
        foundInit = False
        foundGoal = False

        '''
        It only accepts objects of one type per line
        A type with subtypes cannot have objects assigned. Objects need to be assigned to the subtypes
        ':objects' needs to be alone in one line. The same with the final ')'
        '''

        for line in Lines:
            if foundObjects and line.strip() == ")":
                break

            elif ":objects" in line.strip():
                foundObjects = True

            elif not foundObjects or not line.strip():
                continue

            else:
                typ = ""

                # Iterate through the objects in this line reading from the type
                for obj in reversed(list(filter(lambda elem: elem != '', line.strip().split(" ")))):
                    if not typ:
                        typ = obj
                    elif obj != "-":
                        parentType = check_parent_type(typ, env.types)
                        if not parentType:
                            env.types[f"{typ}"].append(obj)
                        else:
                            env.types[f"{parentType}"][f"{typ}"].append(obj)

        '''
        It's okay to define multiple properties in the same line
        ':init' needs to be alone in one line. The same with the final ')'
        '''

        init_state = []

        for line in Lines:
            if foundInit and line.strip() == ")":
                break

            elif ":init" in line.strip():
                foundInit = True

            elif not foundInit or not line.strip():
                continue

            else:
                # For each property in current line search for the ones immutable and add them to the environment
                for prop in list(filter(lambda elm: '=' not in elm, re.findall(r"\((.*?)\)", line.strip()))):  # Omit properties with '='
                    if property_in_predicates(list(filter(lambda elem: elem != '', prop.strip().split(" ")))[0], env.immutablePreds):
                        env.immutableProps.add(f"({prop.strip()})")
                    else:
                        init_state.append(prop.strip())

        '''
        It's okay to define multiple properties in the same line
        There's need to be a space after 'not'
        ':goal' needs to be alone in one line. The same with the final '))' and the keyword 'and'
        '''

        goal_state = []

        for line in Lines:
            if foundGoal and line.strip() == "))":
                break

            elif ":goal" in line.strip():
                foundGoal = True

            elif not foundGoal or not line.strip() or "and" in line.strip():
                continue

            else:
                # For each property in current line add it to the goal state
                for prop in list(re.findall(r"\((.*?)\)", line.strip())):

                    propElems = list(filter(lambda elem: elem != '' and elem != '(' and elem != ')', prop.strip().split(" ")))

                    bit = '!(' if "not" in propElems[0] else '('
                    for idx, x in enumerate(propElems):
                        bit += '' if "not" in x else (x.strip('()') if bit == '(' or bit == '!(' else ' ' + x.strip('()'))
                    bit += ')'

                    goal_state.append(bit)

    return init_state, goal_state

'''
Checks whether the prop_name exists in any of the predicates in the 2nd parameter
'''
def property_in_predicates(prop_name, predicates):
    for pred in predicates:
        if re.search(r"\b" + re.escape(prop_name) + r"\b", pred):
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
