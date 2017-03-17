##############################
#File: Initialize_plot.py    #
#Author: Damodar Rajbhandari #
#Created on March 14, 2017   #
#Updated on March 16, 2017   #
##############################

import numpy as np 
import matplotlib.pyplot as plt

"""
	In CDT 1+1 D, we have two types of triangles - up pointing (type 1) and 
	down pointing (type 2). For simplicity, It will be easy to visualize in 
	Minkowski spacetime. i.e. 

                    ^
                    |___________________                . .  . . . ..    
                    |    |    |    |    |               . . .Type 2 . 
                    |____|____|____|____|               .   . .     . 
               time |    |    |    |  --|------------>  .     . .   . 
               axis |____|____|____|____|               .Type 1 . . .  
                    |    |    |    |    |               . . . . . . . 
                   -|----|----|----|----|-- >
                         space axis 

"""

n = 10
N = np.arange(n)

for j in N: 
	for i in N: 
		
		vertices1 = np.array([[i,j],[i+1,j],[i,j+1]]) #For Type 1 triangle
		vertices2 = np.array([[i+1,j],[i,j+1],[i+1,j+1]]) #For Type 2 triangle
		
		triangle1 = plt.Polygon(vertices1, color = 'r')
		trianlge2 = plt.Polygon(vertices2, color = 'b')

		plt.gca().add_line(triangle1) #gca() stands for get current axis. i.e.
		plt.gca().add_line(trianlge2) #gca() returns the current axis instance.
		plt.axis('scaled') #It will put the triangles properly.

plt.title("Triangulation of 1+1 dimensional universe\nbefore any move or antimove was made")
plt.xlabel("Space axis")
plt.ylabel("Time axis")

xint, yint = np.append(N+1,0) , np.append(N+1,0)
plt.xticks(xint)
plt.yticks(yint)

plt.show(triangle1)
plt.show(trianlge2)


