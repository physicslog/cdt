"""
Path: /Full_cdt_one_plus_one/triangulations.py

Time-stamp: <2017-12-11 22:32:52 (Damodar)>
Author: Damodar Rajbhandari (dphysicslog@gmail.com)

Description: This file consists of how the triangles are glued to 
each other and a class that can memory the neighbors vertices, edges
and triangles. Actually, this is the base file for the triangle_property.py
and generates the topological torus.
"""

# Dependencies
#---------------------------------------------------------
import numpy as np
import scipy as sp
#-----------------------------------------------------------

#-----------------------------------------------------
#                      Classes
#-----------------------------------------------------
# The triangulation object base class
#---------------------------------------------------

class Triangulations:
	"""
	This is the base class for the geometric objects in 
	triangle_property.py and sub_triangle_property.py
	"""

	@classmethod
	def increment_id(self):
		"""
		Increment the static variable last_used_id by 1. Then
		return the new id for use. 
		Tips: last_used_id = max( total ids)
		"""
		self.last_used_id += 1
		return self.last_used_id

	@classmethod
	def reclaim_id(self,object_id):
		"""
		Take an input ID and add it to the list of recycled IDs.
		Return the list of recycled ids. 
		"""
		self.recycled_ids.add(object_id)
		return self.recycled_ids


	@classmethod
	def recycle_id(self):
		"""
		Looks for the minimum element of your recycled IDs (means
		trash IDs). Returns it and removes it from the set
		so that we can used it.
		"""
		# Find the minimum element of recycled Ids.
		minval = min(self.recycled_ids)
		# Remove the minimum element from the set
		self.recycled_ids.remove(minval)
		# Return the returned element for reuse
		return minval

	
	@classmethod 
	def make_id(self):
		"""
		Generate an ID for use. Firstly, it will look in recycled IDs. 
		If none are avaiable, make a brand new ID and return it.
		It should be known that on increasing the IDs we are making
		compact triangulations in the spacetime manifold.
		"""
		if len(self.recycled_ids) > 0:
			new_id = self.recycle_id()
		else:
			new_id = self.increment_id()
		return new_id
		
	
	@classmethod
	def add(self, object_instance):
		"""
		Adds an object of the same type as self to the dictionary containing
		those objects. 
		"""
		self.instances[object_instance.id] = object_instance


	@classmethod
	def delete(self, argument):
		"""
		Deletes an object of the same type as self from the dictionary containing
		those objects and reclaims its id. 
		
		Accepts an id, a list of ids, an object, or a list of objects. 
		"""
		if type(argument) == list: #i.e. if we were passed a list
			if len(argument) == 0: #If list is empty, do nothing.  
				pass
			#IF WE'RE WORKING WITH IDS, BECAUSE IDS ARE IN INTEGER VALUES
			if type(argument[0]) == int: 
				for object_id in argument:
					del self.instances[object_id] #Remove the id from dictionary
					self.reclaim_id(object_id) #Add to the recycle id container
				pass
			else: #IF WE ARE WORKING WITH OBJECTS
				for object_instance in argument:
					#Remove the id from the dictionary
					del self.instances[object_instance.id]
					self.reclaim_id(object_instance.id) # Reclaim the id. 
				pass
		elif type(argument) == int: #we were passed a single object id.
			del self.instances[argument]
			self.reclaim_id(argument)
			pass
		else: #We were passed a single object instance
			del self.instances[argument.id]
			self.reclaim_id(argument.id)
			pass

	@classmethod
	def delete_all(self):
		"""
		Deletes all instances of the same type as self. 
		"""
		to_delete = list(self.instances.keys())
		if len(to_delete) > 0: #Only delete if there is anything to delete.
			self.delete(to_delete) #Calling to_delete method here!


	@classmethod
	def list_ids(self):
		"Returns a list of all the object ids of type self."
		return list(self.instances.keys())


	@classmethod
	def count_instances(self):
		"Counts the number of instances of object of type self."
		return len(list(self.instances))

	def get_id(self):
		"Gets the object id."
		return self.id


	@classmethod
	def parse_input(self,id_or_instance):
		"""
		Enables a function to take an id or an instance as
		input. Always returns a class instance rather than an
		id. Takes in either an id or an instance as input and returns
		the corresponding class instance.
		"""
		if type(id_or_instance) == int \
				and id_or_instance in self.instances.keys():
			other = self.instances[id_or_instance]
		elif self.isinstance(id_or_instance):
			other = id_or_instance
		else:
			raise TypeError("I need a Triangulation subclass instance or ID.")
		return other 
