# Running BRKGA without GUI
from os import listdir
from os.path import isfile, join
from numpy import matrix
from OA import OA
from mutation import brkga_mutation
from mutation import sequencer_mutation
from crossover import brkga_crossover
from collections import Counter
from fitness import Jn

import re
import random
import utilities as util

def check_strength():
    ######## Write code to calculate the lower bound also #########
    # Take Input
    got_input = False
    
    while(not got_input):
        try:
            num_run = raw_input('Enter number of runs: ')
            num_run = int(num_run)
            
            got_input = True

        except ValueError:
            print 'Invalid Input try again ...'

    # Load run_size oa files
    all_files = [f for f in listdir(data_path) if isfile(join(data_path, f))]
    all_files.sort(key = lambda x: int(x.split(',')[0]))

    elite_oa = []
    
    load_data = [i for i, word in enumerate(all_files) if re.search('^' + str(num_run) + ',' + '.*', word)]

    for i in load_data:
        print all_files[i]
        file1 = open(join(data_path, all_files[i]), 'r')
        ar = ''
        for j in file1.readlines():
            ar += j.rstrip(',\n') + ';'
        ar = ar.rstrip(';')
        elite_oa.append(OA(all_files[i].split('.')[0], matrix(ar)))
    S_e = len(load_data)

    for i in elite_oa:
        print i.get_fitness_value()
        print "Other Jn's: "
        for j in range(2, i.array.shape[1]):
            print "  " + str(Jn(i, j))



if __name__ == '__main__':
    data_path = join(util.module_path(), "..\data")
    
    check_strength()
