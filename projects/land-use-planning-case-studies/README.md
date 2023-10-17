# Land Use Planning case studies

## Getting started

To run the models you need to download and extract the hazard data separately.
The hazard data is in a series of .zip files. The model currently assumes you
extract each zip 'as is', where it's located. This should give you a directory
structure like:

```
Coastal_AR2-50/ARI2/Auckland_TIF/*.tif
Coastal_AR2-50/ARI5/Auckland_TIF/*.tif
Coastal_AR2-50/ARI10/Auckland_TIF/*.tif
Coastal_AR2-50/ARI20/Auckland_TIF/*.tif
Coastal_AR2-50/ARI50/Auckland_TIF/*.tif
Coastal_AR100-1000/ARI100/Auckland_TIF/*.tif
Coastal_AR100-1000/ARI200/Auckland_TIF/*.tif
Coastal_AR100-1000/ARI500/Auckland_TIF/*.tif
Coastal_AR100-1000/ARI1000/Auckland_TIF/*.tif
```

Note that some of the ARI10 .tif files appear to be missing.

If you wanted to change this directory structure, you would just need to update
the relative filepaths in `coastal_hazard_maps.csv` to match the new layout.

## Case Study 1: Policy Interventions

Many of the concepts and model parameters are the same as Case Study 4.
The main differences are that Case Study 4 incorporates SLR scenarios, whereas this model doesn't, 
and this model let's you specify a floor height mitigation for the buildings.

The floor height can be specified in two ways:
- As a fixed floor height
- As a freeboard height that gets added to the 1% AEP flood depth.
(You can also vary the flood-level that gets used here, specified as a return period).

### Running the model

To run the model without changing the building floor heights at all, use:

```
riskscape model run CS1-Oakley
```

Refer to Case Study 4 examples for how to vary new development.
By default, new buildings will default to a building height of 0.2m, unless otherwise specified by the model parameters.

To specify a freeboard height of 300mm above the 1% AEP (100-year RP) flood, use:

```
riskscape model run CS1-Oakley -p "freeboard_mm=300"
```

To specify a freeboard height of 300mm above the 50-year flood-depth, use:

```
riskscape model run CS1-Oakley -p "freeboard_mm=300" -p "flood_level_RP=50"
```

Note that `flood_level_RP` will have no effect unless `freeboard_mm` is also specified.

To specify a blanket 0.4m floor height for *all* buildings, use:

```
riskscape model run CS1-Oakley -p "min_floor_height_m=0.4"
```

If you specify *both* `min_floor_height_m` and `freeboard_mm`,
then the new floor height will be the greater of the two values.
Note that it may vary from building to building as to which parameter produces the greater floor height.

When either `min_floor_height_m` or `freeboard_mm` is not explicitly specified,
the model parameter will have no effect, i.e. the default behaviour is to simply use the building's existing floor height.

By default, the floor height mitigations are applied to *all* buildings.
You can choose to apply them only to 'new' builds only to 'existing' buildings.
To apply a blanket 0.4m floor height for all *new* buildings, use:

```
riskscape model run CS1-Oakley -p "min_floor_height_m=0.4" -p "mitigate_buildings='new'"
```

Note that the `mitigate_buildings` possible options are `'new'`, `'existing'`, or `'all'`.

## Case Study 2: Greenfields/Brownfields

This model takes large zoning polygons, segments them by a grid of a specified size, samples each
grid cell against selected hazards (or zoning info), and then produces an overall risk score for each segment.

By default, the risk score ranges from 0-6 reflecting the number of hazards each grid cell is exposed to.
A higher risks score indicates higher risk. A weighting can be applied toeach specific hazard
to increase or decrease the risk score.

The hazards include: within 250m of a known fault, within the tsunami evacuation zone,
in a location of observed landslides, exposed to fluvial flooding of 5cm or more,
exposed to moderate liquefaction susceptibility (i.e. 3 or greater),
and exposed to landslide susceptibility level (LSL) of 3 or greater.

