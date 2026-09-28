
## Geo-processing subpipelines (optional)

Reusable subpipelines for geoprocessing spatial data in a RiskScape model.
These require that an `exposure` attribute is present in the pipeline data,
i.e. they need to come after the [input_exposures](input.md) subpipeline.


### `geoprocess_filter_by_bounds`

Filters the input data so only exposures that intersect the `$filter_layer` bounds
are included in the model results. This can improve performance when your exposure-layer
is national-scale but you are only interested in regional results.

#### Parameters

| name | description | default |
| --- | --- | --- |
| `filter_layer` | Geospatial file or bookmark containing the area of interest. Note that the *bounds* of this layer are used, rather than checking for specific intersections with the geometry that this layer contains. | (required) |

### `geoprocess_filter_by_hazard_bounds`

Filters the input data so that only exposures that intersect the bounds of the `$hazard_layer`
are included in the model results. This can improve performance when your exposure-layer
is national-scale but your hazard-layer only covers a smaller region.

#### Parameters

| name | description | default |
| --- | --- | --- |
| `hazard_layer` | See `input_hazard` subpipeline | (required) |

### `geoprocess_segment_exposures`

Cuts large exposure-layer features into smaller pieces.
This is useful for processing large features, like roads, pipes, or farmland.
This subpipeline should not be used with point data.
Attributes, such as replacement cost, can optionally be scaled to reflect the new segment size.

Note that the resulting segments will not always match the given `segment_size_m`.
For example, the end of a line-string or edges of a polygon may end up smaller than
the given segment size. If cutting by a grid (i.e. `$align_to_grid`), then line-strings
could sometimes end up slightly longer, if they curve around within a grid cell.

#### Parameters

| name | description | default |
| --- | --- | --- |
| `align_to_grid` | Optionally cuts the segments based on a grid that is aligned to the lower-left corner of the given GeoTIFF. This can help to ensure the cut geometry matches the `$hazard_layer` grid they will be sampled against. E.g. if `segment_size_m=10`, then exposure-layer line-strings would be cut based on a 10x10m grid, rather than cut into 10m-long segments. It would be useful to adjust the `$segment_size_m` to match (or be a multiple of) the given GeoTIFF's grid-resolution as well. | `null_of('coverage(floating)')` |
| `scale_attr` | Optionally specifies exposure-layer attributes that should be scaled to reflect the reduction in size. E.g. Useful for spreading the original road's total replacement cost amongst the new road segments. | `{}` |
| `segment_size_m` | Cuts the exposure-layer features into the given segment size, or smaller. | `10` |


