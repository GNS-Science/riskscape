# Using NetCDF files

This directory contains some examples of working with NetCDF files.

To run these examples you need to have the NetCDF plugin enabled in RiskScape.

This could be done with:

```
  riskscape --load-plugin <path-to-riskscape-install-dir>/plugins-optional/netcdf
```

## Using multiple layers

```
  riskscape -P project.ini model run atmospheric
```

## Sampling every time step

```
  riskscape -P project.ini model run sea-temperature
```

## Aggregating across time steps

```
  riskscape -P project.ini model run sea-temperature-aggregated
```

## Acknowledgements

Sample NetCDF files have been obtained from
[Unidata NetCDF Samples](https://archive.unidata.ucar.edu/software/netcdf/examples/files.html)

