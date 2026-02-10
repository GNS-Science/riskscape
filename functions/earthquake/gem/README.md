# README

## Quickstart

This directory contains examples of integrating the 
[GEM Global Vulnerability Model](https://github.com/gem/global_vulnerability_model)
with RiskScape functions. This includes:

- global_vulnerability_model.py: Example Python code of how you might use the Global
Vulnerability Model XML definitions to calculate a Loss Ratio (LR) or Damage Ratio (DR)
for a building.
- project.ini: RiskScape function definitions, which can be used from a RiskScape model.
Only a few example functions, relevant to NZ/US buildings, have been defined.

Using the RiskScape functions requires that:
- RiskScape is setup to use [CPython](https://engine-docs.sites.riskscape.nz/reference/python/cpython.html)
- the Python packages in requirements.txt are installed on your system

The Python code is provided for demonstrative purposes only. You may need to define your
own RiskScape functions in order to get the desired behaviour you want.

Currently the example code has limitations, e.g. it only supports beta distributions (BT).
The functions only determine the vulnerability component, *not* fragility. In order to avoid
excessive noise of low LRs, by default any LR less than 1e-06 is treated as LR=0, i.e. no damage.
This can be customized by passing an optional `min_LR` argument to the Python code.

## Type information

In order to use a GEM vulnerability function, you need an ID that describes the building type,
such as 'CR/LWAL+CDH+DUM/H1/RES'. This is based on a set of building characteristics.
The RiskScape functions use a `GEM_building` type to map between attributes in the building
input data and a suitable ID supported by the GEM vulnerability model.
These building attributes are:

- material: 'W' for wood, 'CR' for reinforced concrete, etc
- storeys: used to find the closest height building available
- strength: an integer between 0 and 2 (0=L, 1=M, 2=H).
This is mapped to ductility ('DU') and seismic code ('CD'), where available in the underlying data.
For example, 'CDH+DUM' is high seismic code and moderate ductility.
- occupancy: 'RES' (residential), 'COM' (commercial), 'IND' (industrial), etc

The IDs supported by a vulnerability model may vary depending on region and Intensity Measure Type.
For example, the NZ vulnerability model does not contain any wood buildings for PGA, but it does
for SA(0.3). So there is not *one* way to map building input data to an ID that is suitable for
all regions.

The Python code provides some helper code to find the most appropriate ID that is supported by
the underlying vulnerability model. However, you should check that this behaviour is appropriate for
the region and risk analysis you are using.

## Licensing

The examples in this directory rely on data made available by the
[Global Earthquake Model Foundation](https://www.globalquakemodel.org) (GEM) licensed under the
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License
http://creativecommons.org/licenses/by-nc-sa/4.0/

