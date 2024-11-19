from nim import SARSA, QLearning, train, play

play(train(player = QLearning(), n_episodes = 0))