import pygame
import sys
import Snake_test_function
import json
import os


def game_main_menu(screen):
    font_big = pygame.font.SysFont("Ubuntu", 108)
    font_small = pygame.font.SysFont("Ubuntu", 32)
    color_s = (255, 255, 255)
    color_q = (255, 255, 255)
    intro = True
    fade = 0
    mid_width = screen.get_rect().center[0]
    mid_hight = screen.get_rect().center[1]
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                fade = 255
                mouse = pygame.mouse.get_pos()
                start_check_high = (((mid_width/2)+50) > mouse[0] > ((mid_width/2)-50))
                start_check_wid = (((3*(mid_hight/2))+50) > mouse[1] > ((3*(mid_hight/2))-50))
                quit_check_high = (((3*(mid_width/2))+50) > mouse[0] > ((3*(mid_width/2))-50))
                quit_check_wid = (((3*(mid_hight/2))+50) > mouse[1] > ((3*(mid_hight/2))-50))
                if start_check_high and start_check_wid:
                    intro = False
                elif quit_check_high and quit_check_wid:
                    pygame.quit()
                    sys.exit()
        screen.fill((0, 0, 0))
        mouse = pygame.mouse.get_pos()
        start_check_high = (((mid_width/2)+50) > mouse[0] > ((mid_width/2)-50))
        start_check_wid = (((3*(mid_hight/2))+50) > mouse[1] > ((3*(mid_hight/2))-50))
        quit_check_high = (((3*(mid_width/2))+50) > mouse[0] > ((3*(mid_width/2))-50))
        quit_check_wid = (((3*(mid_hight/2))+50) > mouse[1] > ((3*(mid_hight/2))-50))
        if start_check_high and start_check_wid:
            color_s = (255, 0, 0)
        else:
            color_s = (255, 255, 255)
        if quit_check_high and quit_check_wid:
            color_q = (255, 0, 0)
        else:
            color_q = (255, 255, 255)
        if fade < 255:
            pygame.time.wait(1)
            fade += 1
        Title = font_big.render("Snake deep genetic", True, (fade, fade, fade))
        title_rect = Title.get_rect()
        title_rect.center = (int(mid_width), int(mid_hight-100))
        screen.blit(Title, title_rect)
        if fade == 255:
            start = font_small.render("Start", True, color_s)
            start_rect = start.get_rect()
            start_rect.center = (int(mid_width/2), int(3*(mid_hight/2)))
            screen.blit(start, start_rect)
            quit = font_small.render("Quit", True, color_q)
            quit_rect = quit.get_rect()
            quit_rect.center = (int(3*(mid_width/2)), int(3*(mid_hight/2)))
            screen.blit(quit, quit_rect)
        pygame.display.flip()
        #print(pygame.mouse.get_pos())


