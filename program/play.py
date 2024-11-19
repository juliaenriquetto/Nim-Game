from nim import SARSA, QLearning, train, play

#play(train(player = SARSA, n_episodes = 0))

play(train(player = QLearning(), n_episodes = 0))