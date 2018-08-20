"""
Path: /Full_cdt_one_plus_one/move_factory.py

Time-stamp: <2017-12-23 14:57:40 (Damodar)>
Author: Damodar Rajbhandari (dphysicslog@gmail.com)

Description: Contains the collection of moves.

"""
# Dependencies
#--------------
import numpy as np 
import scipy as sp 	

# Class data structure we need
#------------------------------
from triangulations import *
import sub_triangle_property as st
import utilities as ut
import error_checking
import initialization 
import state_tracking as s

#Importing all the moves
#----------------------
import sys
sys.path.append('moves')
from AlexanderMove import *
from PinchingMove import *
from CollapseMove import *

# Make a list of move classes.
#----------------------------
#list_of_all_moves = [AlexanderMove, PinchingMove]
increase_move = [AlexanderMove]
col = [CollapseMove]
list_of_all_moves = [AlexanderMove, CollapseMove]

class MovesFactory:
	"""
	A class for the list of moves. 
	"""

	def __init__(self, all_moves = list_of_all_moves):
		self.all_moves = all_moves

	def picked_vertex(self):
		"""
		Returns the random vertex from the spacetime graph.
		"""
		vertices = list(st.vertex.instances.values())
		pick_vertex = np.random.choice(vertices)

		return pick_vertex

	def picked_edge(self,edge_type):
		"""
		Returns the random edge where edge type is specified in
		the input. i.e.
		get_edges("spacelike") OR,
		get_edges("timelike") 
		"""
		pick_vertex = self.picked_vertex()
		if edge_type == "spacelike":
			connected_edges = list(pick_vertex.spacelike_edges)
			pick_edge = st.spacelike.parse_input(int(np.random.choice(connected_edges)))

		elif edge_type == "timelike":
			connected_edges = list(pick_vertex.timelike_edges)
			pick_edge = st.timelike.parse_input(int(np.random.choice(connected_edges)))

		return pick_edge


	def find_two_triangles(self):
		"""
		After picking a spacelike/timelike edge at random, return the two
		tts/sst triangles. For not to voilate the causality, we use tts triangles
		with spacelike edge shared.
		WILL NOT WORK FOR PINCHING MOVE.
		"""
		tts_triangles = list(st.tts_triangle.instances.values())
		pick_spacelike = self.picked_edge("spacelike")

		share_tts_triangles = []
		for s in tts_triangles:
			if pick_spacelike.id in s.spacelike_edges:
				share_tts_triangles.append(s)

		if len(share_tts_triangles) !=2:
			raise ValueError("Need to be exactly 2 tts triangles that share spacelike.")

		return pick_spacelike, share_tts_triangles


	def try_random(self):
		"""
		Randomly pick a move from the list of all moves.
		"""
		mdata = None
		# The move we will attempt:
		try_move = np.random.choice(self.all_moves)
		if try_move != PinchingMove: # WILL NOT WORK FOR PINCHING MOVE
			# Take two triangles at random
			pick_spacelike, share_tts_triangles = self.find_two_triangles()
			# Try the move, return the move data
			mdata = try_move(pick_spacelike, share_tts_triangles)
		return mdata

