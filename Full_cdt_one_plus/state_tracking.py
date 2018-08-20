"""
Path: /Full_cdt_one_plus_one/state_tracking.py

Time-stamp: <2017-12-18 06:57:19 (Damodar)>
Author: Damodar Rajbhandari (dphysicslog@gmail.com)
 
Description: This module will keep track of the toroidal 
             topology. This file contains classes and 
             functions for measuring properties of
             the generated sphere.
"""

#Dependencies:
#-------------
import numpy as np 
import scipy as sp 

#Class data structures:
#---------------------------------
import triangle_property as tp
import sub_triangle_property as st
import utilities as ut 
import state_manipulation as sm
import error_checking 
#---------------------------------- 

#-------------------------------------------------#
# Torus base class that tracks of the property of #
# it and gives the state of our simulation        #
#-------------------------------------------------#

class torus:
	"""
	Contains and calculates the state information for the 
	torus at a given time-step. Meant to be initialized. 

	It's worth noting that printing the torus instances is 
	useful. 
	"""

	def __init__(self):
		# Initialization routine call here. 
		pass

	def euler_characteristic(self):
		"Calculate the Euler characteristic of the torus"
		v = st.vertex.count_instances() # vertices
		e = st.spacelike.count_instances() + st.timelike.count_instances()
		t = st.tts_triangle.count_instances() + st.sst_triangle.count_instances()
		return v - e + t

	def curvature_total(self, normalized = False):
		"""
		Calculates the total Gauss curvature of the torus. If normalized = True
		, also divide by the number of vertices to get an average. 
		"""
		integrated_curvature = 0 
		for point in st.vertex.instances.values():
			integrated_curvature += point.curvature()

		# Maybe normalized
		if normalized:
			integrated_curvature /= float(st.vertex.count_instances)

		return integrated_curvature

	def curvature_std(self):
		"""
		Calculates standard deviation of the Gauss curvature over the
		torus.
		"""
		# Make a list of all local curvatures
		local_curvatures = [point.curvature() for \
                                point in sd.vertex.instances.values()]
		# Get the standard deviation
		return np.std(local_curvatures)

	def surface_area(self):
		"""
		Calculates the surface area of the torus. Basically syntactic sugar.
		returns no. of tts_triangles + no. of sst_triangles
		"""
		return sd.tts_triangle.count_instances() + st.sst_triangle.count_instances()

	def get_vertices(self):
		"Returns a string each vertex in the torus. Output could be long."
		outstring = ''
		for v in st.vertex.instances.values():
			outstring += str(v) + '\n'
		return outstring

	def get_spacelike(self):
		"Returns a string each spacelike edge in the torus. Output could be long."
		outstring = ''
		for e in st.spacelike.instances.values():
			outstring += str(e) + '\n'
		return outstring

	def get_timelike(self):
		"Returns a string each timelike edge in the torus. Output could be long."
		outstring = ''
		for e in st.timelike.instances.values():
			outstring += str(e) + '\n'
		return outstring

	def get_tts_triangle(self):
		"Returns a string each tts triangle in the torus. Output could be long."
		outstring = ''
		for t in sd.tts_triangle.instances.values():
			outstring += str(t) + '\n'
		return outstring

	def get_sst_triangle(self):
		"Returns a string each sst triangle in the torus. Output could be long."
		outstring = ''
		for t in sd.sst_triangle.instances.values():
			outstring += str(t) + '\n'
		return outstring

	def __str__(self):
		"The state of the system at a given time."
		outstring = """Torus Current state:
---------------------------------TOPOLOGY----------------------------------
Number of Vertices:   {}
Number of Spacelike:  {}
Number of Timelike:   {}
No. of TTS Triangles: {}
No. of SST Triangles: {}
Euler Characteristic: {}
---------------------------------CURVATURE---------------------------------
Total: {}
Mean:  {}
Std:   {}
""".format(st.vertex.count_instances(),
			st.spacelike.count_instances(),
			st.timelike.count_instances(),
			sd.tts_triangle.count_instances(),
			sd.sst_triangle.count_instances(),
			self.euler_characteristic(),
			self.curvature_total(),
			self.curvature_total(True),
			self.curvature_std())
		return outstring
#---------------------------------------------------------------------------