To run the model, use:

```
riskscape model run CS2-Drury
```

By default, a 50m x 50m grid is used, so each grid cell is 2,500sqm.
To use a 100m x 100m grid, so each cell is 10,000sqm, use the command:

```
riskscape model run CS2-Drury -p "grid_size_m=100"
```

Flodding, liquefaction, and LSL all have a threshold value. Each grid cell is assigned a 0 or 1 value
based on whether it is exposed to the threshold intensity or greater.
For example, the flood threshold is 0.05m, but you could change it to 0.4m with the command:

```
riskscape model run CS2-Drury -p "flood_threshold=0.4"
```

You can also specify thresholds for liquefaction (`liquefaction_threshold` parameter) and
LSL (`LSL_threshold` parameter).

You can also change the weight that certain hazards give the overall risk score.
Each hazard gets a weighting of 1.0 by default.
To doulbe the weighting given to liquefaction, use the command:

```
riskscape model run CS2-Drury -p "liquefaction_weight=2.0"
```

The weight parameters for other hazards are: `faults_weight`, `observed_landslides_weight`,
`LSL_weight`, `evacuation_zone_weight`, `flood_weight`.

## Case Study 3: Dynamic Adaptive Policy Pathways (DAPP)

The modelling approach taken is:

- The model uses a selection of ARI hazard maps with 10cm SLR incrementsbetween 0cm and 2m.
The entire road line-segment is spatially sampled for any intersections with the hazard-layer (a 10m grid).
- The total length of the exposed segments is taken, i.e. `exposed_length` (converted to km). Note that the exposed segments may not be contiguous - they may cover different parts of the road.
- Seawall mitigation is applied. If the given depth is less than the seawall height, then the hazard intensity becomes null/nothing, i.e. not exposed. Otherwise the hazard depths are used as is (i.e. a breach of the seawall is treated the same as if the seawall was not present at all).
- A single, aggregated inundation depth along the entire road is determined from the mitigated depths.
  - By default, the maximum depth is used as the aggregated hazard intensity, but this can be easily changed to the mean, median, 90th percentile, etc. This should give some idea as to how aggregating the hazard intensity impacts the total fix cost.
- The total `exposed_length` is passed to the Python function, along with the aggregated hazard intensity.
- The Python function calculates a clean-up or repair cost (per km) based on the given hazard intensity. The Python function then also scales the fix cost by the `exposed_length`. If the total fix cost is less than the cleanup cost for 1km for road, then the minimum cleanup cost ($7000) is used.
- The model uses the SeaRise projection data to interpolate a SLR for a given year of interest, based on a particular climate change scenario and percentile.
- The model then uses interpolation to determine the impact (fix cost, fix time, etc) for the projected SLR.
For example, if the SLR for 2070 is 0.35m, the model would then calculate the impact based on the
30cm and 40cm SLR hazard maps, and then interpolate between the two to produce an impact.
- The model double-checks that the interpolated depth is still less than the seawall mitigation.
For example, say the seawall is 1m high and the 200-year event for a 50cm SLR has an inundation depth of 1.03m
and a non-zero loss. If the same event for a 40cm SLR produces a 0.93m depth and a zero loss,
then an *interpolated* depth of 0.98m should still produce a zero loss, because it's below the seawall height.
- Given the road for this model is only 1.09km long, it is not segmented at all. However, in future we would probably want to segment longer roads by some 'minimum repair stretch' distance, that a roading crew could conceivably repair in one go.
- For the road 'heat map' spatial output, the _mitigated_ hazard intensity is used, i.e. only the sections of road where the seawall was breached. For example, if the hazard intensities were `[ 0.95, 1.05, 0.91 ]` and the seawall height was 1.0m, then only the section of road with the `1.05` depth would be included for that event.
Note that the 'heat map' output is based directly on the hazard maps and no interpolation is used at all.

