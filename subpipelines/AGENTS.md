# RiskScape Subpipeline Library — Agent Instructions

This file provides guidance for AI assistants helping users build RiskScape pipeline
models using the subpipeline library. Read this before writing any model code.

Companion files:
- README: https://raw.githubusercontent.com/GNS-Science/riskscape/refs/heads/main/subpipelines/README.md
- Engine docs: https://engine-docs.sites.riskscape.nz
- Engine docs for LLMs: https://engine-docs.sites.riskscape.nz/llms.txt


## Step 1: Fetch these files before writing any model

If the user has local INI files in their working directory, read those files — they may
define bookmarks, functions, or parameters the model depends on.

Fetch all of these files before writing or modifying pipeline models. They define what
subpipelines, functions, and conventions are available.
If the working directory contains a 'subpipelines' directory, look for local copies
of these files first before fetching them from GitHub.

| File | URL |
|------|-----|
| Library index | https://raw.githubusercontent.com/GNS-Science/riskscape/refs/heads/main/subpipelines/project.ini |
| Input subpipelines | https://raw.githubusercontent.com/GNS-Science/riskscape/refs/heads/main/subpipelines/input.ini |
| Sampling subpipelines | https://raw.githubusercontent.com/GNS-Science/riskscape/refs/heads/main/subpipelines/sampling.ini |
| Analysis subpipelines | https://raw.githubusercontent.com/GNS-Science/riskscape/refs/heads/main/subpipelines/analysis.ini |
| Reporting subpipelines | https://raw.githubusercontent.com/GNS-Science/riskscape/refs/heads/main/subpipelines/reporting.ini |
| Probabilistic subpipelines | https://raw.githubusercontent.com/GNS-Science/riskscape/refs/heads/main/subpipelines/probabilistic.ini |
| Geoprocessing subpipelines | https://raw.githubusercontent.com/GNS-Science/riskscape/refs/heads/main/subpipelines/geoprocessing.ini |
| Helper functions | https://raw.githubusercontent.com/GNS-Science/riskscape/refs/heads/main/subpipelines/functions.ini |
| Example models | https://raw.githubusercontent.com/GNS-Science/riskscape/refs/heads/main/subpipelines/examples/project.ini |
| Built-in functions reference | https://engine-docs.sites.riskscape.nz/reference/functions.html#built-in-functions |

## Project import

The `[project]` section must import the subpipeline library. This should be at the top of the `project.ini` file:

```ini
# Latest:
[project]
import = https://raw.githubusercontent.com/GNS-Science/riskscape/refs/heads/main/subpipelines/project.ini
```

Sometimes you may need to use a versioned URL to pin the library to a specific RiskScape release, e.g.

```ini
# Pinned to a specific release (replace VERSION, e.g. 1.13.0):
[project]
import = https://raw.githubusercontent.com/GNS-Science/riskscape/refs/tags/VERSION/subpipelines/project.ini
```

This might be needed if the user is running an older version of RiskScape.
Ideally, the user should run the most recent version of RiskScape.

## Model definitions

Every `[model]` section **must** include `framework = pipeline`. Omitting it is the
most common mistake — the model will not run without it.

```ini
[model My_Model]
framework = pipeline
description = ...
source = '''
...
'''
```


## Pipeline source syntax

- Wrap `source` in triple-quotes: `source = ''' ... '''`
- Connect steps with `->`
- No leading `->` is needed before `input` steps (or `subpipeline('input_exposures')`)
- All subsequent steps need `->` connecting them to the previous step
- No trailing `->` is needed after `save` steps, e.g. `subpipeline('report_event_impact')`

```ini
source = '''
subpipeline('input_exposures')
-> subpipeline('input_hazard')
-> subpipeline('sample_hazard_max')
-> subpipeline('analyse_consequence') as event_impact_table
'''
```

Note that there are no strict whitespace requirements around how
pipeline steps are formatted. Formatting may vary in examples due to
the stylistic preferences of the author.


## Typical pipeline structure

- Model starts with `subpipeline('input_exposures')`
- `as event_impact_table` names the raw results table.
- Multiple report subpipelines can branch from `event_impact_table`
- Workflow order is: input, geoprocess (optional), sample, analyse, report.
- When `sample_region` occurs is somewhat optional - it needs to be between `input_exposures` and `report_regional_impact`

