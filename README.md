# Snake Game with Q-Learning AI

![snake_q_learning-_online-video-cutter com_](https://github.com/user-attachments/assets/d29edc23-e372-4dc8-9297-64699f60afe1)


This repository contains an implementation of the classic Snake game with an AI agent trained using Q-Learning. The project demonstrates how reinforcement learning can be applied to teach an agent to play games autonomously.

## Table of Contents
- [Theory Overview](#theory-overview)
- [State Representation](#state-representation)
- [Reward System](#reward-system)
- [Training Process](#training-process)
- [Agent Comparison](#agent-comparison)
- [Usage](#usage)

## Theory Overview

Q-Learning is a model-free reinforcement learning algorithm that learns the value of an action in a particular state (Q-value) through exploration and exploitation. The agent updates its Q-table using the Bellman equation:

``` Q(s, a) = (1 - α) * Q(s, a) + α * [R(s, a) + γ * max(Q(s', a'))] ``` 

Where:
- `α` (lr) is the learning rate
- `γ` (gamma) is the discount factor
- `R(s, a)` is the immediate reward
- `s'` is the next state

## State Representation

The state is encoded as a 7-bit integer representing the agent's perception of its environment:

 - Bit 6: Danger forward (1 if collision imminent)
 - Bit 5: Danger left
 - Bit 4: Danger right
 - Bit 3: Food forward (1 if food is anytime in front)
 - Bit 2: Food backward
 - Bit 1: Food left
 - Bit 0: Food right

This creates 128 possible states (2^7). The direction checks are relative to the snake's current heading.

## Reward System

The reward function is designed to encourage finding food and avoiding collisions:

- `+10` for eating food
- `-10` for collision (wall or self)
- `+0.5` for moving closer to food
- `-0.5` for moving away from food

This sparse reward system helps the agent learn both short-term (avoiding death) and long-term (finding food) strategies.

## Training Process

The training follows these steps:
1. Initialize Q-table with zeros (128 states × 3 actions)
2. For each episode:
   - Reset the game state
   - While game is active:
     1. Select action (ε-greedy policy)
     2. Execute action, observe reward and new state
     3. Update Q-table using Bellman equation
     4. Transition to new state
3. Save Q-table after training

Key hyperparameters:
- `ε (eps) = 0.1` (exploration rate)
- `α (lr) = 0.1` (learning rate)
- `γ (gamma) = 0.9` (discount factor)
- `episodes = 100,000`

## Agent Comparison

| Metric                     | Q-Learning Agent        | Random Agent          |
|----------------------------|-------------------------|-----------------------|
| Average Score              | 26.201                  | 0.137                 |
| Average Steps              | 292.371                 | 42.15                 |
| Maximum Score              | 57                      | 2                     |

The Q-Learning agent significantly outperforms a random agent by:
- The Q-Learning agent outperforms the random agent by **190x** in average score
- Demonstrates strategic long-term play (292 steps/game vs 42)
- Handles complex scenarios (max score 57 vs random's 2)

## Usage

1. Train the agent (saves Q-table to file):

```bash
python q_learning_agent_train.py
```

2. Watch the trained agent play:

```bash
python q_learning_agent_play.py
```
