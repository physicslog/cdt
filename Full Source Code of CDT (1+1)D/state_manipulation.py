"""
Path: /Full_cdt_one_plus_one/state_manipulation.py

Time-stamp: <2017-12-11 22:32:12 (Damodar)>
Author: Damodar Rajbhandari (dphysicslog@gmail.com)

This module contains classes, functions, and methods which give or
manipulate the state of the simulation. The primary class is the
torus class, which is meant to be initialized and hold the general
state of the simulation. .
"""

### Dependencies
#-------------------------------------------------------------------------
import numpy as np
import scipy as sp
# Class data structures we need
from triangulations import *   
from triangle_property import *
from sub_triangle_property import *
import utilities as ut
import error_checking
#-------------------------------------------------------------------------


### Functions that generate or remove objects en bulk
###-------------------------------------------------------------------------
def make_n_vertices(n):
	"""
	Makes n new vertices and adds them to the hash table. Returns the
	vertex IDS generated.
	"""
	new_vertices = []
	for i in range(n):
		temp = vertex() # a newly created instance for the vertex class
		vertex.add(temp) # It will put this instance in the instances hash table
						# add() method is defined in triangulation.py
		new_vertices.append(temp.id)
	return new_vertices

def delete_all_geometries():
	"Delete all instances of all geometric objects."
	vertex.delete_all()
	spacelike.delete_all()
	timelike.delete_all()
	tts_triangle.delete_all()
	sst_triangle.delete_all()
###-------------------------------------------------------------------------


### Functions that manipulate objects at a higher level. These are
### basically syntactic sugar.
#-------------------------------------------------------------------------
def bisect_spacelike_using_id(spacelike_id):
	"""
	Uses the spacelike_bisect() function to bisect a spacelike edge 
	and update the hash tables properly. Takes a spacelike edge id.
	"""
	# Bisect the spacelike edge and generate two pairs of points, each
	# representing one of the two new edges.
	new_spacelike_edges,newpoint = spacelike.instances[spacelike_id].bisect() 

	# Delete the old spacelike edge
	# Because it will have two spacelike edges with two ids  
	# rather than one ID.
	spacelike.delete(spacelike_id)

	# Add the new point to the hash table
	new_vertex = vertex(newpoint)
	vertex.add(new_vertex)

	# Add the new spacelike edges to the spacelike hash table. We want to return the
	# new IDs (because why not), so a temporary list is generated
	# for this purpose.
	new_spacelike_edge_instances = set([])
	for endpoint_pair in new_spacelike_edges:
		e = spacelike(endpoint_pair)
		spacelike.add(e)
		new_spacelike_edge_instances.add(e)
	return [new_spacelike_edge_instances,new_vertex]

def bisect_timelike_using_id(timelike_id):
	"""
	Uses the timelike.bisect() function to bisect a timelike edge 
	and update the hash tables properly. Takes a timelike edge id.
	"""
	# Bisect the timelike edge and generate two pairs of points, each
	# representing one of the two new edges.
	new_timelike_edges,newpoint = timelike.instances[timelike_id].bisect() 

	# Delete the old timelike edge
	# Because it will have two timelike edges with two ids  
	#rather than one ID.
	timelike.delete(timelike_id)

	# Add the new point to the hash table
	new_vertex = vertex(newpoint)
	vertex.add(new_vertex)

	# Add the new timelike edges to the timelike hash table. We want to return the
	# new IDs (because why not), so a temporary list is generated
	# for this purpose.
	new_timelike_edge_instances = set([])
	for endpoint_pair in new_timelike_edges:
		e = timelike(endpoint_pair)
		timelike.add(e)
		new_timelike_edge_instances.add(e)
	return [new_timelike_edge_instances,new_vertex]


