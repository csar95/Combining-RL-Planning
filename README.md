# Combining RL & Planning

This program was implemented as part of the MSc Dissertation "Combining Reinforcement Learning and Automated Planning".

It is structured in different packages. Each of them has a file that allows to test them on their own.
- The __*Encoding_Module*__ generates the environment with the binary encoding, whereas the __*Encoding_Module_Non_binary_encoding*__ does the same with the non-binary encoding.
- The __*Learning_Module*__ includes the DQL, Double DQL and Double DQL - Plan reuse (DDQL implementation for the 1st & 2nd approaches) agents. The init file can run the RL algorithm with any of those agents.
- The __*Learning_Module_Non_binary_encoding*__ implements the Double DQN algorithm for the non-binary encoding.
- The __*Learning_Module_PER*__ implements the Double DQN w/ Prioritised exp. replay (PER) agent. The init file runs that algorithm.
- The __*Learning_Module_PyTorch*__ implements the Double DQN algorithm with PyTorch instead of Keras.
- The __*Planning_Module*__ includes a file with the class Planner. This class implements methods to translate the policy learnt by the agent into a plan.

We used the main_comparison and main_eval_planners_sols for the evaluation. The former was used to generated the graphs that appear in the project. The second obtains the info. about the quality of the solutions returned by the planning systems.

Finally, __RL_Planning__ is designed to be executed from the console. It only uses the binary encoding and can run the following algorithms: DQL, Double DQL, Double DQL w/ PER and Double DQL w/ Plan reuse (1-4 approach)

usage: RL_Planning.py [-h] [-t AGENTTYPE] [-o OPTION] [-i INITIALETA] [-d DECAYETA] [-m MINETA] [-p PASTPLANS] domain problem

positional arguments:\
&nbsp;&nbsp;&nbsp;domain&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Path to the domain file.\
&nbsp;&nbsp;&nbsp;problem&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Path to the target problem file.

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

