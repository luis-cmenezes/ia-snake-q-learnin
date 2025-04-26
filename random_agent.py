import random
from snake_game import SnakeGame
import pygame

class RandomAgent:
    def __init__(self):
        pass

    def select_action(self):
        return random.choice([0, 1, 2])

if __name__ == "__main__":
    game = SnakeGame()
    agent = RandomAgent()
    clock = pygame.time.Clock()

    while not game.done:
        action = agent.select_action()
        game.step(action)
        game.render()
        clock.tick(10)  # controla a velocidade de renderização

    game.close()
