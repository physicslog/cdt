"""
Path: /snapshot/SpacetimeSnap.py
Author: Damodar Rajbhandari (dphysicslog@gmail.com)
Timestamp: Tue Mar 26 16:15:47 NPT 2019
Description: This module will create an image of the recent
             quantum spacetime using snapshot_initial_values.json
"""

import json

with open('snapshot_initial_values.json') as spacetime:
    data = json.load(spacetime)

vertex = data['vertex'] 
spacelike = data['spacelike'] 
timelike = data['timelike'] 
tts_triangle = data['tts_triangle'] 
sst_triangle = data['sst_triangle'] 

print(vertex)