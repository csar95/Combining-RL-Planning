from Learning_Module.DDQNAgent import *
from Encoding_Module.environment import *
from hyperparameters import *
import os


class Planner:

    def __init__(self, env, pathtomodel=None, reduceactionspace=False):
        self.env = env
        self.agent = DDQNAgent(env, pathtomodel)
        self.reduceactionspace = reduceactionspace

    def get_plan(self):
        plan = []

        episode_reward = 0
        step = 0
        done = False
        current_state = self.env.reset()

        while not done and step < MAX_STEPS_PLANNER:
            # Take actions greedily
            actionsQValues = self.agent.get_qs(current_state)
            legalActionsIds = self.env.get_legal_actions(current_state, self.reduceactionspace)
            # Make the argmax selection among the legal actions
            action = legalActionsIds[np.argmax(actionsQValues[legalActionsIds])]

            plan.append(self.env.allActionsKeys[action])
            new_state, reward, done = self.env.step(action)

            episode_reward += reward

            current_state = new_state
            step += 1

        return plan, episode_reward, done

    def get_real_score(self, plan):
        score = 0

        for action in plan:
            for cost in self.env.allActions[action]['reward'].values():
                score += cost

        return score

    def get_episode_reward(self, plan):
        episode_reward = 0
        self.env.reset()

        for action in plan:
            actionIdx = np.where(self.env.allActionsKeys == action)[0][0]
            new_state, reward, done = self.env.step(actionIdx)
            episode_reward += reward

        return episode_reward

    def save_plan(self, plan, pathtodata):
        if not os.path.isdir(pathtodata):
            os.makedirs(pathtodata)

        f = open(f"{pathtodata}/best_solution", 'w')

        f.write(f"Length of solution: {len(plan)} | Reward: {self.get_episode_reward(plan)} | Real score: {self.get_real_score(plan)}\n\n")
        f.write("Solution:\n")
        for action in plan:
            f.write(f"{action}\n")

        f.close()
