onsset
=================================

[![PyPI version](https://badge.fury.io/py/gridfinder.svg)](https://test.pypi.org/project/gep-onsset/)
[![Build Status](https://travis-ci.com/OnSSET/onsset.svg?branch=master)](https://travis-ci.com/OnSSET/onsset)
[![Documentation Status](https://readthedocs.org/projects/onsset/badge/?version=latest)](https://onsset.readthedocs.io/en/latest/?badge=latest)

Documentation: https://onsset.readthedocs.io/en/latest/index.html#

# Scope

This repository contains the source code of the Open Source Spatial Electrification Tool ([OnSSET](http://www.onsset.org/)). The repository also includes sample test files available in ```.\test_data``` and sample output files available in ```.\sample_output```.

## Installation

**Requirements**

OnSSET requires Python > 3.5 with the following packages installed:
- et-xmlfile
- jdcal
- numpy
- openpyxl
- pandas
- python-dateutil
- pytz
- six
- xlrd


**Install with pip**

```
pip install onsset
```

**Install from GitHub**

Download or clone the repository and install the package in `develop` (editable) mode:

```
git clone https://github.com/AndreasSahlberg/onsset-Ethiopia.git
cd onsset-Ethiopia
python setup.py develop
```

**How to use the tool**

There are two parts to the OnSSET model developed for Ethiopia under this project. 
The user should first use the *Demand_generator.ipynb* to specify the share of the population in each demand Tier in each time-step. The *input_data_ethiopia.csv* file containing extracted GIS data can be used as input. 
In the second step, the output file from the *Demand_generator.ipynb"* is used in the *Scenario_run.ipynb"* to explore least-cost electrification pathways.

For unfamiliar users, a training course on the OnSSET tool and related GIS processes is available at: https://www.open.edu/openlearncreate/course/view.php?id=6816

## Contact
For more information regarding the tool, its functionality and implementation please visit https://www.onsset.org.
