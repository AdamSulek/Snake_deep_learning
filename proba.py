import numpy as np
from math import atan2, degrees

list = [1, 2, 3, 4, 5]
def func(x):
    x_collsion = (0 <= x < len(list))
    if not x_collsion:
        # pass
        print("die")
    else:
        print(x_collsion)
        print("still alive")

def snake_collect_food():
    return["right", "down_right", "down", "down_left",
           "left", "top_left", "top", "top_right"]

lista1 = snake_collect_food()
lista2 = [1, 2, 3]
def snake_collect_input(lista1, lista2):
    snake_synaps = np.array([])
    snake_synaps = np.append(snake_synaps, lista1)
    snake_synaps = np.append(snake_synaps, lista2)
    # snake_synaps = np.around(snake_synaps, decimals=2)
    return np.array([snake_synaps])

if __name__ == "__main__":
    print(snake_collect_input(lista2, lista1))
    # food_angle = degrees(atan2(i - 0,
    #                            i - 0))
    for i in range(-50,50):
        for j in range(-50,50):
            food_angle = degrees(atan2(i - 0,
                                       j - 0))
        print(food_angle)
