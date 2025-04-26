import pygame
import numpy as np
from snake_game import SnakeGame

class QLearningAgentTrain:
    def __init__(self, eps=0.1, lr=0.1, gamma=0.9):
        self.q_table = np.zeros((128, 3))
        self.eps = eps
        self.lr = lr
        self.gamma = gamma

    def select_action(self, state):
        if np.random.rand() < self.eps:
            return np.random.randint(3)
        return np.argmax(self.q_table[state])

    def update(self, state, action, reward, next_state):
        best_next = np.max(self.q_table[next_state]) # max(Q(s+1))
        q_s_a = self.q_table[state, action] 
        self.q_table[state, action] = (1-self.lr) * q_s_a + self.lr * (reward + self.gamma*best_next)

def train_agent(episodes=1000):
    game = SnakeGame(render=False)
    agent = QLearningAgentTrain()

    for episode in range(episodes):
        state = 0
        while not game.done:
            action = agent.select_action(state)
            next_state, reward = game.step(action)
            agent.update(state, action, reward, next_state)
            state = next_state
            # game.render()

        print(f"Episode {episode} finished.")
        print("###############################")
        # Resetar o jogo para o próximo episódio
        game.reset()

    np.save(f"/home/luis/ufu/ia-snake-q-learning/trainings/q_table.npy", agent.q_table)

    game.close()

if __name__ == "__main__":
    train_agent(episodes=100000)
