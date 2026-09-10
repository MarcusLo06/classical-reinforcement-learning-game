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
- `T`: Change the RL algorithm. Levels 0 and 6 use Q-Learning only
- `Space`: Start or stop the selected agent

## Training and Evaluation

- Level 0 Q-Learning: `py -3.13 -B -m qlearning.qLearningResults`
- Level 0 Demo: `py -3.13 -B -m qlearning.qLearningDemo`
- Level 1 SARSA: `py -3.13 -B -m sarsa.sarsaResults`
- Level 1 Policy Comparison: `py -3.13 -B -m evaluation.compareLv1Policy`
- Levels 2 and 3: `py -3.13 -B -m evaluation.level2And3Results`
- Levels 4 and 5: `py -3.13 -B -m evaluation.level4And5Results`
- Level 6 Intrinsic Reward: `py -3.13 -B -m evaluation.level6IntrinsicResults`

Training CSV files and graphs are saved in the `results` folder.

To regenerate all Part I results with the current configuration:

`py -3.13 -B -m evaluation.refreshPart1Results`

Use `--output-dir PATH` to generate a separate candidate set before replacing results.
This command trains each run once and records source hashes, artifact hashes, and
saved-model evaluations in `results/trainingManifest.json`.
SARSA Level 0 is included only to refresh the existing legacy model. It is not a GUI mode.

### Current evaluation results

These results use the teammate's maps and reward rules from `4cc71a8`.
Training uses the configuration below. Evaluation uses epsilon 0 and seed 42.
No settings were tuned to obtain these results.

| Level | Q-Learning | SARSA |
| --- | --- | --- |
| 0 | Completed in 18 steps | Not offered in the GUI |
| 1 | Completed in 23 steps | Did not complete within 400 steps |
| 2 | Completed in 49 steps | Completed in 49 steps |
| 3 | Completed in 43 steps | Completed in 43 steps |
| 4 | Completed in 18 steps | Completed in 18 steps |
| 5 | Completed in 21 steps | Completed in 17 steps |
| 6 | Completed in 46 steps with or without intrinsic reward | Not offered in the GUI |

The Level 1 SARSA run is an unresolved failure, not a successful conservative policy.
It completed none of the 100 saved-model evaluations with seeds 0 to 99.
Level 5 contains two apples in this version. Its results must not be mixed with
the earlier one-apple map or its recordings.

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

| Setting                       | Value | Levels  |
| ----------------------------- | ----: | ------- |
| Base Episodes                 |  3000 | 0-3, 6  |
| Monster Episodes              | 20000 | 4-5     |
| Alpha                         |   0.2 | All     |
| Gamma                         |  0.95 | All     |
| Epsilon Start                 |   1.0 | All     |
| Epsilon End                   |  0.05 | All     |
| Base Epsilon Decay Episodes   |  2700 | 0-3, 6  |
| Monster Epsilon Decay Episodes | 18000 | 4-5     |
| Maximum Steps per Episode     |   400 | All     |
| Random Seed                   |    42 | All     |
| Intrinsic Reward Strength     | 0.001 | 6       |

Q-Learning and SARSA use the same settings when they are compared on the same level. Levels 4 and 5 use more episodes because monster positions increase the state space.

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
| Total Successful Episodes          |                     2702 |                  2702 |
| Episode Reaching 80% Success Rate  |                      408 |                   408 |
| Episode Reaching 100% Success Rate |                      508 |                   508 |
| Last 300 Episode Success Rate      |                     100% |                  100% |
| Last 300 Average Steps             |                    48.35 |                 48.35 |

The success thresholds use 50-episode moving averages. Both runs used seed 42.
Their environment rewards, completion flags, and step counts were identical.
The run with intrinsic reward had additional learning reward, but this did not
produce a measured improvement in learning speed under the current settings.

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
