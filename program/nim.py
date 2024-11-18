import math
import random
import time


class Nim():

    def __init__(self, initial = [1, 3, 5, 7]):

        '''
            Initialize game board.
            Each game board has
                - 'piles'  : a list of how many elements remain in each pile
                - 'player' : 0 or 1 to indicate which player's turn
                - 'winner' : None, 0, or 1 to indicate who the winner is
        '''
        
        self.piles = initial.copy()
        self.player = 0
        self.winner = None

    def avaliable_actions(self, piles):
        
        '''
            self.avaliable_actions(piles) takes a 'piles' list as input
            and returns all of the available actions '(i, j)' int that state.

            Action '(i, j)' represents the action of removing 'j' items
            from pile 'i'.
        '''

        actions = set()

        for i, pile in enumerate(piles):
            for j in range(1, pile + 1):
                actions.add((i, j))

        return actions

    def other_player(self, player):

        '''
            self.other_player(plauyer) returns the player that is not
            'player'. Assumes 'player' is either 0 or 1.
        '''

        return 0 if player == 1 else 1

    def switch_player(self):

        '''
            Switch the current player to the other player.
        '''

        self.player = self.other_player(self.player)

    def move(self, action):
        
        '''
            Make the move 'action' for the current player.
            'action' must be a tuple '(i, j)'.
        '''

        pile, count = action

        # check for errors
        if self.winner is not None:
            raise Exception('Game already won.')
        else:
            if pile < 0 or pile >= len(self.piles):
                raise Exception('Invalid pile.')
            else:
                if count < 1 or count > self.piles[pile]:
                    raise Exception('Invalid number of objects.')
                
        # update pile
        self.piles[pile] -= count
        self.switch_player()

        # check the winner
        if all(pile == 0 for pile in self.piles):
            self.winner = self.player


class SARSA():

    def __init__(self, alpha = 0.5, epsilon = 0.1):

        '''
            Initialize AI with an empty SARSA dictionary,
            an alpha rate and an epsilon rate.

            The SARSA dictionary maps '(state, action)
            pairs to a Q-value.
                - 'state' is a tuple of remaining piles, e.g. [1, 1, 4, 4]
                - 'action' is a tuple '(i, j)' for an action
        '''

        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon

    def update_model(self, old_state, action, new_state, reward):

        '''
            Update SARSA model, given and old state, an action taken
            in that state, a new resulting state, and the reward received
            from taking that action.
        '''

        old_q = self.get_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_value(old_state, action, old_q, reward, best_future)

    def get_value(self, state, action):

        '''
            Return the Q-value for the state 'state' and the action 'action'.
            If no Q-value exists yet in 'self.q', return 0.
        '''        
        key = (tuple(state), action)
        if key in self.q:
            return self.q[key]
        else:
            return 0

    def update_value(self, old_state, action, old_q, reward, future_rewards):

        '''
            Update the Q-value for the state 'state' and the action 'action'
            given the previous Q-value 'old_q', a current reward 'reward',
            and an estimate of future rewards 'future_rewards'.
        '''
        key = (tuple(old_state), action)
        new_q = old_q + self.alpha * (reward + future_rewards - old_q) # Q(s, a) <- Q(s, a) + alpha*(R + gamma(Q(s', a') - Q(s, a))) - SARSA equation
        self.q[key] = new_q

    def choose_action(self, state, epsilon = True):

        '''
            Given a state 'state', return a action '(i, j)' to take.
            
            If 'epsilon' is 'False', then return the best action
            avaiable in the state (the one with the highest Q-value, 
            using 0 for pairs that have no Q-values).

            If 'epsilon' is 'True', then with probability 'self.epsilon'
            chose a random available action, otherwise chose the best
            action available.

            If multiple actions have the same Q-value, any of those
            options is an acceptable return value.
        '''


