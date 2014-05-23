### Fitness functions

from numpy import matrix

def Jn(oa, n):
    # Calculate the Jn value no lower bound calculated
    jn = 0
    for i in range(oa.array.shape[0]):
        for j in range(i + 1, oa.array.shape[0]):
            temp = 0
            for k in range(oa.array.shape[1]):
                if(oa.array[i, k] == oa.array[j, k]):
                    temp += 1
            jn = jn + temp**n
    return jn

def sat_fit(oa):
    # Calculate the saturated fitness value
    s_fit = 0.0
    u_lim = oa.runs - 1
    for i in oa.factors:
        s_fit += i - 1

    # Return normalized saturated fitness value
    return s_fit / u_lim

def J2(oa):
    # Calculate the J2 value
    j2 = 0
    for i in range(oa.array.shape[0]):
        for j in range(i + 1, oa.array.shape[0]):
            j2 = j2 + compute_del(oa, i, j)**2

    # Calculate the lower bound taking weights as 1 for all factors
    w = len(oa.factors)
    n = oa.runs
    fact1 = 0
    fact2 = 0
    for i in oa.factors:
        temp = n*(1.0 / i)
        fact1 = fact1 + temp
        fact2 = fact2 + ((i - 1) * temp**2)

    l = 0.5 * (fact1**2 + fact2 - (n * w**2))
    
    # Return normalized fitness value
    fit_val = j2 - l
    norm_fit_val = 1 - (fit_val / oa.max_fit)
    return (norm_fit_val, fit_val)

def compute_del(oa, i, j):
    if i == j:
        return oa.array.shape[1]
    temp = 0
    for k in range(oa.array.shape[1]):
        if oa.array[i, k] == oa.array[j, k]:
            temp += 1

    return temp

def compute_del_ele(a, b):
    if a == b:
        return 1
    else:
        return 0

def update_j2(oa, c, a, b):
    # oa is the array in which swapping has to occur
    # This function should be consistent with J2(oa)
    # c is the column index, a and b are the rows swapped in c
    ret = 0
    for j in range(oa.array.shape[0]):
        if (j != a and j != b):
            temp = compute_del_ele(oa.array[a, c], oa.array[j, c]) - compute_del_ele(oa.array[b, c], oa.array[j, c])
            if temp:
                ret += ((compute_del(oa, a, j) - compute_del(oa, b, j) - temp) * temp)
    new_j2 = oa.get_j2_value() - 2 * ret

    return (1 - (new_j2 / oa.max_fit), new_j2)
