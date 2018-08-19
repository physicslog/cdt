"""
Path: /Full_cdt_one_plus_one/moves/CollapseMove.py

Time-stamp: <2018-01-28 11:29:09 (Damodar)>
Author: Damodar Rajbhandari (dphysicslog@gmail.com)

Description: This is a module where the Collapse move
is defined. Also called (2 -> 0) move.

Move behavior: Given any two tts triangles that share same
              spacelike edge, this moves collapse the 
              triangles.

             0                                     v'
            / \                                    |
           /   \                                   |
          /     \                                  |
         /  tts  \                                 |
        v---------w            -->                 n
         \  tts  /                                 |
          \     /                                  |
           \   /                                   |
            \ /                                    |
             0                                     w'

        FIGURE: Collapse move 

       * PROBABILITY OF A GIVEN COLLAPSE MOVE IS
         [Ben Rujil, 2013 LCDT]
             P_{alex} = \frac{1}{N*N_{e}(v)} + \frac{1]{N*N_{e}(w)}
             where, N is the number of vertices in our triangulated spacetime
             and, N_{e}(x) is the neighbours of x. 

       * INVERSE PROBABILITY is [Ben Rujil, 2013 LCDT]
             P^{-1}_{collapse} = \frac{1}{N-1}*
             \frac{2}{(N_{e}(v)+N_{e}(w)-4)(N_{e}(v)+N_{e}(w)-5)}
"""

# Class data structure we need
#------------------------------
from Move import * 

# Collapse Move Class
#---------------------

