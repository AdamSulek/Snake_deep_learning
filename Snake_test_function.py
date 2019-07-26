import os
import numpy as np
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def snake_test(snake_brain, map, snake_body, food_obj):
    count = 0
    snake_body.reset()
    while snake_body.alive:
        input = map.snake_collect_input(snake_body, food_obj)
        output = snake_brain.make_decision(input)
        snake_body.brain_command(output)
        snake_body.move(map, food_obj)
        count += 1
    return (evaluate(snake_body, count))


def snake_test_animation(snake_brain, map, snake_body, food_obj):
    input = map.snake_collect_input(snake_body, food_obj)
    output = snake_brain.make_decision(input)
    snake_body.brain_command(output)
    snake_body.move(map, food_obj)


def evaluate(snake_body, count):
    if snake_body.hunger == 0:
        return ((snake_body.length - 4) * 1000) + count - 1000
    else:
        return ((snake_body.length - 4) * 1000) + count


def move_translator(output):
    return np.where(output == np.amax(output))[1][0]


def find_champion(evaluation_list):
    index_val = 0
    max_val = 0
    for idx, val in enumerate(evaluation_list):
        if max_val < val:
            max_val = val
            index_val = idx
    return index_val


def find_best_champions(evaluation_list, number):
    breeding_couple = []
    for i in range(number):
        breeding_couple.append(find_champion(evaluation_list))
        evaluation_list[breeding_couple[i]] = 0
    return breeding_couple



if __name__ == "__main__":
    from Snake import SnakeBrain
    import Snake_game
    import pygame
    import sys

    snake_pop_list = []
    for i in range(20):
        Steve = SnakeBrain()
        genotype = Steve.get_genotype()
        snake_pop_list.append(genotype)

    map = Snake_game.Map(18, 18, 10, 40)
    snake_body = Snake_game.Snake(20, 20)
    snake_body.set_up()
    food_obj = Snake_game.Food(0, 0)
    food_obj.create(map)

    score_list = test_function(snake_pop_list, Steve, map, snake_body, food_obj)

    pygame.init()
    display_width = 1366
    display_hight = 450

    screen = pygame.display.set_mode((display_width, display_hight))

    snake_body.reset()
    index_val = 0
    max_val = 0
    for idx, val in enumerate(score_list):
        if max_val < val:
            max_val = val
            index_val = idx

    print(score_list)

    Steve.set_genotype(snake_pop_list[index_val])
    font = pygame.font.SysFont("Ubuntu", 64)
    score = font.render("DEAD", True, (255, 0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if snake_body.alive:
            input = map.snake_collect_input(snake_body, food_obj)
            output = Steve.make_decision(input)
            snake_body.brain_command(output)
            snake_body.move(map, food_obj)
        screen.fill((0, 0, 0))
        if not snake_body.alive:
            print("dead")
            screen.blit(score, (200, 200))
        map.map_draw(screen, snake_body, food_obj)
        pygame.time.delay(50)
        pygame.display.flip()
