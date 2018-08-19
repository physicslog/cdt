"""
Path: /Full_cdt_one_plus_one/sub_triangle_property.py

Time-stamp: <2017-12-11 22:32:24 (Damodar)>
Author: Damodar Rajbhandari (dphysicslog@gmail.com)

Description: This file consists of a sub-class for triangle's edges,
vertices and triangle itself.
"""

#---------------------------------------------------------#
# Dependencies
import numpy as np
import scipy as sp
import utilities as ut
from functools import reduce

# Data Structure we need!
from triangle_property import *  # Required for parent class
#---------------------------------------------------------#


#***************************************************#
#      Defining class for vertices of a triangle    #
#                         --------                  #
#***************************************************#

class vertex(Triangulations):
	"""
	A class that keeps track of the points such 
	that it always be vertices of a triangle.
	"""

	# Static/global variables
	last_used_id = 0 # Last used ID: get the id from max(list of all active ids)
	recycled_ids = set([]) #List of unused IDs 
	instances = {} # Contains all instances of the class that means 
					# contains all the vertex ids and it's properties.

	# Duplicate checking
	@classmethod
	def find_tts_duplicates(self,tts_triangle_list):
		"""
		Searches through self.instances for vertices with the same
		triangles as in tts_triangle_list. Requires set equality. Returns
		the duplicates.
		"""
		tts_duplicates = []
		for v in self.instances.values():
			if v.tts_triangles == set(tts_triangle_list):
				tts_duplicates.append(v.id)
		return tts_duplicates

	@classmethod
	def find_sst_duplicates(self,sst_triangle_list):
		"""
		Searches through self.instances for vertices with the same
		triangles as in sst_triangle_list. Requires set equality. Returns
		the duplicates.
		"""
		sst_duplicates = []
		for v in self.instances.values():
			if v.sst_triangles == set(sst_triangle_list):
				sst_duplicates.append(v.id)
		return sst_duplicates

	@classmethod
	def is_redundant_id(self,vertex_id):
		"""
		Checks to see if a vertex_id is currently in use or not. If
		the vertex is currently in use, return True. If the vertex is
		currently in recycled IDs, return the string
		'recycled'. Otherwise, returns False.
		"""
		v = vertex_id # For compactness
		if v <= self.last_used_id and v not in self.recycled_ids:
			return True
		elif v <= self.last_used_id and v in self.recycled_ids:
			return 'recycled'
		else:
			return False


	@classmethod
	def isinstance(self,object_instance):
		""""
		Tests if an object_instance is an instance of the vertex class.
		This is a built-in function calls as: isinstance(instance, class)
		"""
		return isinstance(object_instance,vertex)


	# INITIALIZATION FUNCTION
	def __init__(self, new_id = 0, tts_triangle_list = [],sst_triangle_list = []
		, timelike_edge_list = [], spacelike_edge_list = []):
		"""
		Initialize a vertex. This will carry a list of triangles that
		you know are connected to it. To add them to the list of triangles.
		However, by default, this list is empty. 
		Note: The id is the only thing that specify the vertices, edges and triangles.
		In constructor, we have defined:
		* tts_triangle_list = list of all tts type triangles
		* sst_triangle_list = list of all sst type triangles
		* timelike_edge_list = list of all timelike edges
		* spacelike_edge_list = list of all spacelike edges
		* new_id = ID number for vertex and it's just an integer
		(We are using new_id instance variable only for vertex class
		 because we are working with lattices.)
		* set() will make triangle IDs unique. 
		"""

		#ID NUMBER:
		if new_id == 0:
			self.id = self.make_id() # imported from base class. 
		else:
			self.id = new_id

		# LOCAL TRIANGLE LISTS:
		# * Neighbors of type tts
		self.tts_triangles = set(tts_triangle_list) 
		# * Neighbors of type sst
		self.sst_triangles = set(sst_triangle_list)

		#LOCAL EDGES LISTS:
		# * Timelike edges
		self.timelike_edges = set(timelike_edge_list)
		# * Spacelike edges
		self.spacelike_edges = set(spacelike_edge_list)


	def __str__(self):
		"String conversion reveals the vertex objects characteristics."

		tts_string = str([x for x in self.tts_triangles])
		sst_string = str([x for x in self.sst_triangles])
		et_string  = str([x for x in self.timelike_edges])
		es_string  = str([x for x in self.spacelike_edges])
		idstring = str(self.id)
		outstring = "VERTEX OBJECT => \n ID: {} \n TRIANGLE TYPE:\n \
TTS type: {} \n SST type: {} \n EDGES TYPE:\n Timelike edges: {} \n \
Spacelike edges: {}"
		outstring = outstring.format(idstring, tts_string, sst_string,\
		 et_string, es_string)
		
		return outstring

	def __len__(self):
		"""
		Length reveals the number of neighbors vertices attached to self
		which is equal to the total number of edges attached to this vertex.
		"""
		neighbors_vertices = len(self.spacelike_edges) + len(self.timelike_edges)
		return neighbors_vertices

	#Now, we need to define the functions to extract out the 
	# information related edges and triangles.

	#For edges: 
	def find_edges_from_collection(self,collection):
		"Find out what edges contained in collection own this vertex."
		containing_edges = set([])
		for e in collection: 
			if self.id in e.vertices:
				containing_edges.add(e.id)
		return containing_edges

	def find_spacelike_edges(self):
		"Find out what spacelike edges belongs to this vertex."
		return self.find_edges_from_collection(spacelike.instances.values())

	def find_timelike_edges(self):
		"Find out what spacelike edges belongs to this vertex."
		return self.find_edges_from_collection(timelike.instances.values())

	def get_spacelike_edges(self):
		"Returns the objects, not the idss."
		return [spacelike.instances[e] for e in self.spacelike_edges]

	def get_timelike_edges(self):
		"Returns the objects, not the ids."
		return [timelike.instances[e] for e in self.timelike_edges]

	def get_spacelike_edge_ids(self):
		"Returns the ids, not the objects."
		return self.spacelike_edges

	def get_timelike_edge_ids(self):
		"Returns the ids, not the objects."
		return self.timelike_edges

	def set_spacelike_edges(self, spacelike_edge_list):
		"Sets self.edges"
		self.spacelike_edges = set(spacelike_edge_list)

	def set_timelike_edges(self, timelike_edge_list):
		"Sets self.edges"
		self.timelike_edges = set(timelike_edge_list)

	def find_and_set_spacelike_edges(self):
		"""
		Finds attached spacelike edges and sets self.spacelike_edges 
		to include them.
		"""
		new_spacelike_edges = self.find_spacelike_edges()
		self.set_spacelike_edges(new_spacelike_edges)
		return new_spacelike_edges

	def find_and_set_timelike_edges(self):
		"""
		Finds attached timelike edges and sets self.timelike_edges 
		to include them.
		"""
		new_timelike_edges = self.find_timelike_edges()
		self.set_timelike_edges(new_timelike_edges)
		return new_timelike_edges

	#For triangles:
	def find_triangles_from_collection(self,collection):
		"Find out what edges contained in collection own this vertex."
		containing_triangles = set([])
		for t in collection:
			if self.id in t.vertices:
				containing_triangles.add(t.id)
		return containing_triangles

	def find_sst_triangles(self):
		"Find out what sst triangles belongs to this vertex."
		return self.find_triangles_from_collection(sst_triangle.instances.values())

	def find_tts_triangles(self):
		"Find out what tts triangles belongs to this vertex."
		return self.find_triangles_from_collection(tts_triangle.instances.values())

	def get_sst_triangles(self):
		"Return the objects, not the ids"
		return [sst_triangle.instances[t] for t in self.sst_triangles]

	def get_tts_triangles(self):
		"Return the objects, not the ids"
		return [tts_triangle.instances[t] for t in self.tts_triangles]

	def get_sst_triangle_ids(self):
		"Returns the ids, not the objects."
		return self.sst_triangles

	def get_tts_triangle_ids(self):
		"Returns the ids, not the objects."
		return self.tts_triangles 

	def set_sst_triangles(self, sst_triangle_list):
		"Sets self.triangles"
		self.sst_triangles = set(sst_triangle_list)

	def set_tts_triangles(self, tts_triangle_list):
		"Sets self.triangles"
		self.tts_triangles = set(tts_triangle_list)

	def find_and_set_sst_triangles(self):
		"""
		Finds attached sst triangles and sets self.sst_neighbors to include them.
		"""
		new_sst_triangles = self.find_sst_triangles()
		self.set_sst_triangles(new_sst_triangles)
		return new_sst_triangles

	def find_and_set_tts_triangles(self):
		"""
		Finds attached tts triangles and sets self.tts_neighbors to include them.
		"""
		new_tts_triangles = self.find_tts_triangles()
		self.set_tts_triangles(new_tts_triangles)
		return new_tts_triangles

	# Since in 1+1 D, curvature is embedded in vertices
	# So, we will defining about curvature and triangulations.

	def curvature(self):
		"""
		In 2-D triangulated spacetime, curvature is embedded in the vertices. 
		To relate the vertex into curvature, we need to relate Pseudo-Riemann geometry
		with Guass-Bonnet Theorem. To be specific, Theorema Egregium. i.e.
		Curvature at a vertex is directly proportional to the deficit angle
		=> 2*(2*pi - (angle_of_triangle)*(sum of triangles attached to vertex)). 
		Because, RICCI SCALAR = 2*(GAUSSIAN CURVATURE)
		FOR PROOF: https://arxiv.org/pdf/gr-qc/0401099.pdf

		#need to define for every triangle type
		"""
		return 2*(2*np.pi - triangle.angle * len(self.tts_triangles + self.sst_triangles))

	def connect_surrounding_triangles(self):
		"""
		For each triangle around any point on the spacetime, check their
		intersections to find which triangles share an edge. 
		"""
		tts = [tts_triangle.instances[i] for i in self.tts_triangles]
		sst = [sst_triangle.instances[j] for j in self.sst_triangles]
		for tri1 in tts+sst:
			for tri2 in tts+sst:
				tri1.connect_to_triangle(tri2)

	def triangles_shared_with(self, other_instance_or_id):
		"""
		Tests to see whether self is a vertex of one of the same triangles
		as other. Other can be a vertex instance or a vertex ID. If triangles
		exist, returns them. Otherwise, returns false.
		"""
		# Parse input
		other = self.parse_input(other_instance_or_id)
		# The triangles shared with self:
		shared_sst_triangles = ut.set_intersection([set(self.get_sst_triangles()),
												set(other.get_sst_triangles())]) 
		shared_tts_triangles = ut.set_intersection([set(self.get_tts_triangles()),
												set(other.get_tts_triangles())])
		return shared_sst_triangles , shared_tts_triangles 

	def share_a_sst_triangle_with(self, other_instance_or_id):
		"""
		Test to see whether self is a vertex of one the same sst triangles as
		other. Return a boolen value i.e. True or False.
		"""
		shared_sst_triangles = self.triangles_shared_with(other_instance_or_id)[0]
		return bool(shared_sst_triangles)

	def share_a_tts_triangle_with(self, other_instance_or_id):
		"""
		Test to see whether self is a vertex of one the same tts triangles as
		other. Return a boolen value i.e. True or False.
		"""
		shared_tts_triangles = self.triangles_shared_with(other_instance_or_id)[1]
		return bool(shared_tts_triangles)

	# ENSURING EXACTLY ONE LIGHT CONE METHOD:

	def get_sector_vertices(self):
		"""
		Find the number of sector(equals to transition line) in a vertex.
		TRANSITION LINE represents the boundary line of light cone.
		Results: Total sectors == Total transition lines.
		"""
		triangles = self.get_sst_triangles() + self.get_tts_triangles()
		edges = lambda triangle: triangle.get_timelike_edges() + triangle.get_spacelike_edges() 
		#Pick a triangle !
		pick_tri = triangles[0]
		#To check transition from two sector, we need:
		previous_edge = 0 #initially nothing
		transition_line = 0 # Boundary of the light cone.
		# resultant triangles represents the tested triangles in a 1st loop
		resultant_triangles = [triangles[0]]
		# 1st loop
		for i in np.arange(len(triangles)):
			for t in triangles:
				if t not in resultant_triangles:
					for e1 in edges(pick_tri):
						for e2 in edges(t):
							if e1 == e2:
								pick_tri = t
								resultant_triangles.append(t)
								if previous_edge == 0:
									pass
								else:
									if type(e1) == type(previous_edge):
										pass
									else:
										transition_line = transition_line + 1
								previous_edge = e1
		# 2nd loop
		for t in resultant_triangles[0:2]:
			for e1 in edges(pick_tri):
				for e2 in edges(t):
					if e1 == e2:
						pick_tri = t
						if previous_edge == 0:
							pass
						else:
							if type(e1) == type(previous_edge):
								pass
							else:
								transition_line = transition_line + 1
						previous_edge = e1

		return transition_line

	def check_causality(self):
		"""
		This will check whether there is exactly one lightcone for
		each vertices or not. Checks the causality requirement for this
		vertex. Return True, if vertex is causal, else False. 
		
		INFO: In standard CDT, the vertex causality validation is
		always trival. 
		"""
		if self.get_sector_vertices() == 4:
			return True
		else:
			return False

