import numpy
from keras.optimizers import Adam

from Characters.BasicCharacter import BasicCharacter
from Characters.ReversedCharacter import ReversedCharacter
from Constants import *
from Map import Map
# import tensorflow
from Player import Player
from keras.models import Sequential
import keras
from keras.layers import Dense
from collections import deque
from Camera import Camera

rewards = {
    "O": -1,
    "B": 0,
    "C": 1
}

tiles_values = {
    "O": -1,
    "B": 0,
    "C": 1
}

gravity_directions = {
    "B": 5,
    "R": -5
}

tf_values = {
    True: 1,
    False: 0
}


class Agent(Player):
    def __init__(self, map: Map, screen):
        map.update_difficulty(AI_DIFFICULTY)
        super().__init__(map, screen)

        self.actions = [0, 1, 2]
        self.states = self.initiate_states()

        self.learning_rate = 0.15
        self.batch_size = 128
        self.gamma = 0.85
        self.epsilon = 1

        self.model = self.build_model()
        self.memory = deque(maxlen=50000)

    def initiate_states(self):
        states = [X_POSITION, Y_POSITION, tf_values[False], 0, tf_values[False], tf_values[True],
                  gravity_directions["B"]]
        for row in range(10):
            for col in range(MAP_COLS):
                if self.character.getX() + row >= MAP_ROWS:
                    states.append(tiles_values["B"])
                else:
                    states.append(tiles_values[self.map.get_tiles()[self.character.getX() + row][col].getType()])

        return states

    def get_available_actions(self):
        available_actions = [0]  # "none"

        if self.changeable:
            available_actions.append(1)  # "reverse_gravity"
        if self.character.onGround():
            available_actions.append(2)  # "jump"

        return available_actions

    def update_states(self):
        self.states[0] = self.character.getX()
        self.states[1] = self.character.getY()
        self.states[2] = tf_values[self.jumping]
        self.states[3] = self.jump_counter
        self.states[4] = tf_values[self.falling]
        self.states[5] = tf_values[self.changeable]
        self.states[6] = gravity_directions[self.character.type()]

    def update_actions(self):
        self.actions = self.get_available_actions()

    def build_model(self):
        model = Sequential()
        model.add(Dense(len(self.states), activation='relu', input_shape=(len(self.states),)))

        model.add(Dense(128, activation='selu'))
        model.add(Dense(64, activation='tanh'))
        model.add(Dense(32, activation='sigmoid'))
        model.add(Dense(16, activation='elu'))
        model.add(Dense(8, activation='selu'))

        model.add(Dense(len(self.actions), activation='softmax'))
        model.compile(loss='mse', optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate))
        return model

    def _save_model(self, model_name):
        self.model.save(model_name)

    def _load_model(self, model_name):
        return keras.models.load_model(model_name)

    def _update_memory(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def _act(self, state):
        actions = self.model.predict(numpy.reshape(state, (1, -1)))
        exp_exp_tradeoff = random.uniform(0, 1)

        if exp_exp_tradeoff > self.epsilon:
            action = numpy.argmax(actions[0])
        else:
            action = round(numpy.random.choice(actions[0]))
        return action

    def _learn(self, batch_size):
        # If the memory is not big enough
        if len(self.memory) < batch_size:
            return
        # Sample from the memory
        sample_batch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in sample_batch:
            est_reward = reward
            if not done:
                # learning role:
                next_state = numpy.reshape(next_state, (1, -1))
                prediction = self.model.predict(next_state)
                predicted_reward = numpy.amax(prediction[0])
                est_reward = reward + self.gamma * predicted_reward
            state = numpy.reshape(state, (1, -1))
            curr_value = self.model.predict(state)
            curr_value[0][action] = est_reward
            # Update the model
            self.model.fit(state, curr_value, epochs=1, verbose=0)
            self._update_epsilon()

    def _update_epsilon(self):
        epsilon_min = 0.05
        epsilon_decay = 0.995

        if self.epsilon > epsilon_min:
            self.epsilon = self.epsilon * epsilon_decay

    def train(self, n_train_episodes, model_name, text):
        for i in range(n_train_episodes):
            state = self.initiate_states()
            text_counter = 0
            self.score = 0
            done = False

            while not done:
                action = self._act(state)
                done = self.step(action)

                Camera.update()
                self.screen.fill((0, 0, 0))  # Clear the screen, add another layout
                Camera.draw(self.screen, self.map.get_tiles(), self.character, text, text_counter)
                pygame.display.update()  # update the screen
                text_counter += 1

                if done:
                    self.score -= 50
                    print(self.score)

                self._update_memory(state, action, self.score, self.states, done)
                state = self.states

            self._learn(self.batch_size)

            if n_train_episodes % 20 == 0:
                self._save_model(model_name)

        self._save_model(model_name)

    def test(self, n_test_trials, model_name, text):
        self.model = self._load_model(model_name)

        rewards = []
        for trial in range(n_test_trials):
            state = numpy.reshape(self.initiate_states(), (1, -1))

            self.death_handler()
            text_counter = 0
            done = False
            self.score = 0

            print("****************************************************")
            print("TRIAL ", trial)

            while not done:
                actions = self.model.predict(state)
                action = numpy.argmax(actions[0])

                Camera.update()
                self.screen.fill((0, 0, 0))  # Clear the screen, add another layout
                Camera.draw(self.screen, self.map.get_tiles(), self.character, text, text_counter)
                pygame.display.update()  # update the screen
                text_counter += 1

                done = self.step(action)
                if done:
                    print("-------------------------------------------------Trial {}#, Score: {}".format(trial,
                                                                                                         self.score))
            rewards.append(self.score)
        print("Score over time: " + str(sum(rewards) / n_test_trials))  # optional
        return rewards

    # def get_action(self):
    #     if numpy.random.rand() < self.epsilon:
    #         return random.choice(self.actions)
    #     state = numpy.array([self.states[key] for key in self.states.keys()])
    #     q_values = self.model.predict(state.reshape(1, -1)).flatten()
    #     return self.actions[numpy.argmax(q_values)]

    def step(self, action):
        # Perform the action in the game
        if action == "jump" or action == 0:
            self.jumping, self.jump_counter = self.character.jump(self.map, self.jumping, self.jump_counter)
            self.score -= 3

        elif action == "reverse_gravity" or action == 1:
            self.reverse_gravity()
            self.score += 3

        self.isGonnaBeKilled()
        if not self.killed:
            self.stay_alive_handler()
        # self.camera_end, self.jumping, self.jump_counter, self.falling = self.character.movement(self.map,
        # self.camera_end, self.jumping, self.jump_counter, self.falling)

        # Get the updated game state
        self.update_states()

        # Calculate the reward
        # print(self.map.get_tiles())
        # reward = rewards[self.map.get_tiles()[self.character.getX()][self.character.getY()].getType()]

        # Check if the game is over
        self.isGonnaBeKilled()
        done = self.killed or self.character.getX() == MAP_END

        if self.character.getX() == MAP_END:
            self.score += 500

        # Return the new state, reward, and done flag
        self.update_states()
        return done