class CollapseMove(AbstractMove):
	"""
	This class consists of the methods that define the
	Alexander move.
	"""

	def get_ratio_trial_probability(self):
		"""
		* Returns the ratio of trial/proposing probabilities of Triangulations T1 and T2.

		* PROBABILITY OF A GIVEN COLLAPSE MOVE IS [Ben Rujil, 2013 LCDT];
					
					g(T1->T2) = P_{alex} = \frac{1}{N*N_{e}(v)} + \frac{1]{N*N_{e}(w)}

					where, N is the number of vertices in our triangulated spacetime
					and, N_{e}(x) is the neighbours of x. i.e. total number of spacelike
					edges and timelike edges attached to a vertex.

		* INVERSE PROBABILITY is [Ben Rujil, 2013 LCDT]
					g(T2->T1) = P^{-1}_{collapse} = \frac{1}{N-1}*
						\frac{2}{(N_{e}(v)+N_{e}(w)-4)(N_{e}(v)+N_{e}(w)-5)}
		"""
		P_col = (1.0/(self.N*self.N1)) + (1.0/(self.N*self.N2))
		P_inverse_col = (1.0/(self.N-1.0))*(2.0/((self.N1+self.N2-4.0)*(self.N1+self.N2-5.0)))
		return P_inverse_col/P_col

	def get_dNtts_dNsst(self):
		"""
		Return the change in no. of tts triangle and sst triangle during this
		move.
		"""
		dNtts = -2.0
		dNsst = 0

		return dNtts, dNsst

	#------------------------------------------------------------
	# EXTRACT ALL THE INFORMATION FROM THE SELECTED TWO TRIANGLES
	#------------------------------------------------------------
	def delete_timelike_and_its_attached(self):
		"""
		Delete any one old timelike edges from neighbor vertices & triangles
		"""
		# Find two timelike edges which shares self.vertex1
		two_timelike_edges_shares_v1 = [] 
		for r in self.extract_timelike_edges():
			for p in self.extract_timelike_edges():
				if r != p:
					if self.vertex1.id in r.vertices and self.vertex1.id in p.vertices:
						two_timelike_edges_shares_v1 += [r,p]

		# Find two timelike edges which shares self.vertex2 
		two_timelike_edges_shares_v2 = [] 
		for d in self.extract_timelike_edges():
			for s in self.extract_timelike_edges():
				if d != s: 
					if self.vertex2.id in d.vertices and self.vertex2.id in s.vertices:
						two_timelike_edges_shares_v2 += [d,s]

		# Delete and add timelike edges from tts & sst:
		for i in two_timelike_edges_shares_v2[0:2]:
			attached_vertices = [vertex.instances[j] for j in i.vertices]
			[k.timelike_edges.remove(i.id) for k in attached_vertices]
			for l in self.share_tts_triangles:
				for m in l.get_tts_neighbors():
					if m not in self.share_tts_triangles:
						if i.id in m.timelike_edges:
							m.timelike_edges.remove(i.id)
							for z in two_timelike_edges_shares_v1[0:2]:
								for x in z.vertices:
									if x != self.vertex1.id:
										if x in m.vertices:
											m.timelike_edges.add(z.id)

				for n in l.get_sst_neighbors():
					if n not in self.share_tts_triangles:
						if i.id in n.timelike_edges:
							n.timelike_edges.remove(i.id)
							for z in two_timelike_edges_shares_v1[0:2]:
								for x in z.vertices:
									if x != self.vertex1.id:
										if x in n.vertices:
											n.timelike_edges.add(z.id)

			timelike.delete(i.id)

	def add_tri_neighbors(self):
		"""
		Add tts triangle neighbors
		"""
		for l in self.share_tts_triangles:
			for m in l.get_tts_neighbors():
				for n in l.get_tts_neighbors():
					if m != n:
						if m not in self.share_tts_triangles and n not in self.share_tts_triangles:
							m.tts_neighbors.add(n.id)
							n.tts_neighbors.add(m.id)


	#-------------------------------------------------------------------
	# Delete the necessary objects from the graph and update the graph.
	#-------------------------------------------------------------------
	def extract_all_info_and_update(self):
		"""
		Update all the informations of two simplices that is required!
		"""

		# 1. Update the 0w and w0 timelike edges information into 0v and v0.
		# 2. Delete 0w and w0 timelike edges
		self.delete_timelike_and_its_attached()

		self.add_tri_neighbors()


		# 3.Delete the neighbors self.share_tts_triangles[0] and [1] from triangulations object.
		self.delete_tts_triangles_attached()
		# 4. Delete self.share_tts_triangles from tts_triangle object.
		self.delete_old_triangles()

		# 5. Delete self.pick_spacelike from the self.vertex1, self.vertex2
		# and spacelike instances
		self.delete_spacelike_attached()
		spacelike.delete(self.pick_spacelike.id)

		# 6. Announce the information to self.vertex2 's neighbors triangle that
		# self.vertex2 will be deleted soon! So, delete it!
		[i.vertices.remove(self.vertex2.id) for i in self.vertex2.get_tts_triangles()]
		[i.vertices.remove(self.vertex2.id) for i in self.vertex2.get_sst_triangles()]
		[i.vertices.remove(self.vertex2.id) for i in self.vertex2.get_timelike_edges()]
		[i.vertices.remove(self.vertex2.id) for i in self.vertex2.get_spacelike_edges()]

		# 7. Merge the self.vertex2 information into self.vertex1.
		[self.vertex1.tts_triangles.add(i) for i in self.vertex2.tts_triangles]
		[self.vertex1.sst_triangles.add(i) for i in self.vertex2.sst_triangles]
		[self.vertex1.timelike_edges.add(i) for i in self.vertex2.timelike_edges]
		[self.vertex1.spacelike_edges.add(i) for i in self.vertex2.spacelike_edges]

		# 8. Add the self.vertex1 information into self.vertex1 neighbors.
		[i.vertices.add(self.vertex1.id) for i in self.vertex2.get_tts_triangles()]
		[i.vertices.add(self.vertex1.id) for i in self.vertex2.get_sst_triangles()]
		[i.vertices.add(self.vertex1.id) for i in self.vertex2.get_timelike_edges()]
		[i.vertices.add(self.vertex1.id) for i in self.vertex2.get_spacelike_edges()]

		# 9. delete the self.vertex2
		vertex.delete(self.vertex2.id)






