"""
error_checking.py

This module is taken from Jonah Miller (jonah.maxwell.miller@gmail.com)

This file is part of the program which generates
2-D torus of (as close as possible to) uniform curvature for a given
surface area by monte carlo simulation.

This module contains nothing but error checking tools: small, snippets
of code that we use over and over again.
"""


### Dependencies
#-------------------------------------------------------------------------
import numpy as np
import scipy as sp
#-------------------------------------------------------------------------


### Checking
#-------------------------------------------------------------------------
def check_length(S,target_length,object_name=False,function_name=False):
    """
    Ensures that the tuple/set/list S has length target_length. If it
    is not, raises an error. If object name is given, alerts the user
    which object name the list had. If function_name is given, alerts the
    user that function_name function failed.
    """
    if len(S) != target_length:
        print ("ERROR, your object had the wrong length!")
        if object_name:
            print ("Your object is a: {}".format(object_name))
        if function_name:
            print ("Error occurred in: {}".format(function_name))
        print ("Your object: {}".format(S))
        return False
    else:
        return True

def too_many_duplicates(object_type,object_instance,
                        duplicates,allowed_duplicates,function_name):
    """
    If duplicate checking runs and finds too many duplicates, you can
    call this to produce a suitable error message.
    """
    if not 0 <= len(duplicates) <= allowed_duplicates:
        print ("Error in {}".format(function_name))
        print ("The {} ".format(object_type) + \
            "has more than {} duplicate(s)!".format(allowed_duplicates))
        print ("Your {}: {}".format(object_type,object_instance))
        print ("Duplicates: {}".format(duplicates))
        return False
    else:
        return True
#-------------------------------------------------------------------------
