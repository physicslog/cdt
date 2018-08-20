"""
Path: /Full_cdt_one_plus_one/utilities.py

Copyright: Module taken from Jonah Miller (jonah.maxwell.miller@gmail.com)

Description: This module contains functions not necessarily linked to the whole 
program.

"""


# Dependancies
#-------------------------------------------------------------------------
import itertools # For combinations
import math # For factorials
import numpy as np
import functools
import operator
#-------------------------------------------------------------------------


# Functions

# Combinatorics stuff
#-------------------------------------------------------------------------
def swap(a,b):
    "sets a = b, and b = a."
    temp = a
    a = b
    b = temp
    del temp
    return [a,b]

def binomial_coefficient(n,k):
    """
    Returns n choose k.
    """
    if k > n: # Make sure n is greater than k.
        print ("n < k. Reversing your inputs.")
        n,k = swap(n,k)
    return math.factorial(n)/(math.factorial(n-k)*math.factorial(k))

def k_combinations(big_set,k=2):
    """
    Finds and returns the k-combinations of big_set---i.e., the
    subsets of big_set with cardinality k. For convenience reasons,
    the default value of k is 2.
    """
    S = set(big_set) # In case big_set was given to us as a
                     # list. Eliminates redundant elements.
    if k > len(S): # If k > len(S), combinations don't make sense.
        print ("k > len(S). Setting k = len(S).")
        k = len(S)

    combinations = [] # The k_combinations to return
    count = 0 # Test to make sure that the number of k_combinations is
              # equal to len(S) choose k.
    for c in itertools.combinations(S,k): # Get the combinations we need.
        count += 1
        combinations.append(set(c))

    # Just to prevent unexpected errors
    assert count == binomial_coefficient(len(S),k) 

    return combinations
#-------------------------------------------------------------------------


# Set stuff
#-------------------------------------------------------------------------
def set_union(list_of_sets):
    "Calculates the union of an arbitrary number of sets. Syntactic sugar."
    union = set([])
    for s in list_of_sets:
        union |= s
    return union

def set_intersection(list_of_sets):
    """
    Calculates the intersection of an arbitrary number of
    sets. Syntactic sugar.
    """
    intersection = set(list_of_sets[0])
    for s in list_of_sets:
        intersection &= s
    return intersection

def only_element(S):
    """
    If set S contains only 1 element, return that element. Otherwise,
    raise an error.
    """
    assert len(S) == 1
    return list(S)[0]
#-------------------------------------------------------------------------


# Miscellaneous
#-------------------------------------------------------------------------
def round_to_zero(x):
    "If |x| is sufficiently small, round it to zero. Otherwise, return x."
    sufficiently_small = 1E-5
    if np.abs(x) <= sufficiently_small:
        return 0
    else:
        return x

def product(seq):
    """Product of a sequence."""
    return functools.reduce(operator.mul, seq, 1)

def concatenate_strings(list_of_strings):
    "Take every string in a list and concatenate them."
    S = list_of_strings[0]
    for i in range(1,len(list_of_strings)):
        S += list_of_strings[i]
    return S

#---Codes by Damodar Rajbhandari----------------

def tuple_of_set_union(lists_of_tuple_of_sets):
    "Calculates the union of an arbitrary number tuple of sets. Syntactic sugar"
    union = set([])
    for i in lists_of_tuple_of_sets:
        for j in i:
            union |= j
    return union 

def combine(tuple_of_lists):
    """
    Helpful for the function which gives two lists in return.
    Returns, to make it into single list.
    """
    b = []
    for i in tuple_of_lists:
        b += i
    return b