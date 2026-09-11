# Classical Reinforcement Learning Game

Part 1 of the reinforcement learning project, built with Python and Pygame.
Tabular Q-Learning and SARSA agents learn to collect items and avoid hazards in
seven gridworld levels. Later levels add moving monsters and a comparison of
Q-Learning with and without intrinsic reward.

## Quick Start

Use Python 3.13. Run these commands from the project root on Windows:

```powershell
py -3.13 -m pip install pygame matplotlib
py -3.13 -B main.py
```

The game loads the saved Q-tables in `results`; starting the game does not train
the agents. Press `T` to select Q-Learning, then `Space` to run the saved policy.
Agent playback uses epsilon 0, with random selection between tied best actions.

### Controls

- `W`, `A`, `S`, `D`: Move the player
- `E`: Go to the next level
- `Q`: Go to the previous level
- `T`: Cycle through None, Q-Learning, and SARSA. Levels 0 and 6 offer only None and Q-Learning
- `Space`: Start or pause the selected agent

Changing levels resets the episode and pauses the agent. To replay a completed
level, move to a neighboring level and return. Changing the algorithm with `T`
does not reset the episode, so reset before comparing two agents from the start.
For an agent demonstration, start from a fresh level without using manual movement.

Level 6 loads the Q-table trained with intrinsic reward. The without-intrinsic
condition is recorded separately in the training logs, not offered as a GUI mode.

## Training Commands

These commands train agents and overwrite the corresponding saved Q-tables.
Result-generation commands also overwrite their CSV files and graphs. Back up
`results` or use a separate project copy before rerunning them.

- Level 0 Q-Learning: `py -3.13 -B -m qlearning.qLearningResults`
- Level 1 SARSA: `py -3.13 -B -m sarsa.sarsaResults`
- Level 1 Q-Learning and SARSA training and comparison: `py -3.13 -B -m evaluation.compareLv1Policy`
- Levels 2 and 3: `py -3.13 -B -m evaluation.level2And3Results`
- Levels 4 and 5: `py -3.13 -B -m evaluation.level4And5Results`
- Level 6 Intrinsic Reward: `py -3.13 -B -m evaluation.level6IntrinsicResults`

The Level 1 comparison command saves both Q-tables and prints evaluations; it
does not regenerate their training CSV files or graphs. The other commands save
their training CSV files and graphs in `results`.

The Level 6 command trains both conditions but saves only the with-intrinsic
Q-table. Some plotting scripts label the raw item-score reference as
`Maximum Reward`; actual episode returns also include step penalties.

To watch the saved Level 0 policy without training:

```powershell
py -3.13 -B -m qlearning.qLearningDemo
```

## Saved-Model Evaluation

The following results were checked using the current maps, saved Q-tables,
epsilon 0, and seed 42. Each entry is one completed evaluation episode, not a
training average or a guarantee of success on every run.

| Level | Q-Learning                                  | SARSA                  |
| ----- | ------------------------------------------- | ---------------------- |
| 0     | Completed in 18 steps                       | Not offered in the GUI |
| 1     | Completed in 17 steps                       | Completed in 21 steps  |
| 2     | Completed in 49 steps                       | Completed in 49 steps  |
| 3     | Completed in 43 steps                       | Completed in 43 steps  |
| 4     | Completed in 18 steps                       | Completed in 18 steps  |
| 5     | Completed in 19 steps                       | Completed in 19 steps  |
| 6     | Completed in 46 steps with intrinsic reward | Not offered in the GUI |

Both Level 1 agents reached the apple without entering a hazard tile. Levels 4
and 5 include stochastic monster movement, so evaluation paths and outcomes can
vary with the random seed. Level 5 uses two apples and one monster.

### Levels 4 and 5 Training Results

Each run contains 20,000 training episodes with seed 42. The values below are
success rates over the final 300 episodes, not individual points on the
50-episode moving-average curves.

| Level | Q-Learning |   SARSA |
| ----- | ---------: | ------: |
| 4     |     98.33% | 100.00% |
| 5     |     97.67% |  96.67% |

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

## State and Reward Design

Level 0 uses the player's position as its state. Levels 1 to 6 also track
collected apples, keys, opened chests, and the number of held keys. Levels 4 and
5 include monster positions; Level 6 uses the same state format with no monsters.

The training environment uses these rewards:

- Collect an apple: +1, awarded once per apple.
- Open a chest with a key: +2, awarded once per chest; the key is consumed.
- Collect a key: no direct reward.
- Each nonfatal action: -0.01, including actions blocked by a wall or boundary.
- Death from a hazard or monster: -1, ending the episode.
- Complete a level: no additional reward.

An episode is complete when all apples have been collected and all chests have
been opened. In Levels 4 and 5, the monster has a 40% chance of moving to a valid
neighboring tile after an agent action. Collisions are checked before and after
the monster moves.

The GUI score counts item points only. Training and evaluation returns also
include action penalties. For example, completing Level 2 in 49 steps gives
`4 - 0.01 * 49 = 3.51`.

## Learning Settings

The learning parameters are stored in `classicalRLSettings.json`.

| Setting                        | Value | Levels |
| ------------------------------ | ----: | ------ |
| Base Episodes                  |  3000 | 0-3, 6 |
| Monster Episodes               | 20000 | 4-5    |
| Alpha                          |   0.2 | All    |
| Gamma                          |  0.95 | All    |
| Epsilon Start                  |   1.0 | All    |
| Epsilon End                    |  0.05 | All    |
| Base Epsilon Decay Episodes    |  2700 | 0-3, 6 |
| Monster Epsilon Decay Episodes | 18000 | 4-5    |
| Maximum Steps per Episode      |   400 | All    |
| Random Seed                    |    42 | All    |
| Intrinsic Reward Strength      | 0.001 | 6      |

Q-Learning and SARSA use the same settings when they are compared on the same level. Levels 4 and 5 use more episodes because monster positions increase the state space.

## Level 6 Intrinsic Reward

Level 6 uses a long 10x10 sparse-reward maze. The apple is 46 steps away from the starting position.

The intrinsic reward is calculated as:

`intrinsicReward = intrinsicRewardStrength / sqrt(n(s) + 1)`

- The bonus is calculated for the next state reached after an action.
- `n(s)` is the number of previous visits to that state during the episode.
- The counter resets each episode, with the initial state counted as one visit.
- Both conditions use identical environment reward rules.
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
==========================================================================================

## Contribution

### SeungUk Kim (s4028530)

- Contributed to the Part 1 Q-Learning and SARSA implementation and testing across Levels 0 to 6.
- Trained and evaluated the agents, checked saved Q-tables, and compared step counts, rewards, and success rates.
- Worked on the Level 6 sparse-reward maze and count-based intrinsic reward comparison.
- Prepared the Part 1 report sections and result figures, and updated the README with the final implementation and results.
- Prepared the demonstration and explanation of Levels 4, 5, and 6.

## AI Acknowledgment

Common:

- ChatGPT advised which code sections needed to be built and guided the work order.
- ChatGPT helped organize `README.md` to explain the project and execution instructions clearly.
- ChatGPT assisted with checking code, saved-model evaluations, training logs, and report figures.

Level 6:

- The initial Level 6 results did not show a meaningful improvement when intrinsic reward was used.
- ChatGPT was actively used to review the state visit counter, maze design, and object placement.
- ChatGPT helped compare multiple maze layouts, intrinsic reward settings, and random seeds.
- Based on these tests, Level 6 was changed to a long sparse-reward maze using a static map.
- # I ran and checked the final 3,000-episode results, graph, and game behavior.
