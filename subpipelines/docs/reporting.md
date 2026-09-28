
## Reporting subpipelines

Reusable subpipelines for turning the raw pipeline data into model results files.
These subpipelines should come last in the pipeline chain, and handle aggregating the
raw results into summarized output files, e.g. total loss by event, total loss by region, etc.

These subpipelines rely on a `Total` attribute being present in the pipeline data,
which is typically added by an [analysis_](analysis.md) subpipeline. As long as you are summing
the results, you can customize how the results are presented by manipulating the `Total`
struct (e.g. adding or removing attributes) _before_ these subpipelines are called.
The [analyse_by_category](analysis.md#analyse_by_category) subpipeline is one way to manipulate the `Total` attribute so
that it produces a breakdown by category that then gets preserved across any [report_](reporting.md)
subpipelines.

Results are always aggregated by the `event` attribute (if present), as well as any
other criteria (e.g. region). So the same subpipelines are safe to use both with a
single event/hazard-layer (i.e. [input_hazard](input.md#input_hazard) subpipeline) or multiple
hazard-layers/events (i.e. [input_multiple_hazard_geotiffs](input.md#input_multiple_hazard_geotiffs)
subpipeline). So for one unique event (or no `event`), there will be one row of data produced in `event-loss.csv`,
whereas for multiple events, there might be one row of data per return-period.

Typically you would name the analysis pipeline step (e.g. call it `event_impact_table`),
and then you could 'fork' multiple [report_](reporting.md) subpipelines off the same
`event_impact_table` pipeline step, e.g.

```
# ...
-> subpipeline('analyse_consequence') as event_impact_table
# saves an event-impact.csv:
event_impact_table -> subpipeline('report_event_impact')
# saves an region-impact.csv:
event_impact_table -> subpipeline('report_regional_impact')
```


### `report_aggregate_total`

Aggregates by summing the total results by event and any other condition(s) specified.
This doesn't save the data to an output file, and so gives you the flexibility to manipulate
the data further afterwards. Use this when you want finer-grain control
over how the results are saved (i.e. customizing filenames, data sorting, etc).

#### Parameters

| name | description | default |
| --- | --- | --- |
| `group_by` | Optionally changes the results reported so they are broken down based on the given criteria, such as region, construction type, or use category | `{}` |
| `report_decimal_places` | Rounds the results to the given number of decimal places. Use -1 to avoid any rounding | `0` |
| `sum_attr` | Optionally lets you aggregate (sum) a different attribute in the pipeline data, other than `Total`. | `'Total'` |

### `report_event_impact`

Aggregates the results by event and reports the total per event as an `event-impact.csv`
model output file. For example, if the input data were for national event(s), then this
would produce a total national loss table.

#### Parameters

None found

### `report_raw_results`

Reports the raw unaggregated results for the model in a `raw-results.csv` output file.
This will typically include the exposure-layer, the corresponding hazard intensity,
and any other loss or exposure metrics.
This can be useful for checking the results coming out of the model are sensible.

#### Parameters

None found

### `report_regional_impact`

Aggregates the results by event _and_ region, and reports the total per event.
For example, if the input data were for national event(s), then this would
produce a breakdown of the total losses at a regional level. The results are saved
to `region-impact.csv` and `region-impact-map.gpkg` by default, although the parameters
can change this behaviour slightly. Requires the [sample_region](sampling.md#sample_region) subpipeline to have been used earlier
in the pipeline.

You can also optionally group by `$regional_group_by`, for example to get a
breakdown by region _and_ building use category. This will produce row-wise results
(i.e. an extra row of data per `$regional_group_by` value), whereas you could
alternatively use the [analyse_by_category](analysis.md#analyse_by_category) subpipeline to produce a column-wise
breakdown (although that approach would require knowing all the various categories
up front).

#### Parameters

| name | description | default |
| --- | --- | --- |
| `geospatial_output` | Optionally toggles saving the geospatial results (i.e. `region-impact-map.gpkg`). This can be useful when dealing with multiple event scenarios, as the region polygons would get duplicated in this case, which you may not want. | `true` |
| `region_attr` | The name of the region attribute used in the model. The default is 'region', but the model pipeline may rename this if there are multiple regions, e.g. 'SA2'. This value also gets used in the filename, e.g. 'region-impact.csv' would become 'SA2-impact.csv' | `'region'` |
| `regional_group_by` | Optionally changes the results reported so they are broken down row-wise based on the given criteria, such as construction type, or use category | `{}` |

### `report_total_binned`

Aggregates the results by event and reports totals broken down by
[binning](https://en.wikipedia.org/wiki/Data_binning) a continuous value into discrete
buckets. The `$report_bins` specifies the discrete buckets to use, and
`$report_bins_for` specifies the continuous value to assign to buckets.
This does not save the data to a file - you'll need to append a `save()` step
after the subpipeline.

#### Parameters

| name | description | default |
| --- | --- | --- |
| `group_by` | Optionally changes the results reported so they are broken down based on the given criteria, such as region, construction type, or use category | `{}` |
| `report_bin_name` | Gives the 'Bin_xyz' attributes a more meaningful name for the results file. For example, a flood model might use `'Depth_m'`, which would produce results like `Depth_m_<_1_Total_Exposed_Count`, `Depth_m_1_2_Total_Exposed_Count`, etc | `'range'` |
| `report_bins_for` | The attribute with the continuous value to apportion into bins. For example, specifying `hazard` would give you a breakdown of the impacts based on the hazard intensity that each element-at-risk was exposed to. Whereas specifying `Consequence` might give you a breakdown based on the size of each individual loss. This parameter expects a RiskScape expression, so the attribute name should not be enclosed in single-quotes. | `hazard` |
| `report_bins` | The boundary values for each bin. Extra bins will automatically be added for anything below the first value or above the last value. For example `[1,2,3]` would create bins _<1, 1-2, 2-3, 3+_. | (required) |

### `report_total_by_category`

Aggregates the results by event and reports the totals based on discrete categories
(specified by `$report_categories`). The `$report_categories_for` specifies
the attribute in the pipeline that holds the discrete value (e.g. `exposure.Use_Cat`).
The given categories will expand the data column-wise rather than row-wise.
This subpipeline does not save the data to a file - you'll need to append
a `save()` step after the subpipeline.

This subpipeline is similar in functionality to the [analyse_by_category](analysis.md#analyse_by_category) subpipeline.
The main difference is that this pipeline only categorizes the data for a
single output, whereas the [analyse_by_category](analysis.md#analyse_by_category) categorization is intended to
apply to _all_ subsequent results files.

#### Parameters

| name | description | default |
| --- | --- | --- |
| `group_by` | Optionally changes the results reported so they are broken down based on the given criteria, such as region, construction type, or use category | `{}` |
| `report_categories_as` | Gives the 'Category_xyz' attributes a more meaningful name in the results file. | `'Category'` |
| `report_categories_for` | The attribute used to determine which bin to apportion the result into, e.g. `exposure.Use_Cat` | (required) |
| `report_categories` | The list of values that `$report_categories_for` may have. E.g. `['Residential', 'Commercial']` A new column in the results will be created for each item in the list. | (required) |


