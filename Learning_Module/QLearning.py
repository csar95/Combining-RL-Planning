import time
from environment import *


env = Environment()


# ------------------------------------------------------------------------ #

start_time = time.time()
action = env.sample()
colorPrint(str(time.time() - start_time), YELLOW)
print(action)

print(env.allActions[action])

start_time = time.time()
newObservation, reward, done = env.step(action)
colorPrint(str(time.time() - start_time), YELLOW)
print(f"{reward} {done} {newObservation}")