# NOW, CHECKING GLOBAL (OVERALL) CAUSALITY:

	@classmethod
	def check_causality_all(cls):
		"""
		This method will check the global causality 
		of all the vertices and the cls should always
		need vertex class.
		Need to import package: functools
		CALL IT IN DEBUGGING AS:
		st.vertex.check_causality_all()
		If all True: returns True, else False
		"""
		return reduce(lambda x,y: x and y, 
			          map(lambda v: cls.check_causality(v), 
			              cls.instances.values()))


#********************************************************************#

# Defining sub-class of edges
#------------------------------------------
class spacelike(edge):
	"""
	This is a sub-class of edge class that specifies 
	the spacelike edges of a triangle. It should be noted that
	spacelike edges donot have any time direction. 

	ATTRIBUTES: 
	-- last_used_id = the last used point ID. global/static.
					  Shared by all class instances.
	-- recycled_ids = A list of used IDs, which after deletion, 
					  becomes available. Global/Static. Shared by
					  all class instances.
	-- vertices = A list of point IDs for spacelike edge endpoints.
	-- points = A function that returns the points the spacelike edge contains.
	-- id = The identifying number of the simplex. 
	-- length = The LENGTH of an edge(lattice spacing) in the PHYSICAL geometry.
	-- instances = The dictionary containing all instances of the class.

	EXAMPLE of a call: e = spacelike_edge(vertex_pair)
	where vertex_pair = [vertex_id_1, vertex_id_2]
	"""

	#Static/global variables
	last_used_id = 0 # Last used edge ID. 
	recycled_ids = set([]) # List of unused edge IDs <= last_used_ids. 
	instances = {} # Contains all instances of the class. 

	# Constant edge length:
	length = 1 

	# Functions
	@classmethod
	def isinstances(self,object_instance):
		"""
		Tests if an object_instance is an instance of the edge class
		"""
		return isinstance(object_instance, spacelike)

	def __init__(self, vertex_pair = []):
		"""
		Initialize the spacelike edge object ID.
		"""
		#Creating the id 
		self.id = self.make_id()

		#Points contained in spacelike edge(IDs)
		if len(vertex_pair) != 2 and len(vertex_pair) != 0:
			print("Your spacelike edge doesnot have the right number of points!")
			print("Generating spacelike edge with no endpoints.")
			self.vertices = set([])
		else:
			self.vertices = set(vertex_pair) # Consists of no direction
	                                         # type(self.vertices)==set

	def __len__(self):
		"Length reveals the number of vertices."
		return len(self.vertices) 

	def __str__(self):
		"String conversion reveals id and the number of vertices"
		vertex_string = str([x for x in self.vertices])
		idstring = str(self.id)
		return "Space-like edge object.\n ID: {}\n Vertices: {}".format(idstring,
																	vertex_string)

	@classmethod
	def spacelike_exists(self, endpoint_pair):
		"""
		Test to see if the spacelike edge defined by a vertex pair exists.
		If it does, return the spacelike edge ID.
		"""

		if len(endpoint_pair) != 2:
			raise ValueError("Must be a pair of vertex IDs!")
		endpoints = set([vertex.parse_input(i) for i in endpoint_pair])

		possible_spacelike_edges = list(endpoints)[0].get_spacelike_edges()
		same_spacelike_edges = [e.get_id() for e in possible_spacelike_edges \
					 if endpoints == set(e.get_vertices())]
		if same_spacelike_edges:
			return same_spacelike_edges
		else:
			return False

