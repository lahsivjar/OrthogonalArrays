# Run Sequencer mutation on one array to try to get an orthogonal array
from os.path import isfile, join
from numpy import matrix
from OA import OA
from mutation import sequencer_mutation

import utilities as util

def run_seq_mut():
    # Take file path w.r.t. Orthogonal Arrays dir as input takes only dump oa file format
    got_input = False

    while(not got_input):
        try:
            path = raw_input('Enter path of array w.r.t. root OA dir: ')
            oa_name = raw_input('Enter oa name: ')
            count = raw_input('Enter number of times to apply seq mutation: ')
            count = int(count)
            path += oa_name + '.csv'
            path = join(util.module_path(), path)
            if not isfile(path):
                raise ValueError
            
            got_input = True
            
        except ValueError:
            print 'Invalid Input try again ...'

    # Now load the OA
    oa_file = open(path, 'r')
    ar = ''
    for j in oa_file.readlines():
        ar += j.rstrip(',\n') + ';'
    ar = ar.rstrip(';')
    oa = OA(oa_name.split('[')[0], matrix(ar))

    # Apply sequencer mutation
    cont_flag = True

    while(cont_flag):
        for i in range(count):
            seq_oa = sequencer_mutation(oa, 1)
            if seq_oa:
                print 'HIT ' + str(seq_oa.get_fitness_value())
                oa = seq_oa

        cont = raw_input('Enter N to stop else continue again: ')
        if cont == "N":
            cont_flag = False
            util.dump_oa_to_file(oa)
    

if __name__ == '__main__':
    run_seq_mut()
