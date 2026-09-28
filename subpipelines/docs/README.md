# Sub-pipeline library companion

The sub-pipeline libraries are organized around the model workflow phases, i.e.

<img src="https://engine-docs.sites.riskscape.nz/_images/model_framework.svg" alt="RiskScape model workflow" width="75%">

You can read more about the sub-pipelines available, what they do, and the parameters they accept,
by clicking on the links below.

- [Input](./input.md): loads input layers into the model
- [Geo-processing](./geoprocessing.md): Optionally segments/cuts or spatially filters the exposure-layer features.
- [Spatial sampling](./sampling.md): Geospatially determine the hazard intensity for each element-at-risk.
Also matches exposure-layer features to the regional boundaries they fall within.
- [Consequence analysis](./analysis.md): Use a risk-function to determine the impact (e.g. loss, damage, fragility)
for each element-at-risk.
- [Results reporting](./reporting.md): Aggregates the raw model results into summarized form and saves them.
- [Probabilistic](./probabilistic.md): Specialized sub-pipelines to calculate the Average Annual Loss (AAL) for a probabilistic model.
- [Sea-level rise (SLR)](./sea-level-rise.md): Specialized sub-pipelines to calculate coastal inundation for
climate change scenarios (relies on having flood-maps for a range of SLR increments)

Note that the list of sub-pipeline parameters is not always exhaustive.
Some sub-pipelines may refer to using another nested sub-pipeline.
In those cases, some of the nested sub-pipeline's parameters *may* also be
accepted by the parent sub-pipeline (if they are not already hard-coded as
fixed parameters within the parent sub-pipeline).

