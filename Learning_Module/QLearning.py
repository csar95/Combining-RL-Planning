import time
from environment import *


env = Environment()


# ------------------------------------------------------------------------ #

start_time = time.time()
action = env.sample()
colorPrint(str(time.time() - start_time), YELLOW)
print(action)
