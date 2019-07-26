import random
import numpy as np
from copy import deepcopy


def create_new_genom(mother, father):
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
    genotype_new = deepcopy(genotype)
    for idx, genom in enumerate(genotype_new):
        if len(genom.shape) == 2:
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
    population_list = []
    for i in range(NoB):
        population_list.append(mutation(create_new_genom(genotype_father,
                                                         genotype_mother),
                                        prop))
    return population_list


def populate_mult(pop_list, breading_couple, gui, NoB=1000, prop=0.1):
    population_list = []
    for par_num in range(len(breading_couple)-1):
        for i in range(int(NoB/len(breading_couple)-1)):
            gui.breeding_anim()
            mother = pop_list[breading_couple[par_num]]
            father = pop_list[breading_couple[par_num+1]]
            population_list.append(mutation(create_new_genom(mother, father),
                                            prop))
    for i in range(int(NoB/len(breading_couple)-1)):
        mother = pop_list[0]
        father = pop_list[-1]
        population_list.append(mutation(create_new_genom(mother, father),
                                        prop))
    for snake in breading_couple:
        population_list.append(pop_list[snake])
    return population_list


def generation_zero(genotype, NoB=1000, prop=0.1):
    population_list = []
    for i in range(NoB-1):
        population_list.append(mutation(genotype, prop))
    population_list.append(genotype)
    return population_list

if __name__ == "__main__":
    from Snake import SnakeBrain
    Steve = SnakeBrain()
    genotype = Steve.get_genotype()

    sytuacja = np.random.rand(1, 26)
    print(Steve.make_decision(sytuacja))


    breeding = generation_zero(genotype, 10, 0.8)
    print(len(breeding))

    Steve.set_genotype(breeding[4])
    print(Steve.make_decision(sytuacja))

    Steve.set_genotype(breeding[-1])
    print(Steve.make_decision(sytuacja))

    couples = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    large_pop = populate_mult(breeding, couples, 1000, 1000, 0.1)

    print("large pop")
    print(len(large_pop))

    Steve.set_genotype(large_pop[-1])
    print(Steve.make_decision(sytuacja))

    # Potomek.set_genotype(potomek)
    # print("Potomek decyzja")
    # print(Potomek.make_decision(situation))
    #
    # potomek = mutation(potomek)
    #
    # Potomek.set_genotype(potomek)
    # print("Zmutowany potomek decyzja")
    # print(Potomek.make_decision(situation))
