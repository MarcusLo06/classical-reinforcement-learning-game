# classical-reinforcement-learning-game

This game project implement Q learning and SARSA in a gridworld created in Python's pygame library.

It implements Q-Learning and SARSA agents across Levels 0 to 6. Each level introduces different reinforcement learning tasks, including hazards, collectible items, moving monsters, and intrinsic rewards.

## Installation

This project uses Python 3.13, Pygame, and Matplotlib.

py -3.13 -m pip install pygame matplotlib
py -3.13 -B main.py

### Controls

- `W`, `A`, `S`, `D`: Move the player
- `E`: Go to the next level
- `Q`: Go to the previous level

## Training and Evaluation

- Level 0 Q-Learning: `py -3.13 -B -m qlearning.qLearningResults`
- Level 0 Demo: `py -3.13 -B -m qlearning.qLearningDemo`
- Level 1 SARSA: `py -3.13 -B -m sarsa.sarsaResults`
- Level 1 Policy Comparison: `py -3.13 -B -m evaluation.compareLv1Policy`
- Levels 2 and 3: `py -3.13 -B -m evaluation.level2And3Results`
- Levels 4 and 5: `py -3.13 -B -m evaluation.level4And5Results`
- Level 6 Intrinsic Reward: `py -3.13 -B -m evaluation.level6IntrinsicResults`

Training CSV files and graphs are saved in the `results` folder.

## Level Summary

| Level   | Description                                                               |
| ------- | ------------------------------------------------------------------------- |
| Level 0 | Basic Q-Learning with one apple and shortest-path learning                |
| Level 1 | Q-Learning and SARSA comparison around hazard tiles                       |
| Level 2 | Multiple apples, one key, and one chest                                   |
| Level 3 | Multiple collectible items in a more complex map                          |
| Level 4 | One moving monster with probabilistic movement                            |
| Level 5 | A more difficult map with one moving monster                              |
| Level 6 | Sparse-reward maze comparing Q-Learning with and without intrinsic reward |

## Learning Settings

The learning parameters are stored in `classicalRLSettings.json`.

| Setting                   | Value |
| ------------------------- | ----: |
| Episodes                  |  3000 |
| Alpha                     |   0.2 |
| Gamma                     |  0.95 |
| Epsilon Start             |   1.0 |
| Epsilon End               |  0.05 |
| Epsilon Decay Episodes    |  2700 |
| Maximum Steps per Episode |   400 |
| Random Seed               |    42 |
| Intrinsic Reward Strength | 0.001 |

The same learning settings are used when comparing the agents.

## Level 6 Intrinsic Reward

Level 6 uses a long 10x10 sparse-reward maze. The apple is 46 steps away from the starting position.

The intrinsic reward is calculated as:

`intrinsicReward = intrinsicRewardStrength / sqrt(n(s) + 1)`

- `n(s)` is the number of visits to the current state during the episode.
- The state visit counter is reset at the start of each episode.
- The original environment reward is not changed.
- `learningReward = environmentReward + intrinsicReward` is used for the Q-Learning update.

## Level 6 Results

| Metric                             | Without Intrinsic Reward | With Intrinsic Reward |
| ---------------------------------- | -----------------------: | --------------------: |
| Total Successful Episodes          |                      399 |                  2461 |
| Episode Reaching 80% Success Rate  |                     2668 |                   584 |
| Episode Reaching 100% Success Rate |                     2686 |                   599 |
| Last 300 Episode Success Rate      |                     100% |                  100% |
| Last 300 Average Steps             |                    48.52 |                 48.34 |

The agent using intrinsic reward reached a high success rate much earlier. The intrinsic reward encouraged the agent to explore new states before finding the distant environment reward.

## AI Acknowledgement

Common:

- ChatGPT advised which code sections needed to be built and guided the work order.
- ChatGPT helped organise `README.md` to explain the project and execution instructions clearly.

Level 6:

- The initial Level 6 results did not show a meaningful improvement when intrinsic reward was used.
- ChatGPT was actively used to review the state visit counter, maze design, and object placement.
- ChatGPT helped compare multiple maze layouts, intrinsic reward settings, and random seeds.
- Based on these tests, Level 6 was changed to a long sparse-reward maze using a static map.
- I ran and checked the final 3000-episode results, graph, and game behaviour.
