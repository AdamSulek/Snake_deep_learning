# Snake_deep_learning

The aim of this project is automatically play a snake game using a neural
network and genetic algorythm in Python.

The snake brain - represents by neural network contains 26 neurons
with information about situation on a game-map, where:
    direction of the food: 8 neurons
    direction and angel between head and food: 2 neurons 
    distance to wall: 4 nuerons 
    direction of the snake moving: 4 nuerons 
    direction of the snake body: 8 neurons 

The second layer was choosen to be sufficient in the network
architecture as hidden layer.

The third layer is output layer with decision direction:
  0 - left, 1 - forword, 2 - right.

This project used tensorflow library to built neural network
and pygame library to show the results of self-teaching by snake.
