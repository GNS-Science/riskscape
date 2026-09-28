
## Spatial sampling subpipelines

Reusable subpipelines for spatially sampling data in a RiskScape model. These subpipelines
typically come after any [input_](input.md) subpipelines. These subpipelines all require that
an `exposure` attribute is already present in the pipeline data. Most (except
[sample_region](#sample_region)) also require that a `hazard` attribute is present in the pipeline data.


### `sample_hazard`

The simplest strategy to spatially match exposure-layer features against the hazard-layer.
This approach looks for any intersection between the exposure-layer and hazard-layer geometry.
If there are multiple intersections, then the value closest to the centroid of the 
exposure-layer feature is used. Works for vector or raster hazard-layers.

#### Parameters

| name | description | default |
| --- | --- | --- |
| `hazard_buffer_m` | An optional buffer distance, in metres, to use when sampling the hazard-layer. For example, specifying 1 would mean the spatial matching finds any hazard within 1m of the exposure-layer feature. | `0.0` |

### `sample_hazard_max`

Spatially matches exposure-layer features against a GeoTIFF hazard-layer.
If multiple intersections exist, then the maximum intersecting hazard intensity is used.
Any NaN values in the GeoTIFF are ignored and assumed to be 'no data' values.

#### Parameters

| name | description | default |
| --- | --- | --- |
| `sample_hazard_threshold` | The hazard intensity must be *above* this threshold value for an element-at-risk to be considered exposed. | `0.0` |

### `sample_measure_exposed`

Spatially matches the exposure-layer features to the hazard-layer GeoTIFF and measures
the amount of polygon/linestring that was exposed (in km for linestrings and m² for polygons).
This results get added to the pipeline data as a `Total` struct and include the total area/length
of the original geometry, as well as the ratio that was exposed.
Useful for working with flood hazard-layers and large exposure-layer features like roads or farmland.

The resulting `hazard` will be the average hazard intensity across the exposed area
(although `min_hazard` and `max_hazard` are also available in the pipeline data).

#### Parameters

| name | description | default |
| --- | --- | --- |
| `sample_hazard_threshold` | The hazard intensity must be *above* this threshold value for an element-at-risk to be considered exposed. | `0.0` |

### `sample_region`

Spatially matches an exposure-layer feature against a `$region_layer` containing
regional boundaries. Useful for aggregating results by administrative region later
in the pipeline (for example, by [report_regional_impact](reporting.md#report_regional_impact) subpipeline).

#### Parameters

| name | description | default |
| --- | --- | --- |
| `region_buffer_m` | A buffer, in metres, to use when spatially matching an exposure-layer feature to a region-layer. This is to handle features that fall just outside the regional boundaries, e.g. wharfs, lighthouses, etc. A generous 10km buffer is used by default. | `10000` |
| `region_layer` | Regional boundary polygons used to aggregate the results and report them as regional totals. | (required) |


