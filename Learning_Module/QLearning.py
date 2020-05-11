import time
import subprocess
from environment import *


javaAppProcess = subprocess.Popen('java -jar ../Encoding_Module/fastMod.jar', shell=True)
env = Environment()


# ------------------------------------------------------------------------ #

start_time = time.time()
action = env.sample()
colorPrint(str(time.time() - start_time), YELLOW)
print(action)

times = []
for _ in range(1000):
    start_time = time.time()
    env.sample()
    times.append(time.time() - start_time)

print(sum(times)/len(times))

# print(env.allActions[action])

start_time = time.time()
newObservation, reward, done = env.step(action)
colorPrint(str(time.time() - start_time), YELLOW)
print(f"{reward} {done} {newObservation}")

javaAppProcess.kill()  # TODO: CHECK EXCEPTION
