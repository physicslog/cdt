"""
Path: /Full_cdt_one_plus_one/simulation.py

Time-stamp: <2017-12-23 16:11:06 (Damodar)>
Author: Damodar Rajbhandari (dphysicslog@gmail.com)

Description: This module contains the loops for the Metropolis-
             Hastings algorithm. This will create a strong 
             gravity from very weak gravity.

             This module also contains the class for volume increasing
             simulation where it accept all the volume increasing moves
             and increase the volume to our desire.

"""

#Dependencies
#------------
import numpy as np 
import scipy as sp 
import datetime 

#Class data structures we need
#-----------------------------
from triangulations import *
import sub_triangle_property as st
import state_manipulation as sm
import utilities as ut
import error_checking 
import initialization 
import state_tracking as s 
from move_factory import *


#CONSTANTS
#---------
output_suffix = ".lcdt1p1" #The file ending for files generated
output_prefix = "T2_" #The file prefix for files generated
convergence_name = "_M-OPTIMAL"

#Classes
#-------

# Class for volume increasing moves
#----------------------------------

class VolumeIncreasing:
	"""
	This class job is to increase the volume of our intial spacetime
	by using Alexander move. This should run first 
	before running the Metropolis-Hastings sampling to generate the
	strong gravitational field.
	"""
	def __init__(self,n):
		"""
		n is an integer in which we can create (2*n + 18) tts triangles.
		"""
		self.n = n

	def run(self):
		"""
		Returns (2*n + 18) number of tts triangles.
		"""
		for i in np.arange(self.n):
			simplices = MovesFactory(increase_move).try_random()
			simplices.extract_all_info_and_update()

#------------------------------------------------------------------------


# Class for Metropolis-Hastings sampling
#----------------------------------------

class metropolis: 
	"""
	The metropolis class is an ancestor class and never meant to be 
	initialized. It contains methods to help descendant classes to keep
	surface area of the sphere constant.

	The Lambda term in the action is tuned in this method, so
	that the average area is "target_area".
	
	The parameters;
	* alpha = Ratio between length of spacelike and 
	          timelike links.
	* target_area = Desired number of triangles. This adds an area
	                fixing term that allows for small fluctuations.
	* area_damping_strength = Fluctuation parameter for fixed area range.
	* num_sweeps = Number of sweeps
	* sweep_length = How many iterations should a sweep be?
	"""

	def area_damping(self,surface_area):
		"""
		A area_damping (or, Volume Fixing) method enforce the system size approximately
		of the desired size. Area fixing term can be added to the 
		action that suppresses moves that make the size difference larger
		and favours moves that reduce it. This is because even if we 
		fixed the cosmological constant(\lambda), the system size will
		fluctuate. In order to control the size, we need fix the system
		size, letting the \lambda fluctuate.
		In the literature, mostly a quadratic potential is used
		[arXiv:1102.3929 [hep-th]]:
		           S_{control} = area_damping_strength*(A_{current} - A)^{2}
		where, A_{curr} = current area, A = target area and, 
		area_damping_strength > 0 is a constant that controls how strict 
		area fixing should be. If greater it heavily suppressed the moves.

		An exponential function of S_{control}, we treated as a probability.
		"""
		delta_triangles = (surface_area - self.target_area)**2

		return np.exp(-abs(self.area_damping_strength)*delta_triangles)


	def get_ratio_probability_state(self, Lambda, G, alpha, dNtts, dNsst):
		"""
		Return the raio of probabilities of being in state T1 and T2.
		\frac{P(T1)}{P(T2)} = P_ratio_T1_by_T2 = 
		\exp{\frac{\Lambda}{32*np.pi*G}*(\sqrt{4*\alpha -1}\delta N_{tts} + 
		\sqrt{\alpha*(4-\alpha)}\delta N_{sst})}
		where, \delta N = N_{T2} - N_{T1}
		"""
		P_ratio_T1_by_T2 = np.exp((Lambda/(32*np.pi*G))*(np.sqrt(4*alpha-1)*dNtts+
          np.sqrt(alpha*(4-alpha))*dNsst))

		return P_ratio_T1_by_T2

	def loop_once(self):
		"""
		Runs one iteration of the metropolis loop.
		"""
		# Move data for a random move on a random simplex. 
		mdata = MovesFactory().try_random()

		# If a move is topologically acceptable, check the fitness function,
		# causality check then, and possibly accept it. Otherwise, do noting.
		if mdata:
			do_move = self.confirm_move(mdata)
			if do_move:
				mdata.extract_all_info_and_update()

	def sweep(self, n=1, print_current_state = False):
		"""
		Perform n*target_area_iterations of the metropolis
		algorithm. Then if you asked for it, prints status.
		"""
		for i in range(n):
			for j in range(self.target_area):
				self.loop_once()
			if print_current_state:
				print(i)
				print(self.current_state)
			self.current_sweep += 1

	def print_current_state(self):
		"Prints the current state. Just syntactic sugar."
		print(self.current_state)

	def reset_current_sweep(self,new_current_sweep=0):
		"Resets the current sweep to new_current_sweep"
		self.current_sweep = new_current_sweep

#--------------------------------------------------------------------------------

class select_for_area(metropolis):
	"""
	The select_for_area is a descendant of metropolis. It selects only for
	torus of a given surface area, nothing else
	"""