class GameMenu():
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)

    def __init__(self, screen, snake_brain, snake_body, food_obj, map):
        self.operating = True
        self.load = False
        self.snake_body = snake_body
        self.snake_brain = snake_brain
        self.food_obj = food_obj
        self.map = map
        self.font_big = pygame.font.SysFont("Ubuntu", 32)
        self.font_small = pygame.font.SysFont("Ubuntu", 24)
        self.gen_counter = 0
        self.screen = screen
        self.chg = 5
        self.stp = 0
        self.eval = 0
        self.auto_check = False
        self.loop_chk = True
        self.game_clock = 0
        self.next_color = (255, 255, 255)
        self.screen_mid = screen.get_rect().center
        self.list_of_menu = [["Mutation %", 0.1, [int(self.screen_mid[0]*1.5),
                                                  250]],
                             ["Speed", 10, [int(self.screen_mid[0]*1.5), 425]],
                             ["Population", 1000, [int(self.screen_mid[0]*1.5),
                                                   600]]]
        self.list_of_buttons = [["leftMutation", "mutation_decrement_action",
                                 "left_arrow", [self.list_of_menu[0][2][0]-100,
                                                self.list_of_menu[0][2][1]],
                                 (255, 255, 255)],
                                ["rightMutation", "mutation_increment_action",
                                 "right_arrow", [self.list_of_menu[0][2][0]+100,
                                                 self.list_of_menu[0][2][1]],
                                 (255, 255, 255)],
                                ["leftSpeed", "speed_decrement_action",
                                 "left_arrow", [self.list_of_menu[1][2][0]-100,
                                                self.list_of_menu[1][2][1]],
                                 (255, 255, 255)],
                                ["rightSpeed", "speed_increment_action",
                                 "right_arrow", [self.list_of_menu[1][2][0]+100,
                                                 self.list_of_menu[1][2][1]],
                                 (255, 255, 255)],
                                ["leftPopulation", "population_decrement_action",
                                 "left_arrow", [self.list_of_menu[2][2][0]-100,
                                                self.list_of_menu[2][2][1]],
                                 (255, 255, 255)],
                                ["rightPopulation", "population_increment_action",
                                 "right_arrow", [self.list_of_menu[2][2][0]+100,
                                                 self.list_of_menu[2][2][1]],
                                 (255, 255, 255)],
                                ["NextGen", "next_button_action",
                                 "Next Gen", [self.screen_mid[0]*2-100,
                                              self.screen_mid[1]*2-50],
                                 (255, 255, 255)],
                                ["Reset", "reset_action",
                                 "Reset", [100, self.screen_mid[1]*2-50],
                                 (255, 255, 255)],
                                ["Auto gen", "auto_next_button_action",
                                 "Auto gen", [self.screen_mid[0]+100,
                                              self.screen_mid[1]*2-50],
                                 (255, 255, 255)],
                                ["Save", "save_action",
                                 "Save", [200, self.screen_mid[1]*2-50],
                                 (255, 255, 255)],
                                ["Load", "load_action",
                                 "Load", [300, self.screen_mid[1]*2-50],
                                 (255, 255, 255)]]

    def display_buttons(self):
        for button in self.list_of_buttons:
            if button[2] == "left_arrow":
                self.left_arrow(button[3][0], button[3][1], button[4])
            elif button[2] == "right_arrow":
                self.right_arrow(button[3][0], button[3][1], button[4])
            else:
                self.text_button(button[2], button[3][0],
                                 button[3][1], button[4])

    def display_menu(self):
        for menu in self.list_of_menu:
            name_rend = self.font_big.render(menu[0], True, GameMenu.white)
            value_rend = self.font_big.render(str(menu[1]), True, GameMenu.white)
            name_rect = name_rend.get_rect()
            value_rect = value_rend.get_rect()
            name_rect.center = (menu[2][0], menu[2][1]-75)
            value_rect.center = (menu[2][0], menu[2][1])
            self.screen.blit(name_rend, name_rect)
            self.screen.blit(value_rend, value_rect)

    def game_set_up_menu(self):
        self.game_clock = 0
        self.snake_body.reset()
        while self.loop_chk:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.check_mouse_position()
                    self.click_button()
            if self.snake_body.alive and self.game_clock == self.list_of_menu[1][1]:
                input = self.map.snake_collect_input(self.snake_body, self.food_obj)
                output = self.snake_brain.make_decision(input)
                self.snake_body.brain_command(output)
                self.snake_body.move(self.map, self.food_obj)
                self.game_clock = 0
            if self.auto_check and not self.snake_body.alive:
                self.loop_chk = False
            self.game_clock += 1
            self.screen.fill(GameMenu.black)
            self.draw_line()
            self.check_mouse_position()
            self.map.map_draw(self.screen, self.snake_body, self.food_obj)
            self.display_generation_label()
            self.display_menu()
            self.display_buttons()
            pygame.time.wait(5)
            pygame.display.flip()

    def processing(self, progress):
        self.snake_body.reset()
        count = 0
        while self.snake_body.alive:
            Snake_test_function.snake_test_animation(self.snake_brain,
                                                     self.map,
                                                     self.snake_body,
                                                     self.food_obj)
            count += 1
            self.anim_clock()
            self.screen.fill(GameMenu.black)
            self.loading_animaiton(int(self.screen_mid[0]*1.5),
                                   self.screen_mid[1], self.stp)
            self.progress_animation(progress)
            self.map.map_draw(self.screen, self.snake_body, self.food_obj)
            pygame.display.flip()
        self.eval = Snake_test_function.evaluate(self.snake_body, count)

    def breeding_anim(self):
        self.anim_clock()
        self.screen.fill(GameMenu.black)
        pygame.draw.polygon(self.screen, (self.stp, 0, 0),
                            [(self.screen_mid[0], self.screen_mid[1]),
                             (self.screen_mid[0]+15, self.screen_mid[1]-30),
                             (self.screen_mid[0]+45, self.screen_mid[1]-30),
                             (self.screen_mid[0]+60, self.screen_mid[1]),
                             (self.screen_mid[0], self.screen_mid[1]+70),
                             (self.screen_mid[0]-60, self.screen_mid[1]),
                             (self.screen_mid[0]-45, self.screen_mid[1]-30),
                             (self.screen_mid[0]-15, self.screen_mid[1]-30)])
        breed = self.font_big.render("Breeding...",
                                     True, (255, 255-self.stp, 255-self.stp))
        breed_rect = breed.get_rect()
        breed_rect.center = (self.screen_mid[0], self.screen_mid[1]-60)
        self.screen.blit(breed, breed_rect)
        pygame.display.flip()

    def anim_clock(self):
        self.stp += self.chg
        if self.stp == 260:
            self.chg = -5
            self.stp = 255
        elif self.stp == -5:
            self.chg = 5
            self.stp = 0

    def draw_line(self):
        pygame.draw.line(self.screen, GameMenu.white,
                         (self.screen_mid[0], 50),
                         (self.screen_mid[0], self.screen_mid[1]*2 - 50),
                         3)

    def display_generation_label(self):
        gen_label = self.font_big.render("Generation: "+str(self.gen_counter),
                                         True, GameMenu.white)
        self.screen.blit(gen_label, (self.screen_mid[0]+50, 50))

    def check_mouse_position(self):
        mouse = pygame.mouse.get_pos()
        for button in self.list_of_buttons:
            x_check = button[3][0]-50 < mouse[0] < button[3][0]+50
            y_check = button[3][1]-50 < mouse[1] < button[3][1]+50
            if x_check and y_check:
                button[4] = (255, 0, 0)
            else:
                if self.auto_check and button[0] == "Auto gen":
                    button[4] = (0, 255, 0)
                else:
                    button[4] = (255, 255, 255)

    def click_button(self):
        for button in self.list_of_buttons:
            if button[4] == (255, 0, 0):
                getattr(self, button[1])()

    def loading_animaiton(self, pos_x, pos_y, step):
        pygame.draw.polygon(self.screen, (255-step, 255-step, step),
                            [(pos_x+50, pos_y), (pos_x+60, pos_y),
                             (pos_x, pos_y+60), (pos_x, pos_y+50)])
        pygame.draw.polygon(self.screen, (255-step, 255-step, step),
                            [(pos_x-50, pos_y), (pos_x-60, pos_y),
                             (pos_x, pos_y-60), (pos_x, pos_y-50)])
        pygame.draw.polygon(self.screen, (step, step, 255-step),
                            [(pos_x+50, pos_y), (pos_x+60, pos_y),
                             (pos_x, pos_y-60), (pos_x, pos_y-50)])
        pygame.draw.polygon(self.screen, (step, step, 255-step),
                            [(pos_x-50, pos_y), (pos_x-60, pos_y),
                             (pos_x, pos_y+60), (pos_x, pos_y+50)])

    def next_gen_button(self):
        name_rend = self.font_big.render("Next GEN", True, self.next_color)
        name_rect = name_rend.get_rect()
        name_rect.center = (self.screen_mid[0]*2-150, self.screen_mid[1]*2-50)
        self.screen.blit(name_rend, name_rect)

    def progress_animation(self, progress):
        for i in range(int(progress*1000)):
            pygame.draw.rect(self.screen, GameMenu.white,
                             pygame.Rect(int((self.screen_mid[0]*i)/500),
                                         self.screen_mid[1]*2-25,
                                         int(self.screen_mid[0]/500),
                                         25))

    # Graphic elements
    def right_arrow(self, pos_x, pos_y, color):
        pygame.draw.polygon(self.screen, color, [(pos_x, pos_y),
                                                 (pos_x-20, pos_y+30),
                                                 (pos_x+10, pos_y),
                                                 (pos_x-20, pos_y-30)])

    def left_arrow(self, pos_x, pos_y, color):
        pygame.draw.polygon(self.screen, color, [(pos_x, pos_y),
                                                 (pos_x+20, pos_y-30),
                                                 (pos_x-10, pos_y),
                                                 (pos_x+20, pos_y+30)])

    def text_button(self, text, pos_x, pos_y, color):
        name_rend = self.font_big.render(text, True, color)
        name_rect = name_rend.get_rect()
        name_rect.center = (pos_x, pos_y)
        self.screen.blit(name_rend, name_rect)

    # List of button function
    def load_action(self):
        val = 0
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
            if f[-3:] == ".h5":
                if val < int(f[26:-3]):
                    val = int(f[26:-3])
        path = "Snake_genontyp_generation_"+str(val)+".h5"
        if not os.path.exists(path):
            print("nic Takiego nie ma")
        else:
            print(path)
            self.gen_counter = val
            self.load = True
            self.snake_brain.load_genotype(path)

    def save_action(self):
        name = "Snake_genontyp_generation_"+str(self.gen_counter)+".h5"
        self.snake_brain.save_genotype(name)
        print(name)
        # with open(name, 'w') as gen_output:
        #     gen_output.write(self.snake_brain.save_genotype())

        # print(self.snake_brain.save_genotype())

    def reset_action(self):
        self.snake_body.reset()
        self.game_clock = 0

    def auto_next_button_action(self):
        self.auto_check = not self.auto_check

    def next_button_action(self):
        self.loop_chk = False

    def mutation_increment_action(self):
        if self.list_of_menu[0][1] > 0.9:
            pass
        else:
            self.list_of_menu[0][1] += 0.1

    def mutation_decrement_action(self):
        if self.list_of_menu[0][1] < 0.1:
            pass
        else:
            self.list_of_menu[0][1] -= 0.1

    def speed_increment_action(self):
        if self.list_of_menu[1][1] == 20:
            pass
        else:
            self.list_of_menu[1][1] += 1
            self.game_clock = 0

    def speed_decrement_action(self):
        if self.list_of_menu[1][1] == 1:
            pass
        else:
            self.list_of_menu[1][1] -= 1
            self.game_clock = 0

    def population_increment_action(self):
        if self.list_of_menu[2][1] == 10000:
            pass
        else:
            self.list_of_menu[2][1] += 100

    def population_decrement_action(self):
        if self.list_of_menu[2][1] == 100:
            pass
        else:
            self.list_of_menu[2][1] -= 100



if __name__ == "__main__":
    pygame.init()

    display_width = 1366
    display_hight = 768

    screen = pygame.display.set_mode((display_width, display_hight))

    game_main_menu(screen)
    menu = GameMenu(screen)
    menu.game_set_up_menu()
