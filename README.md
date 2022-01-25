# Auto-Mshts

Auto-Mshts is a portable script tool written in python3 programming language In order to calculate **Standard Deviation** (SD) of traditional Mshts experiment result and work out **EC50** value with logistic curve automatically. This script tool provides an easy-to-learn method to adjust calculation parameters by storing main parameters with key-value structure in a static file called **setting.json** and read this file before its running. 

In order to manage each experimental data more conveniently, we suggest that users creating a folder under **/output** directory and naming it after whatever the users like and then set this word to the index of **output_directory** in **setting.json**, in which this tool will output this time's result data only to this folder. 

In general, the result data contains **a csv file** storing the raw data and  SD value of every sample and every repeat, as well as the average value of them. What's more, results of curvefit for every sample and every repeat to calculate EC50 value will be plot into figures and stored in **/figs** directory under the folder created by users.

Last but not least, because of too much matrix computation **this script depends on AVX-512** (a x86 instruction set architecture). So that, **using intel CPUs** may have a much better peformance than using AMDs.

## Requirements

Python 3 (v3.8.10 is recommended)

Numpy

Matplotlib

Scipy

## Source Code Architecture Explanation

The main computation steps are implemented in **main.py** file while **/util** directory is modularization of various functional interfaces. Among them, **util/io** stands for IO operations of this tool, **util/convert** stores many matrix transforms applied in this tool, **util/calculus** is about curvefit to work out EC50 value.

## Installation

`brew install python@3.8`

`pip install numpy scipy matplotlib`

