import math
import random
import time
from typing import List


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
        actions = list(Nim().avaliable_actions(old_state))
        new_action = random.choice(actions)
        best_future = self.get_value(old_state, new_action)
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
        actions = list(Nim().avaliable_actions(state))
        
        # precisa ver se tem ações na lista?

        if epsilon and random.random() < self.epsilon:
            # Choose a random available action 
            return random.choice(actions)

        max_value = float("-inf") # declare a infinity float for max_value so i can use it
        best_actions = []       
        # pick the best action 
        for action in actions:
            q_value = self.get_value(state, action)
            if q_value > max_value:
                max_value = q_value
                best_actions = [action]
            elif q_value == max_value:
                best_actions.append(action)

        return random.choice(best_actions) # choose the best random choice

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
        # Initialize Q-learning with Q-values, learning rate, and exploration rate
        self.q = dict() # Q-value table
        self.alpha = alpha # Learning rate
        self.epsilon = epsilon # Exploration rate

    def update_model(self, old_state, action, new_state, reward):

        '''
            Update Q-learning model, given and old state, an action taken
            in that state, a new resulting state, and the reward received
            from taking that action.
        '''
        # Update Q-values based on the action taken and reward received
        old_q = self.get_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_value(old_state, action, old_q, reward, best_future)

    def get_value(self, state, action):

        '''
            Return the Q-value for the state 'state' and the action 'action'.
            If no Q-value exists yet in 'self.q', return 0.
        '''
        # Get the Q-value for a specific state-action pair
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
        # Update Q-value using the Q-learning update rule
        key = (tuple(old_state), action)
        new_q = old_q + self.alpha * (reward + future_rewards - old_q) #Q(s,a)←Q(s,a)+α×(reward+future_rewards−Q(s,a))
        self.q[key] = new_q

    def best_future_reward(self, state):

        '''
            Given a state 'state', consider all possible '(state, action)'
            pairs available in that state and return the maximum of all
            of their Q-values.

            Use 0 as the Q-value if a '(state, action)' pair has no
            Q-value in 'self.q'. If there are no available actions
            in 'state', return 0.
        '''
        # Get the maximum Q-value for all possible actions in a state
        values = []
        actions = Nim().avaliable_actions(state)
        if not actions:
            return 0
        # Get the max Q-value for all actions in the current state
        for action in actions:
            values.append(self.get_value(state, action))
        max_value = max(values)
        return max_value       

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
        # Choose an action using epsilon-greedy strategy
        actions = list(Nim().avaliable_actions(state))
        
        # If no available actions, return None
        if not actions:
            return None
        q_values = {}
        
        for action in actions:
            q_values[action] = self.get_value(state, action)
        max_q = max(q_values.values())
        
        if epsilon and random.uniform(0, 1) < self.epsilon:
            # Choose a random action with probability epsilon
            return random.choice(actions)
        else:
            # Greedy action selection (best action)
            for action, q in q_values.items():
                if q == max_q:
                    best_actions = action
        return best_actions

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
        avaliable_actions = Nim().avaliable_actions(game.piles)

        # let human make a move
        if game.player == human:
            print('Your turn')
            while True:
                pile = int(input('Choose a pile: '))
                count = int(input('Choose a count: '))
                if (pile, count) in avaliable_actions:
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
            break
def play_sarsa_vs_qlearning(sarsa, qlearning):
    game = Nim()

    while True:
        print("\nCurrent piles:")
        for i, pile in enumerate(game.piles):
            print(f"Pile {i}: {pile}")

        avaliable_actions = Nim().avaliable_actions(game.piles)

        if game.player == 0:
            print("SARSA's turn")
            state = tuple(game.piles)
            action = sarsa.choose_action(state, epsilon=False)
            if action not in avaliable_actions:
                print("Invalid action chosen by SARSA! Skipping turn.")
                continue
            pile, count = action
            print(f"SARSA chose to take {count} from pile {pile}.")
        else:
            print("Q-Learning's turn")
            state = tuple(game.piles)
            action = qlearning.choose_action(state, epsilon=False)
            if action not in avaliable_actions:
                print("Invalid action chosen by Q-Learning! Skipping turn.")
                continue
            pile, count = action
            print(f"Q-Learning chose to take {count} from pile {pile}.")

        game.move((pile, count))

        if game.winner is not None:
            print("\nGAME OVER")
            winner = "SARSA" if game.winner == 0 else "Q-Learning"
            print(f"Winner is {winner}!")
            break