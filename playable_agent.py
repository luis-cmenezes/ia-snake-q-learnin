import pygame
from snake_game import SnakeGame

class HumanAgent:
    def __init__(self):
        self.key_to_direction = {
            pygame.K_UP: (-1, 0),
            pygame.K_DOWN: (1, 0),
            pygame.K_LEFT: (0, -1),
            pygame.K_RIGHT: (0, 1)
        }

    def select_action(self, current_direction):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN and event.key in self.key_to_direction:
                    desired = self.key_to_direction[event.key]
                    return self._direction_to_action(current_direction, desired)

    def _direction_to_action(self, current, desired):
        if desired == current:
            return 0
        if (desired[0], desired[1]) == (-current[1], current[0]):
            return 2  # esquerda
        if (desired[0], desired[1]) == (current[1], -current[0]):
            return 1  # direita
        return 0  # ignora reversão de direção (evita suicídio)

def decode_bit_code(encoded_bit):
    # Descodificar o bit codificado para determinar o estado do jogo
    danger_forward = (encoded_bit >> 6) & 1
    danger_left = (encoded_bit >> 5) & 1
    danger_right = (encoded_bit >> 4) & 1
    food_forward = (encoded_bit >> 3) & 1
    food_backward = (encoded_bit >> 2) & 1
    food_leftward = (encoded_bit >> 1) & 1
    food_rightward = encoded_bit & 1

    # Gerar o texto de situação atual com base na decodificação
    situation = f"DF: {danger_forward} | DL: {danger_left} | DR: {danger_right} | "
    situation += f"FF: {food_forward} | FB: {food_backward} | FL: {food_leftward} | FR: {food_rightward}"

    return situation

if __name__ == "__main__":
    game = SnakeGame()
    agent = HumanAgent()

    while not game.done:
        action = agent.select_action(game.direction)
        if action is None:
            break
        encoded_bit, reward = game.step(action)
        game.render()

        situation = decode_bit_code(encoded_bit)
        font = pygame.font.Font(None, 30)
        situation_text = font.render(situation, True, (255, 255, 255))
        reward_text = font.render(f"Reward: {reward}", True, (255, 255, 255))

        game.display.blit(situation_text, (10, 10))
        game.display.blit(reward_text, (10, 40))

        pygame.display.flip()

    game.close()