def bisect_spacelike(spacelike_id_or_instance):
	"""
	Uses the spacelike_bisect() function to bisect an spacelike edge and update the
	hash tables properly. TAKES AN SPACELIKE EDGE ID OR INSTANCE.
	"""
	if type(spacelike_id_or_instance) == int \
			and spacelike_id_or_instance in spacelike.instances.keys():
		spacelike_id = spacelike_id_or_instance
	elif isinstance(spacelike_id_or_instance,spacelike):
		spacelike_id = spacelike_id_or_instance.get_id()
	else:
		raise TypeError("Bisect_spacelike_edge accepts only spacelike edge ids "+
						"or spacelike edge instances.")
	return bisect_spacelike_using_id(spacelike_id)

def bisect_timelike(timelike_id_or_instance):
	"""
	Uses the space.bisect() function to bisect an timelike edge and update the
	hash tables properly. TAKES AN TIMELIKE EDGE ID OR INSTANCE.
	"""
	if type(timelike_id_or_instance) == int \
			and timelike_id_or_instance in timelike.instances.keys():
		timelike_id = timelike_id_or_instance
	elif isinstance(timelike_id_or_instance,timelike):
		timelike_id = timelike_id_or_instance.get_id()
	else:
		raise TypeError("bisect_timelike_edge accepts only timelike edge ids "+
						"or timelike edge instances.")
	return bisect_timelike_sing_id(timelike_id)

# -------------------------------------------------------------------------
#Testing type
def test_edge_type(edge_object):
	"""
	THIS WILL TEST WHICH EDGE TYPE IS THIS!
	"""
	if isinstance(edge_object,timelike): 
		print("It is timelike!")
	elif isinstance(edge_object,spacelike): 
		print("It is spacelike!")
	else: 
		print("No edge type found!")

def test_triangle_type(triangle_object):
	"""
	THIS WILL TEST WHICH TRIANGLE TYPE IS THIS!
	"""
	if isinstance(triangle_object,tts_triangle): 
		print("It is TTS type triangle!")
	elif isinstance(triangle_object, sst_triangle): 
		print("It is SST type triangle!")
	else: 
		print("No triangle type found!")

#------------------------------------------------------------------

# Functions that make simplices and sub-simplices together. The
# work-horses of state manipulation.
#--------------------------------------------------------------------------
def build_sub_edges_of_triangle(edge_list):
	"""
	ONLY USEFUL AT INITIALIZATION. 

	Takes edge list of a triangle of any type
	Check for redundancies.
	Need to recall: edge_list = (timelike1, timelike2, spacelike1)
	"""

	#For timelike edges: 
	timelike_edge_ids = set([])
	for pair in edge_list[0:2]:
		duplicates = timelike.find_duplicates(pair)
		#If there are no duplicates, then we need to make this timelike edge. 
		if len(duplicates) == 0: 
			# And tell our triangle it exists. 
			new_timelike_edge = timelike(pair)
			timelike_edge_ids.add(new_timelike_edge.id)
			# And add it to the timelike instances hash table
			timelike.add(new_timelike_edge)
		#If there is exactly one duplicates, then we simply add its id
		#to the triangle's timelike ID list
		elif len(duplicates) == 1:
			timelike_edge_ids.add(duplicates[0])
		#If there is more than one duplicate, something went very wrong.
		else:
			error_checking.too_many_duplicates('timelike edge', pair, duplicates, 1, 
												'build_sub_edges_of_triangle')

	#There should be exactly 2 timelike edge ids. 
	assert error_checking.check_length(timelike_edge_ids,2,'timelike edge ids',
								'build_sub_edges_of_triangle')

	#For spacelike edges:
	spacelike_edge_ids = set([])
	pair = edge_list[2]
	duplicates = spacelike.find_duplicates(pair)
	#If there are no duplicates, then we need to make this spacelike edge. 
	if len(duplicates) == 0: 
		# And tell our triangle it exists. 
		new_spacelike_edge = spacelike(pair)
		spacelike_edge_ids.add(new_spacelike_edge.id)
		# And add it to the spacelike instances hash table
		spacelike.add(new_spacelike_edge)
	#If there is exactly one duplicates, then we simply add its id
	#to the triangle's timelike ID list
	elif len(duplicates) == 1:
		spacelike_edge_ids.add(duplicates[0])
	#If there is more than one duplicate, something went very wrong.
	else:
		error_checking.too_many_duplicates('spacelike edge', pair, duplicates, 1, 
                                          'build_sub_edges_of_triangle')

	#There should be exactly 1 spacelike edge ids. 
	assert error_checking.check_length(spacelike_edge_ids,1,'spacelike edge ids',
                                     'build_sub_edges_of_triangle')

	return timelike_edge_ids, spacelike_edge_ids


