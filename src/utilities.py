import os
import sys

def we_are_frozen():
    # All of the modules are built-in to the interpreter, e.g., by py2exe
    return hasattr(sys, "frozen")

def module_path():
    encoding = sys.getfilesystemencoding()
    if we_are_frozen():
        return os.path.dirname(unicode(sys.executable, encoding))
    return os.path.dirname(unicode(__file__, encoding))

def find_levels(n):
    ''' Prime Numbers and one should not return any levels'''
    if n == 1:
        return [1, ]
    ret_list = []
    for i in range(2, int(n/2) + 1):
        if n%i == 0:
            ret_list.append(i)

    return ret_list

def remove_duplicates(fact):
    fact_set = set()
    for i in fact:
        if i not in fact_set:
            yield i
            fact_set.add(i)

def binary_search(lst, start_idx, end_idx, key):
    # Binary search based on fit value in lst with start and end indexes 
    # Return position index if found and insert position if not found
    if key <= lst[end_idx].get_fitness_value():
        return end_idx + 1

    if key >= lst[start_idx].get_fitness_value():
        return start_idx

    if end_idx - start_idx == 1:
        return end_idx

    mid = (int)((start_idx + end_idx) / 2)

    if (key <= lst[mid].get_fitness_value()):
        return binary_search(lst, mid, end_idx, key)
    elif (key > lst[mid].get_fitness_value()):
        return binary_search(lst, start_idx, mid, key)


def dump_oa_to_file(oa):
    dmp_path = os.path.join(module_path(), "..\dump")
    oa.print_array(os.path.join(dmp_path, oa.string))
