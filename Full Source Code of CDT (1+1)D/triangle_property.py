"""
Path: /Full_cdt_one_plus_one/triangle_property.py

Time-stamp: <2017-12-11 22:32:34 (Damodar)>
Author: Damodar Rajbhandari (dphysicslog@gmail.com)

Description: This file consists of class for triangle's edges, 
vertices and triangle itself. 

"""

#---------------------------------------------------------#
# Dependencies
import numpy as np
import scipy as sp
import utilities as ut

#Data structure we need!
from triangulations import * #Required for parent class.

import sub_triangle_property as st # TO VALID CIRCULAR DEPENDENCY
# To check sub-triangle_property syntaxes, comment sub_triangle_property
#************************************************************************

#------------------------------------------#
#               Common CLASSES             #
#------------------------------------------#


#***********************************************#
#      Defining class for edges of a triangle.	#
#                         -----                 #
#***********************************************#

class edge(Triangulations):
	"""
	A class that keeps track of the triangle's edges.
	"""

	def set_vertices(self,new_vertices):
		"Takes an input list or set and resets self's vertices/endpoints."
		if len(new_vertices) == 2 or len(new_vertices) == 0:
			self.vertices = set(new_vertices)
			return self.vertices
		else:
			print ("Error! Wrong number of vertices! Nothing changed.")
			return self.vertices

	def get_vertices(self):
		"Returns the instances, not the ids."
		return [st.vertex.instances[v] for v in list(self.vertices)]

	def get_vertex_ids(self):
		"Returns the ids."
		return self.vertices

	# Duplicate checking
	@classmethod
	def find_duplicates(self,vertex_list):
		"""
		Searches through self.instances for edges with the same
		vertices as in vertex_list. Requires set equality. Returns
		the duplicates.
		"""
		duplicates = []
		for e in self.instances.values():
			if e.vertices == set(vertex_list):
				duplicates.append(e.id)
		return duplicates

	def bisect(self):
		"""
		If the edge length of the triangle is EQUILATERAL, cuts it in
		two and generates two edges with a point between them. Returns
		the edges and the new point ID generated.
		"""
		if len(self.vertices) != 2:
			print ("Your edge doesn't have the right number of points!")
		newpoint = st.vertex.make_id()
		new_edges = [set([newpoint,point]) for point in self.vertices]
		return [new_edges, newpoint]

	def check_topology(self,return_value=False):
		"""
		Check to ensure that the number of endpoints is correct.
		"""
		assert len(self.vertices) == 2 or len(self.vertices) == 0
		if return_value:
			print ("Topology is okay.")

#*****************************************************************#

#---------------------------#
# The triangle class        #
#---------------------------#

