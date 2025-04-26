from snake_game import SnakeGame
from random_agent import RandomAgent
from q_learning_agent_play import QLearningAgentPlay
import pygame
import numpy as np

def play_game_with_random_agent():
    game = SnakeGame(render=False)
    agent = RandomAgent()

    while not game.done:
        action = agent.select_action()
        game.step(action)

    return game.score  # Retorna o score do jogo

def play_game_with_trained_agent(q_table_file):
    game = SnakeGame(render=False)
    agent = QLearningAgentPlay(q_table_file)  # Sem exploração, pois queremos ver o desempenho do treinamento

    state = 0
    while not game.done:
        action = agent.select_action(state)
        state, _ = game.step(action)

    return game.score  # Retorna o score do jogo

def compare_agents(q_table_file, num_games=10):
    qlearning_scores = []
    random_scores = []

    for _ in range(num_games):
        qlearning_scores.append(play_game_with_trained_agent(q_table_file))
        random_scores.append(play_game_with_random_agent())

    avg_qlearning_score = np.mean(qlearning_scores)
    avg_random_score = np.mean(random_scores)

    max_qlearning_score = np.max(qlearning_scores)
    max_random_score = np.max(random_scores)

    print(f"Desempenho QLearning: Média: {avg_qlearning_score}, Máximo: {max_qlearning_score}")
    print(f"Desempenho Random: Média: {avg_random_score}, Máximo: {max_random_score}")

if __name__ == "__main__":
    q_table_file = "/home/luis/ufu/ia-snake-q-learning/trainings/q_table.npy"
    compare_agents(q_table_file, num_games=1000)