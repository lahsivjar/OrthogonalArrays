# Mutation Functions returns a mutated OA

from numpy import matrix
from numpy import concatenate
from OA import OA
from utilities import find_levels
from utilities import remove_duplicates
from fitness import compute_del

import random


def sequencer_mutation(oa, sequencer_rate=0.5):
    ''' Swap two elements from a randomly selected column if not successful swapping return False '''

    if oa.get_fitness_value() < 0.1:
        return False
    
    ar = matrix(oa.array)
    prob = random.random()
    if prob < sequencer_rate:
        # Randomly select a column
        c = random.randint(0, ar.shape[1] - 1)

        # Randomly select two indexes in the column
        idx1 = random.randint(0, oa.runs - 1)
        idx2 = random.randint(0, oa.runs - 1)

        # Swap values at indexes and return the new oa if it is more fit else return False
        temp = ar[:, c].tolist()
        temp_st = temp[idx1]
        temp[idx1] = temp[idx2]
        temp[idx2] = temp_st

        ar[:, c] = matrix(temp)
        tempoa = OA(oa.string, ar)
        if tempoa.get_fitness_value() > oa.get_fitness_value():
            return tempoa

    return False

def mutation_t1(oa, mutation_rate1=0.7):
    ''' Return a new OA with a column from old OA and swaping its values '''
    # It is same as sequencer_mutation

    temp = sequencer_mutation(oa, mutation_rate1)
    if temp:
        return temp
    else:
        return oa

def mutation_t2(oa, mutation_rate2=0.6):
    ''' Create a new OA with all old plus a new factor with some randomly chosen levels'''
    prob = random.random()
    if prob < mutation_rate2:
        lev = find_levels(oa.runs)
        lev_selected = lev[random.randint(0, len(lev)-1)]

        new_col = []
        for i in range(lev_selected):
            for j in range(int(oa.runs/lev_selected)):
                new_col.append(i)

        new_col = matrix(new_col).reshape(oa.runs, 1)

        # here finding factors of new array then finding string representation then again finding the factors Improve it later
        temp_fact = oa.factors[:]
        temp_fact.append(lev_selected)
        temp = str(oa.runs)
        for i in list(remove_duplicates(temp_fact)):
            temp += ',' + str(i) + '^' + str(temp_fact.count(i))

        new_oa = OA(temp, concatenate((oa.array, new_col), axis = 1))

        return new_oa

    return oa

def brkga_mutation(runsize, num_col=4):
    '''Here we will create random mutant solutions of randomly chosen levels and number of factors,
    Also no mutation rate is required as we always have to generate a particular number of mutant,
    solutions based on the size of population. Call this function recursively to generate more than one mutant'''
    lev = find_levels(runsize)

    new_matrix = []
    temp_fact = []
    for l in range(num_col):
        lev_selected = lev[random.randint(0, len(lev)-1)]
        temp_fact.append(lev_selected)
        new_col = []
        for i in range(lev_selected):
            for j in range(int(runsize/lev_selected)):
                new_col.append(i)
        random.shuffle(new_col)
        new_matrix.append(new_col)

    new_matrix = matrix(new_matrix).reshape(num_col, runsize)
    new_matrix = matrix.transpose(new_matrix)

    temp = str(runsize)
    for i in list(remove_duplicates(temp_fact)):
        temp += ',' + str(i) + '^' + str(temp_fact.count(i))

    new_oa = OA(temp, new_matrix)

    return new_oa

##for i in range(100):
##    asf = brkga_mutation(72)
##    print asf.get_fitness_value()
##print asf.string
       
##c = OA('12,3^1,2^4', '1, 0, 0, 0, 0; 0, 1, 1, 0, 1; 0, 0, 1, 1, 1; 0, 1, 0, 1, 0; 0, 0, 0, 0, 0; 1, 1, 1, 0, 0; 1, 0, 1, 1, 1; 1, 1, 0, 1, 1; 2, 0, 0, 1, 0; 2, 1, 1, 0, 0; 2, 0, 0, 0, 1; 2, 1, 1, 1, 1')
##print c.get_fitness_value()
##print c.array
##for i in range(100):
##    t = sequencer_mutation(c, 1)
##    if t:
##        c = t
##        print 'Success at ' + str(i) + ' ' + str(t.get_fitness_value())
##        print t.array
##mutation_t1_1(c, 0.2)
##print c.string
##print c.array
##print c.get_fitness_value()
##d = mutation_t1(c, 1)
##print c.factors
##print d.array
##print c.get_fitness_value()
##print d.get_fitness_value()


##d = mutation_t2(c, 0.5)
##print c.array
##print c.factors
##print d.string
##print d.array
##print d.get_fitness_value()
##print d.factors
##print d.string
