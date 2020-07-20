#!/usr/local/bin/python3.7

from Planning_Module.Planner import *
from Encoding_Module.environment import *
from Learning_Module.DQNAgent import *
from Learning_Module.DDQNAgent import *
from Learning_Module.DDQLAgent_PlanReuse import *
from Learning_Module_PER.DDQNAgentPER import *
from Learning_Module.DeepQLearning import *
from Learning_Module_PER.DDeepQLearningPER import *
from hyperparameters import *
from utils import *

from argparse import ArgumentParser
from pathlib import Path
from os.path import join


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("domain", help="Path to the domain file.", type=Path)
    parser.add_argument("problem", help="Path to the target problem file.", type=Path)
    parser.add_argument("directory", help="Path to the directory where data will be stored.", type=Path)
    parser.add_argument("-t", "--agenttype", default="DDQL", help="Type of agent. Possible values: ['DQL', 'DDQL', 'DDQL_PlanReuse', 'DDQL_PER']", type=str)
    parser.add_argument("-o", "--option", default=None, help="ID of an approach devised to leverage prior knowledge", type=int)
    parser.add_argument("-i", "--initialeta", default=0.0, help="Initial value of eta (4th approach plan DDQL_PlanReuse)", type=float)
    parser.add_argument("-d", "--decayeta", default=0.0, help="Decay factor for eta (4th approach plan DDQL_PlanReuse)", type=float)
    parser.add_argument("-m", "--mineta", default=0.0, help="Minimum value of eta (4th approach plan DDQL_PlanReuse)", type=float)
    parser.add_argument("-p", "--pastplans", default=None, help="Path to directory with past plans", type=Path)

    args = parser.parse_args()

    if not args.domain.exists():
        colorPrint("Invalid path to domain file.", RED)
        exit(1)
    if not args.problem.exists():
        colorPrint("Invalid path to target problem file.", RED)
        exit(1)
    if not args.directory.exists():
        colorPrint("Invalid path to data directory.", RED)
        exit(1)

    if args.agenttype == 'DDQL_PlanReuse' and not args.pastplans:
        colorPrint("You must add the path to past plans to be able to run agent 'DDQL_PlanReuse'.", RED)
        exit(1)

    if args.pastplans and not args.pastplans.exists():
        colorPrint("Invalid path to past plans.", RED)
        exit(1)

    if args.option and args.agenttype != 'DDQL_PlanReuse':
        colorPrint("Invalid option for plan reuse. You must select: -t --agenttype 'DDQL_PlanReuse'", RED)
        exit(1)

    if (args.option != 4 or args.agenttype != 'DDQL_PlanReuse') and (args.initialeta != 0.0 or args.decayeta != 0.0 or args.mineta != 0.0):
        colorPrint("The arguments related to the parameter eta are associated with the 4th approach (DDQL_PlanReuse)", RED)
        exit(1)

    ### 1. ENCODING MODULE
    env = Environment(pathtodomain=args.domain, pathtoproblem=args.problem, pathtopastplans=args.pastplans)

    if args.agenttype == 'DDQL':
        agent = DDQNAgent(env)
    elif args.agenttype == 'DQL':
        agent = DQNAgent(env)
    elif args.agenttype == 'DDQL_PlanReuse':
        if args.option == 1:
            agent = DDQLAgent_PlanReuse(env, prevexp=env.get_previous_plans(reduceactionspace=False), allexpmixed=False)
        elif args.option == 2:
            agent = DDQLAgent_PlanReuse(env, prevexp=env.get_previous_plans(reduceactionspace=False), allexpmixed=True)
        elif args.option == 3 or args.option == 4:
            if args.option == 3:
                args.initialeta = 1
                args.decayeta = 1
            if args.option == 4 and (args.initialeta == 0 or args.decayeta == 0):
                colorPrint("You may want to revise the arguments associated with the parameter eta. Recommended configuration: -i 0.95 -d 0.998 -m 0.0", YELLOW)
            env.get_previous_plans(reduceactionspace=True)
            agent = DDQNAgent(env)
        else:
            colorPrint("Invalid option for plan reuse. Possible values: [1, 2, 3, 4]", RED)
            exit(1)
    elif args.agenttype == 'DDQL_PER':
        agent = DDQNAgentPER(env)
    else:
        colorPrint("Incorrect type of agent.", RED)
        exit(1)

    msg = f"Running RL algorithm: {args.agenttype}"
    if args.agenttype == 'DDQL_PlanReuse':
        msg += f" | Approach: {args.option}"
    if args.agenttype == 'DDQL_PlanReuse' and (args.option == 3 or args.option == 4):
        msg += f" | Initial eta: {args.initialeta} , Decay factor eta: {args.decayeta} , Min. eta: {args.mineta}"
    colorPrint(msg, MAGENTA)

    problemFileName = Path(args.problem).name.split('.')[0]

    ### 2. LEARNING MODULE
    exp_results = deep_q_learning_alg(env, agent, 99, None, initialeta=args.initialeta, mineta=args.mineta,
                                      etadecay=args.decayeta, directory=args.directory, problemfilename=problemFileName) \
        if args.agenttype != 'DDQL_PER' \
        else deep_q_learning_alg_per(env, agent, 99, None, a=ALPHA_PER, directory=args.directory, problemfilename=problemFileName)

    exp_results.save_data(None, 99, directory=args.directory)

    ### 3. PLANNING MODULE
    planner = Planner(env, pathtomodel=join(args.directory, f"{problemFileName}.h5"),
                      reduceactionspace=True if args.option == 3 else False)

    solution, score, finished = get_plan(env, agent, reduceactionspace=True if args.option == 3 else False) \
        if args.agenttype != 'DDQL_PER' \
        else get_plan_per(env, agent)

    planner.save_plan(solution, pathtodata=join(args.directory, "data"))
