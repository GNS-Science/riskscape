# README

## Quickstart

These Volcanic infrastructure vulnerability functions are CPython-based.
In order to use these functions, you must have Python installed on your computer.
You must also have setup RiskScape to use CPython - for instructions on how to do this, refer to:
https://engine-docs.sites.riskscape.nz/reference/python/cpython.html

## Type information

Currently these risk functions do not rely on any specific exposure attributes, so they are compatible
with *any* exposure-layer that contains appropriate insfrastructure geospatial data.

The Volcanic_Hazard type should be compatible with using combine_coverages() to combine several
different volcanic hazard-layers. Note that the hazard-layers are optional, which means that the
risk functions will still work event if a volcanic hazard is missing.

**Note:** the functions won't really complain if the name of a hazard-layer is slightly inconsistent,
for example if you use `PDC_HIM` instead of `pdc_HIM`. To check that values sampled from the
combined_coverages() volcanic layer have the correct attributes that the vulnerability functions expect, you
can pass the sampled hazard to the Volcanic_Multihazard_Info() function. This will return the volcanic hazards
that are currently being used, the missing attributes (that are not being used), as well as any spurious
attributes that are being ignored by the function.

## Licensing

The risk functions in this directory are made available by The New Zealand Institute for Earth Science
Limited (Earth Sciences New Zealand), licensed under Creative Commons Attribution-NonCommercial 4.0 International
https://creativecommons.org/licenses/by-nc/4.0/deed.en
