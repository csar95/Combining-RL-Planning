import time
import subprocess
from environment import *


javaAppProcess = subprocess.Popen('java -jar ../Encoding_Module/fastMod.jar', shell=True)
env = Environment()

# END OF ENVIRONMENT INITIALIZATION ---------------------------------------------------------------------------------- #

times = []
for _ in range(1000):
    start_time = time.time()
    action = env.sample()
    times.append(time.time() - start_time)

colorPrint(str(sum(times)/len(times)), YELLOW)

print(action)

start_time = time.time()
newObservation, reward, done = env.step(action)
colorPrint(str(time.time() - start_time), YELLOW)
print(f"{reward} {done} {newObservation}")

# END OF PROGRAM ----------------------------------------------------------------------------------------------------- #

env.gateway.shutdown()
javaAppProcess.kill()
