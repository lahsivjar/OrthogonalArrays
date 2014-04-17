# Mutation Functions returns a mutated OA

from numpy import matrix
from numpy import concatenate
from OA import OA
from utilities import find_levels
from utilities import remove_duplicates
from fitness import compute_del

import random


def sequencer_mutation(oa, sequencer_rate=0.5, multiplicity=10):
    ''' Move towards a more fit OA by first randomly selecting a factor then shuffleing it to make it better '''

    if oa.get_fitness_value() < 0.1:
        return oa

    ar = oa.array
    ret = oa
    for i in range(ar.shape[1]):
        prob = random.random()
        if prob < sequencer_rate:
            temp = ar[:, i].tolist()
            fit_val = oa.get_fitness_value()
            for j in range(multiplicity):
                random.shuffle(temp)
                ar[:, i] = matrix(temp)
                if fit_val > OA(oa.string, ar).get_fitness_value():
                    ret = OA(oa.string, ar)
                    fit_val = ret.get_fitness_value()

    return ret

def mutation_t1_1(oa, mutation_rate1_1, T=10):
    ''' Take a OA and perform some interchange operations to minimize difference between J2 and lower optimal '''
    # Find which column to perform this mutation on
    c = 1
    # Compute the value of DEL(a, b) for all a, b rows of the selected column
    temp = oa.array[:, c].tolist()
    maximum = 0
    switch_1 = 0
    switch_2 = 0
    for a in range(len(temp)):
        for b in range(a + 1, len(temp)):
            del_val = 0
            for j in range(len(temp)):
                if j != a and j != b and temp[a][0] != temp[b][0]:
                    if temp[a][0] == temp[j][0]:
                        temp1 = 1
                    else:
                        temp1 = 0
                    if temp[b][0] == temp[j][0]:
                        temp2 = 1
                    else:
                        temp2 = 0
                    
                    del_val += (compute_del(oa, a, j) - compute_del(oa, b, j)) * (temp1 - temp2)
            if del_val > maximum:
                maximum = del_val
                switch_1 = a
                switch_2 = b


def mutation_t1(oa, mutation_rate1=0.1):
    ''' Return a new OA with a column from old OA and swaping its values '''
    ### NOT FOUND TO BE VERY EFFECTIVE ###
    
################    # This does type 1 mutation with probablity mutation_rate1 for all the columns of array
################    ar = matrix(oa.array)
################    for i in range(ar.shape[1]):
################        prob = random.random()
################        if prob < mutation_rate1:
################            temp = ar[:, i].tolist()
################            random.shuffle(temp)
################            ar[:, i] = matrix(temp)


    # This does type 1 mutation with probablity mutation_rate1 for only one randomly selected column
    ar = matrix(oa.array)
    prob = random.random()
    if prob < mutation_rate1:
        idx = random.randint(0, ar.shape[1] - 1)
        temp = ar[:, idx].tolist()
        random.shuffle(temp)
        ar[:, idx] = matrix(temp)

    return OA(oa.string, ar)

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
       
##c = OA('12,3^1,2^4', '0, 0, 1, 0, 1; 0, 1, 0, 0, 1; 0, 0, 1, 1, 0; 0, 1, 0, 1, 0; 1, 0, 0, 0, 0; 1, 1, 1, 0, 0; 1, 0, 1, 1, 1; 1, 1, 0, 1, 1; 2, 0, 0, 1, 0; 2, 1, 1, 0, 0; 2, 0, 0, 0, 1; 2, 1, 1, 1, 1')
##print c.get_fitness_value()
##print c.array
##ll = sequencer_mutation(c, 1, 100)
##print ll.get_fitness_value()
##print ll.array
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
