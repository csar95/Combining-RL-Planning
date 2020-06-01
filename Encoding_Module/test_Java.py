import exmod
import time
import json

from py4j.java_gateway import JavaGateway
from py4j.java_collections import SetConverter

# i = exmod.say_hello("Test message")
# i = exmod.add(1.1, 2.2)

allActions = {
    '(action1 a a a)': {
        'reward': {'(reward_a1)':9},
        'precondition': {'(precond_a1)':1,'(precond_a2)':0},
        'effect': {'(effect_a1)':1,'(effect_a2)':0}
    },
    '(action2 b b)': {
        'reward': {'(reward_b1)':15},
        'precondition': {'(precond_b1)':1,'(precond_b2)':0},
        'effect': {'(effect_b1)':1,'(effect_b2)':0}
    }
}

state = {'(precond_a1)':0,'(precond_a2)':0,'(precond_b2)':0}

immutableProps = frozenset(['(precond_b1)'])

# i = exmod.get_legal_actions(state, immutableProps, allActions)
#
# print(set(i))

gateway = JavaGateway()

# s = gateway.jvm.java.util.HashSet()
#
# for elem in immutableProps:
#     s.add(elem)

s = SetConverter().convert(immutableProps, gateway._gateway_client)

fastMod = gateway.entry_point

fastMod.set_all_actions(json.dumps(allActions))
fastMod.set_immutable_props(s)

start_time = time.time()
action = fastMod.get_random_legal_action(json.dumps(state))
print(time.time() - start_time)

print(action)

times = []
for _ in range(1000):
    start_time = time.time()
    fastMod.get_random_legal_action(json.dumps(state))
    times.append(time.time() - start_time)

print(sum(times)/len(times))
