# RiskScape Repository — Agent Instructions

This file provides guidance for AI assistants working with the RiskScape GitHub repository.
Read this before writing or modifying any RiskScape project files.

For detailed guidance on building pipeline models, see:
- `subpipelines/AGENTS.md`: https://raw.githubusercontent.com/GNS-Science/riskscape/refs/heads/main/subpipelines/AGENTS.md

Engine documentation for LLMs: https://engine-docs.sites.riskscape.nz/llms.txt


## Repository structure

| Directory | Contents |
|-----------|----------|
| `subpipelines/` | Reusable subpipeline library for building pipeline models. Start here for most modelling tasks. |
| `data/linz/` | Bookmarks for commonly used NZ exposure-layers from LINZ (roads, rail, building outlines) |
| `data/statsnz/` | Bookmarks for NZ regional boundaries from Stats NZ, used for aggregating model results |
| `data/transpower/` | Bookmarks for Transpower electricity infrastructure (transmission lines, substations) |
| `functions/earthquake/gem/` | GEM Global Vulnerability Model functions for building damage assessment |
| `functions/volcano/` | Risk functions for volcanic impact on infrastructure |
| `case-studies/DEVORA/` | Fully worked volcano risk model for the Auckland region |


## How this repository is used

RiskScape models are defined in `project.ini` files. Users import configuration from
this repository into their own `project.ini` using `import = FILEPATH_OR_URL`.

For example, to use the LINZ bookmarks:

```ini
[project]
import = https://raw.githubusercontent.com/GNS-Science/riskscape/refs/heads/main/data/linz/project.ini
```

Multiple imports can be combined in a single `[project]` section:

```ini
[project]
import = https://raw.githubusercontent.com/GNS-Science/riskscape/refs/heads/main/subpipelines/project.ini
import = https://raw.githubusercontent.com/GNS-Science/riskscape/refs/heads/main/data/linz/project.ini
import = https://raw.githubusercontent.com/GNS-Science/riskscape/refs/heads/main/data/statsnz/project.ini
```


## Before writing any model code

1. Read `subpipelines/AGENTS.md` for pipeline model conventions and common mistakes
2. Fetch the relevant `project.ini` and `README.md` files from the subdirectories
   that contain the bookmarks or functions the user needs
3. Read any local INI files in the user's working directory — these define their
   existing bookmarks, functions, and parameters

Key raw file URLs:

| Resource | URL |
|----------|-----|
| Subpipeline library | https://raw.githubusercontent.com/GNS-Science/riskscape/refs/heads/main/subpipelines/project.ini |
| LINZ bookmarks | https://raw.githubusercontent.com/GNS-Science/riskscape/refs/heads/main/data/linz/project.ini |
| Stats NZ bookmarks | https://raw.githubusercontent.com/GNS-Science/riskscape/refs/heads/main/data/statsnz/project.ini |
| Transpower bookmarks | https://raw.githubusercontent.com/GNS-Science/riskscape/refs/heads/main/data/transpower/project.ini |
| GEM earthquake functions | https://raw.githubusercontent.com/GNS-Science/riskscape/refs/heads/main/functions/earthquake/gem/project.ini |
| Volcano functions | https://raw.githubusercontent.com/GNS-Science/riskscape/refs/heads/main/functions/volcano/project.ini |
| Example models | https://raw.githubusercontent.com/GNS-Science/riskscape/refs/heads/main/subpipelines/examples/project.ini |


## Licensing

Each subdirectory may have different licensing conditions. Always check the `README.md`
in the relevant subdirectory before using data or functions in a project.

## Accessing remote data

Some WFS data services, such as LINZ or StatsNZ, require a user access token for the
bookmarks to work correctly. More details are in the relevant README.md

### Local copy of the data

Large WFS datasets are very slow to access each time the model is run.
Downloading a local copy of the data will run much faster.
To make a local copy of the remote data, use the command:

```
riskscape bookmark evaluate BOOKMARK_NAME
```

This creates a `output/bookmark-eval/BOOKMARK_NAME.gpkg` file locally
that contains the remote data, plus any bookmark modifications.
This `BOOKMARK_NAME.gpkg` can then be used as a model parameter instead
of the `BOOKMARK_NAME` bookmark.

Occasionally a WFS server error may be encountered fetching the data.
Re-run the command if this occurs.
