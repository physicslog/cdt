"""
Path: /Full_cdt_one_plus_one/initialization.py

Time-stamp: <2017-12-11 22:30:51 (Damodar)>
Author: Damodar Rajbhandari (dphysicslog@gmail.com)
 
Description: This file is a part of the LCDT software which generates 
topological 2-torus of (as possible close to) uniform curvature for a
given surface area by Monte-Carlo simulation.

This module initialize the topological torus in a runtime.

Note: "ONLY USEFUL AT INITIALIZATION" means to initialize our 
       standard CDT lattices.
"""

#Dependencies 
#------------
import numpy as np 
import scipy as sp 

#Class data structure we need
from triangle_property import * 
from sub_triangle_property import * 
from triangulations import * 
import utilities as ut 
import state_manipulation as sm

#Constants from voronoi graph:

# Spacelike data:
s= [set([1,4]),
	set([4,5]),
	set([5,1]),
	set([2,6]),
	set([6,7]),
	set([7,2]),
	set([3,8]),
	set([8,9]),
	set([9,3])]

# Timelike data:
t = [set([1,2]),
	set([2,3]),
	set([3,1]),
	set([4,6]),
	set([6,8]),
	set([8,4]),
	set([5,7]),
	set([7,9]),
	set([9,5]),
	set([3,4]),
	set([2,8]),
	set([8,5]),
	set([1,6]),
	set([6,9]),
	set([9,1]),
	set([4,7]),
	set([7,3]),
	set([5,2])]

# For flat geometry, the number of equilateral triangles attached to 
# a vertex should be equal to six. 
# Initialize our universe from foliated structure exactly in 
# standard CDT. Make it non-foliated structure which also consists 
# of SST type triangles by using Monte-Carlo moves
# two_torus_data = [({t1,t2},{s1}),...]
# For triangulated torus: 2*vertices = triangles

two_torus_data = [(set(t[0]),set(t[12]),set(s[3])),
				(set(t[12]),set(t[3]),set(s[0])),
				(set(t[15]),set(t[3]),set(s[4])),
				(set(t[15]),set(t[6]),set(s[1])),
				(set(t[6]),set(t[17]),set(s[5])),
				(set(t[17]),set(t[0]),set(s[2])),
				(set(t[1]),set(t[10]),set(s[6])),
				(set(t[10]),set(t[4]),set(s[3])),
				(set(t[4]),set(t[13]),set(s[7])),
				(set(t[13]),set(t[7]),set(s[4])),
				(set(t[7]),set(t[16]),set(s[8])),
				(set(t[16]),set(t[1]),set(s[5])),
				(set(t[2]),set(t[9]),set(s[0])),
				(set(t[9]),set(t[5]),set(s[6])),
				(set(t[5]),set(t[11]),set(s[1])),
				(set(t[11]),set(t[8]),set(s[7])),
				(set(t[8]),set(t[14]),set(s[2])),
				(set(t[14]),set(t[2]),set(s[8]))]

#Functions required during initialization
def connect_all_triangles():
	"""
	ONLY USEFUL AT INITIALIZATION. 

	This function ensures that every vertex know what
	triangles type it is part of and every triangle 
	know what type of neighbors it has.
	"""
	for point in vertex.instances.values():
		point.find_and_set_tts_triangles()
		point.find_and_set_timelike_edges()
		point.find_and_set_spacelike_edges()
		point.connect_surrounding_triangles()

def build_torus_from_data(torus_data):
	"""
	ONLY USEFUL AT INITIALIZATION. 

	torus_data means two_torus_point_data should be a lists of sets, 
	each with 6 points in it. 
	"""
	#First we need to check that torus_data is what we want.
	for t in torus_data:
		if not (type(t) == tuple and len(t) == 3):
			raise TypeError("Torus data need to be a list of tuple,"
							+ "each of length 2!")
		for i in t: 
			if not (type(i) == set and len(i) == 2):
				raise TypeError("The edges must consists of 2 vertices.")
			for j in i:
				if not (type(j) == int and j > 0):
					raise TypeError("The vertices must all be"
									+ "positive integers!")

	# The vertices in existence will be the union of the triangle 
	# edge tuples. 
	vertex_ids = ut.tuple_of_set_union(torus_data)

	# The last used vertex id is the maximum of the vertex ids
	last_used_vertex_id = max(vertex_ids)

	# Make sure there are no vertices are missing (print torus to 
	# file should not let there be any)
	assert set(range(1, last_used_vertex_id+1)) - vertex_ids == set([])
	# Once we're sure the set is what we want, we need to make sure no
	# torus is currently initialized.
	sm.delete_all_geometries()
	# Make the points we need
	sm.make_n_vertices(last_used_vertex_id)
	# Ensure the points we made are the points in our list
	assert set(vertex.instances.keys()) == vertex_ids

	# Make the triangles we need out of the points.
	tts_triangle_ids = [sm.build_triangle_and_edges(t) for t in torus_data]

	# Connect all the triangles and tell points what triangles contain them !
	connect_all_triangles()

	return tts_triangle_ids

def build_first_two_torus():
	"""
	ONLY USEFUL AT INITIALIZATION. 
	
	The base of initialization. Builds a two torus to operate moves on.
	"""
	return build_torus_from_data(two_torus_data)

