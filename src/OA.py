# OA class for storing OA's
#    eg: OA(8,2^4,4^1) this implies OA with 8-rows
#        and 4 2-level factors and 1 4-level factor

from numpy import matrix
from numpy import savetxt
from fitness import J2


class DimensionError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class OA:

    def __init__(self, oa, array=None):
        self.factors = []
        self.string = oa
        self.fitness = -1
        self.j2 = -1
        
        oa = oa.split(',')

        self.runs = int( oa[0] )
        self.num_factors = 0
        oa.pop(0)
        for i in oa:
            i = i.split('^')
            self.num_factors += int(i[1])
                 
        if (array != None):
            self.set_array(array)
        else:
            self.array = array

    def set_fitness_value(self, fit_val):
        self.fitness = fit_val[0]
        self.j2 = fit_val[1]

    def get_fitness_value(self):
        return self.fitness

    def get_j2_value(self):
        return self.j2

    def set_array(self, array):
        '''set the array for a given orthogonal array description'''
        try:
            if type(array)==matrix:
                temp = array
            else:
                temp = matrix(array)
            if (self.runs != temp.shape[0] or self.num_factors != temp.shape[1]):
                raise DimensionError("Array's dimension doesn't satisfy OA's description")
            
            self.array = temp
            
        except SyntaxError:
            print 'Matrix expected, got ' + str(type(array))
            self.array = None
            return
        except DimensionError as d:
            print d
            self.array = None
            return
        self.factors = (self.array.max(axis = 0) + 1).tolist()[0]
        self.set_fitness_value(J2(self))

    def print_array(self, dest):
        '''Print an orthogonal array, as csv file, to a given destination'''
        dest += '[' + str(self.get_j2_value()) + ']'
        savetxt(dest + '.csv', self.array, delimiter=',', fmt="%d")

###### FOR CHECKING ####
##
##d = OA('12,3^1,2^4', '0, 0, 1, 0, 1; 1, 0, 0, 0, 1; 0, 0, 1, 1, 0; 1, 0, 0, 1, 0; 0, 1, 0, 0, 0; 1, 1, 1, 0, 0; 0, 1, 1, 1, 1; 1, 1, 0, 1, 1; 0, 2, 0, 1, 0; 1, 2, 1, 0, 0; 0, 2, 0, 0, 1; 1, 2, 1, 1, 1')
##print J2(d)