#*********************************************************************#

class timelike(edge):
	"""
	This is a sub-class of edge class that specifies 
	the timelike edges of a triangle. (a,b) means arrow of time 
	going from a to b. i.e. a->b where, a (past event) and b (future event) is the
	end-points of a timelike edge and "a" & "b" are the vertex IDs.

	ATTRIBUTES: 
	-- last_used_id = the last used point ID. global/static.
					  Shared by all class instances.
	-- recycled_ids = A list of used IDs, which after deletion, 
					  becomes available. Global/Static. Shared by
					  all class instances.
	-- vertices = A list of point IDs for spacelike edge endpoints.
	-- points = A function that returns the points the timelike edge contains.
	-- id = The identifying number of the simplex. 
	-- length = The LENGTH of an edge(lattice spacing) in the PHYSICAL geometry.
	-- instances = The dictionary containing all instances of the class.

	EXAMPLE of a call: e = timelike_edge(vertex_pair)
	where vertex_pair = (vertex_id_1, vertex_id_2)
	"""
	#Static/global variables
	last_used_id = 0 # Last used edge ID. 
	recycled_ids = set([]) # List of unused edge IDs <= last_used_ids. 
	instances = {} # Contains all instances of the class. 

	# Constant edge length:
	length = 1 

	# Functions
	@classmethod
	def isinstance(self,object_instance):
		"""
		Tests if an object_instance is an instance of the edge class
		"""
		return isinstance(object_instance, timelike)

	def __init__(self, vertex_pair = []):
		"""
		Initialize the timelike edge object ID.
		"""
		#Creating the id 
		self.id = self.make_id()

		#Points contained in spacelike edge(IDs)
		if len(vertex_pair) != 2 and len(vertex_pair) != 0:
			print("Your spacelike edge doesnot have the right number of points!")
			print("Generating spacelike edge with no endpoints.")
			self.vertices = set([])
		else:
			self.vertices = set(vertex_pair)
		#Gives how to specify the flow of time (direction of time) and existence of
		#light cone. If the container type is other than tuple then, we 
		#consider this is spacelike edge.

		# Need to find which endpoint is past and future so that the edge is directed
		# to either of the past or future direction.
		self.past = tuple(self.vertices)[0]
		self.future = tuple(self.vertices)[1]

	def __len__(self):
		"Length reveals the number of vertices."
		return len(self.vertices)

	def __str__(self):
		"String conversion reveals id and the number of vertices"
		vertex_string = str([x for x in self.vertices])
		idstring = str(self.id)
		return "Time-like edge object.\n ID: {}\n Vertices: {}".format(idstring,
																	vertex_string)

	@classmethod
	def timelike_exists(self, endpoint_pair):
		"""
		Test to see if the timelike edge defined by a vertex pair exists.
		If it does, return the timelike edge ID.
		"""

		if len(endpoint_pair) != 2:
			raise ValueError("Must be a pair of vertex IDs!")
		endpoints = set([vertex.parse_input(i) for i in endpoint_pair])

		possible_timelike_edges = list(endpoints)[0].get_timelike_edges()
		same_timelike_edges = [e.get_id() for e in possible_timelike_edges \
					 if endpoints == set(e.get_vertices())]
		if same_timelike_edges:
			return same_timelike_edges
		else:
			return False

