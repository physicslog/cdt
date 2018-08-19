"""
Path: /Full_cdt_one_plus_one/moves/move.py

Time-stamp: <2017-12-27 07:56:26 (Damodar)>
Author: Damodar Rajbhandari (dphysicslog@gmail.com)

Description: This module contains an abstract base class
             for all the moves.

"""

# Dependencies
#--------------
import numpy as np 
from numpy.random import * 
import scipy as sp
from abc import ABC, abstractmethod

# Class data structure we need
#------------------------------
import sys
sys.path.append('../')
from triangulations import * 
from sub_triangle_property import * 
import utilities as ut 
import state_manipulation as sm


# Abstract base class
#---------------------

class AbstractMove(ABC):
	"""
	This class is an abstract base class for all 
	the moves. 
	"""

	def __init__(self, pick_spacelike, share_tts_triangles):
		self.pick_spacelike = pick_spacelike
		self.vertex1 = vertex.parse_input(list(pick_spacelike.vertices)[0])
		self.vertex2 = vertex.parse_input(list(pick_spacelike.vertices)[1])
		self.share_tts_triangles = share_tts_triangles

		# Total number of vertices in triangulated spacetime. 
		self.N = len(vertex.instances)

		# Total number of neighbors of vertex1(or vertex2)
		self.N1 = len(self.vertex1)
		self.N2 = len(self.vertex2)


	@abstractmethod
	def get_ratio_trial_probability(self):
		"""
		For simple simulator, trial probabilities are same but in our case, it's not!
		* Returns the ratio of trial/proposing probabilities of Triangulations T1 and T2.
		"""
		pass


	@abstractmethod
	def get_dNtts_dNsst(self):
		"""
		Return the change in no. of tts triangle and sst triangle during this move.
		"""
		pass


	# EXTRACT ALL THE INFORMATION FROM THE SELECTED TWO TRIANGLES AND 
	# THEN DELETE THE EDGE AND SHARE TRIANGLES

	def extract_timelike_edges(self):
		"""
		Extract the timelike edges from two triangles. 
		"""
		#Timelike edges from first triangle.
		timelike_t1 = list(self.share_tts_triangles[0].get_timelike_edges())
		#Timelike edges from second triangle
		timelike_t2 = list(self.share_tts_triangles[1].get_timelike_edges())
		return timelike_t1 + timelike_t2

	def extract_vertices(self):
		"""
		Extract the vertices from two triangles.
		"""
		# Boundary of two triangles
		endpoints = self.extract_timelike_edges()
		# Extracted all the vertices of all the timelike edges.
		extracted_vertices_ids = ut.set_union([e.get_vertex_ids() for e in endpoints])
		extracted_vertices = [vertex.instances[i] for i in extracted_vertices_ids]
		return extracted_vertices

	def extract_pick_spacelike(self):
		"""
		Extract all the vertex instances from the self.pick_spacelike
		"""
		return self.vertex1 , self.vertex2

	def delete_spacelike_attached(self):
		"""
		Delete self.pick_spacelike edge from the vertex.
		"""
		# get the id of edge
		pick_spacelike_id = self.pick_spacelike.id

		# Delete from vertex instances
		vertices = list(self.extract_pick_spacelike())
		[i.spacelike_edges.remove(pick_spacelike_id) for i in vertices]

	def delete_tts_triangles_attached(self):
		"""
		Delete self.share_tts_triangles from the vertex, 
		tts_triangle and sst_triangle instances.
		"""
		for i in self.share_tts_triangles:
			sm.remove_triangle(i,tts_triangle)

	def delete_old_triangles(self):
		"""
		Delete the old triangles that share the self.spacelike edge.
		"""
		# Delete these tts triangle instances.
		tts_triangle.delete(self.share_tts_triangles)

	def update_all(self, req_vertices):
		"""
		Update the neighbors!
		"""
		for point in req_vertices:
			point.find_and_set_tts_triangles()
			point.find_and_set_sst_triangles()
			point.find_and_set_timelike_edges()
			point.find_and_set_spacelike_edges()
			point.connect_surrounding_triangles()