### Running the model

To run the model (default is no seawall), use:

```
riskscape model run CS3-Maraetai
```

To run the model with a 1m seawall mitigation, use:

```
riskscape model run CS3-Maraetai -p "seawall_height=1.0"
```

Note that it can be handy to name the output directory to help keep track of results. Use `-r --output DIR_NAME`, e.g.

```
riskscape model run CS3-Maraetai -p "seawall_height=1.0" -r --output Seawall_1m
```

To change the aggregate hazard value that is used in the damage function to the 90th percentile (default is the maximum depth), use:

```
riskscape model run CS3-Maraetai -p "aggregate_hazard=percentile(hazard, 90)"
```

You can specify a particular sea-level rise scenario from the
[SeaRise](data_export_site747_geodata_nz_sea_rise_national_projections_and_vlm_readings.csv) data.
The default is the _'SSP2-4.5 (medium confidence)'_ scenario.
To change to use the _'SSP1-1.9 (medium confidence)'_ sea-level rise projections, use:

```
riskscape model run CS3-Maraetai -p "scenario='SSP1-1.9 (medium confidence)'"
```

The SeaRise scenarios have percentiles associated with each year/SLR projection: p17, p50, p83.
The p50 SLR is used by default. To change to using the p83 SLR, use:

```
riskscape model run CS3-Maraetai -p "projected_SLR=p83"
```

## Case Study 4: Climate Change Interventions

This model uses two building datasets:
- The current building footprints (2023).
- What the buildings may look like in the future in a 'maximum densification' scenario.

The model gradually replaces the current buildings with the future buildings over time.
The [Python function](./functions/building_year.py) let's you control how many of the future
buildings get included in the model, and at what rate the buildings are replaced.
As an initial proof of concept, this just uses a uniform distribution between 2024 and the `max_year` parameter.

The modelling approach taken is:
- The model goes through each building in the future dataset and uses random number generation
to determine whether or not to include the building in the model.
We can scale up and down the intensification being modelled using the `percent_future_buildings` parameter.
E.g. `percent_future_buildings=100` would eventually include *all* the buildings from the future dataset, whereas
`percent_future_buildings=50` would include *half* the future buildings
and `percent_future_buildings=0` would include *no* buildings from the future dataset.
- Each building included from the future dataset is randomly assigned a year of construction
between 2024 and the `max_year` parameter. This becomes the `Construction_Year` attribute. 
The `max_year` is when the model runs up to (default is 2120).
The building's `id` attribute is used to seed the random number generation, so that
these random choices are reproducible. However, you can change the random-seed to make
things truly random, e.g. `-p "random_seed=random_uniform(minint(), maxint())"`.
- Each building in the _current/2023_ dataset is then spatially sampled against the _future_ dataset
to determine whether a future building is going to be constructed on the site of a current building.
If so, the future building's `Construction_Year` then becomes the `Replacement_Year` for the 2023 building.
All-intersections spatial sampling is used so that there is no overlap
between the current and future building polygons.
- The climate change projection data is read from a CSV file, supplied via the `cc_projection` model parameter.
This CSV data is filtered by a particular climate change scenario.
Each filtered row from the CSV file has a `year` and a projected sea-level rise, in metres.
- The 2023 and future building datasets are selectively combined for each event based on the following logic.
  ```
  Year >= exposure.Construction_Year and Year < exposure.Replacement_Year
  ```
  In other words, include all buildings that have been constructed at this point in time and not yet replaced.
  E.g. say a future building is assigned a `Construction_Year` of 2067.
  The current/2023 building in the same location would then be assigned a `Replacement_Year` of 2067.
  The 2023 building would be used for events in 2050 and 2060, but then
  the future building would be used instead for the 2070 event (and later events).
  As the sea-level rise increases, so does the year, so more and more of the future dataset gets used,
  and less and less of the 2023 dataset.
