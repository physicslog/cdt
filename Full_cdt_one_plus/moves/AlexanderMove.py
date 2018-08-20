"""
Path: /Full_cdt_one_plus_one/moves/AlexanderMove.py

Time-stamp: <2017-12-13 08:35:53 (Damodar)>
Author: Damodar Rajbhandari (dphysicslog@gmail.com)

Description: This is a module where the Alexander move
is defined. Also called (2 -> 4) move.

Move behavior: Given any two tts triangles that shares same spacelike edge, 
               this move makes 4 tts triangles from 2. 

             0                                     v'
            / \                                   /|\
           /   \                                 / | \
          /     \                               /  |  \
         /  tts  \                             /   |   \
        v---------w            -->            0----n----0
         \  tts  /                             \   |   /
          \     /                               \  |  /
           \   /                                 \ | /
            \ /                                   \|/
             0                                     w'

        FIGURE: One of the eight possible Alexander moves. Because every
                possible link configuration on the rhombus is allowed. 

              * THE NEW VERTEX (n) AT THE CENTER OF THE RHOMBUS SHOULD 
                BE CAUSAL.
              * THE LINK TYPE OF THE NEWLY ADDED LINK SHOULD BE OPPOSITE 
                TO THAT OF THE CHOSEN LINK. 

               PROBABILITY OF A GIVEN ALEXANDER MOVE IS [Ben Rujil, 2013 LCDT];
                     P_{alex} = \frac{1}{N*N_{e}(v)} + \frac{1]{N*N_{e}(w)}
                     where, N is the number of vertices in our triangulated spacetime
                     and, N_{e}(x) is the neighbours of x. 

               INVERSE PROBABILITY, is a probability of selecting the newly created vertex (n)
               which is [Ben Rujil, 2013 LCDT], 
                     P^{-1}_{alex} = \frac{1]{N+1}

               Since, the volume is changed, we need to check to see if 
               the volume change will make the move topologically 
               unacceptable.

Algorithm: 
- Randomly pick anyone vertex and find the edges that are connected to it. 
- Check whether these edges are spacelike or not. 
- If there are more than one spacelike edges connected to it, randomly pick anyone spacelike edge.
- Find the triangles that share this spacelike edge.
- Apply the Metropolis-Hastings Algorithm whether or not we can create a new point on this edge.
  This means we can create four triangles.
- If yes, delete those triangle IDs and create a new point on this edge. 
- Create two timelike edges by joining the new point and the third vertex (the vertex that is 
  not associated with spacelike edge that we have chosen) of the two previous triangles.
"""

# Class data structure we need
#--------------------------------
from Move import *


# Alexander Move Class 
#----------------------

