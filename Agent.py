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

rewards = {
    "O": -1,
    "B": 0,
    "C": 1
}

tiles_values = {
    "O": -50,
    "B": JUMP + 1,
    "C": 50
}

gravity_directions = {
    "B": 10,
    "R": -10
}

tf_values = {
    True: 1,
    False: 0
}


class Agent(Player):
    def __init__(self, map: Map, screen):
        super().__init__(map, screen)

        self.actions = ["jump", "reverse_gravity", "none"]
        self.states = self.initiate_states()

        self.learning_rate = 0.001
        self.batch_size = 32
        self.gamma = 0.99
        self.epsilon = 0.3

        self.model = self.build_model()
        self.memory = deque(maxlen=2000)

    def initiate_states(self):
        states = [X_POSITION, Y_POSITION, tf_values[False], 0, tf_values[False], tf_values[True], gravity_directions["B"]]
        for row in range(10):
            for col in range(MAP_COLS):
                states.append(tiles_values[self.map.get_tiles()[self.character.getX() + row][col].getType()])

        return states

    def get_available_actions(self):
        available_actions = ["none"]

        if self.changeable:
            available_actions.append("reverse_gravity")
        if self.character.onGround():
            available_actions.append("jump")

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
        model.add(Dense(len(self.states), activation='relu', input_shape=(len(self.states), )))

        model.add(Dense(16, activation='relu'))
        model.add(Dense(8, activation='relu'))
        model.add(Dense(8, activation='relu'))

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

    # def learn(self, batch_size=32, gamma=0.99):
    #     # Sample a batch of experiences from the replay buffer
    #     experiences = self.replay_buffer.sample(batch_size)
    #
    #     # Extract the state, action, reward, next_state, and done variables from the experiences
    #     states = numpy.array([e[0] for e in experiences])
    #     actions = numpy.array([e[1] for e in experiences])
    #     rewards = numpy.array([e[2] for e in experiences])
    #     next_states = numpy.array([e[3] for e in experiences])
    #     dones = numpy.array([e[4] for e in experiences])
    #
    #     # Compute the Q-values for the current states and actions
    #     q_values = self.q_network.predict(states)
    #     q_values = q_values.reshape(-1, self.num_actions)
    #     q_values = q_values[np.arange(len(q_values)), actions]
    #
    #     # Compute the target Q-values for the next states
    #     next_q_values = self.target_q_network.predict(next_states)
    #     next_q_values = next_q_values.reshape(-1, self.num_actions)
    #     max_next_q_values = np.max(next_q_values, axis=1)
    #     target_q_values = rewards + (gamma * max_next_q_values * (1 - dones))
    #
    #     # Update the Q-network weights using the target Q-values
    #     q_values = np.clip(q_values, -10, 10)  # clip the Q-values to avoid exploding gradients
    #     target_q_values = np.clip(target_q_values, -10, 10)  # clip the target Q-values
    #     self.q_network.train_on_batch(states, target_q_values)
    #
    #     # Update the target Q-network weights
    #     self.update_target_q_network()

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

    def train(self, n_train_episodes, model_name):
        for i in range(n_train_episodes):
            state = self.initiate_states()
            done = False

            while not done:
                action = self._act(state)
                reward, done = self.step(action)

                if done:
                    reward = -10

                self._update_memory(state, action, reward, self.states, done)
                state = self.states

            self._learn(self.batch_size)

        self._save_model(model_name)

    def test(self, env, n_test_episodes, model_name):
        # TODO: create test function
        pass

    def get_action(self):
        if numpy.random.rand() < self.epsilon:
            return random.choice(self.actions)
        state = numpy.array([self.states[key] for key in self.states.keys()])
        q_values = self.model.predict(state.reshape(1, -1)).flatten()
        return self.actions[numpy.argmax(q_values)]

    def step(self, action):
        # Perform the action in the game
        if action == "jump":
            self.jumping, self.jump_counter = self.character.jump(self.map, self.jumping, self.jump_counter)

        elif action == "reverse_gravity":
            self.reverse_gravity()

        if action != "none":
            self.camera_end, self.jumping, self.jump_counter, self.falling = self.character.movement(self.map, self.camera_end, self.jumping, self.jump_counter, self.falling)

        # Get the updated game state
        self.update_states()

        # Calculate the reward
        reward = rewards[self.map.get_tiles()[self.character.getX()][self.character.getY()].getType()]

        # Check if the game is over
        done = self.killed or self.gonna_be_killed or self.character.getX() == MAP_END

        # Return the new state, reward, and done flag
        self.update_states()
        return reward, done