```
subpipeline('input_exposures')
 -> subpipeline('input_hazard')
 -> [optional: subpipeline('geoprocess_segment_exposures')]
 -> subpipeline('sample_hazard_max')   # or sample_hazard, sample_measure_exposed
 -> subpipeline('sample_region')
 -> subpipeline('analyse_consequence') as event_impact_table   # or analyse_exposed_value, etc

# Multiple report subpipelines branch from event_impact_table:
event_impact_table -> subpipeline('report_event_impact')
event_impact_table -> subpipeline('report_regional_impact')
```

### Performance notes

For small-scale models (e.g. a few thousand exposure-layer features), don't
bother optimizing performance. For larger national-scale models (e.g. hundreds
of thousands of exposure-layer features), performance may be an issue.

- `input_multiple_hazard_geotiffs` will duplicate exposure-layer features for each hazard GeoTIFF.
  If `sample_region` or `geoprocess_segment_exposures` was *after* `input_multiple_hazard_geotiffs`
  it would do unnecessary extra processing.
- For a large dataset, adding `-> filter(exposed)` before `analyse_consequence` may improve
  performance.
- The probabilistic AAL subpipelines need to see a loss value for *every* event in order
  to calculate the AAL. So filtering unexposed or zero loss results is not recommended.
- The hazard value can be null. RiskScape will skip some operations if they are not null-safe
  (e.g. calling the `analysis_function`). This can help performance without filtering.


## The Total struct

Reporting subpipelines expect a `Total` struct attribute on each row. It must contain
only **numeric values that make sense to sum** across features.

**Include:** counts, loss values, replacement values, exposed lengths/areas.
**Do not include:** hazard intensity (summing depth or velocity is not meaningful),
ratios or percentages.

Subpipelines may append attributes into the `Total` struct, e.g. using the `merge` function.

E.g. the following will copy the `Repl_Cost` attribute from the exposure-layer and report it as
`Exposed_Building_Value` (if exposed) and `Total_Building_Value`:

```
-> subpipeline('analyse_exposed_value', { attribute: 'Repl_Cost', rename: 'Building_Value'})
```

Repeat to report multiple attributes from the exposure-layer, e.g.

```
-> subpipeline('analyse_exposed_value', { attribute: 'Repl_Cost', rename: 'Building_Value'})
-> subpipeline('analyse_exposed_value', { attribute: 'Household_Pop', rename: 'Population'})
```


## Model parameters

A parameter always starts with `$` in pipeline code, e.g. `$analysis_function`.
This defines a placeholder that gets replaced with the parameter's value at run-time.

Default values for parameters are specified as `param.PARAMETER_NAME = VALUE`
lines in the `[model]` section, e.g.

```ini
param.analysis_function = 'Flood_Building_Loss'
```

These go after the `source = ''' ... '''` pipeline definition.

Common parameters that need defining:

```ini
# these will be filepaths for the user's input data:
param.exposure_layer =     # TBD
param.hazard_layer =       # TBD
param.region_layer =       # TBD
# the function name for loss/damage models:
param.analysis_function =  # TBD
```

### Project parameters

Project parameters apply to all models that have a matching parameter. E.g.

```ini
[parameter exposure_layer]
default = foo.shp
description = The exposure layer bookmark to use as input.
```

Any models with a `$exposure_layer` parameter would then use `foo.shp` by default.
These avoid repeating the same default values across multiple models.


## Pipeline steps

RiskScape pipelines use a bespoke language and so have their own quirks.
The subpipeline library is designed to "do the right thing" and avoid common pitfalls.

**NOTE**: Try to reuse the library subpipelines where possible, rather than writing
new pipeline code from scratch.