#*************************************************************************#

# The below classes is the subclass of triangle class. 

class tts_triangle(triangle):
	"""
	A class that define the tts type of triangle object.

	Attributes: 
	-- last_used_id = the last used point ID. global/static
					  SHARED BY ALL CLASS INSTANCES
	-- recycled_ids = A list of used IDs, which, after deletion, become 
					  available. Global/static. SHARED BY ALL CLASS INSTANCES.
	-- points       = A list of points contained by this tts triangle
	-- id = The identifying number of the 2D simplex. USEFUL! 
	-- area = The physical area of a Minkowskian equilateral tts triangle with the 
			  given edge length.
	-- angle = The angle of each angle of an equilateral triangle. 
			   60 degrees.
	-- instances = The dictionary containing all instances of this class.

	Example of call: t = tts_triangle(point_list)
	where point_list = [p1,p2,p3] where p1, p2 and p3 are the vertices of this triangle
	"""

	# Static/global variables
	last_used_id = 0 # Last used triangle ID.
	recycled_ids = set([]) # List of unused vertex IDS <= last_used_id
	instances = {} # Contains all instances of the class

	# Geometric quantities 
	area = np.sqrt(3) * spacelike.length**2 / 4 # area of both type of triangle(alpha = 1)
	angle = np.pi/3 # Angle between the any two edges.

	 # Functions
	@classmethod 
	def isinstance(self, object_instance):
		"Testing if an object_instance is an instance of the tts type triangle class"
		return isinstance(object_instance, tts_triangle)

	#INITIALIZATION
	def __init__(self, point_list=[], spacelike_edge_list=[], timelike_edge_list=[],
		tts_triangle_list=[], sst_triangle_list = []):
		"Initialize a tts type of triangle."

		#Creating ID
		self.id = self.make_id()

		#Relating the vertices of this type of triangle.
		if len(point_list) != 0 and len(point_list) != 3:
			print("Our triangle has the wrong number of points!")
			print("So, we create an empty point list. ")
			self.vertices = set([])
		else:
			self.vertices = set(point_list)

		# Spacelike edges of the triangle IDs. 
		if len(spacelike_edge_list) != 0 and len(spacelike_edge_list) != 1:
			print("Our triangle has the wrong number of spacelike edges")
			print("Creating an empty list.")
			self.spacelike_edges = set([])
		else:
			self.spacelike_edges = set(spacelike_edge_list)

		# Timelike edges of the triangle IDs. 
		if len(timelike_edge_list) != 0 and len(timelike_edge_list) != 2:
			print("Our triangle has the wrong number of timelike edges")
			print("Creating an empty list.")
			self.timelike_edges = set([])
		else:
			self.timelike_edges = set(timelike_edge_list)

		# Neighbors triangle types connected to this type of triangle.

		total_neighbors = len(tts_triangle_list) + len(sst_triangle_list)
		if total_neighbors != 0 and total_neighbors != 3:
			print("Our triangle has the wrong number of neighbors!")
			print("Creating two empty lists for respective neighbors types")
			self.tts_neighbors = set([])
			self.sst_neighbors = set([])

		self.tts_neighbors = set(tts_triangle_list)
		self.sst_neighbors = set(sst_triangle_list)

	def __str__(self):
		"Sring conversion reveals id, neighbors type and number of vertices"
		vertex_string = " Vertices: {}".format(str([x for x in self.vertices]))
		idstring = " ID: {}".format(str(self.id))
		spacelike_edgestring = " Spacelike Edge: {}".format(str(list(self.spacelike_edges)))
		timelike_edgestring = " Timelike Edge: {}".format(str(list(self.timelike_edges)))
		tts_triangle_list = " Neighbor tts triangles: {}".format(str(list(self.tts_neighbors)))
		sst_triangle_list = " Neighbor sst triangles: {}".format(str(list(self.sst_neighbors)))
		outstring = "tts triangle object.\n"+ idstring + "\n" +\
					vertex_string + "\n" + spacelike_edgestring + "\n" +\
					 timelike_edgestring + "\n" + tts_triangle_list + "\n" +\
					 sst_triangle_list
		return outstring

	def __len__(self):
		"Length reveals the number of vertices."
		return len(self.vertices)

