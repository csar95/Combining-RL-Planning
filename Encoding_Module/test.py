from environment import *
import time


def run_test():
    colorPrint("\n------- OBJECTS & TYPES -------", CYAN)
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

    colorPrint("\n------- INIT STATE -------", CYAN)
    print(env.init_state)

    colorPrint("\n------- GOAL STATE -------", CYAN)
    print(env.goal_state)

    colorPrint("\n------- FUNCTIONS VALUES -------", CYAN)
    print(env.allFunctions)

    colorPrint("\n------- REWARDS VALUES -------", CYAN)
    print(env.allRewards)

    # ------------------------------------------------------------------------ #

    colorPrint("\n------- STATE ENCODING -------", CYAN)
    print(env.stateTerms)
    print(env.state)
    print(len(env.state))

    colorPrint("\n------- ALL ACTIONS IN THE ENVIRONMENT -------", CYAN)
    # print(env.allActions["(move-up-slow slow0-0 n2 n8)"])
    # print("(move-up-slow slow0-0 n16 n16)" in env.allActions)
    print(env.allActions)
    print(len(env.allActions))

    # ------------------------------------------------------------------------ #

    # print(f'Is (board p7 slow0-0 n1 n2 n3) legal? {env.is_legal("(board p7 slow0-0 n1 n2 n3)")}')
    # print(f'Is (board p9 slow0-0 n2 n0 n1) legal? {env.is_legal("(board p9 slow0-0 n2 n0 n1)")}')

    colorPrint("\n------- ALL LEGAL ACTIONS FROM THE CURRENT STATE -------", CYAN)

    start_time = time.time()
    idxOfLegalActions = env.get_legal_actions(env.state)
    colorPrint(str(time.time() - start_time), YELLOW)

    print(idxOfLegalActions)
    print(idxOfLegalActions.size)
    print(env.allActionsKeys[idxOfLegalActions])

    colorPrint("\n------- AVERAGE TIME TO GET A RANDOM LEGAL ACTION FROM CURRENT STATE -------", CYAN)

    times = []
    for _ in range(1000):
        start_time = time.time()
        action = env.sample()
        times.append(time.time() - start_time)

    colorPrint(str(sum(times)/len(times)), YELLOW)

    print(action)
    print(env.allActionsKeys[action])
    print(env.allActions[env.allActionsKeys[action]])
    print(idxOfLegalActions)

    colorPrint("\n------- TAKE PREVIOUS ACTION FROM CURRENT STATE -------", CYAN)

    start_time = time.time()
    newObservation, reward, done = env.step(action)
    colorPrint(str(time.time() - start_time), YELLOW)
    print(f"{reward} {done} {newObservation}")


if __name__ == '__main__':
    env = Environment()
    run_test()

# Problem 4 : 91  , 1068
# Problem 5 : 222 , 6096 | 174 , 3704 | 150 , 2706 | 126 , 1882 | 114 , 1539 | 91 , 1038
