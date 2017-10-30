# Causal Dynamical Triangulation(CDT) 1+1 D
Author: [Damodar Rajbhandari](mailto:damicristi7@live.com), Out-reach blogger at [Physics Log](http://www.physicslog.com/)  
Supervisors: [Dr. Jonah Maxwell Miller](mailto:jonah.maxwell.miller@gmail.com) and [Prof. Dr. Udayaraj Khanal](mailto:khanalu@yahoo.com).

## Introduction
After introducing the General Theory of Relativity (in 1915), Einstein pointed out the quantum effects
will lead to the modifications of his theory . In order to study gravity in the
regime where this effects cannot be discarded, such area we called Quantum Gravity. But if
one trying to quantize the quantum fluctuation around a given solution by the classical equation
of general relativity, one discovers that the corresponding quantum field theory is perturbatively
non-renormalizable . This is one of the greatest challenges facing in the theoretical physics
which lies in combining Einstein’s classical theory of gravity with Quantum Field Theory.

One can attempt to construct a theory of quantum gravity is by defining a non-perturbative
quantum field theory as a sum over histories. This technique is the modification of Feynman
path integral into gravitational path integral which was first put forwarded by Stephen Hawking
and Gary William Gibbons for their quantum gravity approach called a “Euclidean Quantum
Gravity ”. This approach uses Euclidean signature (+ + + +). In-short, instead of superposing
the usual Lorentzian spacetimes, they used Euclidean spaces which have four space dimensions. 
The hope of the Euclidean quantum gravity was that spacetime could be assumed to be
Euclidean and that time would emerge dynamically. But, this did not work out. In early 1990s, this work was combined with quan-
tum Regge calculus so that, it could formulated non-perturbatively. This was called Dynamical
Triangulations. This technique encountered the unboundedness in the gravitational action.
And also, the path integral knows nothing about causality (i.e. light cone structure of the
spacetime) and there’s no specification that any test matter will bounded by the light cones. In
an effort to resolve these issues, Renate Loll, Jan Ambjørn and Jerzy Jurkiewicz reformulated
this construction, but with Lorentzian signature imposed from the start. They only map into
Euclidean signature via Wick rotation after constructing the theory. Thus, Causal Dynami-
cal Triangulations was born (initially, it was named as Lorentzian Dynamical Triangulations).
This approach provides concrete evidence that one must include causal structure, in the sense
of having a well-defined light cones everywhere. This model imposed preferred foliation of
time so that we can track of time direction. But the question is, does CDT rely on distinguished
time slicing? Rely on this question, Renate Loll and Samo Jordan introduced the more general
version of CDT which is called as CDT without preferred foliation (equivalent to say, Locally
causal dynamical triangulations) and found the answer to be hopefully no.

The main motivation for choosing this approach is because it is relies on very few funda-
mental physical principles and attempt to quantize gravitational degree of freedom without in-
troduction of additional variables, extra dimensions or new symmetries widely used by String
theory and Loop quantum gravity etc. And also comes with definite numerical approxima-
tion scheme. To study the numerical simulation of 1+1 dimensional CDT with non-foliated
structure, we requires new Monte Carlo moves, which are significantly more difficult to
implement than the generalized Pachner moves used in standard CDT.

## Background theories
1. General Relativity
2. Quantum Mechanics
3. Simplicial complex (Concept will be used in Regge Calculus)
4. Regge Calculus

## Theory Keywords
1. Einstein Hibert Action
2. Feynmann Path Integral
3. Gauss-Bonnet Theorem
4. Wick Rotation
5. Euler characteristic
6. Toroidal Universe, Periodic Boundary Condition (Optional)
7. Partition Function

## Simulation Keywords
1. Data Structure
2. Alexander Move
3. Metropolis Hasting Algorithm

## Recommended Books 
1. [Gravitation](https://www.amazon.com/Gravitation-Charles-W-Misner/dp/0716703440) 
2. [Spacetime and Geometry: An Introduction to General Relativity](https://www.amazon.com/Spacetime-Geometry-Introduction-General-Relativity/dp/0805387323)
3. [A First Course in General Relativity](https://www.amazon.com/First-Course-General-Relativity/dp/0521887054)
4. [Introduction to Quantum Mechanics](https://www.amazon.com/Introduction-Quantum-Mechanics-David-Griffiths/dp/0131118927)
5. [Quantum Mechanics and Path Integrals](https://www.amazon.com/Quantum-Mechanics-Path-Integrals-Emended/dp/0486477223)

## Basics Reading (Online Stuffs)
My Supervisor's blog is wonderful place to start with basic skills needed for doing CDT. Here you are : [The Physics Mill](http://www.thephysicsmill.com/)

1. [Wikibooks: Spacetime](https://en.wikibooks.org/wiki/Special_Relativity/Spacetime)
2. [PBS Space Time](https://www.youtube.com/channel/UC7_gcs09iThXybpVgjHZ_7g/playlists) 

## Further Reading 
### Introductory
1. [Universe from Scratch](https://arxiv.org/abs/hep-th/0509010v3)
2. [Quantum Geometry: Causal Dynamical Triangulations](http://www.thephysicsmill.com/2013/10/13/causal-dynamical-triangulations/) 
3. [The Self-Organizing Quantum](http://www.signallake.com/innovation/SelfOrganizingQuantumJul08.pdf) 
4. [The Emergence of Spacetime, or, Quantum Gravity on Your Desktop](https://arxiv.org/pdf/0711.0273.pdf)
5. [Reconstructing the Universe](https://arxiv.org/pdf/hep-th/0505154.pdf)

### Research Based
1. [Quantum gravity on a laptop: 1+1 Dimensional Causal Dynamical Triangulation   simulaton](http://www.sciencedirect.com/science/article/pii/S2211379712000319)
2. [Numerical Work in SAGE MATH 14: 1+1 Dimensional Causal Dynamical Triangulation](https://quantumtetrahedron.wordpress.com/2014/01/16/numerical-work-in-sage-math-14-11-dimensional-causal-dynamical-triangulation/)
3. [Two Dimensional Causal Dynamical Triangulation](http://physics.wooster.edu/JrIS/Files/Israel_Web_Article.pdf)
4. [A discrete history of the Lorentzian path integral](https://arxiv.org/pdf/hep-th/0212340.pdf)
5. [Locally Causal Dynamical Triangulations in Two Dimensions](https://arxiv.org/abs/1507.04566)
6. [A Numerical Simulation in 1+1 Dimensions of Locally Causal Dynamical Triangulations](http://www.ru.nl/publish/pages/760962/thesis_final_version.pdf)

## Further Reading in higher Dimension
1. [Fixing the Boundaries for Causal Dynamical Triangulations in 2+1 Dimensions](http://london.ucdavis.edu/~reu/REU12/Papers/miller.pdf)
2. [A first look at transition amplitudes in (2+1)-dimensional causal dynamical triangulations](https://arxiv.org/abs/1305.2932v3)
3. [Causal Dynamical Triangulation in Three Dimensions:Tiling spacetime with Tetrahedrons](http://physics.wooster.edu/JrIS/Files/Web_Article_Shrestha.pdf)
4. [A Validation of Causal Dynamical Triangulations](https://arxiv.org/abs/1110.6875) 
5. [Causal Dynamical Triangulations](https://sites.google.com/site/lisaglaserphysics/research/causal-dynamical-triangulations)
6. [Dynamically Triangulating Lorentzian Quantum Gravity](https://arxiv.org/pdf/hep-th/0105267.pdf)
7. [Causal Dynamical Triangulation of Quantum Gravity in Three Dimensions](http://london.ucdavis.edu/~reu/REU07/zhang.pdf)
8. [Globally and Locally Causal Dynamical Triangulations](http://www.ru.nl/publish/pages/548169/thesis.pdf)

Special Thanks: [Dr. Joshua H. Cooperman](mailto:jhcooperman@gmail.com), [Prakrit Shrestha](mailto:prakrit.shrestha@gmail.com).

Foremost, thanks to my brilliant girlfriend Swastika Shrestha, she knows why!

### Thanks For Reading!

##### [Click Here to go in Home page](https://damicristi.github.io/)
