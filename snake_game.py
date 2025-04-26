import numpy as np
import pygame
import random

class SnakeGame:
    def __init__(self, n=15, block_size=40, render=True):
        self.n = n
        self.block_size = block_size
        self.width = n * block_size
        self.height = n * block_size
        self.reset()
        pygame.init()
        if render:
            self.display = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption('Snake')

    def reset(self):
        self.grid = np.zeros((self.n, self.n), dtype=int)
        mid = self.n // 2
        self.snake = [(mid, mid)]
        self.grid[mid, mid] = 2  # cabeça
        self.direction = (-1, 0)  # cima
        self.spawn_food()
        self.score = 0
        self.done = False

    def spawn_food(self):
        empty = list(zip(*np.where(self.grid == 0)))
        self.food = random.choice(empty)
        self.grid[self.food] = 1

    def step(self, action):
        if self.done:
            return 0, -10

        old_head = self.snake[0]
        old_dist = abs(old_head[0] - self.food[0]) + abs(old_head[1] - self.food[1])

        self._move(action)
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        # Verificar colisão com parede ou corpo
        if self._check_danger(new_head):
            self.done = True
            return 0, -10

        eat = (self.grid[new_head] == 1)
        self.snake.insert(0, new_head)
        self.grid[new_head] = 2

        if eat:
            self.score += 1
            reward = 10
            self.spawn_food()
        else:
            tail = self.snake.pop()
            self.grid[tail] = 0
            reward = self._calculate_distance_reward(new_head, old_dist)

        for segment in self.snake[1:]:
            self.grid[segment] = 3  # corpo

        encoded_bit = self._encode_state(new_head)
        return encoded_bit, reward    

    def _move(self, action):
        # 0: frente, 1: esquerda, 2: direita
        dx, dy = self.direction
        if action == 1:
            self.direction = (dy, -dx)
        elif action == 2:
            self.direction = (-dy, dx)

    def _calculate_distance_reward(self, new_head, old_dist):
        new_dist = abs(new_head[0] - self.food[0]) + abs(new_head[1] - self.food[1])
        return 0.5 if new_dist < old_dist else -0.5

    def _encode_state(self, head):
        danger_forward = self._check_danger_forward(head)
        danger_left = self._check_danger_left(head)
        danger_right = self._check_danger_right(head)
        food_forward = self._check_food_forward(head)
        food_backward = self._check_food_backward(head)
        food_leftward = self._check_food_leftward(head)
        food_rightward = self._check_food_rightward(head)
        return (danger_forward << 6) | (danger_left << 5) | (danger_right << 4) | \
            (food_forward << 3) | (food_backward << 2) | (food_leftward << 1) | food_rightward

    def render(self):
        self.display.fill((0, 0, 0))
        for x in range(self.n):
            for y in range(self.n):
                rect = pygame.Rect(y*self.block_size, x*self.block_size, self.block_size, self.block_size)
                if self.grid[x, y] == 1:
                    pygame.draw.rect(self.display, (255, 0, 0), rect)
                elif self.grid[x, y] == 2:
                    pygame.draw.rect(self.display, (0, 255, 0), rect)
                elif self.grid[x, y] == 3:
                    pygame.draw.rect(self.display, (0, 200, 0), rect)
        pygame.display.flip()

    def close(self):
        pygame.quit()

    def _check_danger_forward(self, head):
        # Verificar se há perigo na direção frente (colisão com parede ou corpo)
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        return self._check_danger(new_head)

    def _check_danger_left(self, head):
        # Verificar se há perigo na direção esquerda (colisão com parede ou corpo)
        dx, dy = self.direction
        left = (-dy, dx)
        new_head = (head[0] + left[0], head[1] + left[1])
        return self._check_danger(new_head)

    def _check_danger_right(self, head):
        # Verificar se há perigo na direção direita (colisão com parede ou corpo)
        dx, dy = self.direction
        right = (dy, -dx)
        new_head = (head[0] + right[0], head[1] + right[1])
        return self._check_danger(new_head)

    def _check_danger(self, pos):
        # Verificar colisão com as paredes ou com o corpo da cobra
        if not (0 <= pos[0] < self.n and 0 <= pos[1] < self.n):  # Fora do limite (colisão com a parede)
            return 1
        if self.grid[pos] == 2 or self.grid[pos] == 3:  # Colisão com o corpo (onde 2 é a cabeça, 3 é o corpo)
            return 1
        return 0

    def _check_food_forward(self, head):
        # Coordenadas da cabeça e comida
        head_x, head_y = head
        food_x, food_y = self.food

        # Vetor da cabeça até a comida (v_hf)
        v_hf = (food_x - head_x, food_y - head_y)

        # Vetor de direção atual (normalizado)
        dir_x, dir_y = self.direction

        # Produto escalar v_hf . direction
        dot_product = v_hf[0]*dir_x + v_hf[1]*dir_y

        # Verificar se a projeção está no mesmo sentido da direção e não é zero
        if dot_product > 0:
            return 1
        return 0
    
    def _check_food_backward(self, head):
        # Coordenadas da cabeça e comida
        head_x, head_y = head
        food_x, food_y = self.food

        # Vetor da cabeça até a comida (v_hf)
        v_hf = (food_x - head_x, food_y - head_y)

        # Vetor de direção atual (normalizado)
        dir_x, dir_y = self.direction

        # Produto escalar v_hf . direction
        dot_product = v_hf[0]*dir_x + v_hf[1]*dir_y

        # Verificar se a projeção está no sentido oposto da direção e não é zero
        if dot_product < 0:
            return 1
        return 0

    def _check_food_leftward(self, head):
        # Coordenadas da cabeça e comida
        head_x, head_y = head
        food_x, food_y = self.food

        # Vetor da cabeça até a comida (v_hf)
        v_hf = (food_x - head_x, food_y - head_y)

        # Vetor de direção atual (normalizado)
        dir_left_x, dir_left_y = [-self.direction[1], self.direction[0]]

        # Produto escalar v_hf . direction
        dot_product = v_hf[0]*dir_left_x + v_hf[1]*dir_left_y

        # Verificar se a projeção está no mesmo sentido da direção e não é zero
        if dot_product > 0:
            return 1
        return 0

    def _check_food_rightward(self, head):
        # Coordenadas da cabeça e comida
        head_x, head_y = head
        food_x, food_y = self.food

        # Vetor da cabeça até a comida (v_hf)
        v_hf = (food_x - head_x, food_y - head_y)

        # Vetor de direção atual (normalizado)
        dir_left_x, dir_left_y = [-self.direction[1], self.direction[0]]

        # Produto escalar v_hf . direction
        dot_product = v_hf[0]*dir_left_x + v_hf[1]*dir_left_y

        # Verificar se a projeção está no mesmo sentido da direção e não é zero
        if dot_product < 0:
            return 1
        return 0
