import time
import subprocess
from environment import *


def run_test():
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


if __name__ == '__main__':
    javaAppProcess = subprocess.Popen('java -jar ../Encoding_Module/fastMod.jar', shell=True)
    try:
        env = Environment()
        env.pass_info_to_java()
        run_test()
    finally:
        env.gateway.shutdown()
        javaAppProcess.kill()