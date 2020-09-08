# -*- coding: utf-8 -*-
import pygame
import sys
import time
import random
from math import atan2, degrees
import numpy as np

def display_input_data(screen, snake_synaps, x, y):
    data_label = ["F_r: ", "F_rd: ", "F_d: ", "F_dl: ", "F_l: ", "F_lt: ",
                  "F_t: ", "F_tr: ", "F_dist: ", "F_angl: ", "W_r: ", "W_d: ",
                  "W_l: ", "W_t: ", "D_r: ", "D_d: ", "D_l: ", "D_t: ",
                  "B_r: ", "B_rd: ", "B_d: ", "B_dl: ", "B_l: ", "B_lt: ",
                  "B_t: ", "B_tr: "]
    for idx, val in enumerate(data_label):
        if idx > 12:
            screen.blit(font.render(val+str(snake_synaps[idx]),
                        True, Map.white), (x + 120, y + (30 * (idx-13))))
        else:
            screen.blit(font.render(val+str(snake_synaps[idx]),
                        True, Map.white), (x, y + (30 * idx)))

class GameObject():
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        # self.size = size

class Snake(GameObject):
    def set_up(self):
        self.length = 4
        self.direction = [1, 0]
        self.list_of_body = []
        self.start_x = self.pos_x
        self.start_y = self.pos_y
        self.dir_swaper = True
        self.alive = True
        self.hunger = 400
        for i in range(self.length):
            self.list_of_body.append([self.pos_x, self.pos_y])

    def detect_collision(self, map, x, y, food):
        '''
            This function detect collision of object (x, y parameter) with
            food or with self-body.
        '''
        if food.pos_x == x and food.pos_y == y:
            self.eat()
            food.eaten()
        else:
            x_collsion = (0 <= x < map.map_size)
            y_collsion = (0 <= y < map.map_size)
            for body in self.list_of_body:
                if body[0] == x and body[1] == y:
                    self.die()
            if not x_collsion or not y_collsion:
                self.die()

    def move(self, map, food):
        '''
            This function keep that moving around without food eating
            not take place to long.
        '''
        self.hunger -= 1
        if self.hunger == 0:
            self.die()
        self.pos_x += self.direction[0]
        self.pos_y += self.direction[1]
        self.detect_collision(map, self.pos_x, self.pos_y, food)
        self.list_of_body.append([self.pos_x, self.pos_y])
        if self.length < len(self.list_of_body):
            self.list_of_body.pop(0)

    def eat(self):
        self.length += 1
        if self.hunger > 1000:
            pass
        else:
            self.hunger += 300

    def die(self):
        self.alive = False

    def reset(self, reset_pos_x=None, reset_pos_y=None):
        self.hunger = 400
        self.alive = True
        self.list_of_body = []
        if reset_pos_x is None:
            self.pos_x = self.start_x
        if reset_pos_y is None:
            self.pos_y = self.start_y
        self.length = 4
        self.direction[0] = 1
        self.direction[1] = 0
        for i in range(self.length):
            self.list_of_body.append([self.pos_x, self.pos_y])

    def brain_command(self, decision):
        '''
            # 0 - left
            # 1 - forward
            # 2 - right
        '''
        option = np.where(decision == np.amax(decision))[1][0]
        if option == 0:
            if self.dir_swaper:
                self.direction[0], self.direction[1] = self.direction[1], self.direction[0]
            else:
                self.direction[0], self.direction[1] = -self.direction[1], -self.direction[0]
            self.dir_swaper = not self.dir_swaper
        elif option == 1:
            pass
        elif option == 2:
            if self.dir_swaper:
                self.direction[0], self.direction[1] = -self.direction[1], -self.direction[0]
            else:
                self.direction[0], self.direction[1] = self.direction[1], self.direction[0]
            self.dir_swaper = not self.dir_swaper

class Food(GameObject):
    def eaten(self):
        self.pos_x = random.randint(2, self.max_x - 2)
        self.pos_y = random.randint(2, self.max_y - 2)

    def create(self, map):
        self.max_x = map.map_size
        self.max_y = map.map_size
        self.pos_x = random.randint(0, map.map_size)
        self.pos_y = random.randint(0, map.map_size)

