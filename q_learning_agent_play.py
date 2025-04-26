import pygame
import numpy as np
from snake_game import SnakeGame

class QLearningAgentPlay:
    def __init__(self, q_table_file):
        self.q_table = np.load(q_table_file)

    def select_action(self, state):
        # Sempre escolhe a melhor ação após o treinamento (exploração é desligada)
        return np.argmax(self.q_table[state])

def play_game_with_trained_agent(q_table_file):
    game = SnakeGame()
    agent = QLearningAgentPlay(q_table_file)  # Sem exploração, pois queremos ver o desempenho do treinamento

    state = 0
    while not game.done:
        action = agent.select_action(state)
        next_state, reward = game.step(action)
        state = next_state
        game.render()

        # Adicionar um delay para visualização
        pygame.time.delay(100)  # Delay de 100 ms entre as ações para tornar o jogo assistível

    game.close()

if __name__ == "__main__":
    # Especifique o arquivo da tabela Q que deseja carregar (substitua o caminho conforme necessário)
    q_table_file = "/home/luis/ufu/ia-snake-q-learning/trainings/q_table.npy"
    play_game_with_trained_agent(q_table_file)
