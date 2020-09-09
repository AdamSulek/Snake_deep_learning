import random
import pygame
import numpy as np
from copy import deepcopy
from gui import snake_gui

def create_new_genom(mother, father):
    '''
        Input format:
            mother and father as genotype has format:
                type: <class 'list'>
                len: 6
                each element of list - type: numpy ndarray
                                       len:  26 as length neurons leyer
                                       26 weigth , 26 biases
                                       the last one len is 3 (output biases)

        This function generates genotype with randomly choosing genes
        from two genomes (mother and father).

        Deepcopy is using to create another genotype with different adress,
        but with the same rewritten values (not only poiting to the genotype
        adress).
    '''
    genotype = deepcopy(mother)
    for idx, genom in enumerate(genotype):
        if len(genom.shape) == 2:
            for (x, y), gen in np.ndenumerate(genom):
                decision = random.choice([0, 2])
                if decision == 0:
                    genotype[idx][x, y] = father[idx][x, y]
                elif decision == 1:
                    genotype[idx][x, y] = (father[idx][x, y] + gen)/2
    return genotype

def mutation(genotype, prop = 0.1):
    '''
        Input format:
            genotype - was describe in create_new_genom function documentation
            (mother , father).

        This function keep the format of input with genom.shape == 2.

        Mutation function change with some propability (default=0.1) genom
        (weights) value.
    '''
    genotype_new = deepcopy(genotype)
    for idx, genom in enumerate(genotype_new):
        if len(genom.shape) == 2:
            #range of propability of mutation occurs
            if random.uniform(0, 1) <= prop:
                for (x, y), gen in np.ndenumerate(genom):
                    # decision = random.choice([0, 1])
                    # if decision == 0:
                    random_value = np.random.choice(np.arange(-1, 1, step=0.001),
                                                    size=(1),
                                                    replace=False)

                    genotype_new[idx][x,y] = genotype_new[idx][x,y] + random_value
                    # genotype_new[idx][x,y] = np.random.normal(gen, 1.0)
                    # elif decision == 1:
                    #     x_k = random.randint(0, genom.shape[0]-1)
                    #     y_k = random.randint(0, genom.shape[1]-1)
                    #     genotype_new[idx][x,y], \
                    #     genotype_new[idx][x_k,y_k] = genotype_new[idx][x_k,y_k], \
                    #                                  genotype_new[idx][x,y]

    return genotype_new


def populate(genotype_father, genotype_mother, NoB=1000, prop=0.1):
    '''
        Input format:
            genotype_father and genotype_mother - was describe in
            create_new_genom function documentation (mother, father).

        This function create population list which contain individual with
        genotype inherits from two parents and some mutation may occure.
    '''
    population_list = []
    for i in range(NoB):
        population_list.append(mutation(create_new_genom(genotype_father,
                                                         genotype_mother),
                                                         prop))
    return population_list


def populate_mult(population_list, breading_couple, gui, NoB=1000, prop=0.1):
    '''
        Input format:
            population_list - was describe in create_new_genom function
            documentation (mother, father).
            breading_couple - was describe in create_new_genom function
            documentation (mother, father).
            gui - GameMenu class object

        This function create population which contain individual with
        genotype inherits from two parents and some mutation may occure
        on specific randomly choosen gen (iterable of breading_couple).
    '''
    population_list = []
    for par_num in range(len(breading_couple)-1):
        for i in range(int(NoB/len(breading_couple)-1)):
            gui.breeding_anim()
            mother = population_list[breading_couple[par_num]]
            father = population_list[breading_couple[par_num+1]]
            population_list.append(mutation(create_new_genom(mother, father),
                                            prop))
    for i in range(int(NoB/len(breading_couple)-1)):
        mother = population_list[0]
        father = population_list[-1]
        population_list.append(mutation(create_new_genom(mother, father),
                                        prop))
    for snake in breading_couple:
        population_list.append(population_list[snake])

    return population_list


def generation_zero(genotype, NoB=1000, prop=0.1):
    '''
        Input format:
            genotype - was describe in create_new_genom function documentation.

        This function creates a list of population. Every individual in
        population list has genotype (weights and biases) created with
        mutation function.
    '''
    population_list = []
    for _ in range(NoB-1):
        population_list.append(mutation(genotype, prop))
    population_list.append(genotype)
    return population_list

if __name__ == "__main__":
    from snake import SnakeBrain
    Steve = SnakeBrain()
    genotype = Steve.get_genotype()

    situation = np.random.rand(1, 26)
    print(Steve.make_decision(situation))


    breeding = generation_zero(genotype, 10, 0.8)
    print(len(breeding))

    #to show different decision if use different genotype
    Steve.set_genotype(breeding[4])
    print(Steve.make_decision(situation))

    Steve.set_genotype(breeding[-1])
    print(Steve.make_decision(situation))

    couples = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    large_pop = populate_mult(breeding, couples, 1000, 1000, 0.1)

    print("large pop")
    print(len(large_pop))
