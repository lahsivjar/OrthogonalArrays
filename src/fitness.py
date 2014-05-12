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
    s_fit = 0
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
            temp = 0
            for k in range(oa.array.shape[1]):
                if(oa.array[i, k] == oa.array[j, k]):
                    temp += 1
            j2 = j2 + temp**2

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
    return [l / j2, j2 - l]

def compute_del(oa, i, j):
    if i == j:
        return oa.array.shape[1]
    temp = 0
    for k in range(oa.array.shape[1]):
        if oa.array[i, k] == oa.array[j, k]:
            temp += 1

    return temp
