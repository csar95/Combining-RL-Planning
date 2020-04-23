import time

from fileIO import *
from environment import *


objIndependentPreds = set([])
objDependentPreds = set([])
immutablePreds = set([])
env = Environment()

# ------------------------------------------------------------------------ #

filePath = RESOURCES_FOLDER + "domain.pddl"

# Reading domain file. Obtain the object dependent and independent properties
colorPrint("Reading domain file...", MAGENTA)

read_domain_file(filePath, objIndependentPreds, objDependentPreds, immutablePreds, env)

colorPrint("\n------- TYPES -------", CYAN)

print(env.types)

colorPrint("\n------- ACTIONS -------", CYAN)

print(env.actionsSchemas)

colorPrint("\n------- OBJECT INDEPENDENT PROPERTIES -------", CYAN)
for line in objIndependentPreds:
    print(line)

colorPrint("\n------- OBJECT DEPENDENT PROPERTIES -------", CYAN)
for line in objDependentPreds:
    print(line)

colorPrint("\n------- OBJECT DEPENDENT PROPERTIES (IMMUTABLE) -------", CYAN)
for line in immutablePreds:
    print(line)

# ------------------------------------------------------------------------ #

filePath = RESOURCES_FOLDER + "problem.pddl"

# Reading problem file. Detect the immutable properties and the type of each object
colorPrint("\nReading problem file...", MAGENTA)

init_state = read_problem_file(filePath, immutablePreds, env)

colorPrint("\n------- IMMUTABLE PROPERTIES -------", CYAN)

print(env.immutableProps)

colorPrint("\n------- OBJECTS & TYPES -------", CYAN)

print(env.types)

# ------------------------------------------------------------------------ #

# Initialize the state encoding
env.initialize_state(objDependentPreds, objIndependentPreds, init_state)

colorPrint("\n------- STATE ENCODING -------", CYAN)
print(env.state)
print(len(env.state))

colorPrint("\n------- ALL ACTIONS IN THE ENVIRONMENT -------", CYAN)
# This will be useful to for form the Q-table (COLUMNS -> Actions in the env., ROWS -> States)
start_time = time.time()
env.get_all_actions()
colorPrint(str(time.time() - start_time), YELLOW)
# print(env.allActions)
print(len(env.allActions))

print(env.is_legal("(board p7 slow0-0 n1 n2 n8)"))

print(env.is_legal("(board p9 slow0-0 n2 n0 n1)"))

start_time = time.time()
legalActionsAtInitialState = env.get_legal_actions()
colorPrint(str(time.time() - start_time), YELLOW)

print(legalActionsAtInitialState)
print(len(legalActionsAtInitialState))
