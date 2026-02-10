# RiskScape Repository for Shared Projects

This is a repository that contains:
- example project files for RiskScape modelling
- shared project files that need to be accessible

## Getting started

The idea is that you can take a copy of these project files and then import the configuration
you want for your specific modelling use-case.

In the `[project]` section of your `project.ini` file you can import another INI file that
defines a set of bookmarks or functions. You can then use those bookmarks and functions
in your project.

For example, to import the LINZ bookmarks, you would use:

```
[project]
# import the LINZ bookmarks
import = ..\riskscape\data\linz\project.ini
```

If you are a git user, you can *clone* this repository to take a copy of all the files locally.

For users unfamiliar with git, you can click on the 'Code' button at the top of the page and
select 'Download ZIP'.

Note that the files in this repository will periodically get updated with more examples
and other improvements.

## File organization

The repository structure is broken up along the following lines:

- **data**: Contains common RiskScape bookmarks that can be reused in any project.
  Bookmarks are organized by the data provider:
  - **[linz](data/linz/README.md)**: Commonly used exposure-layers from [LINZ](https://data.linz.govt.nz/),
    such as roads, rail, building outlines.
  - **[statsnz](data/linz/README.md)**: Common regional boundaries from [Stats NZ](https://datafinder.stats.govt.nz/),
    used for aggregating model results.
  - **[transpower](data/transpower/README.md)**: [Transpower Open Data](https://data-transpower.opendata.arcgis.com)
    for electricity infrastructure-layers, such as transmission lines and sub-stations.
- **functions**: Contains RiskScape functions that can be reused for modelling risk.
  Functions are organized by hazard-type.
  - **[GEM](functions/gem/README.md)**: Functions for using the GEM
    [Global Vulnerability Model](https://github.com/gem/global_vulnerability_model) to measure damage to buildings.
  - **[volcano](functions/volcano/README.md)**: Risk functions for assessing volcanic impact on infrastructure.
- **case-studies**: Fully worked model pipelines for various scenarios.
  - **[DEVORA](case-studies/DEVORA/README.md)**: Combines volcano infrastructure functions, 
  exposure-layer bookmarks, and hazard data produced for the Determining Volcanic Risk in Auckland (DEVORA) research programme.
- **projects**: contains various undocumented project files

## License

Note that each sub-directory may have different licensing conditions applied to the data it relates to.
Check the README.md in the sub-directory you are interest in for more details on the license(s) used.

