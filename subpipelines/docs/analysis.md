
## Consequence analysis subpipelines

Reusable subpipelines for the consequence analysis phase of a RiskScape model pipeline.
This may involve calculating a loss or damage using a Python function (or other function,
such as a CSV-based function).

These subpipelines should come after any [input_](input.md) and [sample_](sampling.md) subpipelines, and before
any [report_](reporting.md) subpipelines. These subpipelines typically require that `exposure` and `hazard`
(hazard intensity measure) values are present in the pipeline data. Exposure-based subpipelines
require an `exposed` attribute to be present (true if the feature was exposed to hazard).
All subpipelines add a `Total` attribute to the pipeline data, which contains the
numeric results of interest to aggregate in the [report_](reporting.md) subpipeline steps.

This subpipeline framework is flexible, so that your `$analysis_function` can return
multiple different values, e.g. `{ Building_Loss, Contents_Loss }` and the [report_](reporting.md)
subpipeline step will respect these attributes across any outputs that get saved.
Note that the assumption is that these attributes should all be numeric and safe/sensible
to sum. If your `$analysis_function` returns different types (e.g. a text-string damage
state) or values that don't make sense to sum (e.g. mean damage ratio), then you can still
use subpipelines up to and including the [analysis_](analysis.md) phase, but you may have to use
your own pipeline code to save the results


### `analyse_by_category`

This subpipeline reorganizes the format of the results to simplify
subsequent aggregation steps (i.e. instead of bucketing *in* the [report_](reporting.md) aggregation
steps, this buckets the data *before* aggregation). This turns the `Total` attribute into
column-wise data for each of the `$categories` specified, matching the result to a
category based on the `$match` value.

For example, if `Total` is `{Exposed_Value: 1000}` and `exposure` is `{Use_Cat: 'Residential'}`, `$match` is `'Use_Cat'` and `$categories` is `['Residential', 'Industrial']`, then after the supipeline, `Total` would be transformed
into `{Total_Exposed_Value: 1000, Other_Exposed_Value: 0, Residential_Exposed_Value: 1000, Industrial_Exposed_Value: 0}` (with the first 2 attributes getting populated automatically).

This approach allows the results to be easily aggregated to provide a breakdown based on an
attribute in the exposure-layer, such as by building use category or road type.
This allows aggregated results to be presented in different combinations, such as by
region *and* building use category. This subpipeline can be used in combination with
(i.e. after) other analysis subpipelines, like [analyse_consequence](analysis.md#analyse_consequence).

#### Parameters

| name | description | default |
| --- | --- | --- |
| `categories` | The buckets of possible values that the exposure-layer attribute might have. E.g. for use category this might be `['Residential', 'Industrial', 'Commercial']`. This list doesn't have to be exhaustive - `Other` and `Total` buckets will be added automatically to ensure no results are missed. | (required) |
| `match` | The name of the attribute in the exposure-layer to use for categorization. For example, if categorization is based on use category, then this would be the name of the use category attribute, e.g. `'Use_Cat'` | (required) |

### `analyse_consequence`

The 'consequence analysis' phase of the model workflow, where the risk function
gets called for every element-at-risk in the input dataset. The relevant attributes for the
exposure-layer feature (e.g. construction type) get passed to the risk function, along with
any hazard intensity measure determined from the spatial sampling phase. Typically the
risk function is implemented in Python and approximates a mean damage or fragility curve.
Uncertainty can be incorporated into the risk function through random number generation.

#### Parameters

| name | description | default |
| --- | --- | --- |
| `analysis_function` | The loss/damage/exposure function to use in the analysis | (required) |
| `arguments` | Optionally allows you to pass additional arguments to the risk function, e.g. `{ exposure, hazard, $excess }`. This must always be a struct expression. | `{exposure, hazard}` |
| `consequence_name` | Optionally renames the 'Consequence' attribute in the total results, e.g. 'Building_Loss'. Note that names beginning with 'Total_' are somewhat superfluous (i.e. may end up as 'Total_Total_xyz' in results), and may get automatically dropped from some outputs, such as AAL. | `'Consequence'` |

### `analyse_exposed_population`

The 'consequence analysis' phase of the model workflow suitable for a simple population exposure model.

#### Parameters

| name | description | default |
| --- | --- | --- |
| `population_attr` | The name of the attribute in the exposure-layer that holds the population value. If the exposure-layer is raster-based population data, then this will be `'value'`. | `'value'` |

### `analyse_exposed_value`

The 'consequence analysis' phase of the model workflow for a simple exposure model.
Safe to use repeatedly in the same model pipeline, if there are multiple attributes to report.

#### Parameters

| name | description | default |
| --- | --- | --- |
| `attribute` | The name of the attribute in the exposure-layer that holds the exposed value of interest. E.g. for reporting the exposed value of a building, this might be `'Replacement_Cost'`. | (required) |
| `rename` | Renames the exposure-layer attribute for reporting the results. E.g. the exposure attribute might be called `'Replacement_Cost'`, but you want it to appear in the results as `'Value_NZD'` (i.e. _Exposed_Value_NZD_, _Total_Value_NZD_). | (required) |


