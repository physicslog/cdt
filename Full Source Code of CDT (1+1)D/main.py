
#############################################################
#  1+1 D Causal Dynamical Triangulations without Preferred  #
#             Foliation, Copyright © 2018                   #
#                                                           #
#       A simulation that generates universes at the        #
#          planck scale where gravitational field           #
#                     becomes strong                        #
#                                                           #
#                                                           #
# Time-stamp: <2017-12-11 22:31:05 (Damodar)>               #
# Author: Damodar Rajbhandari (dphysicslog@gmail.com)       #
#                                                           #
# File: main.py                                             #
# Description: This file is the main file where we can      #
#              change parameter of our universe to do cool  #
#              stuffs. And, Start the simulation from here! #
#############################################################

from debugging import *
import json

# Initialize the spacetime
initialization.build_first_two_torus()

# Creating a snapshot of our recent spacetime
#*************************************************************
config = 'initial_values'
data = {}
data['vertex'] = []
data['spacelike'] = []
data['timelike'] = []
data['tts_triangle'] = []
data['sst_triangle'] = []

for i in st.vertex.instances.values():
    data['vertex'].append({
        'id' : int(i.id),
        'tts triangles' : list(i.tts_triangles), # Set is not json serializable.
        'sst triangles' : list(i.sst_triangles),
        'timelike edges' : list(i.timelike_edges),
        'spacelike edges' : list(i.spacelike_edges)
    })

for i in st.spacelike.instances.values():
    data['spacelike'].append({
        'id' : int(i.id),
        'vertices': list(i.vertices)
    })   

for i in st.timelike.instances.values():
    data['timelike'].append({
        'id' : int(i.id),
        'vertices': list(i.vertices)
    }) 

for i in st.tts_triangle.instances.values():
    data['tts_triangle'].append({
        'id' : int(i.id),
        'vertices': list(i.vertices),
        'timelike edges' : list(i.timelike_edges),
        'spacelike edges' : list(i.spacelike_edges),
        'tts neighbors' : list(i.tts_neighbors),
        'sst neighbors' : list(i.sst_neighbors)
    }) 

for i in st.sst_triangle.instances.values():
    data['sst_triangle'].append({
        'id' : int(i.id),
        'vertices': list(i.vertices),
        'timelike edges' : list(i.timelike_edges),
        'spacelike edges' : list(i.spacelike_edges),
        'tts neighbors' : list(i.tts_neighbors),
        'sst neighbors' : list(i.sst_neighbors)
    }) 

# Saving the spacetime snapshot at /snapshot
#***********************************************************
with open('snapshot/snapshot_%s.json' %config,'w') as f:
    json.dump(data,f, indent=4)

#*************************************************************
