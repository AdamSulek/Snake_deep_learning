import Snake_game
import Snake_test_function
from Snake import SnakeBrain
import Snake_Gui
import pygame
import MutationBreading

pygame.init()

display_width = 1366
display_hight = 768

screen = pygame.display.set_mode((display_width, display_hight))

# Set up game parameters
snake_body = Snake_game.Snake(20, 20)
food_obj = Snake_game.Food(0, 0)
map = Snake_game.Map(30, 30, 15, 40)
food_obj.create(map)
snake_body.set_up()

# Set up basic data
snake_brain = SnakeBrain()
gui = Snake_Gui.GameMenu(screen, snake_brain, snake_body, food_obj, map)
population_list = MutationBreading.generation_zero(snake_brain.get_genotype())

# Intro menu
Snake_Gui.game_main_menu(screen)

while gui.operating:
    gui.game_set_up_menu()
    if gui.gen_counter != 0 and not gui.load:
        couples = Snake_test_function.find_best_champions(evaluation_list, 10)
        print(couples)
        population_list = MutationBreading.populate_mult(population_list,
                                                         couples,
                                                         gui,
                                                         gui.list_of_menu[2][1],
                                                         gui.list_of_menu[0][1],
                                                         )
    if gui.load:
        load_gen = snake_brain.get_genotype()
        population_list = MutationBreading.generation_zero(load_gen,
                                                           gui.list_of_menu[2][1],
                                                           gui.list_of_menu[0][1])
        gui.load = False
    evaluation_list = []
    progress = 0.0
    for idx, snake in enumerate(population_list):
        gui.eval = 0
        snake_brain.set_genotype(snake)
        gui.processing(progress)
        evaluation_list.append(gui.eval)
        progress = float(idx)/len(population_list)
    champion = Snake_test_function.find_champion(evaluation_list)
    gui.gen_counter += 1
    snake_brain.set_genotype(population_list[champion])
    gui.loop_chk = True
    print(evaluation_list[champion])
    print(evaluation_list)