class AlexanderMove(AbstractMove):
	"""
	This class consists of the methods that define the Alexander 
	move.
	"""

	def get_ratio_trial_probability(self):
		"""
		 For simple simulator, trial probabilities are same but in our case, it's not!

		* Returns the ratio of trial/proposing probabilities of Triangulations T1 and T2.

		PROBABILITY OF A GIVEN ALEXANDER MOVE IS [Ben Rujil, 2013 LCDT];
					
					g(T1->T2) = P_{alex} = \frac{1}{N*N_{e}(v)} + \frac{1]{N*N_{e}(w)}

					where, N is the number of vertices in our triangulated spacetime
					and, N_{e}(x) is the neighbours of x. i.e. total number of spacelike
					edges and timelike edges attached to a vertex.

		INVERSE PROBABILITY, is a probability of selecting the newly created vertex (n)
		which is [Ben Rujil, 2013 LCDT], 
					
					g(T2->T1) = P^{-1}_{alex} = \frac{1]{N+1}

		"""
		P_alex = (1.0/(self.N*self.N1)) + (1.0/(self.N*self.N2))
		P_inverse_alex = 1.0/(self.N+1.0)

		return P_inverse_alex/P_alex


	def get_dNtts_dNsst(self):
		"""
		Return the change in no. of tts triangle and sst triangle during this move.

		For Alexander move:
		-------------------
		If we pick two tts triangle then;
		\delta N_{tts} = N_{tts}(T2) - N_{tts}(T1)= (N_{tts}(T1) + 2) - N_{tts}(T1)
		               = 2
		and, \delta N_{sst} = 0

		Else if we pick two sst triangle then;
		\delta N_{sst} = N_{sst}(T2) - N_{sst}(T1)= (N_{sst}(T1) + 2) - N_{sst}(T1)
		               = 2
		and, \delta N_{tts} = 0

		But there should not be a combination of sst and tts triangles that share the 
		same edge because it voilate the local causality. 

		FOR OUR ALEXANDER MOVE, IF WE CHOSE TWO TTS TRIANGLES:
		\delta Ntts = 2 because Ntts(T2) = Ntts(T1) + 2
		and \delta Nsst = 0. 
		If we chose two sst triangles:
		\delta Ntts = 0 and \delta Nsst = 2
		"""
		dNtts = 2.0
		dNsst = 0

		return dNtts, dNsst

	# BISECT SELF.PICK_SPACELIKE WITH THE MIDPOINT A NEW VERTEX. 

	def bisect_spacelike_create_vertex(self):
		"""
		Create a new vertex and two spacelike edges by bisecting the
		self.pick_spacelike and delete the self.pick_spacelike.
		i.e. [new_spacelike_edge_instances, new_vertex_instance]
		And, delete the self.pick_spacelike edge.
		"""

		return sm.bisect_spacelike(self.pick_spacelike)

	def create_new_timelike_edges(self, central_vertex):
		"""
		Returns two new timelike edges!
		"""
		vertices = [i for i in self.extract_vertices() if i != self.vertex1 and i != self.vertex2]
		# Combine vertices with ids
		cv = {central_vertex.id, vertices[0].id, vertices[1].id}
		# Create two edges which is not specify by edge type!
		created_edges = [i for i in ut.k_combinations(cv,2) if i != {vertices[0].id, vertices[1].id}] 

		# Now, create two new timelike edges
		new_timelike_edges_instances = set([])
		for endpoint_pair in created_edges:
			e = timelike(endpoint_pair)
			timelike.add(e)
			new_timelike_edges_instances.add(e)

		return new_timelike_edges_instances


	#-----------------------------------------------------------------------------#
	# extract_all_info() IS SUFFIECENT TO EXTRACT ALL THE INFO AND DELETE TASKS!  #
	#-----------------------------------------------------------------------------#
	def extract_all_info_and_update(self):
		"""
		Update all the informations of two simplices that is required
		to build 4 triangles from 2. AND WE CREATE FOUR TTS TRIANGLES!!!
		INFORMATIONS WE HAVE:
		old_timelike_edges, old_vertices, old_tts_neighbors, old_sst_neighbors,
		new_spacelike_edges, new_central_vertex, new_timelike_edges
		
		UPDATE BY CONNECTING ALL THE NEW INFORMATION TO OUR TRIANGULATION
		AND WE DO IT MANUALLY !!!
		"""
		old_timelike_edges = self.extract_timelike_edges()
		old_vertices = self.extract_vertices()

		# Delete the spacelike from self.vertex1 and self.vertex2
		self.delete_spacelike_attached()

		new_spacelike_edges, new_central_vertex = self.bisect_spacelike_create_vertex()
		new_timelike_edges = self.create_new_timelike_edges(new_central_vertex)

		# Delete the neighbors self.share_tts_triangles[0] and [1] from triangulations object.
		self.delete_tts_triangles_attached()
		# Delete self.share_tts_triangles from tts_triangle object.
		self.delete_old_triangles()

		# Creates 4 triangles
		new_tts_triangles = set([])
		for i in old_timelike_edges:
			for j in new_timelike_edges:
				for k in new_spacelike_edges:
					test_vertices = i.vertices | j.vertices | k.vertices
					if len(test_vertices) == 3: # When I found this trick, I loved it!
						nt = tts_triangle(test_vertices, [k.id], [i.id, j.id])
						tts_triangle.add(nt)
						new_tts_triangles.add(nt)

		# Update the informations!
		old_vertices.append(new_central_vertex)
		self.update_all(old_vertices)

