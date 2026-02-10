# README

## Quickstart

The Transpower layers are accessed via [ArcGIS Hub](opendata.arcgis.com)
and so don't require an API key in order to access the data.

The bookmarks reference specific ArcGIS Hub dataset IDs. These dataset IDs were valid
as of August 2025, however, it may be worth double-checking that they still refer to
the latest Transpower data available.

The bookmarks try to download the Transpower GeoJSON data each time they are used.
You could consider downloading the GeoJSON file once, and creating your own copy of the bookmarks,
which might speed up running models slightly.

## Type information

The Transpower bookmarks represent exposure data, such as transmission lines and sub-stations.
Most bookmarks conform to the same RiskScape type (i.e. the `Transpower_Exposure` type), which means they
can be used interchangeably in a model.

Note that the underlying Transpower data may contain more attributes that may be useful for your modelling.
These extra attributes have been removed to make the bookmarks simpler to use. If you need to access
the full set of attributes, try creating your own customized bookmark.

## Licensing

The datasets in this directory are made available by Transpower New Zealand Limited,
licensed under Creative Commons 4.0 Creative Commons Attribution 4.0 International
https://creativecommons.org/licenses/by/4.0
