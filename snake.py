from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Activation
import tensorflow as tf
import numpy as np
import os
#turn-off the warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


class SnakeBrain():
    def __init__(self):
        '''
            This class create model of snake brain.
        '''
        self.brain = Sequential()
        self.brain.add(Dense(16, input_dim=26, activation='sigmoid'))
        self.brain.add(Dense(16, activation='sigmoid'))
        self.brain.add(Dense(3, activation='sigmoid'))
        self.brain.add(Activation("softmax"))
        self.brain.compile(optimizer="adam",
                           loss='mean_squared_error',
                           metrics=['accuracy'])

    def get_genotype(self):
        '''
            This function return weights of neural networks.
        '''
        return self.brain.get_weights()

    def make_decision(self, input_data):
        '''
            model.predict built-in function try out the model
            from the training data passed in argument.
        '''
        return self.brain.predict(input_data)

    def set_genotype(self, genotype):
        '''
            Setter function, built-in.
        '''
        self.brain.set_weights(genotype)

    def save_genotype(self, file):
        self.brain.save_weights(file)

    def load_genotype(self, file):
        self.brain.load_weights(file)

if __name__ == "__main__":
    Steve = SnakeBrain()
    Anna = SnakeBrain()

    situation_on_map = np.random.random_sample((1, 26))
    print("situation_on_map: {}".format(situation_on_map))

    steve_decision = Steve.make_decision(situation_on_map)
    print("steve_decision: {}".format(steve_decision))

    anna_decision = Anna.make_decision(situation_on_map)
    print("anna_decision: {}".format(anna_decision))

    print("Steve genotype is changed by Anna genotype")
    genotype = Anna.get_genotype()
    Steve.set_genotype(genotype)

    print("Decision after genotype changed")
    print("Anna: {}".format(Anna.make_decision(situation_on_map)))
    print("Steve: {}".format(Steve.make_decision(situation_on_map)))

    print(type(anna_decision))
    print(np.where(anna_decision == np.amax(anna_decision)))
    print(np.where(anna_decision == np.amax(anna_decision))[1][0])