class triangle(Triangulations):
	"""
	A class for keeping track of triangle edges
	"""

	def check_neighbor_edge_correlation(self):
		"""
		Ensures there is a bijection between neighbors and edges of same type
		This method can be compatible with both the types of triangle.
		"""
		spacelike_edges = set([])
		timelike_edges = set([])
		for n in self.get_sst_neighbors():
			shared_spacelike_edges = ut.set_intersection([n.spacelike_edges, self.spacelike_edges])
			shared_timelike_edges = ut.set_intersection([n.timelike_edges, self.timelike_edges])
			if len(shared_spacelike_edges) == 1 : 
				spacelike_edges.add(list(shared_spacelike_edges)[0])
			elif len(shared_timelike_edges) == 1 :
				timelike_edges.add(list(shared_timelike_edges)[0])
			else: 
				print(" Sorry, there is no shared edges of sst neigbors.")
		for n in self.get_tts_neighbors():
			shared_spacelike_edges = ut.set_intersection([n.spacelike_edges, self.spacelike_edges])
			shared_timelike_edges = ut.set_intersection([n.timelike_edges, self.timelike_edges])
			if len(shared_spacelike_edges) == 1 : 
				spacelike_edges.add(list(shared_spacelike_edges)[0])
			elif len(shared_timelike_edges) == 1 :
				timelike_edges.add(list(shared_timelike_edges)[0])
			else: 
				print(" Sorry, there is no shared edges of tts_neighbors.")
		if spacelike_edges != self.spacelike_edges and timelike_edges != self.timelike_edges:
			print("\n Erroneous Triangle!\n")
			print(self)
			raise ValueError("Each neighbor doesnot share exactly 1 edges of same type")

	def check_topology(self, return_value = False): 
		"""
		Ensure that the triangle has the correct number of 
		vertices, edges and neighbors.
		"""
		assert len(self.vertices) == 0 or len(self.vertices) == 3
		edges = len(self.spacelike_edges) + len(self.timelike_edges)
		assert edges == 0 or edges == 3
		neighbors = len(self.sst_neighbors) + len(self.tts_neighbors)
		if not 0 <= neighbors <= 3:
			print("\nErroneous Triangle!\n")
			print(self)
			raise ValueError("Number of neighbors are wrong!")
		if return_value:
			print("Topology is okay.")

	def check_topology_v2(self, return_value = False): 
		"""
		Like check topology, but only allows 3 for each value. 
		USEFUL AFTER INITIALIZATION
		"""
		if len(self.vertices) != 3:
			print(self)
			raise ValueError("Number of vertices is wrong!")
		edges = len(self.spacelike) + len(self.timelike)
		if len(edges) != 3:
			print (self)
			raise ValueError("Number edges is wrong!")
		neighbors = len(self.sst_neighbors) + len(self.tts_neigbors)
		if len(neighbors) != 3:
			print (self)
			raise ValueError("Number neighbors are wrong!")
		if return_value:
			print ("Topology is okay.")

	def check_edge_validity(self): 
		"""
		Checks to make sure that the number of endpoints of edges is
		the same as the number of vertices.
		"""
		spacelike_edges = self.get_spacelike_edges()
		timelike_edges = self.get_timelike_edges()
		spacelike_endpoints = [e.get_vertex_ids() for e in spacelike_edges]
		timelike_endpoints = [e.get_vertex_ids() for e in timelike_edges]
		spacelike_endpoint_union = ut.set_union(spacelike_endpoints)
		timelike_endpoint_union = ut.set_union(timelike_endpoints)
		endpoint_union = spacelike_endpoint_union.union(timelike_endpoint_union)
		assert endpoint_union == self.get_vertex_ids()

	def connect_to_triangle(self, other_triangle):
		"""
		Look for the any type of triangle and check if it shares an
		edge with same type.
		"""
		# Do the triangles have an intersection
		intersection = self.vertices & other_triangle.vertices
		#If the triangles share exactly 2 points, acknowledge their
		# neighborliness.
		if len(list(intersection)) == 2:
			# Add other_triangle as neighbors of self triangle
			if type(other_triangle) == st.tts_triangle:
				self.tts_neighbors.add(other_triangle.id)
			elif type(other_triangle) == st.sst_triangle:
				self.sst_neighbors.add(other_triangle.id)
			# Add self triangle as neighbors of other_triangle:
			if type(self) == st.tts_triangle:
				other_triangle.tts_neighbors.add(self.id)
			elif type(self) == st.sst_triangle:
				other_triangle.sst_neighbors.add(self.id)

		self.check_topology()
		other_triangle.check_topology()


	def remove_tts_neighbor(self,other_triangle): 
		"""
		other_triangle is in self.tts_neighbors, remove it from the
		neighbor list. Accepts ids only.
		"""
		if other_triangle in self.tts_neighbors:
			self.tts_neighbors.remove(other_triangle)

	def remove_sst_neighbor(self,other_triangle): 
		"""
		other_triangle is in self.sst_neighbors, remove it from the
		neighbor list. Accepts ids only.
		"""
		if other_triangle in self.sst_neighbors: 
			self.sst_neighbors.remove(other_triangle)

	# Duplicate checking
	@classmethod
	def find_duplicates(self,vertex_list=False,
						spacelike_edge_list=False,timelike_edge_list=False,
						tts_triangle_list=False,sst_triangle_list=False): 
		"""
		Searches through self.instances for triangles with the same
		vertices or the same edges or the same neighbors as the given lists.
		"""

		duplicates = set([])
		for t in self.instances.values():
			if vertex_list:
				if t.vertices == set(vertex_list):
					duplicates.add(t.id)
			if spacelike_edge_list and timelike_edge_list:
				if t.spacelike_edges == set(spacelike_edge_list) \
				and t.timelike_edges == set(timelike_edge_list):
					duplicates.add(t.id)
			if tts_triangle_list and sst_triangle_list:
				if t.tts_neighbors == set(tts_triangle_list)\
				and t.sst_neighbors == set(sst_triangle_list):
					duplicates.add(t.id)
		return duplicates

	# Vertices:
	def get_vertices(self): 
		"Returns the instances, not the ids."
		return [st.vertex.instances[v] for v in self.vertices]

	def get_vertex_ids(self): 
		"Returns the ids."
		return self.vertices

	# Edges

	def get_timelike_edges(self): 
		"Returns the instances, not the ids."
		return [st.timelike.instances[t_e] for t_e in self.timelike_edges]

	def get_spacelike_edges(self): 
		"Returns the instances, not the ids."
		return [st.spacelike.instances[t_e] for t_e in self.spacelike_edges]

	def get_timelike_edges_ids(self): 
		"Returns the ids."
		return self.timelike_edges

	def get_spacelike_edges_ids(self): 
		"Returns the ids."
		return self.spacelike_edges

	#Neighbor triangles
	def get_tts_neighbors(self): 
		"Returns the instances, not the ids."
		return [st.tts_triangle.instances[tts_t] for tts_t in self.tts_neighbors]

	def get_sst_neighbors(self): 
		"Returns the instances, not the ids."
		return [st.sst_triangle.instances[sst_t] for sst_t in self.sst_neighbors]

	def get_tts_neighbor_ids(self): 
		"Return the ids."
		return self.tts_neighbors

	def get_tts_neighbor_ids(self): 
		"Return the ids."
		return self.tts_neighbors

	def make_outstring(self):
		"""
		Makes a string of the form '(v1, v2, v3)' for vertices. Useful
		for output.
		"""
		assert len(self.vertices) == 3
		v = list(self.vertices)
		return "({} {} {})".format(v[0],v[1],v[2])

	def __add__(self,other_triangle):
		"Equivalent to self.connect_to_triangle(other_triangle)."
		self.connect_to_triangle(other_triangle)
#-------------------------------------------------------------------------
