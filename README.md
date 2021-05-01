# Causal Dynamical Triangulations (CDT)
[![License](https://img.shields.io/badge/License-GPL%20v3.0-blue.svg)](LICENSE.md)
[![DOI](https://zenodo.org/badge/84816891.svg)](https://zenodo.org/badge/latestdoi/84816891)
[![Open Issues](https://img.shields.io/github/issues-raw/Damicristi/cdt.svg)](https://github.com/Damicristi/cdt/issues)
[![Join the chat at https://gitter.im/physicslog/cdt-qg-2D](https://img.shields.io/badge/gitter-join%20chat%20→-brightgreen.svg)](https://gitter.im/physicslog/cdt-qg-2D)

Author: [Damodar Rajbhandari](https://damodarrajbhandari.com.np), Outreach blogger at [Physics Log](http://www.physicslog.com/)  
In the Collaboration with [Dr. Jonah Maxwell Miller](https://www.lanl.gov/expertise/profiles/view/jonah-miller) and [Prof. Dr. Udayaraj Khanal](https://en.wikipedia.org/wiki/Udayraj_Khanal).

## Introduction

After introducing the General Theory of Relativity (in 1915), Einstein pointed out that quantum effects will lead to modifications of his theory. We call the unknown theory required to study these effects “quantum gravity”. Unfortunately, a naive quantization of general relativity appears to be perturbatively non-renormalizable. This is one of the greatest challenges facing in modern theoretical physics.

One can attempt to construct a theory of quantum gravity by defining a non-perturbative quantum field theory as a sum over histories. This technique is a modification of Feynman path integral formulation which was first put forwarded by Stephen Hawking and Gary William Gibbons for their quantum gravity approach “Euclidean quantum gravity ”. In-short, instead of superposing the usual Lorentzian spacetimes, they used Euclidean spaces which have four space dimensions. The hope of Euclidean quantum gravity was that spacetime could be assumed to be Euclidean and that time would emerge dynamically. Unfortunately, this did not work out. In the 1990s, this work was combined with quantum Regge calculus so that it could be formulated non-perturbatively. This was called Dynamical Triangulations. This technique failed due to unboundedness in the gravitational action. And also the path integral knows nothing about causality (i.e. light cone structure of the spacetime) and there’s no specification that any test matter will bounded by light cones. In an effort to resolve these issues, Renate Loll, Jan Ambjørn and Jerzy Jurkiewicz reformulated this construction, but with Lorentzian signature imposed from the start. They only map into Euclidean signature via Wick rotation after constructing the theory. Thus, Causal Dynamical Triangulations was born (initially, it was named as Lorentzian Dynamical Triangulations). This approach provides concrete evidence that one must include causal structure, in the sense of having a well-defined light cones everywhere. This model imposed preferred foliation of time so that we can track of time direction.

But the question is, does CDT rely on distinguished time slicing? To answer this question, Renate Loll and Samo Jordan introduced the more general version of CDT which is called CDT without preferred foliation (equivalent to say, Locally causal dynamical triangulations) and found the answer to be hopefully no.

The main motivation for choosing this approach is that it is relies on very few fundamental physical principles and attempts to quantize gravitational degree of freedom without introduction of additional variables, extra dimensions or new symmetries widely used by String theory (for example). Moreover, it comes with definite numerical approximation scheme. To study the numerical simulations of 1+1 dimensional CDT with non-foliated structure, we requires new Monte Carlo moves, which are significantly more difficult to implement than the generalized Pachner moves used in standard CDT.

In short, Causal Dynamical Triangulations (CDT) is an approach to Quantum Gravity based on the sum over histories line of research which gives a quantization of classical Einstein gravity using a discrete approximation to the gravitational path integral, and spacetimes are approximated by Minkowskian equilateral triangles. 

## Background theories
1. General Relativity
2. Quantum Field Theory
3. Regge Calculus

## Theory Keywords
1. Einstein Hibert Action
2. Feynmann Path Integral
3. Gauss-Bonnet Theorem
4. Wick Rotation
5. Euler characteristics
6. Periodic Boundary Condition
7. Boltzmann Probability

## Simulation Keywords
1. Data Structure
2. Causality Test
3. Metropolis-Hastings Algorithm
4. Toroidal Topology
5. Monte-Carlo Moves
6. Volume fixing terms

## Basics Reading
1. [Wikibooks: Spacetime](https://en.wikibooks.org/wiki/Special_Relativity/Spacetime)
2. [PBS Space Time](https://www.youtube.com/channel/UC7_gcs09iThXybpVgjHZ_7g/playlists) 
3. [Einstein Online](http://www.einstein-online.info/index.html)
4. [The Physics Mill](http://www.thephysicsmill.com/)

## Code Documentation
You can download from this link: [Damodar's Bachelor Approved Thesis by Tribhuvan University](https://figshare.com/articles/thesis/An_open_source_code_for_Causal_Dynamical_Triangulations_without_preferred_foliation_in_1_1_-dimensions_with_elementary_expositions/12751772).

## How you can contribute to our open source code at [GitHub](https://github.com/Damicristi/cdt)?
Our programming language preference is Python 3.x. version under the object oriented paradigm. The goals and target of this project are:

- [x]  Data structure
- [x]  Causality test
- [x]  Alexander move
- [x]  Collapse move
- [x]  Generate flat discrete spacetime 
- [x]  Inverse Alexander move
- [ ]  Inverse collapse move
- [ ]  Flip move
- [ ]  Inverse flip move
- [ ]  Pinching move
- [ ]  Inverse pinching move
- [ ]  Volume control terms to fixed the spacetime topology
- [ ]  Metropolis-Hastings algorithm
- [ ]  Generate Quantum spacetime ensembles

## How to cite this project?
Giving credit is a way of respecting the author’s heartfelt dedication and hard work. So, do I prefer. 
```
Damodar Rajbhandari. (2018, July 23). An open source code for
causal dynamical triangulations without preferred foliation 
in (1+1)- dimensions. Zenodo. http://doi.org/10.5281/zenodo.1422810
```
In LaTeX, use this:
```
@misc{damodar_rajbhandari_2018_1422810,
  author = {Damodar Rajbhandari},
  title  = {An open source code for causal dynamical 
            triangulations without preferred foliation in
            (1+1)- dimensions},
  month  = July,
  year   = 2018,
  doi    = {10.5281/zenodo.1422810},
  url    = {https://doi.org/10.5281/zenodo.1422810}
}
```
## Contributors:
Thanks goes to all these wonderful people at ["View Contributors"](https://github.com/Damicristi/cdt/graphs/contributors)

## Visitor counter:
This webpage counts the number of visitors since 20 Jan, 2019. Webpage created on 20 Sept, 2018 and recent edited on 1 May, 2020. 

<script type="text/javascript" src="//rf.revolvermaps.com/0/0/0.js?i=0upkcckxlaf&amp;d=2&amp;p=3&amp;b=4&amp;w=293&amp;g=2&amp;f=arial&amp;fs=12&amp;r=0&amp;c0=362b05&amp;c1=375363&amp;c2=000000&amp;ic0=0&amp;ic1=0" async="async"></script>

