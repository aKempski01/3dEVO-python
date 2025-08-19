# Gather3d Evo - Python
### The following project allows users to compute 2, or 3 dimensional problems from the field of game theory. It is an implementation of work present in paper "". Please cite our work using a following formula "".

### The following repository contains both spatial and mixed games, that can be updated in multiple ways. All configuration is done via a YAML file. The implementation of all program elements allow simple adjustments and modifications of all provided functions.

## Installation
### Our application was developed using python 3.11.3, however it shall run smoothly with other modern python versions.

## For python 3.11.3
```console
pip install requiremens.txt
```

## In case of conflicts try a minimal version
```console
pip install requiremens_minimal.txt
```

## First Run
### To run an algorithm use a following command
```console
python main.py --yaml-path "<PATH TO YOUR YAML FILE>"
```
#### If a --yaml-path argument is not used a default yaml file is being loaded.
#### The results of analysis are saved in runs folder.

### To visualise the results of computations, use a following command: 
```console
python visualise.py 
```

## Problem
### Hawk Dove problem

$\begin{matrix}  & enemy \ Hawk & enemy \ Dove \\ player \ Hawk & (V-C)/2 & V \\ player \ Dove & 0 & V/2 \end{matrix}$

#### yaml command
```yaml
problem_name: HawkDoveProblem
```

### Dynamic Hawk Dove problem

$\begin{matrix}  & enemy \ Hawk & enemy \ Dove \\ player \ Hawk & (V-C)/2 & r * V * 0.25 \\ player \ Dove & 0 & V*0.5*r(+1) \end{matrix}$

#### yaml command
```yaml
problem_name: HawkDoveDynamicProblem
```

## Mortality

## Neighbourhood

## Reproduction

## Resource Function
