import time
from environment import *


env = Environment()

colorPrint("\n------- TYPES -------", CYAN)
print(env.types)

colorPrint("\n------- ACTIONS -------", CYAN)
print(env.actionsSchemas)

colorPrint("\n------- FUNCTIONS -------", CYAN)
for line in env.functions:
    print(line)

colorPrint("\n------- OBJECT INDEPENDENT PROPERTIES -------", CYAN)
for line in env.objIndependentPreds:
    print(line)

colorPrint("\n------- OBJECT DEPENDENT PROPERTIES -------", CYAN)
for line in env.objDependentPreds:
    print(line)

colorPrint("\n------- OBJECT DEPENDENT PROPERTIES (IMMUTABLE) -------", CYAN)
for line in env.immutablePreds:
    print(line)

# ------------------------------------------------------------------------ #

colorPrint("\n------- IMMUTABLE PROPERTIES -------", CYAN)
print(env.immutableProps)

colorPrint("\n------- OBJECTS & TYPES -------", CYAN)
print(env.types)

colorPrint("\n------- GOAL STATE -------", CYAN)
print(env.goal_state)

colorPrint("\n------- FUNCTIONS VALUES -------", CYAN)
print(env.allFunctions)

# ------------------------------------------------------------------------ #

colorPrint("\n------- STATE ENCODING -------", CYAN)
print(env.state)
print(len(env.state))

colorPrint("\n------- ALL ACTIONS IN THE ENVIRONMENT -------", CYAN)
# print(env.allActions)
print(len(env.allActions))

print(env.is_legal("(board p7 slow0-0 n1 n2 n8)"))
print(env.is_legal("(board p9 slow0-0 n2 n0 n1)"))

start_time = time.time()
legalActionsAtInitialState = env.get_legal_actions()
colorPrint(str(time.time() - start_time), YELLOW)

print(legalActionsAtInitialState)
print(len(legalActionsAtInitialState))
