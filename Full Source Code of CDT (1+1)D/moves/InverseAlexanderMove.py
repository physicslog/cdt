"""
Path: /Full_cdt_one_plus_one/moves/InverseAlexanderMove.py

Time-stamp: <2019-01-27 16:03:09 (Damodar)>
Author: Damodar Rajbhandari (dphysicslog@gmail.com)
 
Description: This is a module where the Inverse Alexander move
is defined. Also called (2 -> 4) move.

Move behavior: Given any one vertex which connects 4 tts triangles,
               this move makes 2 tts triangles from 4. Note: We use 
               this move, if Metropolis-Hastings algorithm rejects 
               Alexander move, and vice versa.

                 v'                   0                    
                /|\                  / \                   
               / | \                /   \                  
              /  |  \              /     \                 
             /   |   \            /  tts  \                
            v----n----w   -->    v---------w            
             \   |   /            \  tts  /                
              \  |  /              \     /                 
               \ | /                \   /                  
                \|/                  \ /                   
                 w'                   0                    

           FIGURE: Inverse Alexander Move.

           PROBABILITY OF A GIVEN INVERSE ALEXANDER MOVE IS
           [Ben Rujil, 2013 LCDT];
           P_{ialex} = \frac{1}{N}
           where N is the total number of vertices before applying
           the move.

           INVERSE PROBABILITY is [Ben Rujil, 2013 LCDT];
           P^{-1}_{ialex} = \frac{1}{N-1}(\frac{1}{N_{e}(v)} + 
                                          \frac{1}{N_{e}(w)})
           where N_{e}(x) is the neighbours of x such that the edge
           vw is a timelike edge.

Algorithm:
- Randomly pick a vertex
- Check that vertex contain extactly four tts triangles attached to 
  it or not.
- If Flase! Select another vertex and goto step 2.
- If True! Apply below steps:
- Extract all the vertices, tts, sst, timelike, and spacelike information
- Connect vertices v and w, then make it spacelike edge
- Create two tts triangles. 
- Connect everything! 
- Delete central vertex and previous four tts triangles on the picked region.
- Remove information that above geometrical objects are deleted,
- Provide information about newly created objects.
"""

# Dependencies
#--------------
import numpy as np 
from numpy.random import * 
import scipy as sp

# Class data structure we need
#------------------------------
import sys
sys.path.append('../')
from triangulations import * 
from sub_triangle_property import * 
import utilities as ut 
import state_manipulation as sm
from Move import * 

# Inverse Alexander Move Class
#------------------------------

class InverseAlexanderMove(AbstractMove):
	"""
	This class consists of the methods that define the 
	Inverse Alexander move. 
	"""

	def __str__(self):
		"Prints the name of the Monte-Carlo move"
		return "I'm the inverse of Alexander move."


	def __init__(self, central_vertex):
		# Get central vertex (id or instance) and return its instances
		self.central_vertex = vertex.parse_input(central_vertex)
		# Total number of vertices in triangulated spacetime.
		self.N = len(vertex.instances)
		# Finding what are the spacelike & timelike edges, where one vertex is we
		# are going to find and another is self.N
		self.old_spacelike_edges = list(self.central_vertex.spacelike_edges)
		self.old_timelike_edges = list(self.central_vertex.timelike_edges)
		self.old_tts_triangles = list(self.central_vertex.tts_triangles)

		# Finding the boundary vertices (v,w)
		vertices_v_w = []
		for i in self.old_spacelike_edges:
			for j in spacelike.parse_input(i).vertices:
				if j != self.central_vertex.id:
					vertices_v_w.append(j)
		if len(vertices_v_w) != 2:
			raise TypeError("Our Triangulations is broken at this point")
		# We are using the region from a triangulations before move and
		# try to find the total number neigbors vertices attached to v 
		# and w is because, the total number is unchanged even after 
		# the move is applied. So, total number of neighbor vertices
		# of vertex 1(or vertex 2)
		# Finding the value of N1 and N2
		self.N1 = len(vertex.instances[vertices_v_w[0]])
		self.N2 = len(vertex.instances[vertices_v_w[1]])

		# Finding the boundary vertices (other remaining vertices)
		vertices_others = []
		for i in self.old_timelike_edges:
			for j in timelike.parse_input(i).vertices:
				if j != self.central_vertex.id:
					vertices_others.append(j)
		if len(vertices_others) != 2:
			raise TypeError("Our Triangulations is broken at this point")

		# All boundary vertices ids
		self.ver_v_w = vertices_v_w
		self.ver_others = vertices_others

	def check_neighbor_tts_triangles(self):
		"""
		Check wheither there is four tts triangles 
		attached to a vertex or not. If yes, return
		booleen TRUE.
		"""
		if len(self.old_tts_triangles) == 4:
			return True
		else:
			return False

	def get_ratio_trial_probability(self):
		"""
		Calculating the trial probabilities and then return their ratio.
		"""
		P_ialex = 1.0/(self.N)
		P_inverse_ialex = (1.0/(self.N - 1))*((1.0/(self.N1)) + (1.0/(self.N2)))

		return P_inverse_ialex/P_ialex

	def get_dNtts_dNsst(self):
		"""
		Return the change in the no. of tts and sst triangles during this 
		move.
		"""
		dNtts = -2.0 
		dNsst = 0

		return dNtts, dNsst

	# From above, we have all the necessary ingrediant to prepare 
	# Inverse Alexander Move. Now, below is an implementation of it.
			
	def extract_all_info_and_update(self):
		"""
		Update all the informations
		"""
		# Says there are four tts attached to central vertex
		if self.check_neighbor_tts_triangles() == True:
			
			# Create one new spacelike edge
			sp = spacelike(self.ver_v_w)
			spacelike.add(sp)

			# Creates two new tts triangles
			for i in self.ver_others:
				# Creating the point list representing the triangle's vertices
				tri_vertices = [i, self.ver_v_w[0], self.ver_v_w[1]]
				# Finding the timelikes
				te = []
				for j in vertex.parse_input(i).timelike_edges:
					for k in self.ver_v_w:
						if k in timelike.parse_input(j).vertices:
							te.append(j)

				if len(tri_vertices) == 3:
					nt = tts_triangle(tri_vertices, [sp.id], te)
					tts_triangle.add(nt)

				else:
					raise TypeError("Our Triangulations is broken at this point")


			# Delete old tts triangle from neighbor triangles and vertices 
			for i in self.old_tts_triangles:
				sm.remove_triangle(i,tts_triangle)

			# Delete old spacelike edges
			for i in self.old_spacelike_edges:
				for j in self.ver_v_w:
					if j in spacelike.parse_input(i).vertices:
						vertex.parse_input(j).spacelike_edges.remove(i)
			
			# Delete old timelike edges
			for i in self.old_timelike_edges:
				for j in self.ver_others:
					if j in timelike.parse_input(i).vertices:
						vertex.parse_input(j).timelike_edges.remove(i)


			# Delete Central vertex
			vertex.delete(self.central_vertex)
			# Delete four old tts triangles
			tts_triangle.delete(self.old_tts_triangles)
			# Delete two timelikes
			timelike.delete(self.old_timelike_edges)
			# Delete two spacelikes
			spacelike.delete(self.old_spacelike_edges)
			
			# Update: connect all the triangles with their neighbors
			boundary_vertices = []
			for i in self.ver_v_w + self.ver_others:
				boundary_vertices.append(vertex.parse_input(i))

			self.update_all(boundary_vertices)

		else:
			# Says there are NOT four tts attached to central vertex
			#print("No inverse alexander move is processed.")
			pass
			





