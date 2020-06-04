RESOURCES_FOLDER = "/Users/csr95/Desktop/MSc_Artificial_Intelligence_HWU/MSc_Project_Dissertation/Combining-RL-Planning/Encoding_Module/Resources/"

DOMAIN = "elevators"
PROBLEM = "elevators_p9"

MODEL_NAME = "DQL_Elevators"

# Agent settings
REPLAY_MEMORY_SIZE = 20_000  # 50_000
MIN_REPLAY_MEMORY_SIZE = 1_000  # Minimum number of steps to start training
MINIBATCH_SIZE = 64  # The number of samples we use for training
UPDATE_TARGET_EVERY = 100
HARD_UPDATE = True
TAU = 0.05
DISCOUNT = 0.99
LEARNING_RATE = 0.001

# Environment settings
GOAL_REWARD = 650
EPISODES = 2_500
MAX_STEP_PER_EPISODE = 100
EPSILON_DECAY = 0.995
MIN_EPSILON = 0.0001
# MAX_REWARD = 13

AGGREGATE_STATS_EVERY = 25  # (Episodes)

NUMBER_OF_PREVIOUS_PLANS = 14
REUSE_RATE = 0.5