def build_triangle_and_edges(edge_list):
	"""
	ONLY USEFUL AT INITIALIZATION. AND USES TTS TRIANGLE

	Builds a triangle by creating the triangle object. 
	"""
	# local constants
	triangle_length = 3 # Total no. of edges in a triangle. 

	# Make sure we actually have a collection of 3 triangle edges.
	assert len(edge_list) == triangle_length

	# Make a sets of points that is belongs to a triangle.
	points = ut.set_union(edge_list)

	#Make sure we actually have a collection of 3 triangle vertices. 
	assert len(points) == triangle_length

	# Generate a list of point ids. 
	points = [vertex.parse_input(t).get_id() for t in points]

	# Type-cast to eliminate duplicates.
	vertices = set(points)

	# Build the timelike and spacelike edges contained by triangle of any 
	# and return their ids. 
	# build_sub_edges_of_triangle runs some error checking too.
	timelike_edge_ids, spacelike_edge_ids = build_sub_edges_of_triangle(edge_list)

	# RIGHT NOW, WE ARE ONLY USING TTS TRIANGLE FOR INTIALIZATION OF OUR LATTICE
	# Check to see if the triangle we want to build already exists. 
	tts_duplicates = tts_triangle.find_duplicates(vertices,spacelike_edge_ids,
	                                                      timelike_edge_ids)

	# If there is one duplicate, work with it. If there is more than
	# one, raise an error. If there are no duplicates, make that 
	# triangle! 
	if len(tts_duplicates) == 0:
		# Make a triangle of tts type:
		t = tts_triangle(vertices, spacelike_edge_ids, timelike_edge_ids)
		tts_triangle_id = t.id # Ensure we have the id for this triangle
		tts_triangle.add(t) # Add this triangle to its hash table
	elif len(tts_duplicates) == 1:
		triangle_id = tts_duplicates[0] # The id for our triangle
	else: #If len(tts_duplicates)>1, something went very wrong. 
		assert error.checking.too_many_duplicates('tts_triangle', vertices, tts_duplicates, 1,
			                                       'build_triangle_and_edges') 

	return tts_triangle_id


def remove_triangle(triangle_id_or_instance, triangle_type):
	"""
	Deletes a triangle of specific type from the corresponding hash table.
	 Moreover, removes it from it's neighbors list of neighbors and vertices
	Input: triangle_type = tts_triangle or sst_triangle
	"""
	# Interpret input
	if type(triangle_id_or_instance) == int:
		triangle_id = triangle_id_or_instance
		triangle_instance = triangle_type.instances[triangle_id]
	elif isinstance(triangle_id_or_instance, triangle_type):
		triangle_instance = triangle_id_or_instance
		triangle_id = triangle_instance.get_id()
	else:
		raise ValueError("We need a triangle instance or an ID here")

	# Delete the triangle's id from neighbors triangles
	for n in triangle_instance.get_tts_neighbors():
		if triangle_type == tts_triangle:
			n.remove_tts_neighbor(triangle_id)
		elif triangle_type == sst_triangle:
			n.remove_sst_neighbor(triangle_id)

	for n in triangle_instance.get_sst_neighbors():
		if triangle_type == tts_triangle:
			n.remove_tts_neighbor(triangle_id)
		elif triangle_type == sst_triangle:
			n.remove_sst_neighbor(triangle_id)

	# Delete the triangle's id from neighbors vertices
	if triangle_type == tts_triangle:
		for v in triangle_instance.get_vertices():
			v.tts_triangles.remove(triangle_id)

	elif triangle_type == sst_triangle:
		for v in triangle_instance.get_vertices():
			v.sst_triangles.remove(triangle_id)

	#--------------------------------------------------------------
