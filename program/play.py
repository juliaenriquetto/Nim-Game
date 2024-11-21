from nim import SARSA, QLearning, train, play, play_sarsa_vs_qlearning

#play(train(player = SARSA(), n_episodes = 1000))

#play(train(player = QLearning(), n_episodes = 1000))

play_sarsa_vs_qlearning(train(player = SARSA(), n_episodes = 500), train(player = QLearning(), n_episodes = 500))