class QLearning():

    def __init__(self, alpha = 0.5, epsilon = 0.1):

        '''
            Initialize AI with an empty Q-learning dictionary,
            an alpha rate and an epsilon rate.

            The Q-learning dictionary maps '(state, action)
            pairs to a Q-value.
                - 'state' is a tuple of remaining piles, e.g. [1, 1, 4, 4]
                - 'action' is a tuple '(i, j)' for an action
        '''

        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon

    def update_model(self, old_state, action, new_state, reward):

        '''
            Update Q-learning model, given and old state, an action taken
            in that state, a new resulting state, and the reward received
            from taking that action.
        '''

        old_q = self.get_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_value(old_state, action, old_q, reward, best_future)

    def get_value(self, state, action):

        '''
            Return the Q-value for the state 'state' and the action 'action'.
            If no Q-value exists yet in 'self.q', return 0.
        '''

        raise NotImplementedError

    def update_value(self, old_state, action, old_q, reward, future_rewards):

        '''
            Update the Q-value for the state 'state' and the action 'action'
            given the previous Q-value 'old_q', a current reward 'reward',
            and an estimate of future rewards 'future_rewards'.
        '''

        raise NotImplementedError

    def best_future_reward(self, state):

        '''
            Given a state 'state', consider all possible '(state, action)'
            pairs available in that state and return the maximum of all
            of their Q-values.

            Use 0 as the Q-value if a '(state, action)' pair has no
            Q-value in 'self.q'. If there are no available actions
            in 'state', return 0.
        '''

        raise NotImplementedError

    def choose_action(self, state, epsilon = True):

        '''
            Given a state 'state', return a action '(i, j)' to take.
            
            If 'epsilon' is 'False', then return the best action
            avaiable in the state (the one with the highest Q-value, 
            using 0 for pairs that have no Q-values).

            If 'epsilon' is 'True', then with probability 'self.epsilon'
            chose a random available action, otherwise chose the best
            action available.

            If multiple actions have the same Q-value, any of those
            options is an acceptable return value.
        '''

        raise NotImplementedError


def train(player, n_episodes):

    for episode in range(n_episodes):

        print(f'Playing training game {episode + 1}')

        game = Nim()

        # keep track of last move made either player
        last = {0 : {'state' : None, 'action' : None}, 1 : {'state' : None, 'action' : None}}

        while True:

            # keep track of current state and action
            state, action = game.piles.copy(), player.choose_action(game.piles)

            # keep track of last state and action
            last[game.player]['state'], last[game.player]['action'] = state, action

            # make move
            game.move(action)
            new_state = game.piles.copy()

            # when game is over, update Q values with rewards
            if game.winner is not None:
                player.update_model(state, action, new_state, -1)
                player.update_model(last[game.player]['state'], last[game.player]['action'], new_state, 1)
                break
            # if the game is continuing, no rewards yet
            else:
                if last[game.player]['state'] is not None:
                    player.update_model(last[game.player]['state'], last[game.player]['action'], new_state, 0)

        # return the trained player
        return player


def play(ai, human = None):

    # if no player order set, chose human's order randomly
    if human is None:
        human = 0 if random.uniform(0, 1) < 0.5 else 1
        
    # create new game
    game = Nim()

    while True:

        # print contents of piles
        for i, pile in enumerate(game.piles):
            print(f"Pile {i} : {pile}")

        # compute avaiable actions
        available_actions = Nim.available_actions(game.piles)

        # let human make a move
        if game.player == human:
            print('Your turn')
            while True:
                pile = int(input('Choose a pile: '))
                count = int(input('Choose a count: '))
                if (pile, count) in available_actions:
                    break
                print('Invalid move, try again')
        # have AI make a move
        else:
            print('AI turn')
            pile, count = ai.choose_action(game.piles, epsilon = False)
            print(f'AI chose to take {count} from pile {pile}.')
        
        # make move
        game.move((pile, count))
        
        # check for winner
        if game.winner is not None:
            print('GAME OVER')
            winner = 'Human' if game.winner == human else 'AI'
            print(f'Winner is {winner}')