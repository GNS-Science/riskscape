# README

## Quickstart

The Toitū Te Whenua Land Information New Zealand (LINZ) layers are
accessed via WFS, and so require an API key to access the data.
To setup your API key with RiskScape, copy paste the following:

  [data.linz.govt.nz]
  framework = koordinates
  hostname = data.linz.govt.nz
  api-key = TODO_YOUR_KEY_HERE

and add it to your secrets.ini file.
Replace the `TODO_YOUR_KEY_HERE` with your https://data.linz.govt.nz API key.
You can access or create an API key at: https://data.linz.govt.nz/my/api/

**Tip**: A Windows user could edit their secrets file by entering the following into a command prompt:
  
  notepad %USERPROFILE%\RiskScape\secrets.ini

For more details on configuring secrets in RiskScape, refer to:
https://engine-docs.sites.riskscape.nz/reference/config/secrets.html

## Type information

The LINZ bookmarks mostly represent exposure data, such as building, road, and rail information.
Most bookmarks conform to the same RiskScape type (i.e. the `LINZ_Exposure` type), which means they
can be used interchangeably in a model.

Note that the underlying LINZ data may contain more attributes that may be useful for your modelling.
These extra attributes have been removed to make the bookmarks simpler to use. If you need to access
the full set of attributes, try creating your own customized bookmark.

## Licensing

The datasets in this directory are made available by Toitū Te Whenua Land Information New Zealand,
licensed under the Creative Commons 4.0 Creative Commons Attribution 4.0 International.
Refer to https://data.linz.govt.nz/license/attribution-4-0-international/
