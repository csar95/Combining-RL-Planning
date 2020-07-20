# Combining RL & Planning

This program was implemented as part of the MSc Dissertation "Combining Reinforcement Learning and Automated Planning" by César Gutiérrez Carrero.

It is structured in different packages. Each of them has a file that allows to test them on their own.
- The __*Encoding_Module*__ generates the environment with the binary encoding.
- The __*Encoding_Module_Non_binary_encoding*__ does the same with the non-binary encoding.
- The __*Learning_Module*__ includes the following agents: DQL, Double DQL and Double DQL w/ Plan reuse (DDQL implementation for the 1st & 2nd approaches). The init file can run the RL algorithm with any of those agents.
- The __*Learning_Module_Non_binary_encoding*__ implements the Double DQN algorithm with the non-binary encoding.
- The __*Learning_Module_PER*__ implements the Double DQN w/ Prioritised exp. replay (PER) agent. The init file runs that algorithm.
- The __*Learning_Module_PyTorch*__ implements the Double DQN algorithm with PyTorch instead of Keras.
- The __*Planning_Module*__ includes a file with the class Planner. This class implements methods to translate the policy learnt by the agent into a plan.

I used the __main_comparison__ and __main_eval_planners_sols__ for the evaluation. The former was used to generated the graphs that appear in the project. The latter obtains the info. about the quality of the solutions returned by planning systems.

Finally, __RL_Planning__ is designed to be executed from the console. It only uses the binary encoding and can run the following algorithms: DQL, Double DQL, Double DQL w/ PER and Double DQL w/ Plan reuse (1-4 approach)

usage: RL_Planning.py [-h] [-t AGENTTYPE] [-o OPTION] [-i INITIALETA] [-d DECAYETA] [-m MINETA] [-p PASTPLANS] domain problem directory

positional arguments:\
&nbsp;&nbsp;&nbsp;domain&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Path to the domain file.\
&nbsp;&nbsp;&nbsp;problem&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Path to the target problem file.\
&nbsp;&nbsp;&nbsp;directory&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Path to the directory where data will be stored.

optional arguments:\
&nbsp;&nbsp;&nbsp;-h, --help&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;show this help message and exit\
&nbsp;&nbsp;&nbsp;-t AGENTTYPE, --agenttype AGENTTYPE\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Type of agent. Possible values: ['DQL', 'DDQL', 'DDQL_PlanReuse', 'DDQL_PER']\
&nbsp;&nbsp;&nbsp;-o OPTION, --option OPTION\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ID of an approach devised to leverage prior knowledge\
&nbsp;&nbsp;&nbsp;-i INITIALETA, --initialeta INITIALETA\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Initial value of eta (4th approach plan DDQL_PlanReuse)\
&nbsp;&nbsp;&nbsp;-d DECAYETA, --decayeta DECAYETA\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decay factor for eta (4th approach plan DDQL_PlanReuse)\
&nbsp;&nbsp;&nbsp;-m MINETA, --mineta MINETA\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Minimum value of eta (4th approach plan DDQL_PlanReuse)\
&nbsp;&nbsp;&nbsp;-p PASTPLANS, --pastplans PASTPLANS\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Path to directory with past plans

*The rest of the parameters are read from the __hyperparameters.py__ file.*

------------------------------------ USE EXAMPLES -------------------------------------

*Double DQN algorithm*:\
&nbsp;&nbsp;&nbsp;./RL_Planning.py Resources/elevators.pddl Resources/elevators_p2.pddl ./

*DQN algorithm*:\
&nbsp;&nbsp;&nbsp;./RL_Planning.py Resources/floortile.pddl Resources/floortile_p1.pddl ./ -t DQL

*Double DQN algorithm w/ PER*:\
&nbsp;&nbsp;&nbsp;./RL_Planning.py Resources/transport.pddl Resources/transport_p2.pddl ./ -t DDQL_PER

*Double DQN algorithm w/ Plan reuse (1-3)*:\
&nbsp;&nbsp;&nbsp;./RL_Planning.py Resources/elevators.pddl Resources/elevators_p5.pddl ./ -t DDQL_PlanReuse -o 1 -p Resources/Solutions/elevators_p5_lite/

*Double DQN algorithm w/ Plan reuse (4)*:\
&nbsp;&nbsp;&nbsp;./RL_Planning.py Resources/transport.pddl Resources/transport_p3.pddl ./ -t DDQL_PlanReuse -o 4 -p Resources/Solutions/transport_p3_full/ -i 0.95 -d 0.998 -m 0

--------------------------- DOMAIN AND PROBLEM REQUIREMENTS ---------------------------

In the interest of simplicity a few constraints were established with regard to the requirements and keywords that can be used to define the domain and the target problem:
- The program does not recognise quantified formulas (forall, exists), conditional effects (when), nor disjunctions (or). Only conjunctions (and) and general negations (not) are accepted.
- Domains must include the typing requirement. The action-cost requirement is optional.
- Every object in the problem file as well as the predicates parameters must be typed.
- If a type has subtypes, objects cannot be assigned to the parent type but to any of the subtypes instead.

Moreover, in order for the program to be able to read the files correctly, these must satisfy a specific format:
- Every keyword marking the beginning of a block (:types, :predicates, :action, :function, :objects, :init and :goal) must be alone in one line as well as the final parenthesis that indicates the end of the block.
- Regarding the domain file, each type must be declared in a separate line and all subtypes must appear in the same line as the parent type. On the other hand, objects defined in the problem file must appear in the same line as other objects sharing the same type.
- Predicates inside the :predicates block much be declared in separate lines.
- The definition of the action components (parameters, precondition and effect) must
be done in a separate line.
- In the case of the :functions block, the program accepts the definition of several functions in the same line.
- Regarding the :init block, multiple properties can be defined in the same line, although predicate properties and function properties must be separated.
- Lastly, the parenthesis at the end of the conjunction of properties in the :goal block, that is, the one that corresponds to the and keyword, must be in the same line as the last property.

---------------------------- 1-4 APPROACHES FOR PLAN REUSE ----------------------------

__1.__ The agent explores the state space with full access to action space, whilst at each training step the mini-batch of experience transitions is filled with a percentage of transitions extracted from past plans.

__2.__ The agent explores the state space with full access to action space, and the replay memory buffer is filled with all the experience transitions extracted from past plans.

__3.__ The agent explores the state space with restricted access to the action space. That is, the actions that compose the past plans provided as input have higher priority than those that are not included in any past plan.

__4.__ A variant of the previous approach that includes an additional parameter, η, representing the probability of selecting an action like in the third strategy over selecting an action with unrestricted access to action space.
