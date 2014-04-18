# Running BRKGA without GUI
from os import listdir
from os.path import isfile, join
from numpy import matrix
from OA import OA
from mutation import brkga_mutation
from mutation import sequencer_mutation
from crossover import brkga_crossover
from collections import Counter

import os
import re
import random
import utilities as util

def get_input_and_run_ga():
    # Take Input
    got_input = False
    
    while(not got_input):
        try:
            num_run = raw_input('Enter number of runs: ')
            num_run = int(num_run)
            num_crossover_rate = raw_input('Enter crossover rate: ')
            num_crossover_rate = float(num_crossover_rate)
            frac_mutants = raw_input('Enter mutant fraction: ')
            frac_mutants = float(frac_mutants)
            frac_elites = raw_input('Enter elite fraction: ')
            frac_elites = float(frac_elites)
            max_gen = raw_input('Enter maximum allowed generation: ')
            max_gen = int(max_gen)
            max_col_mut = raw_input('Enter maximum allowed columns for mutation: ')
            max_col_mut = int(max_col_mut)
            tour_sel_size = raw_input('Enter tournament selection size: ')
            tour_sel_size = int(tour_sel_size)
            min_col_accept = raw_input('Enter minimum number of columns for acceptance: ')
            min_col_accept = int(min_col_accept)
            sequencer_rate = raw_input('Enter sequencer mutation rate: ')
            sequencer_rate = float(sequencer_rate)
            initial_seq_mult = raw_input('Enter initial sequencer count: ')
            initial_seq_mult = int(initial_seq_mult)
            growth_rate = raw_input('Enter sequencer mutation count growth rate: ')
            growth_rate = float(growth_rate)
            if num_crossover_rate > 1.0:
                raise ValueError
            if frac_mutants >= 1.0 or frac_elites >= 1.0:
                raise ValueError
            
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

    # Run BRKGA
    # S = Total population, S_e = Elite population, S_m = mutant population
    
    S = int(S_e/frac_elites)
    S_m = int(S*frac_mutants)

    non_elite_oa = []

    # Fill the non_elite_population with randomly generated oa's
    for i in range(S - S_e - S_m):
        non_elite_oa.append(brkga_mutation(num_run, max_col_mut))

    # ---- Generation 0 Completed ---- #

    goto_next_gen = True
    current_gen = 1
    
    while(goto_next_gen):
        print " Undergoing generation " + str(current_gen)
        
        # Generate mutants
        print "  Mutants introduced in population "
        for i in range(S_m):
            temp = brkga_mutation(num_run, max_col_mut)
            non_elite_oa.append(temp)
            print temp.string + ' ' + str(temp.get_fitness_value())

        # Apply sequencer mutation
        seq_mult = int (initial_seq_mult * pow((1 + growth_rate), current_gen))
        sel_seq_oa_idx = tournament_selection(non_elite_oa, tour_sel_size, 1)

        if seq_mult > 1000:
            seq_mult = 1000
        
        for i in range(seq_mult):
            seq_oa = sequencer_mutation(non_elite_oa[sel_seq_oa_idx], sequencer_rate)
            if seq_oa:
                print 'HIT with sequencer mutation'
                del non_elite_oa[sel_seq_oa_idx]
                non_elite_oa.insert(sel_seq_oa_idx, seq_oa)

        # Perform Crossover
        print "  Successful crossovers "
        for i in range(2*(S - S_m - S_e)):
            oa_l = brkga_crossover([random.choice(elite_oa), tournament_selection(non_elite_oa, tour_sel_size)], num_crossover_rate)

            for gen_oa in oa_l:
                if is_not_subset(elite_oa, gen_oa) and gen_oa.array.shape[1] >= min_col_accept:
                    eq = all_equal_set(non_elite_oa, gen_oa)
                    if not eq:
                        non_elite_oa.append(gen_oa)
                        print gen_oa.string + ' ' + str(gen_oa.get_fitness_value())
                    else:
                        for j in eq:
                            if gen_oa.get_fitness_value() < non_elite_oa[j].get_fitness_value():
                                del non_elite_oa[j]
                                non_elite_oa.insert(j, gen_oa)
                                print gen_oa.string + ' ' + str(gen_oa.get_fitness_value())

        non_elite_oa.sort(key = lambda x : x.get_fitness_value())
        non_elite_oa = non_elite_oa[: S - S_e]
        current_gen += 1

        print "  Final members "
        for i in non_elite_oa:
            if i.get_fitness_value() < 0.1:
                dump_oa_to_file(i)
            print i.string + ' ' + str(i.get_fitness_value())

        if current_gen == max_gen:
            cont = raw_input('Continue with next generation (Enter N for No): ')
            if cont == "N":
                goto_next_gen = False
            else:
                max_gen += 10
            for i in non_elite_oa:
                dump_oa_to_file(i)

def is_not_subset(oa_list, oa):
    ''' Returns true if oa is not a subset of any oa in oa_list'''
    
    accept_flag = True
    temp1 = Counter(oa.factors)
    
    for j in oa_list:
        temp2 = Counter(j.factors)

        if not temp1 - temp2:
            accept_flag = False
            break
    return accept_flag

def tournament_selection(oa_list, tour_size, ret_type=0):
    ''' Implements a tournament selection for a list of oa's returns one oa. If 0 return OA else return its index '''
    oa_idx = random.randint(0, len(oa_list) - 1)
    oa = oa_list[oa_idx]
    
    for i in range(tour_size - 1):
        temp_idx = random.randint(0, len(oa_list) - 1)
        temp = oa_list[temp_idx]
        if oa.get_fitness_value() > temp.get_fitness_value():
            oa = temp
            oa_idx = temp_idx
    if ret_type == 0:
        return oa
    else:
        return oa_idx


def all_equal_set(oa_list, oa):
    ''' Returns all the sets in oa_list which are equal to oa '''

    ret = []
    temp1 = Counter(oa.factors)
    
    for j in range(len(oa_list)):
        temp2 = Counter(oa_list[j].factors)

        if not temp1 - temp2:
            if not temp2 - temp1:
                ret.append(j)

    return ret

def dump_oa_to_file(oa):
    dmp_path = os.path.join(util.module_path(), "..\dump")
    oa.print_array(os.path.join(dmp_path, oa.string))

if __name__ == '__main__':
    data_path = os.path.join(util.module_path(), "..\data")
    
    get_input_and_run_ga()