class Map():
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    block_color = (53, 115, 255)

    def __init__(self, pos_x, pos_y, element_size, map_size):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.element_size = element_size
        self.map_size = map_size
        self.map_len = map_size * element_size
        self.list_of_directions = np.array([[1, 0], [1, 1], [0, 1], [-1, 1],
                                            [-1, 0], [-1, -1], [0, -1],
                                            [1, -1]])

    def draw_object(self, screen, pos_x, pos_y, color):
        tmp_x = pos_x * self.element_size + self.pos_x
        tmp_y = pos_y * self.element_size + self.pos_y
        pygame.draw.rect(screen, color, pygame.Rect(tmp_x,
                                                    tmp_y,
                                                    self.element_size,
                                                    self.element_size))

    def draw_object_border(self, screen, pos_x, pos_y, color, b_width):
        tmp_x = pos_x * self.element_size + self.pos_x
        tmp_y = pos_y * self.element_size + self.pos_y
        pygame.draw.rect(screen, color[0], pygame.Rect(tmp_x,
                                                       tmp_y,
                                                       self.element_size,
                                                       self.element_size))
        pygame.draw.rect(screen, color[1], pygame.Rect(tmp_x + b_width,
                                                       tmp_y + b_width,
                                                       (self.element_size -
                                                        2*b_width),
                                                       (self.element_size -
                                                        2*b_width)))

    def draw_map_object(self, screen, color, b_width):
        pygame.draw.rect(screen, color, pygame.Rect(self.pos_x - b_width,
                                                    self.pos_y - b_width,
                                                    self.map_len+2*b_width,
                                                    self.map_len+2*b_width))
        pygame.draw.rect(screen, Map.black, pygame.Rect(self.pos_x,
                                                        self.pos_y,
                                                        self.map_len,
                                                        self.map_len))

    def map_draw(self, screen, snake, food):
        self.draw_map_object(screen, Map.white, 3)
        self.snake_draw(screen, snake)
        self.food_draw(screen, food)

    def snake_draw(self, screen, snake):
        for body in snake.list_of_body:
            if snake.alive:
                self.draw_object_border(screen, body[0], body[1],
                                        [Map.white, Map.red], 1)
            else:
                self.draw_object_border(screen, body[0], body[1],
                                        [Map.white, Map.black], 1)

    def food_draw(self, screen, food):
        self.draw_object(screen, food.pos_x, food.pos_y, Map.block_color)

    def snake_collect_input(self, snake, food):
        '''
            This function return concatenate list from different lists.
        '''
        snake_synaps = np.array([])
        snake_synaps = np.append(snake_synaps, self.snake_collect_food(food, snake))
        snake_synaps = np.append(snake_synaps, self.snake_food_sense(snake, food))
        snake_synaps = np.append(snake_synaps, self.snake_collect_wall(snake))
        snake_synaps = np.append(snake_synaps, self.snake_collect_direction(snake))
        snake_synaps = np.append(snake_synaps, self.snake_collect_body(snake))
        snake_synaps = np.around(snake_synaps, decimals=2)
        return np.array([snake_synaps])

    def snake_collect_food(self, food, snake):
        top = 0.0
        left = 0.0
        right = 0.0
        down = 0.0
        down_left = 0.0
        down_right = 0.0
        top_right = 0.0
        top_left = 0.0
        if food.pos_x == snake.pos_x:
            if food.pos_y > snake.pos_y:
                down = 1.0
            elif food.pos_y < snake.pos_y:
                top = 1.0
        elif food.pos_y == snake.pos_y:
            if food.pos_x > snake.pos_x:
                right = 1.0
            elif food.pos_x < snake.pos_x:
                left = 1.0
        elif food.pos_x - snake.pos_x == food.pos_y - snake.pos_y:
            if food.pos_x - snake.pos_x > 0:
                down_right = 1.0
            else:
                top_left = 1.0
        elif food.pos_x - snake.pos_x == snake.pos_y - food.pos_y:
            if food.pos_x - snake.pos_x > food.pos_y - snake.pos_y:
                top_right = 1.0
            else:
                down_left = 1.0
        return[right, down_right, down, down_left,
               left, top_left, top, top_right]

    def snake_food_sense(self, snake, food):
        food_distance = (((snake.pos_x - food.pos_x)**2) +
                         ((snake.pos_y - food.pos_y)**2))**(.5)
        food_angle = degrees(atan2(snake.pos_y - food.pos_y,
                                   snake.pos_x - food.pos_x))
        if food_distance == 0.0:
            food_distance = 1.0
        return [1.0 / food_distance, food_angle / 360.0]

    def snake_collect_wall(self, snake):
        right_dist = float(self.map_size - snake.pos_x)
        down_dist = float(self.map_size - snake.pos_y)
        return [1 / right_dist, 1 / down_dist, 1 / (self.map_size - right_dist + 1),
                1 / (self.map_size - down_dist + 1)]

    def snake_collect_direction(self, snake):
        right = 0.0
        down = 0.0
        left = 0.0
        top = 0.0
        if snake.direction[0] == 1:
            right = 1.0
        elif snake.direction[0] == -1:
            left = 1.0
        elif snake.direction[1] == 1:
            down = 1.0
        elif snake.direction[1] == -1:
            top = 1.0
        return [right, down, left, top]

    def snake_collect_body(self, snake):
        top = 0.0
        left = 0.0
        right = 0.0
        down = 0.0
        down_left = 0.0
        down_right = 0.0
        top_right = 0.0
        top_left = 0.0
        for body in snake.list_of_body:
            if body[0] == snake.pos_x:
                if body[1] > snake.pos_y:
                    down = 1.0
                elif body[1] < snake.pos_y:
                    top = 1.0
            elif body[1] == snake.pos_y:
                if body[0] > snake.pos_x:
                    right = 1.0
                elif body[0] < snake.pos_x:
                    left = 1.0
            elif body[0] - snake.pos_x == body[1] - snake.pos_y:
                if body[0] - snake.pos_x > 0:
                    down_right = 1.0
                else:
                    top_left = 1.0
            elif body[0] - snake.pos_x == snake.pos_y - body[1]:
                if body[0] - snake.pos_x > body[1] - snake.pos_y:
                    top_right = 1.0
                else:
                    down_left = 1.0
        return [right, down_right, down, down_left,
               left, top_left, top, top_right]

if __name__ == "__main__":
    pygame.init()

    Map_size = (800, 550)

    speed = 150

    block_color = (53, 115, 255)

    screen = pygame.display.set_mode(Map_size)

    clock = pygame.time.Clock()

    snake = Snake(0, 0)
    food = Food(0, 0)
    map = Map(18, 18, 10, 40)
    food.create(map)
    snake.set_up()

    font = pygame.font.SysFont("Ubuntu", 16)
    score = font.render("Score:", True, Map.white)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                snake.change_dir(event)
            pygame.display.update()
        screen.fill(map.black)
        snake.move(map, food)
        map.map_draw(screen, snake, food)
        display_input_data(screen, map.snake_collect_input(snake, food), 436, 18)
        pygame.time.delay(speed)
        pygame.display.flip()
