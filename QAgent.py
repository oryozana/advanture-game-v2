import numpy as np

import Map
import Player
from Constants import *


class QAgent(Player):
    def __init__(self, map: Map, screen):
        self.__init__(map, screen)
        self.q_table = self.generate_q_table()
        self.actions = {"jump", "reverse_gravity"}
        self.stats = np.arange(MAP_ROWS * MAP_COLS).reshape(MAP_ROWS, MAP_COLS)

    def generate_q_table(self):
        tmp_numpy = np.zeros((MAP_ROWS, MAP_COLS), dtype=int)

        for row in range(len(self.map)):
            for col in range(len(self.map)):
                tile = self.map.get_tiles()[row][col]

                if tile.getType() == "O":
                    tmp_numpy[row][col] = -1
                elif row == MAP_END:
                    tmp_numpy[row][col] = MAP_ROWS * MAP_ROWS

                elif tile.getType() == "B":
                    tmp_numpy[row][col] = 0

                elif tile.getType() == "C" and tile.getImgSrc() == COLLIDER_COLORS["R"]:
                    tmp_numpy[row][col] = 5
                elif tile.getType() == "C":
                    tmp_numpy[row][col] = 1

        return tmp_numpy

    def get_available_actions(self):
        available_actions = []

        if self.changeable:
            available_actions.append("reverse_gravity")
        if self.character.onGround():
            available_actions.append("jump")

        return available_actions

    def get_next_state(self):
        pass

    def get_best_route(self):
        state = 0
        route = [0]
        for i in range(MAP_ROWS):
            # execute the map index of the state
            state_location = np.argwhere(self.states == state)[0]

            # calc best action
            action_index = np.argmax(self.q_table[state])  # What is action index ?

            # move according to the action
            # if
            #
            #
            # if action_index == 0 or action_index == 2:  # Left or Right
            #     next_x = state_location[0]
            #     next_y = state_location[1] + move_actions[action_index]
            # else:  # "Up" or "Down"
            #     next_x = state_location[0] + move_actions[action_index]
            #     next_y = state_location[1]

            # Update route and next state
            next_state = self.states[next_x, next_y]
            route.append(next_state)
            state = next_state

            if MAP_END * MAP_COLS - MAP_ROWS <= next_state <= MAP_END * MAP_COLS:
                return route
        return "Fail to find route"

    def get_max_action(self, state):
        '''
        Get the action with the maximum potential reward
        return only legal action
        '''
        available_actions = self.get_available_actions()

        action_value = np.max(self.q_table[state, available_actions])
        action = np.argwhere(self.q_table[state, ] == action_value)

        for act in action:
            if act[0] in available_actions:
                return act[0]
        return None

    def train(self):
        # Hyperparameters
        n_trials = 1000
        n_steps = 500
        alpha = 0.85
        gamma = 0.6
        epsilon = 0.8

        # Learning loop
        for i in range(n_trials):
            state = 0
            action = None
            for j in range(n_steps):
                # get only available actions
                exp_exp_tradeoff = random.uniform(0, 1)

                if exp_exp_tradeoff > epsilon:
                    action = self.get_max_action(state)
                else:
                    action = np.random.choice(self.get_available_actions())

                # Calculate reward and next state
                next_state, reward = self.get_next_state(state, action)

                current_value = self.q_table[state, action]
                next_max_value = np.max(self.q_table[next_state, :])
                # Update table

                self.q_table[state, action] = (1 - alpha) * current_value + alpha * (reward + gamma * next_max_value)
                # Update state
                state = next_state

                if MAP_END * MAP_COLS - MAP_ROWS <= next_state <= MAP_END * MAP_COLS:  # End point
                    break
