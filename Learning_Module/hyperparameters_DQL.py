MODEL_NAME = "DQL_TensorFlow"
REPLAY_MEMORY_SIZE = 50_000
MIN_REPLAY_MEMORY_SIZE = 1_000  # Minimum number of steps to start training
MINIBATCH_SIZE = 64  # The number of samples we use for training
UPDATE_TARGET_EVERY = 5
MIN_REWARD = -100
DISCOUNT = 0.99
LEARNING_RATE = 0.001

# Environment settings
EPISODES = 1000# 20_000
MAX_STEP_PER_EPISODE = 100

# Exploration settings
EPSILON_DECAY = 0.999#0.99975
MIN_EPSILON = 0.001

# Stats settings
AGGREGATE_STATS_EVERY = 20  # Episodes
