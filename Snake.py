from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Activation
import tensorflow as tf
import numpy as np
import os
# wylacza warningi
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


class SnakeBrain():
    def __init__(self):
        # create model of snake brain
        self.brain = Sequential()
        self.brain.add(Dense(16, input_dim=26, activation='sigmoid'))
        self.brain.add(Dense(16, activation='sigmoid'))
        self.brain.add(Dense(3, activation='sigmoid'))
        self.brain.add(Activation("softmax"))
        self.brain.compile(optimizer="adam",
                           loss='mean_squared_error',
                           metrics=['accuracy'])

    def get_genotype(self):
        return self.brain.get_weights()

    def make_decision(self, input_data):
        return self.brain.predict(input_data)

    def set_genotype(self, genotype):
        self.brain.set_weights(genotype)

    def save_genotype(self, file):
        self.brain.save_weights(file)

    def load_genotype(self, file):
        self.brain.load_weights(file)


if __name__ == "__main__":
    Steve = SnakeBrain()
    Anna = SnakeBrain()

    sytuacja_na_mapie = np.random.random_sample((1, 26))
    print(sytuacja_na_mapie)

    print("Sytuacja na mapie")
    print(sytuacja_na_mapie)

    print("Decyzja Steve:")
    decyzja_Steve = Steve.make_decision(sytuacja_na_mapie)
    print(decyzja_Steve)

    print("Decyzja Anna:")
    decyzja_Anna = Anna.make_decision(sytuacja_na_mapie)
    print(decyzja_Anna)

    print("Zamiana genow")
    genotype = Anna.get_genotype()
    Steve.set_genotype(genotype)

    print("Decyzje po zmianie genow")
    print("Anna:")
    print(Anna.make_decision(sytuacja_na_mapie))
    print("Steve:")
    print(Steve.make_decision(sytuacja_na_mapie))

    print(type(decyzja_Anna))
    print(np.where(decyzja_Anna == np.amax(decyzja_Anna)))
    print(np.where(decyzja_Anna == np.amax(decyzja_Anna))[1][0])
