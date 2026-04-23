# Subpipeline library

This directory contains subpipelines that can easily be imported into
your project and reused to build pipeline models. The idea behind these
subpipelines is they are 'building blocks' that let you construct a pipeline
model more easily than writing 100% of the pipeline code from scratch.

The subpipelines in this library achieve common modelling tasks, such as
aggregating results by region, or calculating an Average Annual Loss (AAL)
using probabilistic data.

## Experimental

**CAUTION:** _These subpipelines are currently **experimental**._
_These subpipeline snippets do not constitue a 'formal' RiskScape release._
_Their behaviour may change over time. Subpipelines and parameters may be removed or renamed._
_The subpipeline code has not been exhaustively tested to the same level as_
_built-in RiskScape Engine features._

## File organization

The subpipelines are organized into separate INI files based on the model workflow
phases (i.e. input, geoprocessing, sampling, analysis, reporting). Additional INI files,
such as `probabilistic.ini`, have been used for highly-specific modelling functionality
that falls outside the generic model workflow. Importing the `project.ini`
will import all subpipelines from these INI files.

The `examples/` sub-directory contains working model examples that use
the subpipeline library to construct models. Look at `examples/project.ini`
for an idea of how to organize the subpipelines into models. These example models
are based on the material used in the RiskScape Engine tutorials, so there are
limitations on what is available. For example, there is a working probabilistic
model pipeline, but it simply reuses the 2009 Samoa tsunami hazard data, rather than
actually using realistic probabilistic hazard data.

## Building blocks

The subpipelines only cover the _most common_ modelling tasks that are often repeated across models.
The subpipelines are not exhaustive or foolproof. For example, they only use `sum()`
aggregation to produce a total result (rather than using `mean()` or `percentile()`).

Where the subpipelines don't cover the functionality you require, you can insert
additional pipeline steps into your model between the `subpipeline()` steps to
suit your needs. You can use the CLI wizard to generate pipeline code and then
pick out the pieces you need. Or you could use the subpipeline library code
as a starting point and modify it to fit your modelling requirements.

## Version snapshots

The GitHub repository code may be updated without warning - if your
model relies on these subpipelines, it may cause your model to break or
stop working as intended. To avoid this, we recommend taking a 'snapshot'
of the GitHub subpipelines.

One way to do this is to clone the git repository, and then import your local copy of
`subpipelines/project.ini` into your project. Another approach is to import a
'tagged' version of the subpipelines directly from GitHub, like this:

```
[project]
import = https://raw.githubusercontent.com/GNS-Science/riskscape/refs/heads/VERSION/subpipelines/project.ini
```

But replace `VERSION` with the version of RiskScape you are using, e.g. 1.13.0.
The tag effectively refers to a snapshot of the subpipeline code, so the subpipelines
you use won't change even if the code in the GitHub repository is updated.

The subpipelines library will typically always work with the latest
RiskScape Engine release. You may need to upgrade the version of RiskScape
you have installed locally in order for the latest subpipeline code to work.
Some subpipelines may rely on beta features, so we recommend enabling
the beta plugin or using `riskscape --beta model run`. Refer to the
[Engine documentation](https://engine-docs.sites.riskscape.nz) for more details.

## Parameters

The following principles have been used for the parameters used in the subpipelines
and models:

- Where a subpipeline will _always_ be a user-facing model parameter,
the parameter's name should reflect the modelling term. For example, there's no
suitable default for the `region_layer`, and so this needs to be defined as either
a `param.region_layer` model parameter or a `[parameter region_layer]` project parameter
in the `project.ini` file that is importing the subpipelines.

- Where subpipeline parameters can _optionally_ be used directly as `-p` model parameters, the
parameter name is prefixed with the model phase, in its "plain" form, without the -ing.
For example, subpipeline parameters for the 'reporting' model phase will be prefixed
with `report_`, e.g. `report_decimal_places`. These parameters are typically defined
as `[param xyz]` project parameters alongside the subpipeline.

- Where subpipeline parameters are only intended to be used as a _subpipeline_ parameter,
that can be overridden, they are only defined as part of the subpipeline itself, as
a `param.xyz =`. No model phase prefix is needed, as they should only be used
in the `subpipeline()` step itself, e.g.

```
-> subpipeline('report_total_binned_by_range', { group_by: {region} })
```