Pipeline steps can be used directly in combination with subpipelines.
- [Pipeline step reference](https://engine-docs.sites.riskscape.nz/reference/pipelines/generated.html)

Take care when using pipeline steps directly. The next sections have some tips.

### select() attribute scoping

Attributes declared in a `select()` step cannot be referenced in the same step.
Chain a second step:

```ini
# WRONG
select({ *, intensity * 0.5 as scaled, scaled * 2 as doubled })

# CORRECT
select({ *, intensity * 0.5 as scaled })
 ->
select({ *, scaled * 2 as doubled })
```

### Attribute naming

Name attributes for the output results and use those names consistently throughout
the pipeline. Avoid renaming attributes mid-pipeline — it makes the pipeline harder
to follow and introduces errors when a rename is missed in a downstream step.


## Probabilistic models

Replace `input_hazard` with `input_multiple_hazard_geotiffs` and replace event
reporting subpipelines with:

```ini
subpipeline('probabilistic_aal_hazard_based')
subpipeline('probabilistic_regional_aal_hazard_based')
```

The `Total` struct convention is the same as for single-event models.


## Running the model

The command to run the `My_Model` model is:

```
riskscape --beta model run My_Model
```

`--beta` uses the beta plugin. Some functions or pipeline steps may still be beta.

Parameters can be overridden on the command-line, using `-p "PARAMETER_NAME=NEW_VALUE", e.g.

```
riskscape --beta model run My_Model -p "exposure_layer=bar.gpkg"
```

The above command would use `bar.gpkg` as the model's exposure-layer (i.e. instead of the `foo.shp` default).

## Functions

RiskScape comes with [built-in functions](https://engine-docs.sites.riskscape.nz/reference/functions.html#built-in-functions)
that are primarily used for pipeline mechanics, rather than as risk functions.

Risk functions are typically 'user-defined' as part of the `project.ini` file.

### User-defined functions

For simple fragility and vulnerability curves, CSV-based functions are recommended.
These are easier for non-coding users to visualize/verify the curve.

For simple logic functions, using an expression function may be suitable.
However, it is an esoteric language and comes with quirks.

CPython is typically a suitable choice. Define the exposure argument-type
as `anything` to avoid type-matching errors.

[Risk function introduction](https://engine-docs.sites.riskscape.nz/intro/risk-functions.html)
has examples of all these approaches.

#### Log-normal CDF curves

A common modelling technique is to represent a fragility or vulnerability curve
using a log-normal CDF curve. There are several possible ways to turn this into a
RiskScape function:

1. Generate CSV file(s) that represent the log-normal CDF hazard intensity vs fragility or
damage ratio. This is conceptually simple and easy for a user to verify simply by
plotting the CSV data.

2. Use the built-in `lognorm_cdf` function in an expression function, e.g.

```
[function Tsunami_DS1_Probability]
description = Samoa tsunami damage state 1 fragility curve
framework = expression
source = '''
(building, hazard) -> lognorm_cdf(hazard, -0.53, 0.46)
'''
```

Implementing a single curve is straight-forward, and requires no CPython setup.
However, it is more awkward to test, and the logic gets more complicated when
different asset classes require different curves (e.g. fragility based on construction material).

3. Use a CPython function with `scipy.stats.lognorm`. It is easier to
code more complicated logic in Python. Test code can be added to the Python file.
However, it requires the user has [setup RiskScape to use CPython](https://engine-docs.sites.riskscape.nz/reference/python/cpython.html).


### Built-in function reference

Built-in functions are organized by category:

- [Geometry processing](https://engine-docs.sites.riskscape.nz/reference/functions/generated/geometry-processing.html): For spatial sampling and geoprocessing. 
- [Language functions](https://engine-docs.sites.riskscape.nz/reference/functions/generated/language.html): Type handling, struct and list manipulation
- [Logical functions](https://engine-docs.sites.riskscape.nz/reference/functions/generated/logical.html): if(), not(), is_null()
- [Maths functions](https://engine-docs.sites.riskscape.nz/reference/functions/generated/maths.html): round(), min(), max(), lognorm_cdf() etc.
- [Misc functions](https://engine-docs.sites.riskscape.nz/reference/functions/generated/misc.html): More complicated manipulations, like creating dynamic bookmarks, lookup tables, bucket_range()
- [String functions](https://engine-docs.sites.riskscape.nz/reference/functions/generated/strings.html): basic string manipulation
- [Beta functions](https://engine-docs.sites.riskscape.nz/reference/functions/generated/beta.html): requires the beta plugin to use (i.e. `riskscape --beta`)

## Checklist

Before finishing a model:

- [ ] `framework = pipeline` on every `[model]` section
- [ ] `source = ''' ... '''` uses triple-quotes
- [ ] Steps are connected with `->` appropriately
- [ ] Library subpipelines are reused where possible
- [ ] New attributes declared in a `select()` are not referenced until the next step
- [ ] `Total` struct contains only numeric values sensible to sum
- [ ] `[project]` imports the subpipeline library
- [ ] User-facing parameters have `param.NAME` declarations and/or `[parameter]` project declarations as appropriate
