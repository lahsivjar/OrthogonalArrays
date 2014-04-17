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
