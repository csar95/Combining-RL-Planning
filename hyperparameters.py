RESOURCES_FOLDER = "/Users/csr95/Desktop/MSc_Artificial_Intelligence_HWU/MSc_Project_Dissertation/Combining-RL-Planning/Encoding_Module/Resources/"
DATA_FOLDER = "/Users/csr95/Desktop/MSc_Artificial_Intelligence_HWU/MSc_Project_Dissertation/Combining-RL-Planning/Data/"
FIGURES_FOLDER = "/Users/csr95/Desktop/MSc_Artificial_Intelligence_HWU/MSc_Project_Dissertation/Combining-RL-Planning/Figures/"
MODELS_FOLDER = "/Users/csr95/Desktop/MSc_Artificial_Intelligence_HWU/MSc_Project_Dissertation/Combining-RL-Planning/Models/"

DOMAIN = "elevators"
PROBLEM = "elevators_p4"

# Agent settings
REPLAY_MEMORY_SIZE = 20_000  # 50_000
MIN_REPLAY_MEMORY_SIZE = 1_000  # Minimum number of steps to start training
MINIBATCH_SIZE = 64  # The number of samples we use for training
UPDATE_TARGET_EVERY = 100
HARD_UPDATE = False  # True --> Hard update | False --> Soft update
TAU = 0.01
DISCOUNT = 0.99
LEARNING_RATE = 0.001

# Environment settings
GOAL_REWARD = 800
EPISODES = 4000
MAX_STEP_PER_EPISODE = 100
EPSILON_DECAY = 0.9975
MIN_EPSILON = 0.0001
# MAX_REWARD = 13

SHOW_STATS_EVERY = 25  # (Episodes)

NUMBER_OF_PREVIOUS_PLANS = 15  # 33
REUSE_RATE = 0.25
REDUCE_ACTION_SPACE = False  # False --> Alg. uses full action space
                             # True --> Alg. filters legal actions with the ones appearing on the prior plans whenever it's possible, otherwise it uses the full action space

MAX_STEPS_PLANNER = 20