- The model then uses interpolation to determine the impact (reinstatement cost, life safety risk, etc)
for each SLR from the `cc_projection` CSV file.
For example, if the SLR for 2070 is 0.35m, the model would then calculate the impact based on the
30cm and 40cm SLR hazard maps, and then interpolate between the two to produce an impact.
- The `development-over-time.csv` shows the total number/value of buildings used in each SLR/Year.
You can also optionally output the building dataset (i.e. the exact combination of 2023 and future buildings)
at various years. This can help visualize the development over time.

### Running the model

To run the model (default is no future development), use:

```
riskscape model run CS4-Orewa
```

To run the model to include 25% of the future buildings, use:

```
riskscape model run CS4-Orewa -p "percent_future_buildings=25"
```

Note that it can be handy to name the output directory to help keep track of results. Use `-r --output DIR_NAME`, e.g.

```
riskscape model run CS4-Orewa -p "percent_future_buildings=25" -r --output FutureDevelopment25percent
```

You can also examine exactly what the building dataset will look like at various points (years) in the model.
This also includes some information about the building-level losses that feed into the event-impact table.
You can output the buildings at up to four different points (years).
E.g. to see what using 50% of the future buildings would look like in 2050 and 2090, use:

```
riskscape model run CS4-Orewa -p "percent_future_buildings=50" -p "snapshot_year1=2050" -p "snapshot_year2=2090"
```

You can specify a particular sea-level rise scenario from the
[SeaRise](data_export_site747_geodata_nz_sea_rise_national_projections_and_vlm_readings.csv) data.
The default is the _'SSP2-4.5 (medium confidence)'_ scenario.
To change to use the _'SSP1-1.9 (medium confidence)'_ sea-level rise projections, use:

```
riskscape model run CS4-Orewa -p "scenario='SSP1-1.9 (medium confidence)'"
```

The SeaRise scenarios have percentiles associated with each year/SLR projection: p17, p50, p83.
The p50 SLR is used by default. To change to using the p83 SLR, use:

```
riskscape model run CS4-Orewa -p "projected_SLR=p83"
```

By providing your own CSV file, you can use any combination of year/SLR data in the model that you want.
The model expects the CSV file to contain `scenario`, `year`, and `p50` (SLR) columns.

For example, to include 25% of the future buildings without any change in sea-level at all, use:

```
riskscape model run CS4-Orewa -p "cc_projection='no_SLR.csv'" -p "scenario='None'" -p "percent_future_buildings=25"
```

You can exclude certain areas from being developed at all.
The areas are specified by polygons in a geospatial file or bookmark.
For example, the following command will build 25% of the future buildings _except_ in any polygons
contained in the Danger_Zones.shp file.

```
riskscape model run CS4-Orewa -p "no_intensification='Danger_Zones.shp'" -p "percent_future_buildings=25"
```

Finally you can specify areas where a `retreat` approach should be used and buildings should be removed
and not replaced at all. Again, the areas of retreat are simply polygons in a specified file.
You can optionally specify a year to have all buildings removed by (default 2120).
For example, to remove any buildings in any of the 'Danger_Zones.shp' polygons by 2075, use:

```
riskscape model run CS4-Orewa -p "retreat_by=2075" -p "retreat='Danger_Zones.shp'"
```

Note: you could also use the `retreat_by` parameter to only remove _some_ of the buildings in the area.
For example, to remove approximately *half* the buildings, you could specify a `retreat_by` year of 2220
(i.e. 100 years *after* the last year being modelled).

By default, the model only reports losses for the years in the SeaRise CSV data
(2005 and 2020-2120 in 10-year increments).
However, you can see losses for any particular year you are interested in.
The SLR for your year of interest will be interpolated from the SeaRise data available (rounded to the nearest cm).
For example, to get losses for the years 2025, 2045, 2065, 2085, and 2105, use:

```
riskscape model run CS4-Orewa -p "years=[2025, 2045, 2065, 2085, 2105]"
```
