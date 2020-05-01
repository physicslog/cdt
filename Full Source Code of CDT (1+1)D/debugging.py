"""
Path: /Full_cdt_one_plus_one/Debugging.py

Time-stamp: <2017-12-11 22:30:27 (Damodar)>
Author: Damodar Rajbhandari (dphysicslog@gmail.com)
 
Description: This is a file for debugging purpose only.
Load it into the python 3 interpreter and use it to play 
around with the program in the command line.
HAPPY HACKING!
"""

#For sure: 
import numpy as np 
import scipy as sp 
import random 

#Class data structure and methods we need: 
import utilities as ut 
import triangulations as t 
# In order to valid CIRCULAR DEPENDENCY,sub_triangle_property should be 
# imported first than triangle_property.
import sub_triangle_property as st 
import triangle_property as tp 
import initialization
import state_manipulation as sm
import error_checking 
import move_factory as m
import simulation as simu

# To print the saved snapshot, use this:
# cd snapshot
# python SpacetimeSnap.py


 
