### Functions for different type of crossover techniques for Orthogonal Arrays

from numpy import concatenate
from OA import OA
from utilities import remove_duplicates

import random


def one_point_crossover(oa, crossover_rate=0.7):
    prob = random.random()
    if prob < crossover_rate:
        orthogonal_array = [oa[0].array, oa[1].array]
        run_size = oa[0].runs
        factors = [len(oa[0].factors), len(oa[1].factors)]

        index_of_crossover = [random.randint(0, factors[0] - 1), random.randint(0, factors[1] - 1)]

        [left_1, right_1] = [orthogonal_array[0][:, :index_of_crossover[0]], orthogonal_array[0][:, index_of_crossover[0]:]]
        [left_2, right_2] = [orthogonal_array[1][:, :index_of_crossover[1]], orthogonal_array[1][:, index_of_crossover[1]:]]

        [left_fact_1, right_fact_1] = [oa[0].factors[:index_of_crossover[0]], oa[0].factors[index_of_crossover[0]:]]
        [left_fact_2, right_fact_2] = [oa[1].factors[:index_of_crossover[1]], oa[1].factors[index_of_crossover[1]:]]
        [fact_1, fact_2] = [left_fact_1 + right_fact_2, left_fact_2 + right_fact_1]
        temp = [str(run_size), str(run_size)]
        for i in list(remove_duplicates(fact_1)):
            temp[0] += ',' + str(i) + '^' + str(fact_1.count(i))
        for i in list(remove_duplicates(fact_2)):
            temp[1] += ',' + str(i) + '^' + str(fact_2.count(i))

        oa_left = OA(temp[0], concatenate([left_1, right_2], 1))
        oa_right = OA(temp[1], concatenate([left_2, right_1], 1))

        return [oa_left, oa_right]
    return [oa[0], oa[1]]


def brkga_crossover(oa, crossover_rate=0.7):
    # In Brkga only one offspring is generated from one crossover
    elite = oa[0].array
    non_elite = oa[1].array
    fact = []
    ret = []

    # or[0].array belongs to elite population
    if oa[0].num_factors > oa[1].num_factors:
        total = oa[0].num_factors
        idx = 1
    else:
        total = oa[1].num_factors
        idx = 0

    for i in range(total):
        prob = random.random()
        if i < oa[idx].num_factors:
            if prob < crossover_rate:
                fact.append(oa[0].factors[i])
                if i==0:
                    child = elite[:, i]
                else:
                    child = concatenate([child, elite[:, i]], 1)
            else:
                fact.append(oa[1].factors[i])
                if i==0:
                    child = non_elite[:, i]
                else:
                    child = concatenate([child, non_elite[:, i]], 1)
        else:
            if idx == 1 and prob < crossover_rate:
                fact.append(oa[0].factors[i])
                child = concatenate([child, elite[:, i]], 1)
            elif idx == 0 and prob >= crossover_rate:
                fact.append(oa[1].factors[i])
                child = concatenate([child, non_elite[:, i]], 1)
                
    temp = str(oa[0].runs)
    for i in list(remove_duplicates(fact)):
        temp += ',' + str(i) + '^' + str(fact.count(i))

    ret.append(OA(temp, child))
    return ret
        

        
###### For Checking ####
##a = OA('4,2^4', '1, 2, 3, 4; 1, 2, 13, 14; 21, 22, 23, 24; 31, 32, 33, 34')
##b = OA('4,3^5', '4, 5, 6, 7, 45; 14, 15, 16, 17, 31; 24, 25, 26, 27, 2; 34, 35, 36, 37, 7')
##print a.array
##print b.array
##c = brkga_crossover([a, b], 1)
##print c.array
##print c.string
##d = brkga_crossover([a, b], 0)
##print d.array
##print d.string
##one_point_crossover([a, b], 1)
##d = OA('12,3^1,2^4', '0, 0, 1, 0, 1; 1, 0, 0, 0, 1; 0, 0, 1, 1, 0; 1, 0, 0, 1, 0; 0, 1, 0, 0, 0; 1, 1, 1, 0, 0; 0, 1, 1, 1, 1; 1, 1, 0, 1, 1; 0, 2, 0, 1, 0; 1, 2, 1, 0, 0; 0, 2, 0, 0, 1; 1, 2, 1, 1, 1')
####print a.array
####print a.factors
####print b.array
####print b.factors
####lolo = brkga_crossover([b, a])
####print lolo.array
####print lolo.factors
####print lolo.num_factors
####print lolo.fitness
##
##[m, n] = one_point_crossover([d, d], 1)
##print m.array
##print m.get_fitness_value()
##print n.array
##print n.get_fitness_value()
##[m, n] = one_point_crossover([m, n], 1)
##print m.array
##print m.get_fitness_value()
##print n.array
##print n.get_fitness_value()
##print d.factors
##print d.array
