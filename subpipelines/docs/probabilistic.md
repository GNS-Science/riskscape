
## Probabilistic modelling

Reusable subpipelines for building probabilistic RiskScape models, such as generating
Average Annual Loss (AAL) model results files.

Currently these cover using the trapezoid approach for calculating an AAL
for hazard-based probabilistic models. A hazard-based probabilistic model is one
where you have a handful of events that correspond to known return periods, such
as a 1-in-50 event, a 1-in-100 event, etc. For more details of how this AAL
calculation works, refer to the [worked example](https://engine-docs.sites.riskscape.nz/advanced/probabilistic/hazard-based.html)
in the RiskScape Engine documentation.

Typically these subpipelines would be used in the 'reporting' phase of the model
workflow, after the [analysis_](analysis.md) subpipelines. They expect a `Total` attribute to be present that contains the loss or exposure information to calculate an AAL for.
Where `Total` contains multiple attributes, an AAL will be calculated separately for
each attribute, e.g. if `Total` contains `{ Exposed_Value, Loss }`, then the subpipelines
would produce `{ AAL_Exposed_Value, AAL_Loss }`.

Typically these subpipelines will be used in combination with the
[input_multiple_hazard_geotiffs](input.md#input_multiple_hazard_geotiffs) subpipeline, which will load all the hazard-based
probabilistic data. By default, these subpipelines will look for a `return_period`
column in the `$hazard_csv` file containing the Average Recurrence Interval (ARI) details,
although you can use `$return_period_attr` if the CSV column is called something else.

If a single ARI event is split across multiple different GeoTIFFs (e.g. separate floodmaps
for different regions), then you should avoid any other unnecessary columns in the
`$hazard_csv` file, as these columns will be used to identify unique events. So a
CSV row containing `{ARI: 100, filepath: foo.tif, other: foo region}` and a row
containing `{ARI: 100, filepath: bar.tif, other: bar region}` would be treated as two
separate events, because the `other` column is unique. Whereas without the `other`
column, the results for each row would be combined into a single ARI 100 event.
Note that the [probabilistic_aal_hazard_based_multi_scenario](probabilistic.md#probabilistic_aal_hazard_based_multi_scenario) sub-pipeline also lets
you generate separate AAL calculations for different scenarios, e.g. 'with adaptation'
and 'without adaptation'.


### `probabilistic_aal_hazard_based`

Reports a single total Average Annual Loss (AAL) for a hazard-based probabilistic model
using the trapezoid rule. The results are saved to `average-loss.csv` output file.

See also [probabilistic_aal_trapz](#probabilistic_aal_trapz) nested subpipeline for more parameters that
can potentially be used with this subpipeline.

#### Parameters

None found

### `probabilistic_aal_hazard_based_multi_scenario`

Similar to the [probabilistic_aal_hazard_based](probabilistic.md#probabilistic_aal_hazard_based) subpipeline, except it reports an
Average Annual Loss (AAL) for results that span multiple different probabilistic 'scenarios'.
For example, the input hazard data might contain ARIs for different climate change scenarios.
The regional AAL is also computed at the same time for convenience.
This subpipeline is also safe to use when there is only *one* specified scenario
(i.e. the `$scenario_attr` column doesn't exist), it will just always add an extra
'scenario' column to the output results. Results are saved to `average-loss.csv` and
`region-average-loss.csv` output files. Requires that [sample_region](sampling.md#sample_region) was used earlier in the pipeline.

See also [probabilistic_aal_trapz](#probabilistic_aal_trapz) nested subpipeline, which also accepts
a `$return_period_attr` parameter that can be used with this subpipeline.

#### Parameters

| name | description | default |
| --- | --- | --- |
| `region_attr` | The name of the region attribute used in the model. The default is `'region'`, but the model may rename that | `'region'` |
| `return_period_attr` | The column name from the `$hazard_csv` input data that holds the ARI (as an integer value). | `'return_period'` |
| `scenario_attr` | The column name from the `$hazard_csv` input data that holds the scenario 'name'. ARIs (i.e. CSV rows) that belong to the same scenario should share the same scenario name. | `'scenario'` |

### `probabilistic_aal_trapz`

Uses the trapezoid rule to estimate the Average Annual Loss for a hazard-based
probabilistic model. This doesn't save the AAL to file, so a `save` step would
need to follow this subpipeline. Use this subpipeline when you want more
finer-grain control over how the results are saved (i.e. customizing filenames,
data sorting, etc).

#### Parameters

| name | description | default |
| --- | --- | --- |
| `aal_group_by` | Optionally changes the AAL results reported so they are broken down based on the given criteria, such as region, construction type, or use category | `{}` |
| `include_totals` | By default, any attributes beginning with `Total_` are excluded from the AAL. These `Total_` attributes are often added automatically by analysis and sampling subpipelines, e.g. so that [report_event_impact](reporting.md#report_event_impact) can report both the exposed and total value for comparison. These total values typically don't make sense being reported as an AAL (because they are totals, the values are static across different ARI events). However, you may still want to include `Total_` attributes added to the `Total` struct manually, e.g. if the `$analysis_function` returns a `Total_Loss` attribute. | `false` |
| `return_period_attr` | The column name from the `$hazard_csv` input data that holds the ARI (as an integer value). | `'return_period'` |

### `probabilistic_regional_aal_hazard_based`

Reports an AAL for each region, using the trapezoid rule.
Suitable for a hazard-based probabilistic model. Requires the [sample_region](sampling.md#sample_region)
subpipeline to have been used earlier in the pipeline.
The results are saved to `region-average-loss.csv` and `region-average-loss-map.gpkg` output files by default.

See also [probabilistic_aal_trapz](#probabilistic_aal_trapz) nested subpipeline, which also accepts
a `$return_period_attr` parameter that can be used with this subpipeline.

#### Parameters

| name | description | default |
| --- | --- | --- |
| `region_attr` | The name of the region attribute used in the model. The default is 'region', but the model may rename that | `'region'` |
| `regional_group_by` | Optionally changes the results reported so they are broken down row-wise based on the given criteria, such as construction type, or use category | `{}` |