#***********************************************************************#

class sst_triangle(triangle):
	"""
	A sub-class that define the sst type of triangle object.

	Attributes: 
	-- last_used_id = the last used point ID. global/static
					  SHARED BY ALL CLASS INSTANCES
	-- recycled_ids = A list of used IDs, which, after deletion, become 
					  available. Global/static. SHARED BY ALL CLASS INSTANCES.
	-- points       = A list of points contained by this sst triangle
	-- id = The identifying number of the 2D simplex. USEFUL! 
	-- area = The physical area of a Minkowskian equilateral tts triangle with the 
			  given edge length.
	-- angle = The angle of each angle of an equilateral triangle. 
			   60 degrees.
	-- instances = The dictionary containing all instances of this class.

	Example of call: t = sst_triangle(point_list)
	where point_list = [p1,p2,p3] where p1, p2 and p3 are the vertices of this triangle
	"""

	# Static/global variables
	last_used_id = 0 # Last used triangle ID.
	recycled_ids = set([]) # List of unused vertex IDS <= last_used_id
	instances = {} # Contains all instances of the class

	# Geometric quantities 
	area = np.sqrt(3) * timelike.length**2 / 4 # area of both type of triangle($\alpha = 1$)
	angle = np.pi/3 # Angle between the any two edges.

	 # Functions
	@classmethod 
	def isinstance(self, object_instance):
		"Testing if an object_instance is an instance of the tts type triangle class"
		return isinstance(object_instance, sst_triangle)

	#INITIALIZATION
	def __init__(self, point_list=[], spacelike_edge_list=[], timelike_edge_list=[],
		tts_triangle_list=[], sst_triangle_list = []):
		"Initialize a sst type of triangle."

		#Creating ID
		self.id = self.make_id()

		#Relating the vertices of this type of triangle.
		if len(point_list) != 0 and len(point_list) != 3:
			print("Our triangle has the wrong number of points!")
			print("So, we create an empty point list. ")
			self.vertices = set([])
		else:
			self.vertices = set(point_list)

		# Spacelike edges of the triangle IDs. 
		if len(spacelike_edge_list) != 0 and len(spacelike_edge_list) != 2:
			print("Our triangle has the wrong number of spacelike edges")
			print("Creating an empty list.")
			self.spacelike_edges = set([])
		else:
			self.spacelike_edges = set(spacelike_edge_list)

		# Timelike edges of the triangle IDs. 
		if len(timelike_edge_list) != 0 and len(timelike_edge_list) != 1:
			print("Our triangle has the wrong number of timelike edges")
			print("Creating an empty list.")
			self.timelike_edges = set([])
		else:
			self.timelike_edges = set(timelike_edge_list)

		# Neighbors triangle types connected to this type of triangle.
		total_neighbors = len(tts_triangle_list) + len(sst_triangle_list)
		if total_neighbors != 0 and total_neighbors != 3:
			print("Our triangle has the wrong number of neighbors!")
			print("Creating two empty lists for respective neighbors types")
			self.tts_neighbors = set([])
			self.sst_neighbors = set([])

		self.tts_neighbors = set(tts_triangle_list)
		self.sst_neighbors = set(sst_triangle_list)

	def __str__(self):
		"Sring conversion reveals id, neighbors type and number of vertices"
		vertex_string = " Vertices: {}".format(str([x for x in self.vertices]))
		idstring = " ID: {}".format(str(self.id))
		spacelike_edgestring = " Spacelike Edge: {}".format(str(list(self.spacelike_edges)))
		timelike_edgestring = " Timelike Edge: {}".format(str(list(self.timelike_edges)))
		tts_triangle_list = " Neighbor tts triangles: {}".format(str(list(self.tts_neighbors)))
		sst_triangle_list = " Neighbor sst triangles: {}".format(str(list(self.sst_neighbors)))
		outstring = "sst triangle object.\n"+ idstring + "\n" +\
					vertex_string + "\n" + spacelike_edgestring + "\n" +\
					 timelike_edgestring + "\n" + tts_triangle_list + "\n" +\
					 sst_triangle_list
		return outstring

	def __len__(self):
		"Length reveals the number of vertices."
		return len(self.vertices)

#*************************************************************************#
